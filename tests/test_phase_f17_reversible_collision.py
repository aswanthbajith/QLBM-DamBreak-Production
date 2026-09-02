"""
Phase F17: Test Suite for Reversible Two-Phase Collision Circuit & Uncomputation.
"""

import pytest
import numpy as np

from classical.d2q9 import W
from quantum.f17_reversible_primitives import FixedPointQ412
from quantum.f17_reversible_collision import ReversibleTwoPhaseCollisionCircuit


def test_reversible_two_phase_collision_and_uncomputation():
    """Verify reversible collision forward pass, moment calculation, and 100% uncomputation."""
    circuit = ReversibleTwoPhaseCollisionCircuit(omega_f=1.0, omega_g=1.42857)

    # Initial uniform liquid state
    f_in = [FixedPointQ412.to_fixed(W[i] * 1.0) for i in range(9)]
    g_in = [FixedPointQ412.to_fixed(W[i] * 1.0) for i in range(9)]

    f_post, g_post, meta = circuit.execute_collision(f_in, g_in)

    assert len(f_post) == 9
    assert len(g_post) == 9
    assert meta["is_uncomputed"] == True
    assert meta["garbage_residual"] == 0.0
    assert abs(meta["rho"] - 1.0) < 0.01
    assert abs(meta["alpha"] - 1.0) < 0.01
