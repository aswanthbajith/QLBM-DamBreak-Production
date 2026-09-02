"""
Phase F27: Test Suite for Gate-Level Resource Validation vs Analytical Estimates.
"""

import pytest
from quantum.f25_gate_resource_model import F25GateResourceModel


def test_resource_estimates_consistency():
    """Verify Toffoli and T-gate scaling consistency."""
    node_res = F25GateResourceModel.calculate_node_gate_resources(bit_width=16)

    assert node_res["logical_qubits_node"] == 624
    assert node_res["toffoli_count_node"] == 21168
    assert node_res["t_gate_count_node"] == 21168 * 4
