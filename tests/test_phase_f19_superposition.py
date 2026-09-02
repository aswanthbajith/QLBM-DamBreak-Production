"""
Phase F19: Test Suite for Superposition and Inner-Product Preservation.
"""

import pytest
import numpy as np

from classical.d2q9 import W
from quantum.f17_reversible_primitives import FixedPointQ412
from quantum.f19_superposition import SuperpositionVerificationEngine


def test_superposition_and_inner_product_preservation():
    """Verify global unitary inner product preservation for superpositions of distinct states."""
    engine = SuperpositionVerificationEngine()

    f1 = [FixedPointQ412.to_fixed(W[i] * 1.0) for i in range(9)]
    g1 = [FixedPointQ412.to_fixed(W[i] * 1.0) for i in range(9)]

    delta = FixedPointQ412.to_fixed(0.02)
    f2 = list(f1)
    f2[1] += delta
    f2[3] += delta
    f2[2] -= delta
    f2[4] -= delta
    g2 = list(g1)

    res = engine.test_superposition_and_inner_product(f1, g1, f2, g2)

    assert res["physical_collapsed"] == True
    assert res["joint_state_distinct"] == True
    assert res["inner_product_joint"] == 0.0
    assert res["mode_reconstruction_error"] == 0
    assert res["is_global_unitary"] == True
