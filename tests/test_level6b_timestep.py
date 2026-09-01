"""
Unit tests for Level-6B hybrid timestep progression and quantum call accounting.
"""

import pytest
import numpy as np

from quantum.level6b_hybrid_solver import Level6BHybridTwoPhaseLBM


class TestLevel6BTimestep:
    """Test suite for Level-6B timestep stepping and execution accounting."""

    def test_01_step_counter_and_quantum_calls(self):
        """Verify quantum call counter increments by exactly (nx * ny) per timestep."""
        nx, ny = 8, 8
        s_6b = Level6BHybridTwoPhaseLBM(nx=nx, ny=ny)

        assert s_6b.step_count == 0
        assert s_6b.quantum_calls_total == 0

        s_6b.step()
        assert s_6b.step_count == 1
        assert s_6b.quantum_calls_total == 64
        assert s_6b.classical_reconstructions_total == 1

        s_6b.step()
        assert s_6b.step_count == 2
        assert s_6b.quantum_calls_total == 128
        assert s_6b.classical_reconstructions_total == 2

    def test_02_velocity_clamping_boundedness(self):
        """Verify velocity clamping strictly enforces max |u| <= 0.15."""
        nx, ny = 8, 8
        s_6b = Level6BHybridTwoPhaseLBM(nx=nx, ny=ny, g_acc=-0.01)

        for _ in range(10):
            diag = s_6b.step()
            assert diag["max_u"] <= 0.150001
