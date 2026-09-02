"""
Phase F21: Reversible Curvature Stencil Engine.

Computes discrete interface curvature kappa = -div(n):
|n_x, n_y> |0> -> |n_x, n_y> |kappa>
"""

from typing import Tuple, List, Dict, Any
import numpy as np

from quantum.f21_fixed_point import F21FixedPointCSFMath


class F21ReversibleCurvature:
    """
    Computes interface curvature kappa = -div(n) with fixed-point clamping.
    """

    def __init__(self, nx: int, ny: int, frac_bits: int = 12):
        self.nx = nx
        self.ny = ny
        self.math = F21FixedPointCSFMath(frac_bits=frac_bits)

    def compute_curvature_stencils(
        self,
        nx_vec: np.ndarray,
        ny_vec: np.ndarray,
    ) -> np.ndarray:
        """
        Computes kappa = clip(-(div_x(nx) + div_y(ny)), -2.0, 2.0).
        """
        ny, nx = self.ny, self.nx
        div_nx = np.zeros((ny, nx), dtype=np.int32)
        div_ny = np.zeros((ny, nx), dtype=np.int32)
        kappa = np.zeros((ny, nx), dtype=np.int32)

        for y in range(ny):
            for x in range(1, nx - 1):
                diff_nx = int(nx_vec[y, x + 1]) - int(nx_vec[y, x - 1])
                div_nx[y, x] = diff_nx // 2

        for y in range(1, ny - 1):
            for x in range(nx):
                diff_ny = int(ny_vec[y + 1, x]) - int(ny_vec[y - 1, x])
                div_ny[y, x] = diff_ny // 2

        for y in range(ny):
            for x in range(nx):
                div_total = div_nx[y, x] + div_ny[y, x]
                neg_div = -div_total
                kappa[y, x] = self.math.fixed_clip(neg_div, -2.0, 2.0)

        return kappa
