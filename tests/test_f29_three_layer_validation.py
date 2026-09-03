"""
Phase F29: Test Suite for Three-Layer Physical Validation (Layer A, B, C).
"""

import pytest
from quantum.f29_three_layer_validator import F29ThreeLayerValidator


def test_three_layer_validation_pipeline():
    """Verify Layer A, Layer B, and Layer C validation pipelines."""
    # Layer A
    res_a = F29ThreeLayerValidator.run_layer_a_validation(nx=4, ny=4, num_trials=50, seed=42)
    assert res_a["is_layer_a_exact"] == True

    # Layer B
    res_b = F29ThreeLayerValidator.run_layer_b_validation(nx=4, ny=4, timesteps=[1, 2, 4])
    assert len(res_b) == 3
    for row in res_b:
        assert row["mass_drift"] == 0.0

    # Layer C
    res_c = F29ThreeLayerValidator.run_layer_c_validation()
    assert res_c["is_physically_validated"] == True
    assert res_c["dimensionless_surge_front_error"] < 0.05
