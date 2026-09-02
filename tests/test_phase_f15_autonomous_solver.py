"""
Phase F15: Test Suite for Autonomous Quantum Two-Phase Dam-Break Solver.
"""

import pytest
import numpy as np

from classical.level4_two_phase import Level4TwoPhaseLBM
from quantum.f15_autonomous_solver import PhaseF15AutonomousTwoPhaseQLBM


def test_autonomous_carleman_multi_step_solver():
    """Verify autonomous multi-step execution with zero intermediate classical queries."""
    solver = PhaseF15AutonomousTwoPhaseQLBM(nx=4, ny=4)

    assert solver.F15_AUTONOMOUS == True
    assert solver.num_state_preparations == 1
    assert solver.num_classical_extractions == 0
    assert solver.num_re_encodings == 0
    assert solver.num_quantum_timesteps == 0

    # Advance 8 autonomous timesteps
    for _ in range(8):
        solver.step()

    assert solver.num_quantum_timesteps == 8
    assert solver.num_state_preparations == 1
    assert solver.num_classical_extractions == 0
    assert solver.num_re_encodings == 0

    # Final decode at step T
    fields = solver.decode_final_fields()
    assert solver.num_classical_extractions == 1
    assert "f" in fields and "g" in fields
    assert float(np.sum(fields["f"])) > 0.0
