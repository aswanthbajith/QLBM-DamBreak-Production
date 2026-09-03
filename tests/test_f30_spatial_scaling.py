"""
Phase F30: Test Suite for Spatial Qubit Scaling (2x2 to 16x16).
"""

import pytest
from quantum.f30_scaling_engine import F30ScalingEngine


def test_spatial_qubit_allocations():
    """Verify exact logical qubit allocations across grid dimensions."""
    q_2x2 = F30ScalingEngine.calculate_lattice_qubits(2, 2, bit_width=16)
    assert q_2x2["total_logical_qubits"] == 2352
    assert q_2x2["workspace_qubits"] == 48

    q_4x4 = F30ScalingEngine.calculate_lattice_qubits(4, 4, bit_width=16)
    assert q_4x4["total_logical_qubits"] == 9264

    q_8x8 = F30ScalingEngine.calculate_lattice_qubits(8, 8, bit_width=16)
    assert q_8x8["total_logical_qubits"] == 36912

    q_16x16 = F30ScalingEngine.calculate_lattice_qubits(16, 16, bit_width=16)
    assert q_16x16["total_logical_qubits"] == 147504
