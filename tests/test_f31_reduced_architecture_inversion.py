"""
Phase F31: Test Suite for Adjoint Inversion of Compressed-Environment Architecture.
"""

import pytest
import numpy as np
from classical.d2q9 import C_X, C_Y
from quantum.f31_reduced_architecture import F31ResourceReducedQuantumCircuit


def test_compressed_architecture_exact_inversion():
    """Verify that execute_inverse_timestep restores initial populations identically."""
    circ = F31ResourceReducedQuantumCircuit(nx=4, ny=4, frac_bits=12, bit_width=16)

    # Initial state
    f_in = np.random.randint(100, 500, size=(9, 4, 4))
    g_in = np.random.randint(100, 500, size=(9, 4, 4))
    e_comp = np.zeros((14, 4, 4), dtype=int)

    # Compute conserved moments
    rho = np.sum(f_in, axis=0)
    alpha = np.sum(g_in, axis=0)
    jx = np.sum(f_in * np.array(C_X)[:, None, None], axis=0)
    jy = np.sum(f_in * np.array(C_Y)[:, None, None], axis=0)

    f_next, g_next, e_out, meta = circ.execute_one_timestep(f_in, g_in, e_comp)

    f_restored, g_restored, meta_inv = circ.execute_inverse_timestep(
        f_next, g_next, e_out, rho, alpha, jx, jy
    )

    assert meta_inv["is_inversion_exact"] == True
    assert np.array_equal(f_restored, f_in)
    assert np.array_equal(g_restored, g_in)
