"""
Automated Test Suite for Phase F Quantum Collision & Parameter Oracle (Phases F1, F2, F3, F4, F5).

Validates:
1. Canonical Level-4 reference collision across all 7 physical test cases.
2. Parameterized collision matrix C(alpha, u) construction, spectral conditioning, and unitarity.
3. Coherent fixed-point moment arithmetic across word lengths (8, 10, 12, 16 bits).
4. Parameterized quantum collision oracle dilation precision and OAA success.
"""

import pytest
import numpy as np
import scipy.linalg as la

from classical.d2q9 import C_X, C_Y, W, CS2
from classical.equilibrium import compute_equilibrium
from quantum.reference_collision import reference_one_node_level4_collision
from quantum.parameterized_collision_oracle import (
    build_parameterized_collision_matrix,
    CoherentFixedPointMomentOracle,
    ParameterizedQuantumCollisionOracle,
)


def _generate_state(rho: float, alpha: float, u_vec: np.ndarray) -> np.ndarray:
    """Generates a physical test state z of length 18."""
    rho_grid = np.array([[rho]])
    u_grid = u_vec[:, None, None]
    f_eq = compute_equilibrium(rho_grid, u_grid)[:, 0, 0]
    f_in = f_eq + 0.01 * np.array([0.1, -0.2, 0.05, 0.15, -0.1, 0.05, -0.05, 0.1, -0.1])
    f_in *= (rho / np.sum(f_in))

    g_eq = np.zeros(9, dtype=np.float64)
    for i in range(9):
        c_u = C_X[i] * u_vec[0] + C_Y[i] * u_vec[1]
        g_eq[i] = W[i] * alpha * (1.0 + 3.0 * c_u)
    g_in = g_eq + (0.005 * np.array([-0.05, 0.1, -0.1, 0.05, 0.0, -0.05, 0.1, -0.05, 0.0]) if alpha > 0 else np.zeros(9))
    if alpha > 0:
        g_in *= (alpha / np.sum(g_in))

    return np.concatenate([f_in, g_in])


def test_reference_collision_seven_cases():
    """Verify Level-4 reference collision across all 7 canonical physical cases."""
    cases = [
        ("Liquid Node", 1.0, 1.0, np.array([0.0, 0.0]), None),
        ("Gas Node", 0.1, 0.0, np.array([0.0, 0.0]), None),
        ("Interface Node", 0.55, 0.5, np.array([0.0, 0.0]), None),
        ("Stationary Node", 1.0, 0.5, np.array([0.0, 0.0]), None),
        ("Moving Node", 1.0, 0.8, np.array([0.05, 0.02]), None),
        ("High-Mach Stress Test", 1.0, 1.0, np.array([0.086, 0.043]), None),
        ("Dam-Break Gravity Node", 1.0, 1.0, np.array([0.02, -0.01]), np.array([0.0, -0.0005])),
    ]

    for label, rho, alpha, u, force in cases:
        z_in = _generate_state(rho, alpha, u)
        z_out, meta = reference_one_node_level4_collision(
            z=z_in,
            nu_L=0.05,
            nu_G=0.01,
            tau_g=0.70,
            force_vec=force,
            alpha_override=alpha,
        )

        assert z_out.shape == (18,)
        assert np.all(np.isfinite(z_out))
        rho_out = np.sum(z_out[:9])
        alpha_out = np.sum(z_out[9:])
        assert abs(rho_out - rho) < 1e-14, f"Mass conservation failed in {label}"
        assert abs(alpha_out - alpha) < 1e-14, f"Phase conservation failed in {label}"


def test_parameterized_matrix_deterministic_sweep():
    """Verify parameterized collision matrix C(alpha, u) and dilation U_C across parameter space."""
    alphas = [0.0, 0.25, 0.5, 0.75, 1.0]
    u_mags = [0.0, 0.02, 0.05, 0.08]

    P = np.zeros((18, 64), dtype=np.float64)
    P[:18, :18] = np.eye(18)

    for a in alphas:
        for um in u_mags:
            u_vec = np.array([um * np.cos(np.pi/4), um * np.sin(np.pi/4)])
            C_mat, alpha_C, U_C, diag_info = build_parameterized_collision_matrix(a, u_vec)

            # 1. Unitarity
            unitarity_err = float(la.norm(U_C.conj().T @ U_C - np.eye(64), 2))
            assert unitarity_err < 1e-14, f"Dilation is non-unitary: {unitarity_err}"

            # 2. Block encoding projection
            proj_err = float(la.norm(P @ (alpha_C * U_C) @ P.T - C_mat, 2))
            assert proj_err < 1e-14, f"Block encoding projection error {proj_err} exceeds 1e-14"

            # 3. Conditioning
            assert diag_info["condition_number"] < 50.0
            assert diag_info["best_p_m"] > 0.85, f"Expected OAA success > 85%, got {diag_info['best_p_m']}"


def test_coherent_fixed_point_moment_oracle_scaling():
    """Verify coherent fixed-point moment calculation across word lengths (8, 10, 12, 16 bits)."""
    rho_true = 1.05
    alpha_true = 0.75
    u_true = np.array([0.04, -0.02])
    z_in = _generate_state(rho_true, alpha_true, u_true)

    # Exact moments of the actual population vector z_in
    rho_exact = float(np.sum(z_in[:9]))
    alpha_exact = float(np.sum(z_in[9:]))
    ux_exact = float(np.sum(z_in[:9] * C_X)) / rho_exact

    precisions = [
        (8, 4),   # 8-bit Q4.4
        (10, 6),  # 10-bit Q4.6
        (12, 8),  # 12-bit Q4.8
        (16, 12), # 16-bit Q4.12
    ]

    errors = []
    for total_bits, frac_bits in precisions:
        oracle = CoherentFixedPointMomentOracle(total_bits=total_bits, frac_bits=frac_bits)
        moments = oracle.evaluate_moments(z_in)

        err_rho = abs(moments["rho"] - rho_exact) / rho_exact
        err_alpha = abs(moments["alpha"] - alpha_exact) / alpha_exact
        err_ux = abs(moments["u_x"] - ux_exact) / (abs(ux_exact) + 1e-15)

        max_err = max(err_rho, err_alpha, err_ux)
        errors.append(max_err)

    # 12-bit error should be < 10%, 16-bit error should be < 1%
    assert errors[2] < 0.10, f"12-bit error {errors[2]} exceeds 10%"
    assert errors[3] < 0.01, f"16-bit error {errors[3]} exceeds 1%"


def test_parameterized_quantum_collision_oracle_execution():
    """Verify ParameterizedQuantumCollisionOracle against canonical Level-4 reference."""
    oracle = ParameterizedQuantumCollisionOracle()
    test_cases = [
        (1.0, 1.0, np.array([0.0, 0.0])),
        (0.1, 0.0, np.array([0.0, 0.0])),
        (0.55, 0.5, np.array([0.0, 0.0])),
        (1.0, 0.8, np.array([0.05, 0.02])),
        (1.0, 1.0, np.array([0.086, 0.043])),
    ]

    for rho, alpha, u in test_cases:
        z_in = _generate_state(rho, alpha, u)
        z_post, metrics = oracle.execute_collision(z_in, alpha=alpha, u_vec=None, apply_oaa=False)

        assert metrics["unitarity_error"] < 1e-14
        assert metrics["proj_block_error"] < 1e-14
        assert metrics["relative_error_vs_level4"] < 1e-12
        assert metrics["oaa_success_prob"] > 0.85
