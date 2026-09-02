"""
Phase F15: Test Suite for Tensor Manifold Consistency & Truncation Bounds.
"""

import pytest
import numpy as np

from quantum.f15_carleman_collision import CarlemanTwoPhaseCollision


def test_tensor_manifold_consistency_bounds():
    """Verify tensor manifold defect E_tensor = ||Y_2 - z (x) z|| / ||z (x) z|| remains bounded."""
    carleman = CarlemanTwoPhaseCollision(nu_L=0.05, nu_G=0.05, tau_phi=0.70)

    # Low-Mach state
    z_low_mach = np.ones(18) * 0.05
    z_post, meta = carleman.evaluate_carleman_collision(z_low_mach)

    # In low-Mach regime, manifold defect is bounded
    assert meta["manifold_defect"] < 1.0, f"Manifold defect too large: {meta['manifold_defect']}"
