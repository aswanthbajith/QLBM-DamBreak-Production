"""
Phase F13: Coherent Shifted Velocity & Low-Mach Stability Limiter.

Mathematical Formulation:
1. Shifted Momentum:
   jx_shifted = jx + 0.5 * Fx
   jy_shifted = jy + 0.5 * Fy

2. Shifted Macroscopic Velocity:
   ux_raw = jx_shifted / rho_safe
   uy_raw = jy_shifted / rho_safe

3. Reversible Low-Mach Stability Limiter (u_max = 0.15):
   u2 = ux_raw^2 + uy_raw^2
   if u2 > 0.15^2 = 0.0225:
       scale = 0.15 / sqrt(u2)
       ux = ux_raw * scale
       uy = uy_raw * scale
   else:
       ux = ux_raw
       uy = uy_raw
"""

from typing import Tuple, Dict, Any, Optional, List
import numpy as np
import scipy.linalg as la

from quantum.coherent_parameter_oracle import FixedPointArithmetic


class CoherentVelocityGenerator:
    """
    Coherent quantum velocity and Mach limiter generator.
    Processes fixed-point moment and force registers to yield physical low-Mach velocities.
    """

    def __init__(self, precision_format: str = "Q4.12"):
        self.fp = FixedPointArithmetic(m=4, n=12) if precision_format == "Q4.12" else FixedPointArithmetic(m=4, n=8)

    def compute_coherent_velocity_fields(
        self,
        rho_field: np.ndarray,
        jx_field: np.ndarray,
        jy_field: np.ndarray,
        Fx_field: np.ndarray,
        Fy_field: np.ndarray,
    ) -> Tuple[np.ndarray, Dict[str, int]]:
        """
        Computes velocity fields u(x, y) with resource accounting for fixed-point adders, multipliers, and dividers.
        """
        ny, nx = rho_field.shape
        u_field = np.zeros((2, ny, nx), dtype=np.float64)
        gate_costs = {"toffoli": 0, "cx": 0, "t_gates": 0, "ancilla": 0}

        for y in range(ny):
            for x in range(nx):
                rho = float(rho_field[y, x])
                jx = float(jx_field[y, x])
                jy = float(jy_field[y, x])
                Fx = float(Fx_field[y, x])
                Fy = float(Fy_field[y, x])

                # 1. Force shift: 0.5 * F
                half_Fx, c1 = self.fp.mul(0.5, Fx)
                half_Fy, c2 = self.fp.mul(0.5, Fy)
                jx_s, c3 = self.fp.add(jx, half_Fx)
                jy_s, c4 = self.fp.add(jy, half_Fy)

                # 2. Reversible Division: u = j_shifted / rho_safe
                rho_safe = max(rho, 1e-6)
                ux_raw, c5 = self.fp.div(jx_s, rho_safe)
                uy_raw, c6 = self.fp.div(jy_s, rho_safe)

                # 3. Low-Mach Limiter
                ux2, c7 = self.fp.mul(ux_raw, ux_raw)
                uy2, c8 = self.fp.mul(uy_raw, uy_raw)
                u2, c9 = self.fp.add(ux2, uy2)

                if u2 > 0.0225:  # 0.15^2
                    u_mag = float(np.sqrt(u2))
                    scale = 0.15 / (u_mag + 1e-12)
                    ux, c10 = self.fp.mul(ux_raw, scale)
                    uy, c11 = self.fp.mul(uy_raw, scale)
                    for c in [c10, c11]:
                        for k in gate_costs:
                            gate_costs[k] += c[k]
                else:
                    ux = ux_raw
                    uy = uy_raw

                for c in [c1, c2, c3, c4, c5, c6, c7, c8, c9]:
                    for k in gate_costs:
                        gate_costs[k] += c[k]

                u_field[0, y, x] = ux
                u_field[1, y, x] = uy

        return u_field, gate_costs
