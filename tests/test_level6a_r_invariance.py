"""
Unit tests verifying Carleman invariant manifold properties and streaming non-invariance.
"""

import pytest
import numpy as np
import scipy.linalg as la

from classical.d2q9 import C_X, C_Y
from quantum.level6_lifted_carleman import lift_state_order2, apply_lifted_spatial_streaming


class TestLevel6ARInvariance:
    """Test suite verifying Carleman manifold invariance and non-invariance."""

    def test_01_uniform_state_exact_invariance(self):
        """Verify uniform (spatially constant) state preserves manifold under S_lifted."""
        ny, nx = 4, 4
        f = np.full((9, ny, nx), 1.0 / 9.0)
        g = np.full((9, ny, nx), 1.0 / 9.0)

        Y0 = np.zeros((342, ny, nx), dtype=np.float64)
        for y in range(ny):
            for x in range(nx):
                z_node = np.concatenate((f[:, y, x], g[:, y, x]))
                Y0[:, y, x] = lift_state_order2(z_node)

        Y_str = apply_lifted_spatial_streaming(Y0, ny, nx)

        # Check invariance at every node
        for y in range(ny):
            for x in range(nx):
                z_node = Y_str[:18, y, x]
                quad_actual = Y_str[18:, y, x]
                quad_expected = np.kron(z_node, z_node)
                diff = la.norm(quad_actual - quad_expected)
                assert diff < 1e-12, f"Uniform state must be invariant: {diff:.4e}"

    def test_02_gradient_state_non_invariance_detection(self):
        """Verify state with spatial gradients breaks invariant manifold under S_lifted."""
        ny, nx = 4, 4
        f = np.random.rand(9, ny, nx)
        g = np.random.rand(9, ny, nx)

        Y0 = np.zeros((342, ny, nx), dtype=np.float64)
        for y in range(ny):
            for x in range(nx):
                z_node = np.concatenate((f[:, y, x], g[:, y, x]))
                Y0[:, y, x] = lift_state_order2(z_node)

        Y_str = apply_lifted_spatial_streaming(Y0, ny, nx)

        inconsistencies = []
        for y in range(ny):
            for x in range(nx):
                z_node = Y_str[:18, y, x]
                quad_actual = Y_str[18:, y, x]
                quad_expected = np.kron(z_node, z_node)
                diff = la.norm(quad_actual - quad_expected) / (la.norm(quad_expected) + 1e-15)
                inconsistencies.append(diff)

        mean_err = np.mean(inconsistencies)
        assert mean_err > 0.5, f"Gradient state must fail manifold invariance: {mean_err:.4e}"
