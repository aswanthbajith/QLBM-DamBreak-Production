"""
Phase F21: Test Suite for Autonomy and Interlock Verification.
"""

import pytest
from quantum.f21_solver import PhaseF21ReversibleCSFSolver


def test_f21_autonomy_counters():
    """Verify exactly 1 init, 0 intermediate extractions, 0 re-encodings, 1 final readout."""
    solver = PhaseF21ReversibleCSFSolver(nx=4, ny=4, sigma=0.001)

    assert solver.num_state_preparations == 1
    assert solver.num_classical_extractions == 0
    assert solver.num_re_encodings == 0

    for _ in range(8):
        res = solver.step()
        assert res["is_autonomous"] == True
        assert res["csf_is_uncomputed"] == True

    assert solver.num_classical_extractions == 0
    assert solver.num_re_encodings == 0

    fields = solver.decode_final_fields()
    assert solver.num_classical_extractions == 1
