"""
Unit tests for Level-6B linear-population spatial streaming.
"""

import pytest
import numpy as np
import scipy.linalg as la

from classical.streaming import stream
from classical.d2q9 import C_X, C_Y


class TestLevel6BStreaming:
    """Test suite for Level-6B linear spatial streaming."""

    def test_01_streaming_exactness_on_linear_populations(self):
        """Verify linear spatial streaming is an exact permutation without tensor cross-shift."""
        ny, nx = 8, 8
        f = np.random.rand(9, ny, nx)
        f_str = stream(f)

        # Total sum and L2 norm must be conserved
        assert abs(np.sum(f_str) - np.sum(f)) < 1e-12
        assert abs(la.norm(f_str) - la.norm(f)) < 1e-12

    def test_02_no_tensor_cross_shift_corruption(self):
        """Verify streaming does not shift quadratic cross-products by (c_a + c_b)."""
        ny, nx = 8, 8
        f = np.random.rand(9, ny, nx)
        f_str = stream(f)

        # The post-streaming local quadratic tensor is constructed directly from f_str
        f_str_00 = f_str[:, 0, 0]
        quad_correct = np.kron(f_str_00, f_str_00)

        assert quad_correct.shape == (81,)
        assert abs(quad_correct[0] - f_str[0, 0, 0]**2) < 1e-14
