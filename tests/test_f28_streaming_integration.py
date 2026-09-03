"""
Phase F28: Test Suite for Spatial Streaming Permutation (S^dag S = I).
"""

import pytest
import numpy as np
from classical.d2q9 import C_X, C_Y


def test_streaming_permutation_unitarity():
    """Verify coordinate shift permutation is strictly unitary / invertible."""
    f = np.arange(9 * 2 * 2).reshape((9, 2, 2))

    # Forward Streaming
    f_stream = np.zeros_like(f)
    for i in range(9):
        dx, dy = int(C_X[i]), int(C_Y[i])
        f_stream[i] = np.roll(np.roll(f[i], dx, axis=1), dy, axis=0)

    # Inverse Streaming
    f_unstream = np.zeros_like(f_stream)
    for i in range(9):
        dx, dy = int(C_X[i]), int(C_Y[i])
        f_unstream[i] = np.roll(np.roll(f_stream[i], -dx, axis=1), -dy, axis=0)

    assert np.array_equal(f_unstream, f)
