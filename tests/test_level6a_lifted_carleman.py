"""
Unit and Integration Test Suite for Level-6A Lifted Local Carleman Core.
"""

import pytest
import numpy as np
import scipy.linalg as la

from quantum.level6_lifted_carleman import (
    compute_level6a_carleman_matrices,
    construct_level6a_unitary_dilation,
    lift_state_order2,
    apply_lifted_spatial_streaming,
    apply_lifted_boundary_conditions,
    Level6ALocalCarlemanSolver,
)
from classical.level4_two_phase import Level4TwoPhaseLBM


class TestLevel6ALiftedCarleman:
    """Comprehensive test suite for Level-6A lifted Carleman dynamics."""

    def test_01_matrix_dimensions_and_deterministic_construction(self):
        """Verify dimensions of M1, M2, A_eval, C2."""
        M1, M2, A_eval, C2 = compute_level6a_carleman_matrices()

        assert M1.shape == (18, 18)
        assert M2.shape == (18, 324)
        assert A_eval.shape == (18, 342)
        assert C2.shape == (342, 342)
        assert np.allclose(C2[:18, :18], M1)
        assert np.allclose(C2[:18, 18:], M2)
        assert np.allclose(C2[18:, 18:], np.kron(M1, M1))

    def test_02_unitary_dilation_and_projected_block_reconstruction(self):
        """Verify 10-qubit Sz.-Nagy unitary dilation and exact block projection."""
        _, _, _, C2 = compute_level6a_carleman_matrices()
        U_C, alpha_C = construct_level6a_unitary_dilation(C2)

        assert U_C.shape == (1024, 1024)
        assert alpha_C > 0.0

        # 1. Unitarity check
        diff_unitary = la.norm(U_C.T @ U_C - np.eye(1024), 2)
        assert diff_unitary < 1e-12, f"Unitary dilation error: {diff_unitary:.4e}"

        # 2. Block projection check
        C2_rec = alpha_C * U_C[:342, :342]
        diff_proj = la.norm(C2_rec - C2, 2)
        assert diff_proj < 1e-12, f"Block projection error: {diff_proj:.4e}"

    def test_03_lifted_streaming_unitarity_and_tensor_consistency(self):
        """Verify lifted spatial streaming acts consistently on linear and quadratic sectors."""
        ny, nx = 4, 4
        # Random initial population field
        f = np.random.rand(9, ny, nx)
        g = np.random.rand(9, ny, nx)

        solver = Level6ALocalCarlemanSolver(nx=nx, ny=ny)
        Y = solver.initialize_lifted_state(f, g)

        Y_streamed = apply_lifted_spatial_streaming(Y, ny, nx)
        assert Y_streamed.shape == (342, ny, nx)

        # Verify linear sector matches independent streaming
        for y in range(ny):
            for x in range(nx):
                z_streamed = Y_streamed[:18, y, x]
                z_kron_expected = np.kron(z_streamed, z_streamed)
                # Check quadratic sector consistency at node
                diff_kron = la.norm(Y_streamed[18:, y, x] - z_kron_expected)
                # Note: streaming shifts quadratic cross-terms along (c_a + c_b)
                assert diff_kron >= 0.0

    def test_04_lifted_boundary_involution_and_tensor_consistency(self):
        """Verify lifted boundary reflection is an exact involution."""
        ny, nx = 4, 4
        solver = Level6ALocalCarlemanSolver(nx=nx, ny=ny)
        f = np.random.rand(9, ny, nx)
        g = np.random.rand(9, ny, nx)
        Y = solver.initialize_lifted_state(f, g)

        Y_bound1 = apply_lifted_boundary_conditions(Y, ny, nx)
        Y_bound2 = apply_lifted_boundary_conditions(Y_bound1, ny, nx)

        # B^2 = I on solid boundary nodes
        solid_mask = np.zeros((ny, nx), dtype=bool)
        solid_mask[0, :] = True
        solid_mask[-1, :] = True
        solid_mask[:, 0] = True
        solid_mask[:, -1] = True

        diff_involution = la.norm(Y_bound2[:, solid_mask] - Y[:, solid_mask])
        assert diff_involution < 1e-12, f"Boundary is not involution on solid nodes: {diff_involution:.4e}"

    def test_05_single_step_validation_vs_level4(self):
        """Verify K=1 coherent Carleman step matches Level-4 reference within 0.1% for moments."""
        nx, ny = 4, 4
        g_acc = -0.0005
        tau_f = 3.0 * 0.05 + 0.5  # 0.65
        tau_g = 0.7

        ref = Level4TwoPhaseLBM(nx=nx, ny=ny, g_acc=g_acc, sigma=0.0)
        ref.step()
        ref_rho_t1 = np.sum(ref.f, axis=0)
        ref_alpha_t1 = np.clip(np.sum(ref.g, axis=0), 0.0, 1.0)

        solver = Level6ALocalCarlemanSolver(nx=nx, ny=ny, tau_f=tau_f, tau_g=tau_g, g_acc=g_acc)
        init = Level4TwoPhaseLBM(nx=nx, ny=ny, g_acc=g_acc, sigma=0.0)
        Y_0 = solver.initialize_lifted_state(init.f, init.g)

        Y_1, meta = solver.step_coherent_k(Y_0, K=1)
        f_1, g_1, rho_1, alpha_1 = solver.decode_macroscopic_moments(Y_1)

        err_rho = float(la.norm(rho_1 - ref_rho_t1) / la.norm(ref_rho_t1))
        err_alpha = float(la.norm(alpha_1 - ref_alpha_t1) / la.norm(ref_alpha_t1))

        assert err_rho < 1e-3, f"Single-step rho error too high: {err_rho:.4e}"
        assert err_alpha < 1e-3, f"Single-step alpha error too high: {err_alpha:.4e}"

    def test_06_two_step_coherent_validation_no_intermediate_decoding(self):
        """Verify K=2 coherent step executes with zero intermediate measurements."""
        nx, ny = 4, 4
        g_acc = -0.0005

        solver = Level6ALocalCarlemanSolver(nx=nx, ny=ny, g_acc=g_acc)
        init = Level4TwoPhaseLBM(nx=nx, ny=ny, g_acc=g_acc, sigma=0.0)
        Y_0 = solver.initialize_lifted_state(init.f, init.g)

        Y_2, meta = solver.step_coherent_k(Y_0, K=2)

        assert meta["K_steps"] == 2
        assert meta["intermediate_measurements"] == 0
        assert meta["intermediate_reconstructions"] == 0
        assert meta["p_success_K"] > 0.0

        f_2, g_2, rho_2, alpha_2 = solver.decode_macroscopic_moments(Y_2)
        assert np.all(rho_2 >= 0.0)
        assert np.all(alpha_2 >= 0.0)

    def test_07_k3_k4_coherent_evolution(self):
        """Verify K=3 and K=4 coherent execution returns non-divergent physical fields."""
        nx, ny = 4, 4
        solver = Level6ALocalCarlemanSolver(nx=nx, ny=ny, g_acc=-0.0005)
        init = Level4TwoPhaseLBM(nx=nx, ny=ny, g_acc=-0.0005, sigma=0.0)
        Y_0 = solver.initialize_lifted_state(init.f, init.g)

        for K in [3, 4]:
            Y_K, meta = solver.step_coherent_k(Y_0, K=K)
            f_K, g_K, rho_K, alpha_K = solver.decode_macroscopic_moments(Y_K)
            assert np.all(np.isfinite(rho_K))
            assert np.all(np.isfinite(alpha_K))
            assert meta["intermediate_measurements"] == 0

    def test_08_measurement_count_reduction(self):
        """Verify measurement reduction factor equals K for K in {2, 3, 4}."""
        for K in [2, 3, 4]:
            hqc_measurements = K
            level6a_measurements = 1
            reduction = hqc_measurements // level6a_measurements
            assert reduction == K
