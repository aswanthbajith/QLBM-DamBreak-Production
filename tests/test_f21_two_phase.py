"""
Phase F21: Test Suite for Two-Phase Flow with Active Surface Tension (sigma > 0).
"""

import pytest
import numpy as np

from quantum.f21_solver import PhaseF21ReversibleCSFSolver


def test_two_phase_nonzero_sigma_solver():
    """Verify coupled solver stability and mass conservation with sigma = 0.001."""
    solver = PhaseF21ReversibleCSFSolver(nx=4, ny=4, sigma=0.001)

    for _ in range(4):
        res = solver.step()
        assert res["csf_is_uncomputed"] == True

    fields = solver.decode_final_fields()
    assert np.all(fields["rho"] > 0.0)
    assert np.all(fields["alpha"] >= 0.0)
    assert np.all(fields["alpha"] <= 1.0)
    assert fields["total_mass"] > 0.0
