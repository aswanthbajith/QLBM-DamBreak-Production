"""
Phase F29: Test Suite for 4x4 Scalable Quantum Circuit Execution and Inversion.
"""

import pytest
import numpy as np
from quantum.f29_scalable_circuit import F29ScalableQuantumCircuit


def test_4x4_circuit_forward_and_inverse():
    """Verify single step and exact adjoint inversion on 4x4 grid."""
    circ = F29ScalableQuantumCircuit(nx=4, ny=4, frac_bits=12, bit_width=16)

    f_in = np.random.randint(100, 500, size=(9, 4, 4))
    g_in = np.random.randint(100, 500, size=(9, 4, 4))
    e_f = np.zeros((9, 4, 4), dtype=int)
    e_g = np.zeros((9, 4, 4), dtype=int)

    f_next, g_next, ef_out, eg_out, meta = circ.execute_one_timestep(f_in, g_in, e_f, e_g)

    assert meta["is_mass_conserved"] == True
    assert meta["mass_drift"] == 0
    assert np.sum(f_next) == np.sum(f_in)

    f_restored, g_restored, meta_inv = circ.execute_inverse_timestep(f_next, g_next, ef_out, eg_out)

    assert meta_inv["is_inversion_exact"] == True
    assert np.array_equal(f_restored, f_in)
    assert np.array_equal(g_restored, g_in)
