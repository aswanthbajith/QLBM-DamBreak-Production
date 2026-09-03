"""
Phase F34: Test Suite for Ideal Quantum vs Reference Cross-Check.
"""

import pytest
from quantum.f33_hardware_demo import F33HardwareDamBreakDemo


def test_ideal_circuit_execution_mode_a():
    """Verify Mode A ideal simulation executes and yields valid physical state."""
    demo = F33HardwareDamBreakDemo(nx=2, ny=2, bits_per_node=4)
    res = demo.execute_mode(mode="ideal", num_timesteps=1, shots=1024)

    assert res["is_executed"] == True
    assert res["mode"] == "MODE_A_IDEAL_SIMULATOR"
    assert res["extracted_fields"]["total_mass"] > 0
