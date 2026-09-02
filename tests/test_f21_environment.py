"""
Phase F21: Test Suite for CSF Environmental Memory Footprint.
"""

import pytest
from quantum.f21_environment import F21CSFEnvironmentAudit


def test_csf_qubit_accounting():
    """Verify exact qubit counts for CSF computation."""
    res = F21CSFEnvironmentAudit.calculate_csf_qubits(nx=4, ny=4)

    assert res["num_nodes"] == 16
    assert res["total_active_qubits"] == 16 * 48
    assert res["is_uncomputed"] == True
