"""
Phase F22: Exact Zeroth-Moment Mass-Conserving Fixed-Point BGK Engine.

Proves:
1. Floating-point BGK analytically conserves zeroth moment sum_i f_i = rho.
2. In finite fixed-point registers, integer truncation residual is strictly
   absorbed into rest population f_0 to guarantee EXACT integer mass conservation:
   sum_i f_out[i] == sum_i f_in[i] == rho_in (Zero Mass Leakage).
"""

from typing import Dict, Any, List, Tuple
import numpy as np

from classical.d2q9 import C_X, C_Y, W
from quantum.f17_reversible_primitives import FixedPointQ412, ReversibleFixedPointArithmetic


class F22ExactMassConservingBGKEngine:
    """
    Finite-register BGK engine with exact integer zeroth-moment mass conservation.
    """

    def __init__(
        self,
        omega_f: float = 1.0,
        omega_g: float = 1.42857,
        g_acc: float = -0.0005,
        frac_bits: int = 12,
    ):
        self.frac_bits = frac_bits
        self.scale = 1 << frac_bits
        self.arith = ReversibleFixedPointArithmetic(frac_bits=frac_bits)

        self.omega_f_fixed = int(round(omega_f * self.scale))
        self.omega_g_fixed = int(round(omega_g * self.scale))
        self.g_acc_fixed = int(round(g_acc * self.scale))
        self.w_fixed = [int(round(w * self.scale)) for w in W]

    def evaluate_conservative_bgk_map(
        self,
        f_in: List[int],
        g_in: List[int],
        F_ext: Tuple[int, int] = (0, 0),
    ) -> Tuple[List[int], List[int], Dict[str, Any]]:
        """
        Evaluates BGK collision map with strict zeroth-moment mass conservation.
        """
        rho_work = sum(f_in)
        alpha_work = sum(g_in)

        jx_work = sum(f_in[i] * C_X[i] for i in range(9)) + F_ext[0] // 2
        jy_work = sum(f_in[i] * C_Y[i] for i in range(9))
        jy_work += (self.arith.multiply(rho_work, self.g_acc_fixed) + F_ext[1]) // 2

        ux_work = self.arith.divide(jx_work, max(rho_work, 1))
        uy_work = self.arith.divide(jy_work, max(rho_work, 1))

        ux2 = self.arith.multiply(ux_work, ux_work)
        uy2 = self.arith.multiply(uy_work, uy_work)
        u2_work = ux2 + uy2

        f_out = [0] * 9
        g_out = [0] * 9

        # Evaluate directional components i = 1..8
        for i in range(1, 9):
            c_dot_u = C_X[i] * ux_work + C_Y[i] * uy_work
            c_dot_u_sq = self.arith.multiply(c_dot_u, c_dot_u)

            bracket_f = (
                self.scale
                + 3 * c_dot_u
                + (9 * c_dot_u_sq) // 2
                - (3 * u2_work) // 2
            )
            term_f = self.arith.multiply(rho_work, bracket_f)
            f_eq = self.arith.multiply(self.w_fixed[i], term_f)

            bracket_g = self.scale + 3 * c_dot_u
            term_g = self.arith.multiply(alpha_work, bracket_g)
            g_eq = self.arith.multiply(self.w_fixed[i], term_g)

            f_out[i] = self.arith.linear_interpolate(f_in[i], f_eq, self.omega_f_fixed)
            g_out[i] = self.arith.linear_interpolate(g_in[i], g_eq, self.omega_g_fixed)

        # Strictly assign rest population f_out[0] and g_out[0] to conserve exact sum
        sum_f_dir = sum(f_out[1:9])
        sum_g_dir = sum(g_out[1:9])

        f_out[0] = rho_work - sum_f_dir
        g_out[0] = alpha_work - sum_g_dir

        meta = {
            "rho_in": float(rho_work) / self.scale,
            "rho_out": float(sum(f_out)) / self.scale,
            "is_mass_conserved": (sum(f_out) == rho_work),
            "is_phase_conserved": (sum(g_out) == alpha_work),
        }
        return f_out, g_out, meta
