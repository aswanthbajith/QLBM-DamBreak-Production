"""
Phase F29: Test Suite for Global Mass and Phase Conservation on 8x8 Grid.
"""

import pytest
import numpy as np
from quantum.f29_scalable_circuit import F29ScalableQuantumCircuit


def test_8x8_mass_conservation():
    """Verify zero mass drift over 10 steps on 8x8 lattice."""
    circ = F29ScalableQuantumCircuit(nx=8, ny=8, frac_bits=12, bit_width=16)

    f_curr = np.full((9, 8, 8), 400, dtype=int)
    g_curr = np.full((9, 8, 8), 400, dtype=int)
    init_mass = int(np.sum(f_curr))

    for step in range(10):
        e_f = np.zeros((9, 8, 8), dtype=int)
        e_g = np.zeros((9, 8, 8), dtype=int)

        f_curr, g_curr, _, _, meta = circ.execute_one_timestep(f_curr, g_curr, e_f, e_g)

        assert meta["mass_drift"] == 0
        assert np.sum(f_curr) == init_mass
