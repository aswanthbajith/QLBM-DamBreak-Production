"""
Phase F19: Test Suite for Autonomy and Absence of Intermediate Reads.
"""

import pytest
import numpy as np

from quantum.f19_solver import PhaseF19ReversibleDamBreakSolver


def test_autonomy_interlocks():
    """Verify operational counters confirm 0 intermediate reads and 0 re-encodings."""
    solver = PhaseF19ReversibleDamBreakSolver(nx=4, ny=4)

    assert solver.num_state_preparations == 1
    assert solver.num_classical_extractions == 0
    assert solver.num_re_encodings == 0

    for _ in range(16):
        solver.step()

    assert solver.num_classical_extractions == 0
    assert solver.num_re_encodings == 0

    fields = solver.decode_final_fields()
    assert solver.num_classical_extractions == 1
