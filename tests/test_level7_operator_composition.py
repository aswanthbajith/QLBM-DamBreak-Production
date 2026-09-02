"""
Unit tests for Level-7 block-encoding operator composition and dilation leakage.
"""

import pytest
import numpy as np
import scipy.linalg as la

from quantum.level6_lifted_carleman import (
    compute_level6a_carleman_matrices,
    construct_level6a_unitary_dilation,
)


class TestLevel7OperatorComposition:
    """Test suite verifying block-encoding composition mechanics."""

    def test_01_unprojected_dilation_leakage_growth(self):
        """Verify unprojected dilation powers leak severely outside the physical subspace."""
        _, _, _, C2 = compute_level6a_carleman_matrices(tau_f=0.65, tau_g=0.7, rho_0=1.0, g_acc=0.0)
        U_C, alpha_C = construct_level6a_unitary_dilation(C2)

        dim_C2 = 342
        P = np.zeros((dim_C2, 1024), dtype=np.float64)
        P[:dim_C2, :dim_C2] = np.eye(dim_C2)

        # K=2 unprojected
        C2_2 = np.linalg.matrix_power(C2, 2)
        UC_2 = np.linalg.matrix_power(alpha_C * U_C, 2)
        err_unproj_2 = la.norm(P @ UC_2 @ P.T - C2_2, 2)

        assert err_unproj_2 > 10.0, f"Unprojected K=2 leakage must be detected: {err_unproj_2:.4e}"

    def test_02_projective_reset_composition_exactness(self):
        """Verify projected reset chain [P (alpha_C U_C) P^T]^K reproduces C2^K exactly."""
        _, _, _, C2 = compute_level6a_carleman_matrices(tau_f=0.65, tau_g=0.7, rho_0=1.0, g_acc=0.0)
        U_C, alpha_C = construct_level6a_unitary_dilation(C2)

        dim_C2 = 342
        P = np.zeros((dim_C2, 1024), dtype=np.float64)
        P[:dim_C2, :dim_C2] = np.eye(dim_C2)

        P_UC_P = P @ (alpha_C * U_C) @ P.T
        for K in [1, 2, 3, 4]:
            C2_K = np.linalg.matrix_power(C2, K)
            proj_K = np.linalg.matrix_power(P_UC_P, K)
            diff = la.norm(proj_K - C2_K, 2)
            assert diff < 1e-12, f"Projected reset error too high at K={K}: {diff:.4e}"
