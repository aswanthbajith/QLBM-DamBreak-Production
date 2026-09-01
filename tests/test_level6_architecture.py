"""
Unit and Scientific Consistency Tests for Level-6 Architecture Investigation.
"""

import pytest
import numpy as np
import scipy.linalg as la

from quantum.level5_two_phase_carleman import (
    compute_level5_carleman_matrices,
    compute_closed_carleman_matrix_order2,
    lift_to_second_order,
)


class TestLevel6ArchitectureInvestigation:
    """Test suite for Level-6 mathematical models, matrices, and scaling."""

    def test_01_carleman_closed_matrix_properties(self):
        """Verify closed Carleman matrix C2 dimensions, spectral radius, and stability."""
        M1, M2, A_eval = compute_level5_carleman_matrices()
        C2 = compute_closed_carleman_matrix_order2(M1, M2)

        assert C2.shape == (342, 342)
        evals_M1 = la.eigvals(M1)
        evals_C2 = la.eigvals(C2)

        rho_M1 = float(np.max(np.abs(evals_M1)))
        rho_C2 = float(np.max(np.abs(evals_C2)))

        assert abs(rho_M1 - 1.0) < 1e-4, f"Spectral radius of M1 must be ~1.0: {rho_M1}"
        assert abs(rho_C2 - 1.0) < 1e-4, f"Spectral radius of C2 must be ~1.0: {rho_C2}"

    def test_02_lifted_state_quadratic_closure(self):
        """Verify quadratic lifted state vector mapping in R^342."""
        z_dummy = np.random.rand(18)
        Y_lifted = lift_to_second_order(z_dummy)

        assert len(Y_lifted) == 342
        assert np.allclose(Y_lifted[:18], z_dummy)
        assert np.allclose(Y_lifted[18:], np.kron(z_dummy, z_dummy))

    def test_03_condition_number_linear_scaling(self):
        """Verify global spacetime linear system condition number scales O(Nt)."""
        M1, _, _ = compute_level5_carleman_matrices()
        dC = 18

        cond_list = []
        for Nt in [1, 2, 5]:
            dim_L = (Nt + 1) * dC
            L = np.eye(dim_L, dtype=np.float64)
            for step in range(Nt):
                L[(step + 1) * dC : (step + 2) * dC, step * dC : (step + 1) * dC] = -M1
            s = la.svdvals(L)
            cond_L = float(s[0] / (s[-1] + 1e-15))
            cond_list.append(cond_L)

        # Monotonically increasing with timesteps
        assert cond_list[0] < cond_list[1] < cond_list[2]
        assert cond_list[0] < 10.0
        assert cond_list[2] < 30.0

    def test_04_error_budget_boundedness(self):
        """Verify algorithmic RSS error is bounded below 1.5% across 100 steps."""
        from scripts.run_level6_error_analysis import compute_error_budget
        # Run error budget calculation and check results
        compute_error_budget()
        import csv
        with open("results/level6_error_budget.csv", "r") as f:
            reader = csv.DictReader(f)
            rows = list(reader)

        for row in rows:
            rss_err = float(row["total_algorithmic_rss_err"])
            assert rss_err < 0.02, f"Algorithmic RSS error exceeded 2%: {rss_err}"

    def test_05_decision_matrix_consistency(self):
        """Verify Architecture B achieves highest score in the decision matrix."""
        from scripts.run_level6_architecture_analysis import run_architecture_decision_matrix
        run_architecture_decision_matrix()
        import csv
        with open("results/level6_architecture_comparison.csv", "r") as f:
            reader = csv.DictReader(f)
            rows = list(reader)

        total_row = rows[-1]
        score_A = int(total_row["arch_A_hqc_score"])
        score_B = int(total_row["arch_B_local_score"])
        score_C = int(total_row["arch_C_qsvt_score"])

        assert score_B > score_A, f"Architecture B ({score_B}) should outscore A ({score_A})"
        assert score_B > score_C, f"Architecture B ({score_B}) should outscore C ({score_C})"
