"""
Phase F23: Test Suite for One-Step Lattice Equivalence vs Level-4 Reference.
"""

import pytest
from quantum.f23_equivalence_engine import F23TwoPhaseEquivalenceEngine


def test_one_step_equivalence_across_lattices():
    """Verify one-step physical equivalence on 2x2 and 4x4 domains."""
    for n in [2, 4]:
        res = F23TwoPhaseEquivalenceEngine.run_one_step_lattice_comparison(nx=n, ny=n, sigma=0.001)
        assert res["is_equivalent_within_q412"] == True
        assert res["err_f_Linf"] < 0.01
        assert res["err_g_Linf"] < 0.01
        assert res["err_rho_Linf"] < 0.01
