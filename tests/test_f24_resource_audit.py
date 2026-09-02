"""
Phase F24: Test Suite for Resource Audit and 624-Qubit Exact Derivation.
"""

import pytest
from quantum.f24_resource_audit import F24ResourceForensicAudit


def test_exact_624_qubit_derivation():
    """Verify exact 624 logical qubits per node breakdown."""
    audit = F24ResourceForensicAudit.audit_qubit_breakdown(nx=4, ny=4, bit_width=16)

    assert audit["system_qubits_per_node"] == 288
    assert audit["environment_qubits_per_node"] == 288
    assert audit["csf_ancillas_per_node"] == 48
    assert audit["total_qubits_per_node"] == 624
    assert audit["is_624_exact"] == True
    assert audit["total_lattice_qubits"] == 624 * 16
