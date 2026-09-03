"""
Phase F29: Test Suite for Clean-Room 4x4 Equivalence (1,000 Trials).
"""

import pytest
from quantum.f29_three_layer_validator import F29ThreeLayerValidator


def test_4x4_cleanroom_1000_trials():
    """Verify 0 LSB discrepancy over 1,000 randomized 4x4 trials."""
    res = F29ThreeLayerValidator.run_layer_a_validation(nx=4, ny=4, num_trials=1000, seed=42)

    assert res["num_trials"] == 1000
    assert res["exact_matches"] == 1000
    assert res["max_discrepancy_lsb"] == 0
    assert res["is_layer_a_exact"] == True
