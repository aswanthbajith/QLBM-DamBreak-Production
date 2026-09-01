"""
Unit tests for Level-6B Continuum Surface Force (CSF) surface tension.
"""

import pytest
import numpy as np
import scipy.linalg as la

from quantum.level6b_hybrid_solver import Level6BHybridTwoPhaseLBM
from classical.level4_two_phase import Level4TwoPhaseLBM


class TestLevel6BCSF:
    """Test suite for Level-6B CSF surface tension integration."""

    def test_01_surface_tension_force_consistency(self):
        """Verify CSF force calculation matches Level-4 reference."""
        nx, ny = 16, 8
        s_6b = Level6BHybridTwoPhaseLBM(nx=nx, ny=ny, sigma=0.001)
        s_ref = Level4TwoPhaseLBM(nx=nx, ny=ny, sigma=0.001)

        F_s_6b = s_6b.compute_surface_tension_force()
        F_s_ref = s_ref.compute_surface_tension_force()

        assert np.allclose(F_s_6b[0], F_s_ref[0], atol=1e-12)
        assert np.allclose(F_s_6b[1], F_s_ref[1], atol=1e-12)

    def test_02_zero_sigma_clean_isolation(self):
        """Verify zero surface tension cleanly disables CSF force."""
        nx, ny = 16, 8
        s_6b = Level6BHybridTwoPhaseLBM(nx=nx, ny=ny, sigma=0.0)
        F_s = s_6b.compute_surface_tension_force()

        assert np.all(F_s[0] == 0.0)
        assert np.all(F_s[1] == 0.0)
