"""
Unit tests verifying Sz.-Nagy unitary dilation, unprojected leakage, and projective reset.
"""

import pytest
import numpy as np
import scipy.linalg as la

from quantum.level6_lifted_carleman import (
    compute_level6a_carleman_matrices,
    construct_level6a_unitary_dilation,
)


class TestLevel6ARBlockEncoding:
    """Test suite verifying block-encoding and dilation properties."""

    def test_01_one_step_block_encoding_exactness(self):
        """Verify one-step block encoding reproduces C2 to machine precision."""
        _, _, _, C2 = compute_level6a_carleman_matrices()
        U_C, alpha_C = construct_level6a_unitary_dilation(C2)

        dim_C2 = 342
        P = np.zeros((dim_C2, 1024), dtype=np.float64)
        P[:dim_C2, :dim_C2] = np.eye(dim_C2)

        diff = la.norm(P @ (alpha_C * U_C) @ P.T - C2, 2)
        assert diff < 1e-12, f"One-step block encoding error: {diff:.4e}"

    def test_02_repeated_dilation_subspace_leakage(self):
        """Verify unprojected U_C^2 leaks heavily into dilation complement subspace."""
        _, _, _, C2 = compute_level6a_carleman_matrices()
        U_C, alpha_C = construct_level6a_unitary_dilation(C2)

        dim_C2 = 342
        P = np.zeros((dim_C2, 1024), dtype=np.float64)
        P[:dim_C2, :dim_C2] = np.eye(dim_C2)

        C2_2 = np.linalg.matrix_power(C2, 2)
        UC_2 = np.linalg.matrix_power(alpha_C * U_C, 2)
        diff_unproj = la.norm(P @ UC_2 @ P.T - C2_2, 2)

        # Unprojected error must be large (> 1.0)
        assert diff_unproj > 5.0, f"Unprojected leakage must be detected: {diff_unproj:.4e}"

    def test_03_projective_reset_preserves_powers(self):
        """Verify intermediate projective reset [P U_C P]^K reproduces C2^K exactly."""
        _, _, _, C2 = compute_level6a_carleman_matrices()
        U_C, alpha_C = construct_level6a_unitary_dilation(C2)

        dim_C2 = 342
        P = np.zeros((dim_C2, 1024), dtype=np.float64)
        P[:dim_C2, :dim_C2] = np.eye(dim_C2)

        for K in [1, 2, 3, 4]:
            C2_K = np.linalg.matrix_power(C2, K)
            P_UC_P = P @ (alpha_C * U_C) @ P.T
            proj_K = np.linalg.matrix_power(P_UC_P, K)

            diff_proj = la.norm(proj_K - C2_K, 2)
            assert diff_proj < 1e-12, f"Projected power error too high for K={K}: {diff_proj:.4e}"
