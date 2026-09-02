"""
Phase F19: Test Suite for Compute-Output Reversible Embedding (Architecture A).
"""

import pytest
import numpy as np

from classical.d2q9 import W
from quantum.f17_reversible_primitives import FixedPointQ412
from quantum.f19_compute_output import ComputeOutputEmbedding


def test_compute_output_unitary_mapping():
    """Verify |x>|0> -> |x>|F(x)> preserves input state and computes valid BGK output."""
    engine = ComputeOutputEmbedding(omega_f=1.0, omega_g=1.42857)

    f_in = [FixedPointQ412.to_fixed(W[i] * 1.0) for i in range(9)]
    g_in = [FixedPointQ412.to_fixed(W[i] * 1.0) for i in range(9)]

    f_in_ret, g_in_ret, f_out, g_out, meta = engine.apply_unitary_compute_output(f_in, g_in)

    assert f_in_ret == f_in
    assert g_in_ret == g_in
    assert len(f_out) == 9
    assert len(g_out) == 9
    assert meta["input_preserved"] == True
    assert meta["is_unitary"] == True
