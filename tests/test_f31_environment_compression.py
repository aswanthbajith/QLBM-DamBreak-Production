"""
Phase F31: Test Suite for Compressed Environment Representation (14 fields/node).
"""

import pytest
import numpy as np
from quantum.f31_reduced_architecture import F31ResourceReducedQuantumCircuit


def test_environment_compression_field_count():
    """Verify compressed environment utilizes exactly 14 fields per node (224 qubits)."""
    circ = F31ResourceReducedQuantumCircuit(nx=4, ny=4, frac_bits=12, bit_width=16)

    f_in = np.full((9, 4, 4), 400, dtype=int)
    g_in = np.full((9, 4, 4), 400, dtype=int)
    e_comp = np.zeros((14, 4, 4), dtype=int)

    f_next, g_next, e_out, meta = circ.execute_one_timestep(f_in, g_in, e_comp)

    assert e_out.shape == (14, 4, 4)
    assert meta["environment_compressed_fields"] == 14
    assert meta["is_mass_conserved"] == True
