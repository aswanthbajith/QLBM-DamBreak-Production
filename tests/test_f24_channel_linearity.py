"""
Phase F24: Test Suite for Quantum Channel Linearity and Complete Positivity.
"""

import pytest
import numpy as np
import scipy.linalg as la

from quantum.f22_stinespring import F22StinespringDilationProof
from quantum.f23_arbitrary_density_matrix import F23ArbitraryDensityMatrixTest


def test_channel_linearity_on_convex_combinations():
    """Verify E(a * rho_1 + (1 - a) * rho_2) == a * E(rho_1) + (1 - a) * E(rho_2)."""
    dim = 4
    mapping = {0: 1, 1: 2, 2: 2, 3: 0}
    proof = F22StinespringDilationProof(dim, mapping)

    rho1 = F23ArbitraryDensityMatrixTest.generate_random_density_matrix(dim, seed=10)
    rho2 = F23ArbitraryDensityMatrixTest.generate_random_density_matrix(dim, seed=20)

    a = 0.65
    rho_combo = a * rho1 + (1.0 - a) * rho2

    e_combo = proof.apply_channel_to_density_matrix(rho_combo)
    e1 = proof.apply_channel_to_density_matrix(rho1)
    e2 = proof.apply_channel_to_density_matrix(rho2)

    linear_sum = a * e1 + (1.0 - a) * e2
    diff = float(la.norm(e_combo - linear_sum))

    assert diff < 1e-14
