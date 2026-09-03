"""
Phase F28: Test Suite for 2x2 End-to-End Reversible Quantum Circuit Execution.
"""

import pytest
import numpy as np
from quantum.f28_2x2_circuit import F28EndToEnd2x2QuantumCircuit


def test_2x2_circuit_single_step():
    """Verify single timestep execution on a 2x2 lattice."""
    circ = F28EndToEnd2x2QuantumCircuit(frac_bits=12, bit_width=16)

    # Initial state: 4 nodes with uniform populations
    f_in = np.full((9, 2, 2), 450, dtype=int)
    g_in = np.full((9, 2, 2), 450, dtype=int)
    e_f = np.zeros((9, 2, 2), dtype=int)
    e_g = np.zeros((9, 2, 2), dtype=int)

    f_next, g_next, ef_out, eg_out, meta = circ.execute_one_timestep(f_in, g_in, e_f, e_g)

    assert meta["is_mass_conserved"] == True
    assert meta["is_phase_conserved"] == True
    assert meta["mass_drift"] == 0
    assert np.sum(f_next) == np.sum(f_in)
