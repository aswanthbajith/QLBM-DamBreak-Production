"""
Phase F19: Test Suite for BGK Non-Injectivity & Bijectivity Counterexamples.
"""

import pytest
import numpy as np

from classical.d2q9 import W
from quantum.f17_reversible_primitives import FixedPointQ412
from quantum.f19_compute_output import ComputeOutputEmbedding


def test_bgk_many_to_one_counterexample():
    """Verify that multiple distinct input states map to the exact same physical post-collision state."""
    engine = ComputeOutputEmbedding(omega_f=1.0, omega_g=1.42857)

    # State 1: Uniform equilibrium
    f1 = [FixedPointQ412.to_fixed(W[i] * 1.0) for i in range(9)]
    g1 = [FixedPointQ412.to_fixed(W[i] * 1.0) for i in range(9)]

    # State 2: Perturbed non-equilibrium state with net 0 mass and 0 momentum difference
    delta = FixedPointQ412.to_fixed(0.02)
    f2 = list(f1)
    f2[1] += delta
    f2[3] += delta
    f2[2] -= delta
    f2[4] -= delta
    g2 = list(g1)

    f1_out, g1_out, _ = engine.evaluate_physical_bgk(f1, g1)
    f2_out, g2_out, _ = engine.evaluate_physical_bgk(f2, g2)

    # Input states are distinct
    assert f1 != f2
    # Output states are identical (non-injective collapse)
    assert f1_out == f2_out
    assert g1_out == g2_out
