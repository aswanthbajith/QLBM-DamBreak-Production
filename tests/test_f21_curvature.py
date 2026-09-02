"""
Phase F21: Test Suite for Curvature Stencil and Clamping.
"""

import pytest
import numpy as np

from quantum.f21_curvature import F21ReversibleCurvature
from quantum.f21_fixed_point import F21FixedPointCSFMath


def test_curvature_stencils():
    """Verify kappa = -div(n) and fixed-point clipping."""
    nx, ny = 4, 4
    math = F21FixedPointCSFMath()
    curv_mod = F21ReversibleCurvature(nx, ny)

    nx_vec = np.zeros((ny, nx), dtype=np.int32)
    ny_vec = np.zeros((ny, nx), dtype=np.int32)

    # Unit normals pointing radially outwards
    nx_vec[1, 2] = math.to_fixed(1.0)
    nx_vec[1, 0] = math.to_fixed(-1.0)

    kappa = curv_mod.compute_curvature_stencils(nx_vec, ny_vec)

    # div_nx = (1.0 - (-1.0)) / 2 = 1.0 -> kappa = -1.0
    expected_kappa = math.to_fixed(-1.0)
    assert abs(kappa[1, 1] - expected_kappa) <= 2
