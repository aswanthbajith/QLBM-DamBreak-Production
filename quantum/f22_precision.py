"""
Phase F22: Multi-Precision Scaling Engine (Q4.12 vs Q4.16 vs Q4.20).

Audits relative error scaling of gradients, normals, curvature, and CSF forces
as a function of fractional bit-width.
"""

from typing import Dict, Any, List
import numpy as np

from classical.level4_two_phase import Level4TwoPhaseLBM
from quantum.f21_fixed_point import F21FixedPointCSFMath
from quantum.f21_csf import F21ReversibleCSFPipeline


class F22PrecisionScalingStudy:
    """
    Evaluates fixed-point error convergence across Q4.12, Q4.16, and Q4.20.
    """

    @staticmethod
    def run_droplet_precision_benchmark(
        nx: int = 8,
        ny: int = 8,
        sigma: float = 0.005,
    ) -> List[Dict[str, Any]]:
        """
        Runs precision benchmark on an 8x8 circular droplet.
        """
        # Classical ground-truth reference
        c_lbm = Level4TwoPhaseLBM(nx=nx, ny=ny, sigma=sigma)
        cx, cy = (nx - 1) / 2.0, (ny - 1) / 2.0
        alpha = np.zeros((ny, nx), dtype=np.float64)
        for y in range(ny):
            for x in range(nx):
                r = np.sqrt((x - cx) ** 2 + (y - cy) ** 2)
                alpha[y, x] = 0.5 * (1.0 - np.tanh((r - 2.0) / 0.8))
        c_lbm.alpha = np.copy(alpha)
        c_Fs = c_lbm.compute_surface_tension_force()
        c_norm_l2 = float(la_norm := np.linalg.norm(c_Fs))

        results = []
        for name, frac in [("Q4.12", 12), ("Q4.16", 16), ("Q4.20", 20)]:
            math = F21FixedPointCSFMath(frac_bits=frac)
            pipeline = F21ReversibleCSFPipeline(nx, ny, sigma=sigma, frac_bits=frac)

            alpha_reg = np.zeros((ny, nx), dtype=np.int32)
            for y in range(ny):
                for x in range(nx):
                    alpha_reg[y, x] = math.to_fixed(alpha[y, x])

            Fs_x_fix, Fs_y_fix, meta = pipeline.execute_reversible_csf(alpha_reg)
            q_Fs = np.zeros((2, ny, nx), dtype=np.float64)
            for y in range(ny):
                for x in range(nx):
                    q_Fs[0, y, x] = math.to_float(Fs_x_fix[y, x])
                    q_Fs[1, y, x] = math.to_float(Fs_y_fix[y, x])

            err_inf = float(np.max(np.abs(q_Fs - c_Fs)))
            err_rel = float(np.linalg.norm(q_Fs - c_Fs) / (c_norm_l2 + 1e-14))

            results.append({
                "format": name,
                "frac_bits": frac,
                "lsb_resolution": 1.0 / (1 << frac),
                "force_Linf_error": err_inf,
                "force_relative_L2_error": err_rel,
                "is_sub_1_percent": (err_rel < 0.01),
            })
        return results
