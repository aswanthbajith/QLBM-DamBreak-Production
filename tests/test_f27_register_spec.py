"""
Phase F27: Test Suite for Register Specification and Memory Allocation.
"""

import pytest
from quantum.f24_resource_audit import F24ResourceForensicAudit


def test_q4_12_register_allocation():
    """Verify exact 624-qubit local node allocation."""
    audit = F24ResourceForensicAudit.audit_qubit_breakdown(nx=1, ny=1, bit_width=16)

    assert audit["system_qubits_per_node"] == 288
    assert audit["environment_qubits_per_node"] == 288
    assert audit["csf_ancillas_per_node"] == 48
    assert audit["total_qubits_per_node"] == 624
