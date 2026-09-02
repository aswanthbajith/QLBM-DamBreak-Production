"""
Phase F19: Test Suite for Multi-Step Information Accounting & Memory Scaling.
"""

import pytest
import numpy as np

from quantum.f19_solver import PhaseF19ReversibleDamBreakSolver


def test_information_accounting_multi_step():
    """Verify multi-step execution and information register scaling."""
    solver = PhaseF19ReversibleDamBreakSolver(nx=4, ny=4)

    for _ in range(8):
        res = solver.step()
        assert res["is_unitary_embedding"] == True

    fields = solver.decode_final_fields()
    assert fields["total_mass"] > 0.0
    assert fields["phase_mass"] > 0.0
