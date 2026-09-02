"""
Automated Test Suite for One-Node Quantum Collision and Observable Readout (Phase E).

Validates:
1. Exact local Level-4 classical collision reference across physical regimes.
2. Quantified error of fixed linearized collision C_lin vs physical state variations.
3. Machine-precision fidelity of Parameterized Quantum Collision (Route C1a) vs Level 4:
   - Density error < 1e-6
   - Phase error < 1e-6
   - Momentum error < 1e-5
   - Total map error < 1e-12
4. Strict 6-qubit Sz.-Nagy unitary dilation (||U†U - I|| < 1e-14).
5. Quantum moment readout (Hadamard overlap test and square-root decoding).
6. Multi-collision repeated powers (K=1, 2, 4, 8, 16) under projective resets.
"""

import pytest
import numpy as np
import scipy.linalg as la

from classical.d2q9 import C_X, C_Y, W, CS2
from classical.equilibrium import compute_equilibrium
from quantum.one_node_collision import (
    exact_one_node_level4_collision,
    LinearizedOneNodeCollision,
    ParameterizedOneNodeCollision,
    QuantumMomentReadout,
)


def _make_test_state(rho: float, alpha: float, u_vec: np.ndarray) -> np.ndarray:
    """Helper to generate consistent initial population vector z."""
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


def test_exact_one_node_classical_reference():
    """Verify that exact_one_node_level4_collision conserves mass and phase."""
    for rho, alpha, u in [(1.0, 1.0, np.array([0.0, 0.0])), (0.1, 0.0, np.array([0.02, -0.01])), (0.55, 0.5, np.array([0.05, 0.02]))]:
        z_in = _make_test_state(rho, alpha, u)
        z_out = exact_one_node_level4_collision(z_in, alpha, u)

        rho_out = np.sum(z_out[:9])
        alpha_out = np.sum(z_out[9:])
        assert abs(rho_out - rho) < 1e-14, f"Mass conservation failed: |{rho_out} - {rho}|"
        assert abs(alpha_out - alpha) < 1e-14, f"Phase conservation failed: |{alpha_out} - {alpha}|"


def test_linearized_collision_defect_sweep():
    """Verify that fixed C_lin has quantified non-zero error on varying physical states."""
    c_lin_solver = LinearizedOneNodeCollision()
    test_cases = [
        ("Gas Phase (alpha=0.0, rho=0.1)", 0.1, 0.0, np.array([0.0, 0.0])),
        ("Convective Flow (u=[0.05, 0.02])", 1.0, 0.8, np.array([0.05, 0.02])),
        ("High-Speed Flow (u=[0.10, 0.05])", 1.0, 1.0, np.array([0.10, 0.05])),
    ]
    for label, rho, alpha, u in test_cases:
        z_in = _make_test_state(rho, alpha, u)
        z_exact = exact_one_node_level4_collision(z_in, alpha, u)
        z_lin = c_lin_solver.apply(z_in)

        err = float(la.norm(z_lin - z_exact) / la.norm(z_exact))
        assert err > 1e-3, f"Expected non-negligible error for {label}, got {err}"


