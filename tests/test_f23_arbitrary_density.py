"""
Phase F23: Test Suite for Arbitrary Complex Density Matrix Properties.
"""

import pytest
from quantum.f23_arbitrary_density_matrix import F23ArbitraryDensityMatrixTest


def test_random_density_matrices_cptp():
    """Verify Hermiticity, unit trace, and positive semidefiniteness on random dense density matrices."""
    dim = 4
    mapping = {0: 1, 1: 2, 2: 2, 3: 0}

    for seed in [1, 42, 100, 777]:
        res = F23ArbitraryDensityMatrixTest.test_cptp_on_random_density_matrix(dim, mapping, seed=seed)
        assert res["is_valid_density_matrix"] == True
        assert res["is_hermitian"] == True
        assert res["is_unit_trace"] == True
        assert res["is_positive_semidefinite"] == True
