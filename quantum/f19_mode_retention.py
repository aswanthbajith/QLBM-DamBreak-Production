"""
Phase F19: Mode-Retaining Reversible Collision Embedding (Architecture C).

Implements the bijective decomposition:
|f> |0> -> |f_eq> |f_neq>

where f_neq = f - f_eq stores non-equilibrium kinetic stress modes.
Physical relaxation scales f_neq by (1 - omega_f), preserving all degrees of freedom reversibly.
"""

from typing import Tuple, Dict, Any, List
import numpy as np

from classical.d2q9 import C_X, C_Y, W
from quantum.f17_reversible_primitives import FixedPointQ412, ReversibleFixedPointArithmetic


class ModeRetainingEmbedding:
    """
    Architecture C: Mode-Retaining Reversible Embedding.
    Decomposes populations into conserved equilibrium (f_eq) and dissipative non-equilibrium (f_neq).
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

    def decompose_modes(
        self,
        f_in: List[int],
        g_in: List[int],
    ) -> Tuple[List[int], List[int], List[int], List[int], Dict[str, Any]]:
        """
        Executes reversible mode decomposition:
        |f, g> |0, 0> -> |f_eq, g_eq> |f_neq, g_neq>
        """
        rho_work = sum(f_in)
        alpha_work = sum(g_in)

        jx_work = sum(f_in[i] * C_X[i] for i in range(9))
        jy_work = sum(f_in[i] * C_Y[i] for i in range(9))
        jy_work += self.arith.multiply(rho_work, self.g_acc_fixed) // 2

        ux_work = self.arith.divide(jx_work, max(rho_work, 1))
        uy_work = self.arith.divide(jy_work, max(rho_work, 1))

        ux2 = self.arith.multiply(ux_work, ux_work)
        uy2 = self.arith.multiply(uy_work, uy_work)
        u2_work = ux2 + uy2

        f_eq = [0] * 9
        g_eq = [0] * 9
        f_neq = [0] * 9
        g_neq = [0] * 9

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
            f_eq[i] = self.arith.multiply(self.w_fixed[i], term_f)
            f_neq[i] = f_in[i] - f_eq[i]

            bracket_g = FixedPointQ412.SCALE + 3 * c_dot_u
            term_g = self.arith.multiply(alpha_work, bracket_g)
            g_eq[i] = self.arith.multiply(self.w_fixed[i], term_g)
            g_neq[i] = g_in[i] - g_eq[i]

        meta = {
            "rho": FixedPointQ412.to_float(rho_work),
            "alpha": FixedPointQ412.to_float(alpha_work),
            "is_bijective": True,
        }
        return f_eq, g_eq, f_neq, g_neq, meta

    def reconstruct_from_modes(
        self,
        f_eq: List[int],
        g_eq: List[int],
        f_neq: List[int],
        g_neq: List[int],
    ) -> Tuple[List[int], List[int]]:
        """Exact inverse reconstruction: f = f_eq + f_neq."""
        f_rec = [f_eq[i] + f_neq[i] for i in range(9)]
        g_rec = [g_eq[i] + g_neq[i] for i in range(9)]
        return f_rec, g_rec
