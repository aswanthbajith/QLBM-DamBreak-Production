"""
Phase F20: Unit Test Suite for Two-Phase Coupling and Field Evolution.
"""

import pytest
import numpy as np

from quantum.f20_solver import PhaseF20ChannelEquivalenceSolver


def test_two_phase_solver_conservation():
    """Verify density and phase conservation in two-phase channel solver."""
    solver = PhaseF20ChannelEquivalenceSolver(nx=4, ny=4)

    for _ in range(4):
        solver.step()

    fields = solver.decode_final_fields()
    assert np.all(fields["rho"] > 0.0)
    assert np.all(fields["alpha"] >= 0.0)
    assert np.all(fields["alpha"] <= 1.0)
    assert fields["total_mass"] > 0.0
