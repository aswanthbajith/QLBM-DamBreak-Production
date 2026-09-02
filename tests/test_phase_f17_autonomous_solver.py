"""
Phase F17: Test Suite for Autonomous Quantum Two-Phase Dam-Break Solver.
"""

import pytest
import numpy as np

from quantum.f17_autonomous_solver import PhaseF17ReversibleAutonomousQLBM


def test_autonomous_reversible_dam_break_solver():
    """Verify autonomous multi-step execution over T=16 with zero classical feedback."""
    solver = PhaseF17ReversibleAutonomousQLBM(nx=4, ny=4)

    assert solver.F17_AUTONOMOUS == True
    assert solver.num_state_preparations == 1
    assert solver.num_classical_extractions == 0
    assert solver.num_re_encodings == 0
    assert solver.num_quantum_timesteps == 0

    # Execute 16 autonomous timesteps
    for _ in range(16):
        res = solver.step()
        assert res["is_uncomputed"] == True
        assert res["total_garbage_residual"] == 0.0

    assert solver.num_quantum_timesteps == 16
    assert solver.num_state_preparations == 1
    assert solver.num_classical_extractions == 0
    assert solver.num_re_encodings == 0

    # Final decode at step T
    fields = solver.decode_final_fields()
    assert solver.num_classical_extractions == 1
    assert "f" in fields and "g" in fields
    assert fields["total_mass"] > 0.0
    assert fields["phase_mass"] > 0.0
