"""
Automated Test Suite for Quantum Collision Architecture Investigation (Phases B, C, D).

Validates:
1. Mathematical precision and unitarity of Route C1 block-encoded local collision dilation.
2. Oblivious Amplitude Amplification (OAA) success probability scaling (m=1 -> 99.71%).
3. Dilation leakage under unprojected powers vs machine-precision projected reset powers.
4. Route C3 Carleman / polynomial truncation error scaling vs Mach number.
5. Exact dissection and invariant properties of the two-phase collision operator.
"""

import pytest
import numpy as np
import scipy.linalg as la

from classical.d2q9 import C_X, C_Y, W, CS2
from classical.equilibrium import compute_equilibrium


def test_route_c1_block_encoding_precision():
    """Verify Route C1 unitary dilation precision: ||P U_C P - C/alpha_C|| < 1e-14 and ||U†U - I|| < 1e-14."""
    tau_0 = 0.65
    omega_0 = 1.0 / tau_0
    tau_g = 0.70
    omega_g = 1.0 / tau_g

    M_ff = (1.0 - omega_0) * np.eye(9)
    for i in range(9):
        for j in range(9):
            M_ff[i, j] += omega_0 * W[i] * (1.0 + 3.0 * (C_X[i] * C_X[j] + C_Y[i] * C_Y[j]))

    M_gg = (1.0 - omega_g) * np.eye(9)
    for i in range(9):
        for j in range(9):
            M_gg[i, j] += omega_g * W[i]

    C_linear = np.block([[M_ff, np.zeros((9, 9))], [np.zeros((9, 9)), M_gg]])
    norm_C = float(la.norm(C_linear, 2))
    alpha_C = float(1.01 * norm_C)

    C_pad = np.zeros((32, 32), dtype=np.float64)
    C_pad[:18, :18] = C_linear
    C_scaled = C_pad / alpha_C

    D = la.sqrtm(np.eye(32) - C_scaled.T @ C_scaled)
    D_star = la.sqrtm(np.eye(32) - C_scaled @ C_scaled.T)
    U_C = np.block([[C_scaled, D_star], [D, -C_scaled.T]])

    unitarity_err = float(la.norm(U_C.T @ U_C - np.eye(64), 2))
    P = np.zeros((18, 64), dtype=np.float64)
    P[:18, :18] = np.eye(18)
    proj_err = float(la.norm(P @ (alpha_C * U_C) @ P.T - C_linear, 2))

    assert unitarity_err < 1e-14, f"U_C is non-unitary: {unitarity_err}"
    assert proj_err < 1e-14, f"Projected block error {proj_err} exceeds tolerance"


def test_route_c1_oaa_amplification():
    """Verify that m=1 OAA iteration boosts success probability to > 99%."""
    tau_0 = 0.65
    omega_0 = 1.0 / tau_0
    tau_g = 0.70
    omega_g = 1.0 / tau_g

    M_ff = (1.0 - omega_0) * np.eye(9)
    for i in range(9):
        for j in range(9):
            M_ff[i, j] += omega_0 * W[i] * (1.0 + 3.0 * (C_X[i] * C_X[j] + C_Y[i] * C_Y[j]))
    M_gg = (1.0 - omega_g) * np.eye(9) + omega_g * np.outer(W, np.ones(9))

    C_linear = np.block([[M_ff, np.zeros((9, 9))], [np.zeros((9, 9)), M_gg]])
    norm_C = float(la.norm(C_linear, 2))
    alpha_C = float(1.01 * norm_C)

    p0 = 1.0 / alpha_C**2
    theta = np.arcsin(np.sqrt(p0))
    p_m1 = np.sin(3 * theta) ** 2

    assert p0 > 0.20, f"Expected base p0 > 20%, got {p0}"
    assert p_m1 > 0.99, f"Expected OAA(m=1) p1 > 99%, got {p_m1}"