def test_parameterized_collision_precision():
    """Verify that Parameterized Quantum Collision achieves machine-precision matching with Level 4."""
    param_solver = ParameterizedOneNodeCollision()
    test_cases = [
        (1.0, 1.0, np.array([0.0, 0.0])),
        (0.1, 0.0, np.array([0.0, 0.0])),
        (0.55, 0.5, np.array([0.0, 0.0])),
        (1.0, 0.8, np.array([0.05, 0.02])),
        (1.0, 1.0, np.array([0.10, 0.05])),
    ]
    for rho, alpha, u in test_cases:
        z_in = _make_test_state(rho, alpha, u)
        z_exact = exact_one_node_level4_collision(z_in, alpha, u)
        z_quantum = param_solver.apply(z_in, alpha, u)

        # 1. Collision map error
        map_err = float(la.norm(z_quantum - z_exact) / la.norm(z_exact))
        assert map_err < 1e-12, f"Collision map error {map_err} exceeds 1e-12"

        # 2. Density error
        rho_q = np.sum(z_quantum[:9])
        rho_e = np.sum(z_exact[:9])
        assert abs(rho_q - rho_e) < 1e-6, f"Density error {abs(rho_q - rho_e)} exceeds 1e-6"

        # 3. Phase error
        alpha_q = np.sum(z_quantum[9:])
        alpha_e = np.sum(z_exact[9:])
        assert abs(alpha_q - alpha_e) < 1e-6, f"Phase error {abs(alpha_q - alpha_e)} exceeds 1e-6"

        # 4. Momentum error
        jx_q = np.sum(z_quantum[:9] * C_X)
        jx_e = np.sum(z_exact[:9] * C_X)
        assert abs(jx_q - jx_e) < 1e-5, f"Momentum Jx error {abs(jx_q - jx_e)} exceeds 1e-5"


def test_parameterized_dilation_unitarity():
    """Verify that the 6-qubit Sz.-Nagy dilation is strictly unitary across the parameter space."""
    param_solver = ParameterizedOneNodeCollision()
    for alpha in [0.0, 0.25, 0.5, 0.75, 1.0]:
        for u_mag in [0.0, 0.02, 0.05, 0.10]:
            u_vec = np.array([u_mag, 0.5 * u_mag])
            _, _, U_C = param_solver.construct_matrix(alpha, u_vec)

            unitarity_err = float(la.norm(U_C.conj().T @ U_C - np.eye(64), 2))
            assert unitarity_err < 1e-14, f"Dilation is non-unitary (err={unitarity_err}) for alpha={alpha}, u={u_vec}"


def test_quantum_moment_readout():
    """Verify quantum moment readout via overlap test and probability decoding."""
    rho_true = 1.05
    alpha_true = 0.75
    u_true = np.array([0.04, -0.02])
    z_in = _make_test_state(rho_true, alpha_true, u_true)
    norm_z = float(la.norm(z_in))
    psi_18 = z_in / norm_z

    # 1. Overlap Test Readout
    moments_overlap = QuantumMomentReadout.extract_moments_overlap(psi_18, norm_z)
    assert abs(moments_overlap["rho"] - rho_true) < 1e-14
    assert abs(moments_overlap["alpha"] - alpha_true) < 1e-14
    assert abs(moments_overlap["j_x"] - np.sum(z_in[:9] * C_X)) < 1e-14

    # 2. Probability Decoding Readout
    probs_18 = (z_in / norm_z) ** 2
    f_dec, g_dec, moments_prob = QuantumMomentReadout.decode_from_probabilities(probs_18, norm_z)
    assert la.norm(f_dec - z_in[:9]) < 1e-14
    assert la.norm(g_dec - z_in[9:]) < 1e-14
    assert abs(moments_prob["rho"] - rho_true) < 1e-14


def test_multi_collision_projected_powers():
    """Verify that multi-collision evolution under projective reset reproduces exact matrix powers."""
    param_solver = ParameterizedOneNodeCollision()
    alpha = 0.8
    u_vec = np.array([0.03, 0.01])
    C_mat, alpha_C, U_C = param_solver.construct_matrix(alpha, u_vec)

    P = np.zeros((18, 64), dtype=np.float64)
    P[:18, :18] = np.eye(18)

    for K in [1, 2, 4, 8, 16]:
        C_K = np.linalg.matrix_power(C_mat, K)
        proj_K = np.linalg.matrix_power(P @ (alpha_C * U_C) @ P.T, K)
        err = float(la.norm(proj_K - C_K, 2) / la.norm(C_K, 2))
        assert err < 1e-14, f"Projective reset power error at K={K} exceeds tolerance: {err}"
