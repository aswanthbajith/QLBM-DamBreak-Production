"""
Phase F33: Test Suite for Ideal Quantum Simulator Dam-Break Circuit.
"""

import pytest
from quantum.f33_hardware_demo import F33HardwareDamBreakDemo


def test_ideal_dam_break_execution():
    """Verify Mode A ideal simulation executes without error."""
    demo = F33HardwareDamBreakDemo(nx=2, ny=2, bits_per_node=4)
    res = demo.execute_mode(mode="ideal", num_timesteps=1, shots=500)

    assert res["is_executed"] == True
    assert res["mode"] == "MODE_A_IDEAL_SIMULATOR"
    assert "rho" in res["extracted_fields"]
    assert res["extracted_fields"]["total_shots"] == 500
