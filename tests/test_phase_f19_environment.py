"""
Phase F19: Test Suite for Environment / Stinespring Embedding (Architecture B).
"""

import pytest
import numpy as np

from classical.d2q9 import W
from quantum.f17_reversible_primitives import FixedPointQ412
from quantum.f19_environment import EnvironmentStinespringEmbedding


def test_environment_stinespring_embedding():
    """Verify |x>|0>_E -> |F(x)>|x>_E environmental state retention."""
    env_engine = EnvironmentStinespringEmbedding(omega_f=1.0, omega_g=1.42857)

    f_in = [FixedPointQ412.to_fixed(W[i] * 1.0) for i in range(9)]
    g_in = [FixedPointQ412.to_fixed(W[i] * 1.0) for i in range(9)]

    f_out, g_out, e_f, e_g, meta = env_engine.execute_environment_dilation(f_in, g_in)

    assert e_f == f_in
    assert e_g == g_in
    assert meta["environment_retained"] == True
    assert meta["is_unitary"] == True
