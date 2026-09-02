"""
Phase F21: Reversible Norm and Unit Normal Vector Engine.

Computes:
|grad_x, grad_y> |0> -> |grad_x, grad_y> |norm, n_x, n_y, mask>
"""

from typing import Tuple, List, Dict, Any
import numpy as np

from quantum.f21_fixed_point import F21FixedPointCSFMath


class F21ReversibleNorm:
    """
    Computes gradient magnitude, interface mask, and unit normal vector.
    """

    def __init__(self, nx: int, ny: int, frac_bits: int = 12):
        self.nx = nx
        self.ny = ny
        self.math = F21FixedPointCSFMath(frac_bits=frac_bits)
        self.mask_thresh_fixed = self.math.to_fixed(1e-3)

    def compute_unit_normals(
        self,
        grad_x: np.ndarray,
        grad_y: np.ndarray,
    ) -> Tuple[np.ndarray, np.ndarray, np.ndarray, np.ndarray]:
        """
        Returns (grad_norm, nx_vec, ny_vec, mask).
        """
        ny, nx = self.ny, self.nx
        grad_norm = np.zeros((ny, nx), dtype=np.int32)
        nx_vec = np.zeros((ny, nx), dtype=np.int32)
        ny_vec = np.zeros((ny, nx), dtype=np.int32)
        mask = np.zeros((ny, nx), dtype=bool)

        for y in range(ny):
            for x in range(nx):
                gx = int(grad_x[y, x])
                gy = int(grad_y[y, x])

                gx2 = self.math.fixed_mul(gx, gx)
                gy2 = self.math.fixed_mul(gy, gy)
                norm_sq = gx2 + gy2
                norm_val = self.math.fixed_sqrt(norm_sq)
                grad_norm[y, x] = norm_val

                if norm_val > self.mask_thresh_fixed:
                    mask[y, x] = True
                    nx_vec[y, x] = self.math.fixed_div(gx, norm_val)
                    ny_vec[y, x] = self.math.fixed_div(gy, norm_val)
                else:
                    mask[y, x] = False
                    nx_vec[y, x] = 0
                    ny_vec[y, x] = 0

        return grad_norm, nx_vec, ny_vec, mask
