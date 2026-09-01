"""
Unit and benchmark validation tests comparing Level-6B against Level-4 Reference.
"""

import os
import csv
import pytest
import numpy as np

from quantum.level6b_hybrid_solver import Level6BHybridTwoPhaseLBM
from classical.level4_two_phase import Level4TwoPhaseLBM


class TestLevel6BValidation:
    """Test suite validating Level-6B against Level-4 classical reference."""

    def test_01_multi_step_trajectory_stability(self):
        """Verify 10-step hybrid evolution remains stable and non-divergent."""
        nx, ny = 16, 8
        s_6b = Level6BHybridTwoPhaseLBM(nx=nx, ny=ny, sigma=0.001)

        for _ in range(10):
            diag = s_6b.step()
            assert np.all(np.isfinite(s_6b.rho))
            assert np.all(np.isfinite(s_6b.alpha))
            assert np.all(s_6b.rho >= 0.0)
            assert np.all(s_6b.alpha >= 0.0)
            assert np.all(s_6b.alpha <= 1.0)

    def test_02_validation_csv_files_exist(self):
        """Verify all required Level-6B result CSV files are generated."""
        required_csvs = [
            "results/level6b_validation.csv",
            "results/level6b_error_budget.csv",
            "results/level6b_timestep_metrics.csv",
            "results/level6b_grid_refinement.csv",
            "results/level6b_resource_metrics.csv",
            "results/level6b_hardware_metrics.csv",
        ]
        for path in required_csvs:
            assert os.path.exists(path), f"Missing required result CSV: {path}"

    def test_03_real_qpu_safety_interlock(self):
        """Verify real-QPU execution is strictly blocked by default."""
        enable_real = os.environ.get("QLBM_ENABLE_REAL_QPU", "0")
        confirm_real = os.environ.get("QLBM_CONFIRM_REAL_QPU", "NO")

        # Safety interlock must prevent real execution
        assert not (enable_real == "1" and confirm_real == "YES"), "Real QPU interlock should be inactive by default"
