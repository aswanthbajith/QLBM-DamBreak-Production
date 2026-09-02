"""
Phase F20: Unit Test Suite for Entanglement Preservation and Positivity.
"""

import pytest
import numpy as np

from quantum.f20_channel import F20QuantumChannel
from quantum.f20_entanglement import F20EntanglementAudit


def test_entanglement_positivity():
    """Verify (E (x) I)(rho_SR) produces a valid positive density matrix."""
    dim = 4
    mapping = {0: 1, 1: 1, 2: 2, 3: 0}
    channel = F20QuantumChannel(dim, mapping)
    ent_audit = F20EntanglementAudit(channel)

    res = ent_audit.test_entangled_pair(x1=0, x2=1)
    assert res["is_valid_density_matrix"] == True
    assert res["min_eigenvalue_joint"] >= -1e-12
    assert abs(res["trace_joint"] - 1.0) < 1e-12
