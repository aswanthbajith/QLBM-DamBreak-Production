"""
Phase F21: Test Suite for Reversible CSF Force Multiplication.
"""

import pytest
import numpy as np

from quantum.f21_force import F21ReversibleCSFForce
from quantum.f21_fixed_point import F21FixedPointCSFMath


def test_csf_force_computation():
    """Verify F_s = sigma * kappa * grad(alpha)."""
    nx, ny = 4, 4
    sigma = 0.005
    math = F21FixedPointCSFMath()
    force_mod = F21ReversibleCSFForce(nx, ny, sigma=sigma)

    kappa = np.zeros((ny, nx), dtype=np.int32)
    gx = np.zeros((ny, nx), dtype=np.int32)
    gy = np.zeros((ny, nx), dtype=np.int32)
    mask = np.zeros((ny, nx), dtype=bool)

    kappa[1, 1] = math.to_fixed(-1.0)
    gx[1, 1] = math.to_fixed(0.4)
    gy[1, 1] = math.to_fixed(0.0)
    mask[1, 1] = True

    Fs_x, Fs_y = force_mod.compute_surface_forces(kappa, gx, gy, mask)

    # Expected Fs_x = 0.005 * (-1.0) * 0.4 = -0.002
    expected_fsx = math.to_fixed(-0.002)
    assert abs(Fs_x[1, 1] - expected_fsx) <= 2
    assert Fs_y[1, 1] == 0
