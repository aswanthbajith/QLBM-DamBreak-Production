"""
Phase F13: Test Suite for Coherent Collision & Sz.-Nagy Unitary Dilation.
"""

import pytest
import numpy as np
import scipy.linalg as la

from quantum.coherent_collision import CoherentCollisionOracle


def test_coherent_collision_oracle():
    """Verify local node collision dilation unitarity and output."""
    oracle = CoherentCollisionOracle(nu_L=0.05, nu_G=0.05, tau_phi=0.70)
    z_in = np.ones(18) * 0.1
    u_vec = np.array([0.02, -0.01])
    F_vec = np.array([0.0001, -0.0005])

    z_post, meta = oracle.execute_coherent_node_collision(
        z_node=z_in,
        rho=0.9,
        alpha=0.6,
        u_vec=u_vec,
        F_vec=F_vec,
    )

    assert len(z_post) == 18
    assert meta["unitarity_error"] < 1e-12
    assert meta["p0_success"] > 0.20
