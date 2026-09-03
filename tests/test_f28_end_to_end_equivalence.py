"""
Phase F28: Test Suite for End-to-End Equivalence (Circuit vs Independent Clean-Room Reference).
"""

import pytest
import numpy as np
from quantum.f28_2x2_circuit import F28EndToEnd2x2QuantumCircuit
from quantum.f28_cleanroom_2x2_reference import F28CleanRoom2x2Reference


def test_1000_trials_2x2_end_to_end_equivalence():
    """Verify 0 LSB discrepancy over 1,000 randomized 2x2 state trials."""
    rng = np.random.default_rng(42)
    circ = F28EndToEnd2x2QuantumCircuit(frac_bits=12, bit_width=16)
    ref = F28CleanRoom2x2Reference(frac_bits=12)

    matches = 0
    max_disc = 0

    for _ in range(1000):
        f_in = rng.integers(50, 450, size=(9, 2, 2))
        g_in = rng.integers(50, 450, size=(9, 2, 2))
        e_f = np.zeros((9, 2, 2), dtype=int)
        e_g = np.zeros((9, 2, 2), dtype=int)

        f_circ, g_circ, _, _, _ = circ.execute_one_timestep(f_in, g_in, e_f, e_g)
        f_ref, g_ref = ref.step(f_in, g_in)

        diff_f = int(np.max(np.abs(f_circ - f_ref)))
        diff_g = int(np.max(np.abs(g_circ - g_ref)))
        disc = max(diff_f, diff_g)

        if disc > max_disc:
            max_disc = disc

        if disc == 0:
            matches += 1

    assert matches == 1000
    assert max_disc == 0
