"""
Phase F21: Test Suite for Multi-Step Dam-Break Evolution with Nonzero Surface Tension.
"""

import pytest
import numpy as np

from classical.level4_two_phase import Level4TwoPhaseLBM
from quantum.f21_solver import PhaseF21ReversibleCSFSolver


def test_multistep_physical_equivalence_nonzero_sigma():
    """Compare Phase F21 reversible solver against classical Level-4 solver with sigma = 0.001."""
    sigma = 0.001
    c_solver = Level4TwoPhaseLBM(nx=4, ny=4, sigma=sigma, g_acc=-0.0005, dam_width_ratio=0.5, dam_height_ratio=0.5)
    q_solver = PhaseF21ReversibleCSFSolver(nx=4, ny=4, sigma=sigma, g_acc=-0.0005, dam_width_ratio=0.5, dam_height_ratio=0.5)

    for _ in range(4):
        c_solver.step()
        q_solver.step()

    fields = q_solver.decode_final_fields()
    err_f = float(np.max(np.abs(fields["f"] - c_solver.f)))
    err_g = float(np.max(np.abs(fields["g"] - c_solver.g)))

    assert err_f < 0.25
    assert err_g < 0.15
