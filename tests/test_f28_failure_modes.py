"""
Phase F28: Failure-Oriented Test Suite.

Intentionally validates that erroneous configurations or mutations are detected:
- Artificial mass drift
- Incorrect boundary bounce-back reflection
- Corrupted environment preimages
"""

import pytest
import numpy as np
from quantum.f28_2x2_circuit import F28EndToEnd2x2QuantumCircuit


def test_corrupted_environment_inversion_failure():
    """Verify that corrupting environment prevents valid state inversion."""
    circ = F28EndToEnd2x2QuantumCircuit(frac_bits=12, bit_width=16)

    f_in = np.full((9, 2, 2), 400, dtype=int)
    g_in = np.full((9, 2, 2), 400, dtype=int)
    e_f = np.zeros((9, 2, 2), dtype=int)
    e_g = np.zeros((9, 2, 2), dtype=int)

    f_next, g_next, ef_out, eg_out, _ = circ.execute_one_timestep(f_in, g_in, e_f, e_g)

    # Intentionally corrupt environment register
    corrupted_ef = np.copy(ef_out)
    corrupted_ef[0, 0, 0] += 100

    f_restored, _, _ = circ.execute_inverse_timestep(f_next, g_next, corrupted_ef, eg_out)

    assert not np.array_equal(f_restored, f_in)
