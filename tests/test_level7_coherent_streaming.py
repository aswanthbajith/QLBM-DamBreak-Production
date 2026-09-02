"""
Unit tests for Level-7 coherent spatial streaming permutation circuits and bounce-back boundaries.
"""

import pytest
import numpy as np
import scipy.linalg as la

from classical.streaming import stream
from classical.d2q9 import OPPOSITE


class TestLevel7CoherentStreaming:
    """Test suite verifying unitary streaming and boundary properties."""

    def test_01_streaming_unitarity_and_norm_conservation(self):
        """Verify spatial streaming permutation matrix is unitary and conserves state norm."""
        ny, nx = 4, 4
        f = np.random.rand(9, ny, nx)
        f_str = stream(f)

        assert abs(la.norm(f_str) - la.norm(f)) < 1e-12
        assert abs(np.sum(f_str) - np.sum(f)) < 1e-12

    def test_02_bounce_back_involution(self):
        """Verify solid wall bounce-back satisfies exact involution B^2 = I."""
        opp = OPPOSITE
        for i in range(9):
            assert opp[opp[i]] == i, f"Bounce-back involution failed for velocity {i}"
