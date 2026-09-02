"""
Phase F27: Test Suite for Precision Scaling and Error Convergence (Q4.8 to Q4.16).
"""

import pytest
from quantum.f26_pareto_analysis import F26ParetoAnalysis


def test_precision_sweep_conservation():
    """Verify exact integer mass conservation across precision formats."""
    sweep = F26ParetoAnalysis.run_precision_accuracy_sweep(nx=4, ny=4, sigma=0.001)

    assert len(sweep) == 7
    for row in sweep:
        assert row["is_mass_conserved"] == True
        assert row["is_phase_conserved"] == True
