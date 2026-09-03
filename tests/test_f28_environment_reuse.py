"""
Phase F28: Test Suite for Multi-Timestep Environment Refresh and Reuse.
"""

import pytest
import numpy as np
from quantum.f28_2x2_circuit import F28EndToEnd2x2QuantumCircuit


def test_multi_timestep_environment_refresh():
    """Verify that discarding environment to bath enables multi-timestep evolution."""
    circ = F28EndToEnd2x2QuantumCircuit(frac_bits=12, bit_width=16)

    f_curr = np.full((9, 2, 2), 400, dtype=int)
    g_curr = np.full((9, 2, 2), 400, dtype=int)

    for step in range(4):
        # Fresh reservoir bath ancillas |0>_E at every step
        e_f_fresh = np.zeros((9, 2, 2), dtype=int)
        e_g_fresh = np.zeros((9, 2, 2), dtype=int)

        f_next, g_next, ef_out, eg_out, meta = circ.execute_one_timestep(
            f_curr, g_curr, e_f_fresh, e_g_fresh
        )

        assert meta["is_mass_conserved"] == True
        assert meta["is_phase_conserved"] == True

        # System state advances
        f_curr = f_next
        g_curr = g_next
