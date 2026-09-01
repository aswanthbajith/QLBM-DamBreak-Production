"""
Unit and integration tests for Level-6B Hybrid K=1 Local-Carleman Two-Phase Solver.
"""

import pytest
import numpy as np
import scipy.linalg as la

from quantum.level6b_hybrid_solver import Level6BHybridTwoPhaseLBM
from classical.level4_two_phase import Level4TwoPhaseLBM


class TestLevel6BHybrid:
    """Test suite for Level-6B hybrid solver core mechanics."""

    def test_01_solver_initialization_consistency(self):
        """Verify solver initializes physical fields matching Level-4 reference."""
        nx, ny = 16, 8
        s_6b = Level6BHybridTwoPhaseLBM(nx=nx, ny=ny)
        s_ref = Level4TwoPhaseLBM(nx=nx, ny=ny)

        assert np.allclose(s_6b.rho, s_ref.rho)
        assert np.allclose(s_6b.alpha, s_ref.alpha)
        assert np.allclose(s_6b.f, s_ref.f)
        assert np.allclose(s_6b.g, s_ref.g)

    def test_02_single_timestep_carleman_collision_accuracy(self):
        """Verify K=1 single-timestep Carleman collision matches Level-4 reference."""
        nx, ny = 16, 8
        s_6b = Level6BHybridTwoPhaseLBM(nx=nx, ny=ny, sigma=0.0)
        s_ref = Level4TwoPhaseLBM(nx=nx, ny=ny, sigma=0.0)

        s_6b.step()
        s_ref.step()

        err_rho = float(la.norm(s_6b.rho - s_ref.rho) / la.norm(s_ref.rho))
        err_alpha = float(la.norm(s_6b.alpha - s_ref.alpha) / la.norm(s_ref.alpha))

        # Must match reference to high precision
        assert err_rho < 1e-3, f"Single-step rho error too high: {err_rho:.4e}"
        assert err_alpha < 1e-3, f"Single-step alpha error too high: {err_alpha:.4e}"

    def test_03_mass_conservation_boundedness(self):
        """Verify liquid phase mass drift is bounded below 2% across 20 steps."""
        nx, ny = 16, 8
        s_6b = Level6BHybridTwoPhaseLBM(nx=nx, ny=ny)
        init_mass = float(np.sum(s_6b.alpha))

        for _ in range(20):
            s_6b.step()

        final_mass = float(np.sum(s_6b.alpha))
        mass_drift = abs(final_mass - init_mass) / init_mass

        assert mass_drift < 0.02, f"Mass drift exceeded 2%: {mass_drift:.4e}"
