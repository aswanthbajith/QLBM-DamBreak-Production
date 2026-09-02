"""
Phase F24: Momentum Perturbation and Equilibrium Consistency Forensic Audit.

Proves:
1. Since c_0 = (0, 0), absorbing integer truncation residual into f_0 has
   EXACTLY ZERO effect on fluid momentum:
   Delta j = c_0 * Delta f_0 = (0, 0) (Strict Momentum Preservation).
2. Quantifies difference between guarded and unguarded BGK maps.
"""

from typing import Dict, Any, List
import numpy as np

from classical.d2q9 import C_X, C_Y
from quantum.f22_mass_conservation import F22ExactMassConservingBGKEngine
from quantum.f20_fixed_point import F20FixedPointBGKEngine


class F24MomentumForensicAudit:
    """
    Rigorously verifies momentum invariance under rest-particle integer redistribution.
    """

    @staticmethod
    def audit_momentum_invariance(
        f_in: List[int],
        g_in: List[int],
        F_ext: tuple = (0, 0),
    ) -> Dict[str, Any]:
        """
        Compares momentum j_x, j_y between guarded and uncorrected collision outputs.
        """
        engine_guarded = F22ExactMassConservingBGKEngine()
        engine_uncorrected = F20FixedPointBGKEngine()

        f_guard, g_guard, _ = engine_guarded.evaluate_conservative_bgk_map(f_in, g_in, F_ext=F_ext)
        f_raw, g_raw, _ = engine_uncorrected.evaluate_bgk_map(f_in, g_in, F_ext=F_ext)

        jx_guard = sum(f_guard[i] * C_X[i] for i in range(9))
        jy_guard = sum(f_guard[i] * C_Y[i] for i in range(9))

        jx_raw = sum(f_raw[i] * C_X[i] for i in range(9))
        jy_raw = sum(f_raw[i] * C_Y[i] for i in range(9))

        delta_jx = abs(jx_guard - jx_raw)
        delta_jy = abs(jy_guard - jy_raw)

        return {
            "jx_guard": jx_guard,
            "jx_raw": jx_raw,
            "jy_guard": jy_guard,
            "jy_raw": jy_raw,
            "delta_jx": delta_jx,
            "delta_jy": delta_jy,
            "is_momentum_strictly_preserved": (delta_jx == 0 and delta_jy == 0),
            "mass_guard_conserved": (sum(f_guard) == sum(f_in)),
            "mass_raw_drift": abs(sum(f_raw) - sum(f_in)),
        }
