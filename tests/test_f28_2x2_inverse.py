"""
Phase F28: Test Suite for 2x2 Reversible Adjoint Inverse Execution (C^-1 C = I).
"""

import pytest
import numpy as np
from quantum.f28_2x2_circuit import F28EndToEnd2x2QuantumCircuit


def test_2x2_circuit_exact_inversion():
    """Verify that execute_inverse_timestep restores initial populations identically."""
    circ = F28EndToEnd2x2QuantumCircuit(frac_bits=12, bit_width=16)

    f_in = np.random.randint(100, 500, size=(9, 2, 2))
    g_in = np.random.randint(100, 500, size=(9, 2, 2))
    e_f = np.zeros((9, 2, 2), dtype=int)
    e_g = np.zeros((9, 2, 2), dtype=int)

    f_next, g_next, ef_out, eg_out, _ = circ.execute_one_timestep(f_in, g_in, e_f, e_g)

    f_restored, g_restored, meta_inv = circ.execute_inverse_timestep(f_next, g_next, ef_out, eg_out)

    assert meta_inv["is_inversion_exact"] == True
    assert np.array_equal(f_restored, f_in)
    assert np.array_equal(g_restored, g_in)
