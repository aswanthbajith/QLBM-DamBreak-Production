"""
Phase F20: Unit Test Suite for Autonomous Quantum Channel Execution.
"""

import pytest
from quantum.f20_solver import PhaseF20ChannelEquivalenceSolver


def test_autonomy_counters():
    """Verify exactly 1 init, 0 intermediate reads, 0 re-encodings, 1 final readout."""
    solver = PhaseF20ChannelEquivalenceSolver(nx=4, ny=4)

    assert solver.num_state_preparations == 1
    assert solver.num_classical_extractions == 0
    assert solver.num_re_encodings == 0

    for _ in range(8):
        res = solver.step()
        assert res["is_cptp_channel"] == True

    assert solver.num_classical_extractions == 0
    assert solver.num_re_encodings == 0

    fields = solver.decode_final_fields()
    assert solver.num_classical_extractions == 1
