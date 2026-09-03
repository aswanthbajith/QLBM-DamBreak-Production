"""
Phase F30: Test Suite for Clean-Room Multi-Lattice Engine (4x4, 8x8).
"""

import pytest
import numpy as np
from quantum.f30_cleanroom_reference import F30CleanRoomScalableReference


def test_cleanroom_multi_lattice_conservation():
    """Verify cleanroom reference conserves mass and phase on 4x4 and 8x8 grids."""
    for n in [4, 8]:
        ref = F30CleanRoomScalableReference(nx=n, ny=n, frac_bits=12)
        f_in = np.full((9, n, n), 400, dtype=int)
        g_in = np.full((9, n, n), 400, dtype=int)

        f_out, g_out = ref.step(f_in, g_in)

        assert np.sum(f_out) == np.sum(f_in)
        assert np.sum(g_out) == np.sum(g_in)
