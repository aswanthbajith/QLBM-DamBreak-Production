"""
Phase F29: Test Suite for Multi-Timestep Evolution (T=1..32).
"""

import pytest
import numpy as np
from quantum.f29_scalable_circuit import F29ScalableQuantumCircuit


def test_4x4_multi_timestep_conservation():
    """Verify exact discrete mass conservation across T=1..32 on 4x4 grid."""
    circ = F29ScalableQuantumCircuit(nx=4, ny=4, frac_bits=12, bit_width=16)

    f_curr = np.random.randint(100, 500, size=(9, 4, 4))
    g_curr = np.random.randint(100, 500, size=(9, 4, 4))
    init_mass = int(np.sum(f_curr))
    init_phase = int(np.sum(g_curr))

    for step in range(32):
        e_f = np.zeros((9, 4, 4), dtype=int)
        e_g = np.zeros((9, 4, 4), dtype=int)

        f_curr, g_curr, _, _, meta = circ.execute_one_timestep(f_curr, g_curr, e_f, e_g)

        assert meta["is_mass_conserved"] == True
        assert np.sum(f_curr) == init_mass
        assert np.sum(g_curr) == init_phase
