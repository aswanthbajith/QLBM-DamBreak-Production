"""
Phase F22: Test Suite for Multi-Timestep CPTP Channel Solver with Exact Mass Conservation.
"""

import pytest
import numpy as np

from classical.level4_two_phase import Level4TwoPhaseLBM
from quantum.f22_channel_solver import PhaseF22CPTPChannelSolver


def test_multistep_cptp_channel_mass_conservation():
    """Verify exact zero mass leakage across multi-step evolution with active CSF."""
    solver = PhaseF22CPTPChannelSolver(nx=4, ny=4, sigma=0.001)

    initial_fields = solver.decode_final_fields()
    initial_mass = initial_fields["total_mass"]

    for step_idx in range(16):
        res = solver.step()
        assert res["is_mass_conserved"] == True
        assert res["mass_drift_int"] == 0

    final_fields = solver.decode_final_fields()
    # Total mass must remain EXACTLY equal to initial decoded mass (0.0000000000 mass drift)
    assert abs(final_fields["total_mass"] - initial_mass) == 0.0