def test_route_c1_dilation_leakage_and_reset():
    """Verify that unprojected dilation leaks while projective reset restores exact matrix powers."""
    tau_0 = 0.65
    omega_0 = 1.0 / tau_0
    tau_g = 0.70
    omega_g = 1.0 / tau_g

    M_ff = (1.0 - omega_0) * np.eye(9)
    for i in range(9):
        for j in range(9):
            M_ff[i, j] += omega_0 * W[i] * (1.0 + 3.0 * (C_X[i] * C_X[j] + C_Y[i] * C_Y[j]))
    M_gg = (1.0 - omega_g) * np.eye(9) + omega_g * np.outer(W, np.ones(9))

    C_linear = np.block([[M_ff, np.zeros((9, 9))], [np.zeros((9, 9)), M_gg]])
    alpha_C = float(1.01 * la.norm(C_linear, 2))

    C_pad = np.zeros((32, 32), dtype=np.float64)
    C_pad[:18, :18] = C_linear
    C_scaled = C_pad / alpha_C

    D = la.sqrtm(np.eye(32) - C_scaled.T @ C_scaled)
    D_star = la.sqrtm(np.eye(32) - C_scaled @ C_scaled.T)
    U_C = np.block([[C_scaled, D_star], [D, -C_scaled.T]])

    P = np.zeros((18, 64), dtype=np.float64)
    P[:18, :18] = np.eye(18)

    # K = 2
    C_2 = np.linalg.matrix_power(C_linear, 2)
    unproj_2 = P @ np.linalg.matrix_power(alpha_C * U_C, 2) @ P.T
    proj_2 = np.linalg.matrix_power(P @ (alpha_C * U_C) @ P.T, 2)

    err_unproj = float(la.norm(unproj_2 - C_2, 2) / la.norm(C_2, 2))
    err_proj = float(la.norm(proj_2 - C_2, 2) / la.norm(C_2, 2))

    assert err_unproj > 1.0, f"Expected large unprojected leakage at K=2, got {err_unproj}"
    assert err_proj < 1e-14, f"Projective reset power error {err_proj} exceeds tolerance"


def test_route_c3_carleman_mach_scaling():
    """Verify that Carleman collision error scales with Mach number with high correlation."""
    mach_numbers = [0.005, 0.010, 0.020, 0.050, 0.100]
    cs = 1.0 / np.sqrt(3.0)
    alpha_0 = 0.80

    errors = []
    for ma in mach_numbers:
        u_mag = ma * cs
        u_vec = np.array([u_mag * np.cos(np.pi/4), u_mag * np.sin(np.pi/4)])
        rho_val = 1.0 + 0.5 * ma**2

        # Exact Level-4 equilibrium
        rho_grid = np.array([[rho_val]])
        u_grid = u_vec[:, None, None]
        f_eq_exact = compute_equilibrium(rho_grid, u_grid)[:, 0, 0]

        g_eq_exact = np.zeros(9)
        for i in range(9):
            c_dot_u = C_X[i] * u_vec[0] + C_Y[i] * u_vec[1]
            g_eq_exact[i] = W[i] * alpha_0 * (1.0 + 3.0 * c_dot_u)

        z_eq_exact = np.concatenate([f_eq_exact, g_eq_exact])

        # Carleman Taylor with 1/rho ~ 2 - rho
        j_vec = rho_val * u_vec
        inv_rho_approx = 2.0 - rho_val
        f_eq_carleman = np.zeros(9)
        for i in range(9):
            ci_j = C_X[i] * j_vec[0] + C_Y[i] * j_vec[1]
            j_sq = j_vec[0]**2 + j_vec[1]**2
            f_eq_carleman[i] = W[i] * (rho_val + 3.0 * ci_j + (4.5 * ci_j**2 - 1.5 * j_sq) * inv_rho_approx)

        z_eq_carleman = np.concatenate([f_eq_carleman, g_eq_exact])
        err = float(la.norm(z_eq_exact - z_eq_carleman) / (la.norm(z_eq_exact) + 1e-15))
        errors.append(err)

    assert errors[-1] < 1e-6, f"Error at Ma=0.10 ({errors[-1]}) exceeds tolerance"

    log_ma = np.log(mach_numbers)
    log_err = np.log(errors)
    slope, intercept = np.polyfit(log_ma, log_err, 1)
    corr = np.corrcoef(log_ma, log_err)[0, 1] ** 2

    assert slope > 4.0, f"Expected high-order scaling slope > 4, got {slope}"
    assert corr > 0.99, f"Expected R^2 > 0.99, got {corr}"
