"""
Phase F31: Test Suite for Clean-Room 4x4 Equivalence (1,000 Trials).
"""

import pytest
import numpy as np
from quantum.f31_reduced_architecture import F31ResourceReducedQuantumCircuit
from quantum.f31_cleanroom_reference import F31CleanRoomReference


def test_cleanroom_1000_trials_f31():
    """Verify 0 LSB discrepancy over 1,000 randomized state trials."""
    rng = np.random.default_rng(42)
    circ = F31ResourceReducedQuantumCircuit(nx=4, ny=4, frac_bits=12, bit_width=16)
    ref = F31CleanRoomReference(nx=4, ny=4, frac_bits=12)

    matches = 0
    max_disc = 0

    for _ in range(1000):
        f_in = rng.integers(50, 450, size=(9, 4, 4))
        g_in = rng.integers(50, 450, size=(9, 4, 4))
        e_comp = np.zeros((14, 4, 4), dtype=int)

        f_circ, g_circ, _, _ = circ.execute_one_timestep(f_in, g_in, e_comp)
        f_ref, g_ref = ref.step(f_in, g_in)

        diff = max(int(np.max(np.abs(f_circ - f_ref))), int(np.max(np.abs(g_circ - g_ref))))
        if diff > max_disc:
            max_disc = diff
        if diff == 0:
            matches += 1

    assert matches == 1000
    assert max_disc == 0
