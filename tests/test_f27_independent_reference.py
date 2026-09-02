"""
Phase F27: Test Suite for Independent Clean-Room Reference Comparison.
"""

import pytest
from quantum.f27_cleanroom_reference import F27CleanRoomReference


def test_cleanroom_1000_trials():
    """Verify 0 LSB discrepancy over 1000 randomized state trials."""
    res = F27CleanRoomReference.run_exhaustive_and_randomized_trials(num_trials=1000, seed=42)

    assert res["num_trials"] == 1000
    assert res["exact_matches"] == 1000
    assert res["max_discrepancy_lsb"] == 0
    assert res["is_zero_discrepancy"] == True
