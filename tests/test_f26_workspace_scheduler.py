"""
Phase F26: Test Suite for Reversible Workspace Scheduling.
"""

import pytest
from quantum.f26_workspace_scheduler import F26WorkspaceScheduler


def test_sequential_workspace_bounds():
    """Verify that peak workspace ancillas do not exceed 48 qubits for 16-bit registers."""
    footprint = F26WorkspaceScheduler.calculate_optimized_node_footprint(bit_width=16)

    assert footprint["system_qubits"] == 288
    assert footprint["environment_qubits"] == 288
    assert footprint["peak_workspace_ancillas"] == 48
    assert footprint["total_logical_qubits_node"] == 624
    assert footprint["is_workspace_strictly_bounded"] == True
