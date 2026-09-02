"""
Phase F24: Independent Reference Implementation and 1000-State Monte Carlo Validation.

Builds an independent fixed-point integer reference implementation of D2Q9 two-phase BGK
to test against the Phase F22/F23 solver engine.
"""

from typing import Dict, Any, List, Tuple
import numpy as np

from classical.d2q9 import C_X, C_Y, W
from quantum.f22_mass_conservation import F22ExactMassConservingBGKEngine


class F24IndependentIntegerReference:
    """
    Independent reference implementation of fixed-point integer two-phase BGK.
    """

    def __init__(self, frac_bits: int = 12):
        self.frac_bits = frac_bits
        self.scale = 1 << frac_bits
        self.w_fixed = [int(round(w * self.scale)) for w in W]

    def compute_reference_bgk(
        self,
        f_in: List[int],
        g_in: List[int],
        omega_f_fixed: int = 4096,
        omega_g_fixed: int = 5851,
        F_ext: Tuple[int, int] = (0, 0),
        g_acc_fixed: int = -2,
    ) -> Tuple[List[int], List[int]]:
        """
        Independent clean-room calculation of conservative fixed-point BGK.
        """
        rho = sum(f_in)
        alpha = sum(g_in)

        # Shifted momentum
        jx = sum(f_in[i] * C_X[i] for i in range(9)) + F_ext[0] // 2
        jy = sum(f_in[i] * C_Y[i] for i in range(9)) + (((rho * g_acc_fixed) >> self.frac_bits) + F_ext[1]) // 2

        ux = (jx << self.frac_bits) // max(rho, 1)
        uy = (jy << self.frac_bits) // max(rho, 1)

        u2 = ((ux * ux) >> self.frac_bits) + ((uy * uy) >> self.frac_bits)

        f_out = [0] * 9
        g_out = [0] * 9

        for i in range(1, 9):
            cu = C_X[i] * ux + C_Y[i] * uy
            cu2 = (cu * cu) >> self.frac_bits

            bracket_f = self.scale + 3 * cu + (9 * cu2) // 2 - (3 * u2) // 2
            term_f = (rho * bracket_f) >> self.frac_bits
            f_eq = (self.w_fixed[i] * term_f) >> self.frac_bits

            bracket_g = self.scale + 3 * cu
            term_g = (alpha * bracket_g) >> self.frac_bits
            g_eq = (self.w_fixed[i] * term_g) >> self.frac_bits

            # Linear relaxation
            diff_f = f_eq - f_in[i]
            f_out[i] = f_in[i] + ((diff_f * omega_f_fixed) >> self.frac_bits)

            diff_g = g_eq - g_in[i]
            g_out[i] = g_in[i] + ((diff_g * omega_g_fixed) >> self.frac_bits)

        f_out[0] = rho - sum(f_out[1:9])
        g_out[0] = alpha - sum(g_out[1:9])

        return f_out, g_out

    @staticmethod
    def run_1000_state_monte_carlo(seed: int = 42) -> Dict[str, Any]:
        """
        Runs 1000 randomized state evaluations comparing independent reference against F22/F23 engine.
        """
        rng = np.random.default_rng(seed)
        ref = F24IndependentIntegerReference()
        engine = F22ExactMassConservingBGKEngine()

        num_trials = 1000
        matches = 0
        max_discrepancy = 0

        for _ in range(num_trials):
            # Generate random physically reasonable distributions
            rho_rand = rng.integers(2000, 5000)
            alpha_rand = rng.integers(500, 4000)

            # Random fractions summing to rho and alpha
            f_parts = rng.integers(10, 500, size=9)
            f_in = [int(val) for val in (f_parts * rho_rand // np.sum(f_parts))]
            f_in[0] += rho_rand - sum(f_in)

            g_parts = rng.integers(10, 500, size=9)
            g_in = [int(val) for val in (g_parts * alpha_rand // np.sum(g_parts))]
            g_in[0] += alpha_rand - sum(g_in)

            f_ref, g_ref = ref.compute_reference_bgk(f_in, g_in)
            f_eng, g_eng, _ = engine.evaluate_conservative_bgk_map(f_in, g_in)

            diff_f = max(abs(a - b) for a, b in zip(f_ref, f_eng))
            diff_g = max(abs(a - b) for a, b in zip(g_ref, g_eng))
            disc = max(diff_f, diff_g)

            if disc > max_discrepancy:
                max_discrepancy = disc

            if disc == 0:
                matches += 1

        return {
            "num_trials": num_trials,
            "exact_matches": matches,
            "match_rate_percent": (matches / num_trials) * 100.0,
            "max_discrepancy": max_discrepancy,
            "is_100_percent_consistent": (matches == num_trials),
        }
