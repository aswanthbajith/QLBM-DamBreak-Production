"""
Phase F23: Test Suite for Positivity Guard and Non-Negative Integer Bounds.
"""

import pytest
from quantum.f23_positivity_guard import F23PositivityGuardedBGK


def test_positivity_guarded_f0():
    """Verify that rest particle f0 and all directional components remain non-negative."""
    # Case 1: Standard positive f0
    f_dir = [100, 100, 100, 100, 50, 50, 50, 50]  # sum = 600
    rho_target = 1000
    f_out = F23PositivityGuardedBGK.enforce_positivity_and_conservation(f_dir, rho_target)
    assert all(x >= 0 for x in f_out)
    assert sum(f_out) == rho_target
    assert f_out[0] == 400

    # Case 2: Extreme velocity exceeding rest density
    f_dir_extreme = [200, 200, 200, 200, 100, 100, 100, 100]  # sum = 1200
    rho_small = 800
    f_out_scaled = F23PositivityGuardedBGK.enforce_positivity_and_conservation(f_dir_extreme, rho_small)
    assert all(x >= 0 for x in f_out_scaled)
    assert sum(f_out_scaled) == rho_small
