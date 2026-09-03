"""
Phase F33: Test Suite for Multi-Layer Cross-Validation.
"""

import pytest
from quantum.f33_validation import F33HardwareValidator


def test_full_hardware_validation_pipeline():
    """Verify full hardware validation suite executes across ideal, noisy, and qpu checks."""
    report = F33HardwareValidator.run_full_validation_suite(shots=500)

    assert "ideal_result" in report
    assert "noisy_result" in report
    assert "real_qpu_result" in report
    assert report["noise_degradation"]["is_signal_distinguishable"] == True
