"""
Phase F33: Test Suite for Noisy Quantum Simulator Execution (Mode B).
"""

import pytest
from quantum.f33_hardware_demo import F33HardwareDamBreakDemo


def test_noisy_dam_break_execution():
    """Verify Mode B noisy simulation produces realistic non-trivial counts."""
    demo = F33HardwareDamBreakDemo(nx=2, ny=2, bits_per_node=4)
    res = demo.execute_mode(mode="noisy", num_timesteps=1, shots=500)

    assert res["is_executed"] == True
    assert res["mode"] == "MODE_B_NOISY_SIMULATOR"
    assert len(res["counts"]) > 0
