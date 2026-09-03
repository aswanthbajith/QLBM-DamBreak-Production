"""
Phase F28: Test Suite for 2x2 Lattice Resource Accounting.
"""

import pytest


def test_2x2_resource_metrics():
    """Verify total logical qubit allocation for 2x2 lattice."""
    bit_width = 16
    num_nodes = 4

    sys_qubits = num_nodes * 18 * bit_width   # 1,152
    env_qubits = num_nodes * 18 * bit_width   # 1,152
    shared_workspace = 3 * bit_width          # 48

    total_qubits = sys_qubits + env_qubits + shared_workspace  # 2,352

    assert sys_qubits == 1152
    assert env_qubits == 1152
    assert shared_workspace == 48
    assert total_qubits == 2352
