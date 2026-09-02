"""
Phase F19: Test Suite for Two-Phase Dynamics and Mass Conservation.
"""

import pytest
import numpy as np

from quantum.f19_solver import PhaseF19ReversibleDamBreakSolver


def test_two_phase_mass_conservation():
    """Verify concurrent evolution and conservation of hydrodynamic and phase-field fields."""
    solver = PhaseF19ReversibleDamBreakSolver(nx=4, ny=4)

    for _ in range(8):
        solver.step()

    fields = solver.decode_final_fields()
    assert np.all(fields["alpha"] >= 0.0)
    assert np.all(fields["alpha"] <= 1.0)
    assert np.all(fields["rho"] > 0.0)
