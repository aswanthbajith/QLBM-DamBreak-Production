"""
Phase F20: Unit Test Suite for Fixed-Point Arithmetic and Quantization.
"""

import pytest
from classical.d2q9 import W
from quantum.f17_reversible_primitives import FixedPointQ412
from quantum.f20_fixed_point import F20FixedPointBGKEngine


def test_fixed_point_bgk_evaluation():
    """Verify finite-register evaluation of D2Q9 BGK collision."""
    engine = F20FixedPointBGKEngine(omega_f=1.0, omega_g=1.42857)

    f_in = [FixedPointQ412.to_fixed(W[i] * 1.0) for i in range(9)]
    g_in = [FixedPointQ412.to_fixed(W[i] * 1.0) for i in range(9)]

    f_out, g_out, meta = engine.evaluate_bgk_map(f_in, g_in)

    assert len(f_out) == 9
    assert len(g_out) == 9
    assert abs(meta["rho"] - 1.0) < 1e-4
    assert abs(meta["alpha"] - 1.0) < 1e-4
