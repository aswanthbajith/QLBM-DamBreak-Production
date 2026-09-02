"""
Phase F21: Test Suite for Reversible Gradient Stencils.
"""

import pytest
import numpy as np

from quantum.f21_gradient import F21ReversibleGradient
from quantum.f21_fixed_point import F21FixedPointCSFMath


def test_gradient_stencils():
    """Verify central-difference gradient stencils on discrete fixed-point lattice."""
    nx, ny = 4, 4
    math = F21FixedPointCSFMath()
    grad_mod = F21ReversibleGradient(nx, ny)

    # Linear field alpha = 0.5 * x / (nx - 1)
    alpha = np.zeros((ny, nx), dtype=np.int32)
    for y in range(ny):
        for x in range(nx):
            alpha[y, x] = math.to_fixed(0.5 * x / (nx - 1))

    gx, gy = grad_mod.compute_gradient_stencils(alpha)

    # (alpha[x+1] - alpha[x-1]) / 2 = (0.5 * (x+1 - (x-1)) / (nx-1)) / 2 = 0.5 / (nx-1)
    expected_gx = math.to_fixed(0.5 / (nx - 1))
    assert abs(gx[1, 1] - expected_gx) <= 1
    assert gy[1, 1] == 0  # no variation in y
