"""
Phase F34: Test Suite for Multi-Layer Cross-Validation Matrix.
"""

import pytest
from quantum.f34_hardware_validation import F34HardwareValidator


def test_f34_validation_matrix():
    """Verify multi-layer validation matrix executes across ideal, noisy, and qpu dry-run."""
    report = F34HardwareValidator.run_full_validation_matrix(shots=500)

    assert "ideal" in report
    assert "noisy" in report
    assert "real_qpu" in report
    assert "dry_run" in report
    assert report["errors"]["is_distinguishable_from_noise"] == True
