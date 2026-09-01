"""
Unit & Numerical Tests for Level-5 Coupled Two-Phase Carleman Linearization.
"""

import pytest
import numpy as np
import scipy.linalg as la

from quantum.level5_two_phase_carleman import (
    compute_level5_carleman_matrices,
    lift_to_second_order,
    compute_closed_carleman_matrix_order2,
    analyze_carleman_operator_properties,
    construct_level5_unitary_dilation,
)
from classical.level4_two_phase import Level4TwoPhaseLBM
from scripts.run_level5_carleman_validation import run_carleman_step


class TestLevel5Carleman:
    """Test suite for Level-5 Carleman matrices and properties."""

    def test_01_matrix_dimensions(self):
        """Verify dimensions of M1, M2, A_eval, C2."""
        M1, M2, A_eval = compute_level5_carleman_matrices()
        C2 = compute_closed_carleman_matrix_order2(M1, M2)

        assert M1.shape == (18, 18)
        assert M2.shape == (18, 324)
        assert A_eval.shape == (18, 342)
        assert C2.shape == (342, 342)

    def test_02_single_step_carleman_accuracy(self):
        """Verify single-step Carleman prediction matches Level-4 nonlinear step within 0.1%."""
        nx, ny = 4, 4
        g_acc = -0.0005
        solver = Level4TwoPhaseLBM(nx=nx, ny=ny, g_acc=g_acc, sigma=0.0)
        M1, M2, A_eval = compute_level5_carleman_matrices(
            tau_f=1.0 / (3.0 * 0.05 + 0.5), tau_g=0.7, g_acc=g_acc
        )

        f_start = np.copy(solver.f)
        g_start = np.copy(solver.g)

        solver.step()
        f_k, g_k = run_carleman_step(f_start, g_start, A_eval, ny, nx)

        err_f = float(la.norm(f_k - solver.f) / la.norm(solver.f))
        err_g = float(la.norm(g_k - solver.g) / la.norm(solver.g))

        assert err_f < 1e-3, f"Single-step f error too high: {err_f:.4e}"
        assert err_g < 1e-3, f"Single-step g error too high: {err_g:.4e}"

    def test_03_mass_conservation(self):
        """Verify Carleman evolution strictly conserves mass over 10 steps."""
        nx, ny = 4, 4
        solver = Level4TwoPhaseLBM(nx=nx, ny=ny, g_acc=-0.0005, sigma=0.0)
        M1, M2, A_eval = compute_level5_carleman_matrices()

        f_k = np.copy(solver.f)
        g_k = np.copy(solver.g)
        m0 = float(np.sum(g_k))

        for _ in range(10):
            f_k, g_k = run_carleman_step(f_k, g_k, A_eval, ny, nx)

        m_final = float(np.sum(g_k))
        rel_diff = abs(m_final - m0) / m0
        assert rel_diff < 1e-12, f"Carleman mass drift too high: {rel_diff:.4e}"

    def test_04_unitary_dilation(self):
        """Verify 10-qubit Sz.-Nagy unitary dilation satisfies U_C^\dagger U_C = I_1024."""
        _, _, A_eval = compute_level5_carleman_matrices()
        U_C, alpha = construct_level5_unitary_dilation(A_eval)

        assert U_C.shape == (1024, 1024)
        assert alpha > 0.0

        diff = la.norm(U_C.T @ U_C - np.eye(1024), 2)
        assert diff < 1e-12, f"Unitary dilation error too high: {diff:.4e}"

    def test_05_operator_spectral_properties(self):
        """Verify spectral properties of Carleman operator."""
        props = analyze_carleman_operator_properties()
        assert props["spectral_radius_M1"] > 0.0
        assert props["sparsity_A_eval"] > 0.80  # More than 80% sparse
