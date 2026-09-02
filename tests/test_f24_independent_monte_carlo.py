"""
Phase F24: Test Suite for Independent Clean-Room 1000-State Monte Carlo Validation.
"""

import pytest
from quantum.f24_independent_reference import F24IndependentIntegerReference


def test_independent_1000_state_monte_carlo():
    """Verify 100% agreement against clean-room independent reference implementation."""
    res = F24IndependentIntegerReference.run_1000_state_monte_carlo(seed=42)

    assert res["num_trials"] == 1000
    assert res["exact_matches"] == 1000
    assert res["match_rate_percent"] == 100.0
    assert res["max_discrepancy"] == 0
    assert res["is_100_percent_consistent"] == True
