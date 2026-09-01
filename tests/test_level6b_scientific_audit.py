"""
Unit and regression tests for Level-6B Scientific Audit and Error-Origin Findings.
"""

import os
import csv
import pytest
import numpy as np
import scipy.linalg as la

from quantum.level6_lifted_carleman import (
    compute_level6a_carleman_matrices,
    lift_state_order2,
)
from classical.equilibrium import compute_equilibrium
from classical.d2q9 import C_X, C_Y, W


class TestLevel6BScientificAudit:
    """Test suite verifying scientific audit findings for Level 6B."""

    def test_01_carleman_mach_scaling_quadratic_law(self):
        """Verify local Carleman collision error scales quadratically with Mach number."""
        M1, M2, A_eval, _ = compute_level6a_carleman_matrices(tau_f=0.65, tau_g=0.7, rho_0=1.0, g_acc=0.0)

        # Evaluate error at Ma = 0.01 and Ma = 0.1
        errors = {}
        for ma in [0.01, 0.1]:
            u_test = np.array([ma / np.sqrt(3.0), ma / np.sqrt(3.0)])
            rho_test = 1.0 + 0.05 * ma
            alpha_test = 0.8

            f_eq = compute_equilibrium(np.array([[rho_test]]), u_test[:, None, None])[:, 0, 0]
            g_eq = np.zeros(9)
            for i in range(9):
                c_dot_u = C_X[i] * u_test[0] + C_Y[i] * u_test[1]
                g_eq[i] = W[i] * alpha_test * (1.0 + 3.0 * c_dot_u)

            z_exact = np.concatenate((f_eq, g_eq))
            Y_test = lift_state_order2(z_exact)
            z_star_carleman = A_eval @ Y_test

            err = float(la.norm(z_star_carleman - z_exact) / la.norm(z_exact))
            errors[ma] = err

        ratio = errors[0.1] / errors[0.01]
        # For quadratic scaling O(Ma^2), ratio should be approximately (0.1/0.01)^2 = 100
        assert 80.0 <= ratio <= 120.0, f"Expected O(Ma^2) scaling ratio ~100, got {ratio:.2f}"

    def test_02_audit_csv_artifacts_exist(self):
        """Verify all required scientific audit CSV files exist."""
        required_csvs = [
            "results/level6b_error_origin.csv",
            "results/level6b_long_time_error.csv",
            "results/level6b_control_experiments.csv",
            "results/level6b_relaxation_audit.csv",
            "results/level6b_force_audit.csv",
            "results/level6b_mass_momentum.csv",
            "results/level6b_convergence_audit.csv",
        ]
        for path in required_csvs:
            assert os.path.exists(path), f"Missing audit CSV: {path}"

    def test_03_grid_convergence_monotonic_decrease(self):
        """Verify grid convergence audit demonstrates monotonic reduction in error on fine meshes."""
        csv_path = "results/level6b_convergence_audit.csv"
        with open(csv_path, "r") as f:
            reader = csv.DictReader(f)
            rows = list(reader)

        errors_alpha = [float(r["alpha_rel_l2_error_T10"]) for r in rows]
        # Must be strictly decreasing
        for i in range(len(errors_alpha) - 1):
            assert errors_alpha[i + 1] < errors_alpha[i], f"Error not decreasing at mesh {rows[i+1]['mesh']}"
