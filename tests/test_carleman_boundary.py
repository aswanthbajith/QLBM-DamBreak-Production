import pytest
import numpy as np
from classical.reference_solver import apply_two_phase_boundary


class TestCarlemanBoundary:
    """
    Rigorously tests Step 10: Half-Way Bounce-Back Boundary Condition Properties.
    """

    def test_01_boundary_mass_conservation(self):
        np.random.seed(42)
        f_post = np.random.uniform(0.1, 1.0, (9, 4, 4))
        g_post = np.random.uniform(0.0, 1.0, (9, 4, 4))
        f_pre = np.copy(f_post)
        g_pre = np.copy(g_post)
        
        f_b, g_b = apply_two_phase_boundary(f_post, g_post, f_pre, g_pre)
        
        assert np.isclose(np.sum(f_b), np.sum(f_post))
        assert np.isclose(np.sum(g_b), np.sum(g_post))
