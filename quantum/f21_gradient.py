"""
Phase F21: Reversible Discrete Gradient Stencil Engine.

Computes discrete central-difference phase gradients with zero-flux boundary conditions:
|alpha> |0> -> |alpha> |grad_x(alpha), grad_y(alpha)>
"""

from typing import Tuple, List, Dict, Any
import numpy as np

from quantum.f21_fixed_point import F21FixedPointCSFMath


class F21ReversibleGradient:
    """
    Reversible central-difference phase gradient operator on discrete fixed-point registers.
    """

    def __init__(self, nx: int, ny: int, frac_bits: int = 12):
        self.nx = nx
        self.ny = ny
        self.math = F21FixedPointCSFMath(frac_bits=frac_bits)

    def compute_gradient_stencils(
        self,
        alpha_reg: np.ndarray,
    ) -> Tuple[np.ndarray, np.ndarray]:
        """
        Computes grad_x and grad_y in fixed-point representation.
        alpha_reg has shape (ny, nx).
        """
        ny, nx = self.ny, self.nx
        grad_x = np.zeros((ny, nx), dtype=np.int32)
        grad_y = np.zeros((ny, nx), dtype=np.int32)

        # Internal stencils with zero-flux boundaries (matching Level-4)
        for y in range(ny):
            for x in range(1, nx - 1):
                # (alpha[y, x+1] - alpha[y, x-1]) / 2
                diff_x = int(alpha_reg[y, x + 1]) - int(alpha_reg[y, x - 1])
                grad_x[y, x] = diff_x // 2

        for y in range(1, ny - 1):
            for x in range(nx):
                # (alpha[y+1, x] - alpha[y-1, x]) / 2
                diff_y = int(alpha_reg[y + 1, x]) - int(alpha_reg[y - 1, x])
                grad_y[y, x] = diff_y // 2

        return grad_x, grad_y
