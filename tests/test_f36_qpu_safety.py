"""
Phase F36: Test Suite for QPU Safety Guard & Dry-Run Submission.
"""

import pytest
from quantum.f36_qpu_executor import F36QPUExecutor


def test_safety_guard_blocks_without_optin():
    """Verify live QPU submission is blocked when safety flags/tokens are unset."""
    executor = F36QPUExecutor(nx=2, ny=2, bits_per_node=4)
    res = executor.execute_live_qpu(shots=100)

    assert res["is_executed"] == False
    assert "BLOCKED" in res["status"]


def test_dry_run_generates_valid_artifacts():
    """Verify dry-run mode transpiles and saves artifacts to results/f36/."""
    executor = F36QPUExecutor(nx=2, ny=2, bits_per_node=4)
    meta = executor.execute_dry_run()

    assert meta["mode"] == "DRY_RUN"
    assert meta["logical_qubits"] == 16
    assert meta["transpiled_depth"] > 0
    assert meta["native_2q_gates"] > 0
    assert "DRY_RUN_SUCCESS" in meta["status"]
