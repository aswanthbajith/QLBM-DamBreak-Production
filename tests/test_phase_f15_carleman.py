"""
Phase F15: Test Suite for Carleman Linearization & Unitary Dilation.
"""

import pytest
import numpy as np
import scipy.linalg as la

from quantum.f15_carleman_collision import CarlemanTwoPhaseCollision


def test_carleman_matrix_dimensions_and_properties():
    """Verify Carleman matrix dimensions and Sz.-Nagy dilation unitarity."""
    carleman = CarlemanTwoPhaseCollision(nu_L=0.05, nu_G=0.05, tau_phi=0.70)

    assert carleman.A_C.shape == (342, 342)
    assert carleman.U_A.shape == (1024, 1024)

    # Unitarity of 1024x1024 Sz.-Nagy dilation
    err_U = float(la.norm(carleman.U_A.conj().T @ carleman.U_A - np.eye(1024), 2))
    assert err_U < 1e-12, f"Carleman dilation non-unitary: {err_U}"
    assert carleman.p0_success > 0.0


def test_carleman_node_collision_execution():
    """Verify local node collision on lifted state."""
    carleman = CarlemanTwoPhaseCollision(nu_L=0.05, nu_G=0.05, tau_phi=0.70)
    z_in = np.ones(18) * 0.05

    z_post, meta = carleman.evaluate_carleman_collision(z_in)

    assert len(z_post) == 18
    assert meta["unitarity_error"] < 1e-12
    assert meta["manifold_defect"] >= 0.0
