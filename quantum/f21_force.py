"""
Phase F21: Reversible Continuum Surface Force (CSF) Engine.

Computes:
|kappa, grad_x, grad_y, sigma, mask> |0> -> |... > |F_sx, F_sy>
"""

from typing import Tuple, List, Dict, Any
import numpy as np

from quantum.f21_fixed_point import F21FixedPointCSFMath


class F21ReversibleCSFForce:
    """
    Computes continuum surface force F_s = sigma * kappa * grad(alpha).
    """

    def __init__(self, nx: int, ny: int, sigma: float = 0.001, frac_bits: int = 12):
        self.nx = nx
        self.ny = ny
        self.sigma = sigma
        self.math = F21FixedPointCSFMath(frac_bits=frac_bits)
        self.sigma_fixed = self.math.to_fixed(sigma)

    def compute_surface_forces(
        self,
        kappa: np.ndarray,
        grad_x: np.ndarray,
        grad_y: np.ndarray,
        mask: np.ndarray,
    ) -> Tuple[np.ndarray, np.ndarray]:
        """
        Returns (F_sx, F_sy) in fixed-point representation.
        """
        ny, nx = self.ny, self.nx
        F_sx = np.zeros((ny, nx), dtype=np.int32)
        F_sy = np.zeros((ny, nx), dtype=np.int32)

        if self.sigma_fixed <= 0:
            return F_sx, F_sy

        for y in range(ny):
            for x in range(nx):
                if mask[y, x]:
                    k_val = int(kappa[y, x])
                    gx = int(grad_x[y, x])
                    gy = int(grad_y[y, x])

                    sigma_k = self.math.fixed_mul(self.sigma_fixed, k_val)
                    F_sx[y, x] = self.math.fixed_mul(sigma_k, gx)
                    F_sy[y, x] = self.math.fixed_mul(sigma_k, gy)
                else:
                    F_sx[y, x] = 0
                    F_sy[y, x] = 0

        return F_sx, F_sy
