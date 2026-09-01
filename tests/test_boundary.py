import pytest
import numpy as np
from classical.boundary import apply_noslip_box
from classical.d2q9 import OPPOSITE

class TestBoundary:
    def test_01_noslip_box_reflection(self):
        f_pre = np.ones((9, 4, 4))
        f_post = np.zeros((9, 4, 4))
        f_b = apply_noslip_box(f_post, f_pre)
        # Check that perimeter boundaries are reflected
        for i in range(9):
            opp = OPPOSITE[i]
            assert np.allclose(f_b[i, 0, :], f_pre[opp, 0, :])
            assert np.allclose(f_b[i, -1, :], f_pre[opp, -1, :])
