"""
Phase F25: Test Suite for Gate-Level Synthesis and Resource Estimation.
"""

import pytest
from quantum.f25_gate_resource_model import F25GateResourceModel


def test_node_resource_calculation():
    """Verify gate resource counts for 16-bit Q4.12 node."""
    res = F25GateResourceModel.calculate_node_gate_resources(bit_width=16)

    assert res["bit_width"] == 16
    assert res["logical_qubits_node"] == 624
    assert res["toffoli_count_node"] > 10000
    assert res["t_gate_count_node"] == res["toffoli_count_node"] * 4
    assert res["clifford_gate_count_node"] == res["toffoli_count_node"] * 8


def test_lattice_resource_calculation():
    """Verify whole-lattice scaling across 4x4 domain."""
    lat = F25GateResourceModel.calculate_lattice_resources(nx=4, ny=4, bit_width=16, timesteps=32)

    assert lat["num_nodes"] == 16
    assert lat["total_logical_qubits"] == 624 * 16
    assert lat["total_toffolis_simulation"] > 5000000
