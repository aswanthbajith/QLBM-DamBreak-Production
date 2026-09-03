"""
Phase F31: Test Suite for Multi-Timestep Conservation under Compressed Environment.
"""

import pytest
import numpy as np
from quantum.f31_reduced_architecture import F31ResourceReducedQuantumCircuit


def test_f31_multi_timestep_mass_conservation():
    """Verify zero mass drift over 32 timesteps on 4x4 grid."""
    circ = F31ResourceReducedQuantumCircuit(nx=4, ny=4, frac_bits=12, bit_width=16)

    f_curr = np.random.randint(100, 500, size=(9, 4, 4))
    g_curr = np.random.randint(100, 500, size=(9, 4, 4))
    init_mass = int(np.sum(f_curr))
    init_phase = int(np.sum(g_curr))

    for step in range(32):
        e_comp = np.zeros((14, 4, 4), dtype=int)
        f_curr, g_curr, _, meta = circ.execute_one_timestep(f_curr, g_curr, e_comp)

        assert meta["is_mass_conserved"] == True
        assert np.sum(f_curr) == init_mass
        assert np.sum(g_curr) == init_phase
