"""
Phase F28: Test Suite for Boundary Bounce-Back Involution (B^2 = I).
"""

import pytest
import numpy as np
from classical.d2q9 import OPPOSITE


def test_boundary_bounce_back_involution():
    """Verify velocity bounce-back operator is strictly self-inverse: B^2 = I."""
    f = np.arange(9 * 2 * 2).reshape((9, 2, 2))

    # Apply B
    f_b1 = np.zeros_like(f)
    for i in range(9):
        opp_i = OPPOSITE[i]
        f_b1[opp_i] = f[i]

    # Apply B again
    f_b2 = np.zeros_like(f_b1)
    for i in range(9):
        opp_i = OPPOSITE[i]
        f_b2[opp_i] = f_b1[i]

    assert np.array_equal(f_b2, f)
