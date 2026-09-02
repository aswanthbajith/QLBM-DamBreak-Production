"""
Unit and benchmark tests for Level-7 Coherent Multi-Step Solver Prototype.
"""

import pytest
import numpy as np

from quantum.level7_coherent_multistep import Level7CoherentMultiStepSolver
from quantum.level6b_hybrid_solver import Level6BHybridTwoPhaseLBM


class TestLevel7MultiStepPrototype:
    """Test suite verifying Level-7 coherent multi-step solver prototype."""

    def test_01_prototype_initialization(self):
        """Verify solver prototype initializes correctly."""
        s7 = Level7CoherentMultiStepSolver(nx=4, ny=4)
        assert s7.f.shape == (9, 4, 4)
        assert s7.g.shape == (9, 4, 4)
        assert np.all(s7.rho >= 0.0)

    def test_02_coherent_k2_block_execution(self):
        """Verify K=2 coherent step executes stably with bounded density and phase."""
        s7 = Level7CoherentMultiStepSolver(nx=4, ny=4)
        diag = s7.step_coherent_block(K=2)

        assert diag["K_steps"] == 2
        assert diag["p_success_unamplified"] > 0.0
        assert np.all(np.isfinite(s7.rho))
        assert np.all(np.isfinite(s7.alpha))
        assert np.all(s7.rho > 0.0)

    def test_03_coherent_k4_block_execution(self):
        """Verify K=4 coherent step executes stably."""
        s7 = Level7CoherentMultiStepSolver(nx=4, ny=4)
        diag = s7.step_coherent_block(K=4)

        assert diag["K_steps"] == 4
        assert np.all(np.isfinite(s7.rho))
        assert np.all(s7.alpha >= 0.0)
        assert np.all(s7.alpha <= 1.0)
