"""
Phase F28: Test Suite for Independent Clean-Room 2x2 Engine.
"""

import pytest
import numpy as np
from quantum.f28_cleanroom_2x2_reference import F28CleanRoom2x2Reference


def test_cleanroom_reference_step():
    """Verify cleanroom reference executes single step and conserves mass."""
    ref = F28CleanRoom2x2Reference(frac_bits=12)

    f_in = np.full((9, 2, 2), 400, dtype=int)
    g_in = np.full((9, 2, 2), 400, dtype=int)

    f_out, g_out = ref.step(f_in, g_in)

    assert np.sum(f_out) == np.sum(f_in)
    assert np.sum(g_out) == np.sum(g_in)
