"""
Automated Diagnostic Test Suite for Level-6A-S Scientific Stability and Failure Analysis.
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
from classical.d2q9 import C_X, C_Y, W


class TestLevel6AStabilityAnalysis:
    """Scientific test suite validating the diagnostic failure analysis findings."""

    def test_01_single_site_carleman_accuracy(self):
        """Verify local single-site Carleman collision error is < 0.2% across 4 steps."""
        _, _, _, C2 = compute_level6a_carleman_matrices(tau_f=0.65, tau_g=0.7, g_acc=-0.0005)
        # Liquid node state
        z_exact = np.concatenate((np.full(9, 1.0 / 9.0), np.full(9, 1.0 / 9.0)))
        Y_carleman = lift_state_order2(z_exact)

        for step in range(1, 5):
            f_in = z_exact[:9]
            g_in = z_exact[9:18]
            rho_in = np.sum(f_in)
            alpha_in = np.clip(np.sum(g_in), 0.0, 1.0)
            u_x_in = np.sum(C_X * f_in) / rho_in
            u_y_in = (np.sum(C_Y * f_in) + 0.5 * (rho_in - 0.1) * (-0.0005)) / rho_in

            f_eq = np.zeros(9)
            g_eq = np.zeros(9)
            for i in range(9):
                cu = 3.0 * (C_X[i] * u_x_in + C_Y[i] * u_y_in)
                u2 = 1.5 * (u_x_in**2 + u_y_in**2)
                f_eq[i] = W[i] * rho_in * (1.0 + cu + 0.5 * cu**2 - u2)
                g_eq[i] = W[i] * alpha_in * (1.0 + cu + 0.5 * cu**2 - u2)

            f_next_exact = f_in - (1.0 / 0.65) * (f_in - f_eq) + (1.0 - 0.5 / 0.65) * W * 3.0 * C_Y * (rho_in - 0.1) * (-0.0005)
            g_next_exact = g_in - (1.0 / 0.7) * (g_in - g_eq)
            z_exact = np.concatenate((f_next_exact, g_next_exact))

            Y_carleman = C2 @ Y_carleman
            z_carleman = Y_carleman[:18]

            err_local = float(la.norm(z_carleman - z_exact) / la.norm(z_exact))
            assert err_local < 0.002, f"Single-site error exceeded 0.2% at step {step}: {err_local:.4e}"

    def test_02_unitary_dilation_subspace_leakage(self):
        """Verify unprojected dilation power U_C^2 leaks into complement subspace."""
        _, _, _, C2 = compute_level6a_carleman_matrices(tau_f=0.65, tau_g=0.7, g_acc=-0.0005)
        U_C, alpha_C = construct_level6a_unitary_dilation(C2)

        dim_C2 = 342
        P = np.zeros((dim_C2, 1024), dtype=np.float64)
        P[:dim_C2, :dim_C2] = np.eye(dim_C2)

        # K=1: exact
        diff_1 = la.norm(P @ (alpha_C * U_C) @ P.T - C2, 2)
        assert diff_1 < 1e-12, f"K=1 block encoding must be exact: {diff_1:.4e}"

        # K=2: subspace leakage detected
        C2_2 = np.linalg.matrix_power(C2, 2)
        UC_2 = np.linalg.matrix_power(alpha_C * U_C, 2)
        diff_2 = la.norm(P @ UC_2 @ P.T - C2_2, 2)
        assert diff_2 > 10.0, f"K=2 dilation leakage must be detected: {diff_2:.4e}"

    def test_03_tensor_inconsistency_after_spatial_streaming(self):
        """Verify spatial streaming causes tensor sector de-correlation (E_tensor > 1.0)."""
        nx, ny = 4, 4
        solver = Level6ALocalCarlemanSolver(nx=nx, ny=ny, tau_f=0.65, tau_g=0.7, g_acc=-0.0005)
        init = Level4TwoPhaseLBM(nx=nx, ny=ny, g_acc=-0.0005, sigma=0.0)
        Y_0 = solver.initialize_lifted_state(init.f, init.g)

        # Apply 1 full step (collision + streaming + boundary)
        Y_1, _ = solver.step_coherent_k(Y_0, K=1)

        # Measure tensor inconsistency
        inconsistencies = []
        for y in range(ny):
            for x in range(nx):
                z_node = Y_1[:18, y, x]
                quad_actual = Y_1[18:, y, x]
                quad_expected = np.kron(z_node, z_node)
                e_node = float(la.norm(quad_actual - quad_expected) / (la.norm(quad_expected) + 1e-15))
                inconsistencies.append(e_node)

        mean_e_tensor = float(np.mean(inconsistencies))
        assert mean_e_tensor > 1.0, f"Tensor inconsistency should exceed 100%: {mean_e_tensor:.4e}"

    def test_04_four_modes_diagnostic_consistency(self):
        """Verify HQC (Mode B) and Coherent (Mode C) results match diagnostic CSV."""
        import csv
        with open("results/level6a_mode_comparison.csv", "r") as f:
            reader = csv.DictReader(f)
            rows = list(reader)

        assert len(rows) == 4
        # K=1 Mode B matches Mode C
        assert abs(float(rows[0]["Mode_B_HQC_rho_err"]) - float(rows[0]["Mode_C_Coherent_rho_err"])) < 1e-6
        # K=2 Mode C has higher error due to un-relifted tensor
        assert float(rows[1]["Mode_C_Coherent_rho_err"]) > float(rows[1]["Mode_B_HQC_rho_err"])

    def test_05_rejection_of_ma3_scaling_in_spatial_flow(self):
        """Verify empirical Mach scaling exponent is near 0 in spatial simulation."""
        import csv
        with open("results/level6a_mach_scaling.csv", "r") as f:
            reader = csv.DictReader(f)
            rows = list(reader)

        errs = [float(r["rho_err_K2"]) for r in rows]
        # In spatial flow, error is virtually identical across Mach numbers (~0.399)
        max_diff = max(errs) - min(errs)
        assert max_diff < 0.01, f"Error should be dominated by tensor mismatch, not Mach: {max_diff}"
