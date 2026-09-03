"""
Phase F33: Test Suite for Quantum State Preparation Circuit.
"""

import pytest
from quantum.f33_state_preparation import F33StatePreparation


def test_dam_break_state_prep_gates():
    """Verify state preparation circuit creates valid gates and registers."""
    circ, meta = F33StatePreparation.build_dam_break_initial_state(nx=2, ny=2, bits_per_field=4)

    assert circ.num_qubits == 16
    assert meta["1q_gates"] > 0
    assert meta["depth"] > 0
    assert meta["fidelity"] == 1.0
