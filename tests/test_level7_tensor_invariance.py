"""
Unit tests for Level-7 tensor invariance and manifold preservation under spatial advection.
"""

import pytest
import numpy as np
import scipy.linalg as la

from classical.streaming import stream
from classical.level4_two_phase import Level4TwoPhaseLBM
from quantum.level6_lifted_carleman import (
    lift_state_order2,
    apply_lifted_spatial_streaming,
)


class TestLevel7TensorInvariance:
    """Test suite verifying tensor invariance under coherent spatial advection."""

    def test_01_naive_lifted_streaming_fails_manifold(self):
        """Verify naive S(x)S shifts quadratic cross-terms erroneously on non-uniform state."""
        nx, ny = 4, 4
        s_init = Level4TwoPhaseLBM(nx=nx, ny=ny)
        f, g = s_init.f, s_init.g

        Y_spatial = np.zeros((342, ny, nx), dtype=np.float64)
        for y in range(ny):
            for x in range(nx):
                z_node = np.concatenate((f[:, y, x], g[:, y, x]))
                Y_spatial[:, y, x] = lift_state_order2(z_node)

        Y_str_naive = apply_lifted_spatial_streaming(Y_spatial, ny, nx)

        inconsistencies = []
        for y in range(ny):
            for x in range(nx):
                z_str = Y_str_naive[:18, y, x]
                quad_actual = Y_str_naive[18:, y, x]
                quad_expected = np.kron(z_str, z_str)
                diff = la.norm(quad_actual - quad_expected) / (la.norm(quad_expected) + 1e-15)
                inconsistencies.append(diff)

        assert np.mean(inconsistencies) > 0.5, "Naive S(x)S must fail invariant manifold condition"

    def test_02_linear_streaming_recomp_exact_manifold(self):
        """Verify linear permutation streaming + local re-formation preserves manifold exactly."""
        nx, ny = 4, 4
        s_init = Level4TwoPhaseLBM(nx=nx, ny=ny)
        f_str = stream(s_init.f)
        g_str = stream(s_init.g)

        inconsistencies = []
        for y in range(ny):
            for x in range(nx):
                z_str = np.concatenate((f_str[:, y, x], g_str[:, y, x]))
                Y_node = lift_state_order2(z_str)
                quad_actual = Y_node[18:]
                quad_expected = np.kron(z_str, z_str)
                diff = la.norm(quad_actual - quad_expected)
                inconsistencies.append(diff)

        assert np.max(inconsistencies) < 1e-12, "Recomputed quadratic tensor must match to machine precision"
