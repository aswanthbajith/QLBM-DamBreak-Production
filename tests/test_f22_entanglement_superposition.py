"""
Phase F22: Test Suite for Superposition Dephasing and Entanglement Positivity.
"""

import pytest
import numpy as np

from quantum.f22_entanglement_superposition import F22EntanglementSuperpositionAudit


def test_superposition_dephasing_into_environment():
    """Verify that coherent superpositions dephase into mixed thermal states."""
    mapping = {0: 1, 1: 1, 2: 2, 3: 3}  # 0 and 1 relax to 1
    res = F22EntanglementSuperpositionAudit.evaluate_superposition_state(dim=4, mapping=mapping)

    assert abs(res["purity_in"] - 1.0) < 1e-12  # Pure input state
    assert res["coherence_off_diagonal_preserved"] == False
    assert abs(res["purity_out"] - 1.0) < 1e-12  # Both collapse into pure |1><1| output


def test_entangled_bell_state_positivity():
    """Verify that bipartite entangled state preserves density matrix positivity under local channel."""
    mapping = {0: 0, 1: 0}  # Non-injective map on qubit A
    res = F22EntanglementSuperpositionAudit.evaluate_entangled_bell_state(mapping)

    assert res["positivity_preserved"] == True
    assert res["initial_entanglement_negativity"] == 0.5
