"""
Phase F21: Test Suite for Gradient Norm and Unit Normal Vector.
"""

import pytest
import numpy as np

from quantum.f21_norm import F21ReversibleNorm
from quantum.f21_fixed_point import F21FixedPointCSFMath


def test_norm_and_unit_normals():
    """Verify gradient magnitude, interface masking, and unit normals."""
    nx, ny = 4, 4
    math = F21FixedPointCSFMath()
    norm_mod = F21ReversibleNorm(nx, ny)

    gx = np.zeros((ny, nx), dtype=np.int32)
    gy = np.zeros((ny, nx), dtype=np.int32)

    # Gradient along x at node (1, 1)
    gx[1, 1] = math.to_fixed(0.4)
    gy[1, 1] = math.to_fixed(0.3)

    norm_val, nx_vec, ny_vec, mask = norm_mod.compute_unit_normals(gx, gy)

    # Expected norm = sqrt(0.4^2 + 0.3^2) = 0.5
    expected_norm = math.to_fixed(0.5)
    assert abs(norm_val[1, 1] - expected_norm) <= 2
    assert mask[1, 1] == True
    # nx = 0.4 / 0.5 = 0.8, ny = 0.3 / 0.5 = 0.6
    assert abs(nx_vec[1, 1] - math.to_fixed(0.8)) <= 2
    assert abs(ny_vec[1, 1] - math.to_fixed(0.6)) <= 2
