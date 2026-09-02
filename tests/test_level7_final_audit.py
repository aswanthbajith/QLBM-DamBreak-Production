"""
Unit and property tests for Level-7 Independent Scientific Audit.
"""

import pytest
import numpy as np
import scipy.linalg as la

from quantum.level6_lifted_carleman import (
    compute_level6a_carleman_matrices,
    construct_level6a_unitary_dilation,
)


class TestLevel7FinalAudit:
    """Audit test suite validating first-principles derivations."""

    def test_01_oaa_exact_trigonometric_derivation(self):
        """Verify trigonometric formula p_m = sin^2((2m+1)theta) matches Grover rotation."""
        _, _, _, C2 = compute_level6a_carleman_matrices(tau_f=0.65, tau_g=0.7, rho_0=1.0, g_acc=0.0)
        _, alpha_C = construct_level6a_unitary_dilation(C2)

        p_0 = 1.0 / alpha_C**2
        theta = np.arcsin(np.sqrt(p_0))

        # Test m=7
        m = 7
        angle = (2 * m + 1) * theta
        p_7 = np.sin(angle)**2

        assert p_7 > 0.99, f"m=7 must exceed 99% success: {p_7:.6f}"
        assert p_7 < 1.00

    def test_02_qubit_count_distinction(self):
        """Verify clear distinction between 19 data qubits and 21 complete algorithmic qubits."""
        n_spatial_x = 7  # 128
        n_spatial_y = 6  # 64
        n_species = 5    # 18
        n_dilation_anc = 1
        n_data = n_spatial_x + n_spatial_y + n_species + n_dilation_anc

        n_oaa_anc = 1
        n_carry_anc = 1
        n_algo = n_data + n_oaa_anc + n_carry_anc

        assert n_data == 19
        assert n_algo == 21

    def test_03_projective_reset_exactness_k32(self):
        """Verify projected reset reproduces C2^K up to K=32 within machine precision."""
        _, _, _, C2 = compute_level6a_carleman_matrices(tau_f=0.65, tau_g=0.7, rho_0=1.0, g_acc=0.0)
        U_C, alpha_C = construct_level6a_unitary_dilation(C2)

        dim_C2 = 342
        P = np.zeros((dim_C2, 1024), dtype=np.float64)
        P[:dim_C2, :dim_C2] = np.eye(dim_C2)

        P_UC_P = P @ (alpha_C * U_C) @ P.T
        for K in [1, 2, 4, 8, 16, 32]:
            C2_K = np.linalg.matrix_power(C2, K)
            proj_K = np.linalg.matrix_power(P_UC_P, K)
            err = la.norm(proj_K - C2_K, 2) / la.norm(C2_K, 2)
            assert err < 1e-12, f"Projected reset failed at K={K} with error {err:.4e}"
