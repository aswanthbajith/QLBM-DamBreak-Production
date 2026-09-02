"""
Phase F19: Test Suite for Physical Equivalence against Classical Level-4 Oracle.
"""

import pytest
import numpy as np

from classical.level4_two_phase import Level4TwoPhaseLBM
from quantum.f19_solver import PhaseF19ReversibleDamBreakSolver


def test_physical_equivalence_level4():
    """Verify physical agreement between reversible embedding solver and Level-4 reference."""
    c_solver = Level4TwoPhaseLBM(nx=4, ny=4, g_acc=-0.0005, sigma=0.0, dam_width_ratio=0.5, dam_height_ratio=0.5)
    q_solver = PhaseF19ReversibleDamBreakSolver(nx=4, ny=4, g_acc=-0.0005, dam_width_ratio=0.5, dam_height_ratio=0.5)

    for _ in range(4):
        c_solver.step()
        q_solver.step()

    fields = q_solver.decode_final_fields()
    err_f = float(np.max(np.abs(fields["f"] - c_solver.f)))
    err_g = float(np.max(np.abs(fields["g"] - c_solver.g)))

    assert err_f < 0.25
    assert err_g < 0.15
