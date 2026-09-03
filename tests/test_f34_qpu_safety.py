"""
Phase F34: Test Suite for QPU Double Opt-In Safety Gates & Dry-Run Mode.
"""

import pytest
from quantum.f34_qpu_runner import F34QPURunner


def test_qpu_safety_gate_blocks_by_default():
    """Verify live QPU submission is safely blocked without opt-in and credentials."""
    runner = F34QPURunner(nx=2, ny=2, bits_per_node=4)
    res = runner.execute_live_qpu(shots=100)

    assert res["is_executed"] == False
    assert "BLOCKED" in res["status"]


def test_qpu_dry_run_execution():
    """Verify dry-run mode transpiles and archives metadata successfully."""
    runner = F34QPURunner(nx=2, ny=2, bits_per_node=4)
    meta = runner.execute_dry_run()

    assert meta["mode"] == "DRY_RUN"
    assert meta["logical_qubits"] == 16
    assert meta["transpiled_depth"] > 0
    assert meta["native_2q_gates"] > 0
    assert "DRY_RUN_COMPLETED" in meta["status"]
