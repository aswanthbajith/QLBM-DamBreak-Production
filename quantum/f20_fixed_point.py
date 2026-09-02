"""
Phase F20: Exact Finite-Register Fixed-Point Representation and Quantization Engine.

Defines the exact register formats, bit-widths, rounding, clipping, and overflow behavior
for D2Q9 hydrodynamic and phase-field BGK collision.
"""

from typing import Tuple, List, Dict, Any
import numpy as np

from classical.d2q9 import C_X, C_Y, W
from quantum.f17_reversible_primitives import FixedPointQ412, ReversibleFixedPointArithmetic


class F20FixedPointBGKEngine:
    """
    Finite-register BGK collision engine supporting exact register-level accounting.
    """

    def __init__(
        self,
        omega_f: float = 1.0,
        omega_g: float = 1.42857,
        g_acc: float = -0.0005,
    ):
        self.arith = ReversibleFixedPointArithmetic(frac_bits=FixedPointQ412.FRAC_BITS)
        self.omega_f_fixed = FixedPointQ412.to_fixed(omega_f)
        self.omega_g_fixed = FixedPointQ412.to_fixed(omega_g)
        self.g_acc_fixed = FixedPointQ412.to_fixed(g_acc)
        self.w_fixed = [FixedPointQ412.to_fixed(w) for w in W]

    def evaluate_bgk_map(
        self,
        f_in: List[int],
        g_in: List[int],
        F_ext: Tuple[int, int] = (0, 0),
    ) -> Tuple[List[int], List[int], Dict[str, Any]]:
        """
        Evaluates exact finite-register BGK map F(x) with optional external force.
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

        for i in range(9):
            c_dot_u = C_X[i] * ux_work + C_Y[i] * uy_work
            c_dot_u_sq = self.arith.multiply(c_dot_u, c_dot_u)

            bracket_f = (
                FixedPointQ412.SCALE
                + 3 * c_dot_u
                + (9 * c_dot_u_sq) // 2
                - (3 * u2_work) // 2
            )
            term_f = self.arith.multiply(rho_work, bracket_f)
            f_eq = self.arith.multiply(self.w_fixed[i], term_f)

            bracket_g = FixedPointQ412.SCALE + 3 * c_dot_u
            term_g = self.arith.multiply(alpha_work, bracket_g)
            g_eq = self.arith.multiply(self.w_fixed[i], term_g)

            f_out[i] = self.arith.linear_interpolate(f_in[i], f_eq, self.omega_f_fixed)
            g_out[i] = self.arith.linear_interpolate(g_in[i], g_eq, self.omega_g_fixed)

        meta = {
            "rho": FixedPointQ412.to_float(rho_work),
            "alpha": FixedPointQ412.to_float(alpha_work),
            "ux": FixedPointQ412.to_float(ux_work),
            "uy": FixedPointQ412.to_float(uy_work),
        }
        return f_out, g_out, meta
