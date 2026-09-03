"""
Phase F28: Test Suite for Multi-Step Discrete Mass and Phase Conservation.
"""

import pytest
import numpy as np
from quantum.f28_2x2_circuit import F28EndToEnd2x2QuantumCircuit


def test_2x2_exact_mass_conservation_16_steps():
    """Verify zero mass drift over 16 consecutive timesteps on 2x2 lattice."""
    circ = F28EndToEnd2x2QuantumCircuit(frac_bits=12, bit_width=16)

    f_curr = np.random.randint(100, 500, size=(9, 2, 2))
    g_curr = np.random.randint(100, 500, size=(9, 2, 2))
    initial_mass = int(np.sum(f_curr))
    initial_phase = int(np.sum(g_curr))

    for step in range(16):
        e_f = np.zeros((9, 2, 2), dtype=int)
        e_g = np.zeros((9, 2, 2), dtype=int)

        f_curr, g_curr, _, _, meta = circ.execute_one_timestep(f_curr, g_curr, e_f, e_g)

        assert np.sum(f_curr) == initial_mass
        assert np.sum(g_curr) == initial_phase
        assert meta["mass_drift"] == 0
