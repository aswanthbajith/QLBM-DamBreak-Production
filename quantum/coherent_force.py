"""
Phase F13: Coherent Spatial Force & Continuum Surface Force (CSF) Engine.

Mathematical Formulation:
1. Gravitational Buoyancy Force:
   F_buoyancy(x,y) = [0, (rho(x,y) - rho_G) * g_acc]^T

2. Reversible Coordinate-Shift Stencils for CSF:
   grad_x(alpha) = 0.5 * (S_x^+1 - S_x^-1) alpha
   grad_y(alpha) = 0.5 * (S_y^+1 - S_y^-1) alpha
   n = grad(alpha) / (|grad(alpha)| + 1e-12)
   kappa = - div(n) = - 0.5 * [ (S_x^+1 - S_x^-1) n_x + (S_y^+1 - S_y^-1) n_y ]
   F_CSF = sigma * kappa * grad(alpha)
"""

from typing import Tuple, Dict, Any, Optional, List
import numpy as np
import scipy.linalg as la

from quantum.coherent_parameter_oracle import FixedPointArithmetic


class CoherentForceGenerator:
    """
    Coherent quantum force and CSF stencil generator.
    Evaluates interface gradients and curvatures via reversible spatial coordinate shifts.
    """

    def __init__(
        self,
        nx: int = 4,
        ny: int = 4,
        g_acc: float = -0.0005,
        sigma: float = 0.001,
        rho_G: float = 0.1,
        precision_format: str = "Q4.12",
    ):
        self.nx = nx
        self.ny = ny
        self.g_acc = g_acc
        self.sigma = sigma
        self.rho_G = rho_G
        self.fp = FixedPointArithmetic(m=4, n=12) if precision_format == "Q4.12" else FixedPointArithmetic(m=4, n=8)

        self.n_x = int(np.ceil(np.log2(nx))) if nx > 1 else 1
        self.n_y = int(np.ceil(np.log2(ny))) if ny > 1 else 1

    def compute_coherent_force_fields(
        self,
        rho_field: np.ndarray,
        alpha_field: np.ndarray,
    ) -> Tuple[np.ndarray, Dict[str, int]]:
        """
        Computes total force vector field F(x, y) = F_buoyancy + F_CSF using fixed-point arithmetic and spatial stencils.
        """
        F = np.zeros((2, self.ny, self.nx), dtype=np.float64)
        gate_costs = {"toffoli": 0, "cx": 0, "t_gates": 0, "ancilla": 0}

        # 1. Buoyancy body force
        for y in range(self.ny):
            for x in range(self.nx):
                diff_rho, c1 = self.fp.add(float(rho_field[y, x]), -self.rho_G)
                Fy_buoy, c2 = self.fp.mul(diff_rho, self.g_acc)
                F[1, y, x] = Fy_buoy
                for c in [c1, c2]:
                    for k in gate_costs:
                        gate_costs[k] += c[k]

        # 2. Continuum surface force (CSF)
        if self.sigma > 0.0 and self.nx >= 3 and self.ny >= 3:
            grad_x = np.zeros((self.ny, self.nx), dtype=np.float64)
            grad_y = np.zeros((self.ny, self.nx), dtype=np.float64)

            # Central difference shift stencils
            grad_x[:, 1:-1] = (alpha_field[:, 2:] - alpha_field[:, :-2]) / 2.0
            grad_y[1:-1, :] = (alpha_field[2:, :] - alpha_field[:-2, :]) / 2.0

            grad_norm = np.sqrt(grad_x**2 + grad_y**2) + 1e-12
            mask = grad_norm > 1e-3

            nx_vec = np.where(mask, grad_x / grad_norm, 0.0)
            ny_vec = np.where(mask, grad_y / grad_norm, 0.0)

            div_nx = np.zeros_like(nx_vec)
            div_ny = np.zeros_like(ny_vec)
            div_nx[:, 1:-1] = (nx_vec[:, 2:] - nx_vec[:, :-2]) / 2.0
            div_ny[1:-1, :] = (ny_vec[2:, :] - ny_vec[:-2, :]) / 2.0

            kappa = np.clip(-(div_nx + div_ny), -2.0, 2.0)

            for y in range(self.ny):
                for x in range(self.nx):
                    if mask[y, x]:
                        term_sig, c3 = self.fp.mul(self.sigma, float(kappa[y, x]))
                        Fx_csf, c4 = self.fp.mul(term_sig, float(grad_x[y, x]))
                        Fy_csf, c5 = self.fp.mul(term_sig, float(grad_y[y, x]))
                        F[0, y, x] += Fx_csf
                        F[1, y, x] += Fy_csf
                        for c in [c3, c4, c5]:
                            for k in gate_costs:
                                gate_costs[k] += c[k]

            # Shift stencil gate overhead
            shift_toffoli = 4 * (self.n_x + self.n_y) * self.nx * self.ny
            shift_cx = 8 * (self.n_x + self.n_y) * self.nx * self.ny
            gate_costs["toffoli"] += shift_toffoli
            gate_costs["cx"] += shift_cx
            gate_costs["t_gates"] += 4 * shift_toffoli

        return F, gate_costs
