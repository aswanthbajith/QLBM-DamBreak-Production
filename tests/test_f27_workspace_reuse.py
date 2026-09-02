"""
Phase F27: Test Suite for Workspace Lifetime and Uncomputation Scheduling.
"""

import pytest
from quantum.f26_workspace_scheduler import F26WorkspaceScheduler


def test_workspace_peak_48_qubits():
    """Verify that peak scratchpad memory is bounded to 48 qubits for 16-bit registers."""
    schedule = F26WorkspaceScheduler.get_sequential_schedule(bit_width=16)

    assert len(schedule) == 5
    for phase in schedule:
        assert phase["peak_in_phase"] <= 48
