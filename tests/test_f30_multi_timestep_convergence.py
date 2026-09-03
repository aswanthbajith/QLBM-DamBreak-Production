"""
Phase F30: Test Suite for Multi-Timestep Convergence and Stability.
"""

import pytest
import numpy as np
from quantum.f29_scalable_circuit import F29ScalableQuantumCircuit


def test_multi_timestep_stability_32_steps():
    """Verify stability and exact zero drift over 32 timesteps on 4x4 grid."""
    circ = F29ScalableQuantumCircuit(nx=4, ny=4, frac_bits=12, bit_width=16)

    f_curr = np.full((9, 4, 4), 400, dtype=int)
    g_curr = np.full((9, 4, 4), 400, dtype=int)
    init_mass = int(np.sum(f_curr))

    for step in range(32):
        e_f = np.zeros((9, 4, 4), dtype=int)
        e_g = np.zeros((9, 4, 4), dtype=int)

        f_curr, g_curr, _, _, meta = circ.execute_one_timestep(f_curr, g_curr, e_f, e_g)

        assert meta["is_mass_conserved"] == True
        assert np.sum(f_curr) == init_mass
