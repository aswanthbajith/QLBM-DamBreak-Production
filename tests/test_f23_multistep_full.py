"""
Phase F23: Test Suite for Full Multi-Timestep CPTP Channel Trajectory vs Level-4 Reference.
"""

import pytest
from quantum.f23_equivalence_engine import F23TwoPhaseEquivalenceEngine


def test_full_multistep_cptp_trajectory():
    """Verify multi-step accuracy and zero mass drift across T=1..32."""
    trajectory = F23TwoPhaseEquivalenceEngine.run_multistep_comparison_trajectory(
        nx=4, ny=4, sigma=0.001, timesteps=[1, 2, 4, 8, 16, 32]
    )

    assert len(trajectory) == 6
    for row in trajectory:
        assert row["is_conserved"] == True
        assert row["mass_drift"] == 0.0
        assert row["f_Linf"] < 0.20
        assert row["g_Linf"] < 0.15
