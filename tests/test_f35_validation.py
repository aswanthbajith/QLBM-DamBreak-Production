"""
Phase F35: Test Suite for Multi-Layer Cross-Validation Matrix.
"""

import pytest
from quantum.f35_multi_layer_validator import F35MultiLayerValidator


def test_validation_matrix_runs():
    """Verify validation matrix runs and verifies signal-to-noise distinguishability."""
    report = F35MultiLayerValidator.run_full_validation_matrix(shots=500)

    assert "ideal" in report
    assert "noisy" in report
    assert "real_qpu" in report
    assert "dry_run" in report
    assert report["errors"]["is_distinguishable_from_noise"] == True
