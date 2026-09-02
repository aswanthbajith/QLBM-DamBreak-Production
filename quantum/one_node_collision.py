"""
One-Node Quantum Collision Core and Observable Readout for Two-Phase QLBM (Phase E).

Implements:
1. Exact local classical Level-4 collision reference (Phase E1).
2. Linearized fixed 6-qubit quantum collision dilation (Route C1 / Phase E2).
3. Parameterized state-dependent 6-qubit quantum collision dilation (Route C1a / Phase E3).
4. Quantum observable readout and moment extraction (Phase E4).
"""

from typing import Tuple, Dict, Any, Optional
import numpy as np
import scipy.linalg as la
from classical.d2q9 import C_X, C_Y, W, CS2
from classical.equilibrium import compute_equilibrium


def exact_one_node_level4_collision(
    z: np.ndarray,
    alpha: float,
    u_vec: np.ndarray,
    nu_L: float = 0.05,
    nu_G: float = 0.01,
    tau_g: float = 0.70,
    force_vec: Optional[np.ndarray] = None,
) -> np.ndarray:
    """
    Exact local Level-4 classical collision reference for one spatial node.
    
    Inputs:
    - z: local population vector of length 18: [f_0..f_8, g_0..g_8]
    - alpha: local phase fraction
    - u_vec: local velocity [u_x, u_y]
    - nu_L, nu_G: liquid and gas kinematic viscosities
    - tau_g: phase-field relaxation time
    - force_vec: external body force (buoyancy + surface tension)
    
    Returns:
    - z_prime: post-collision local population vector of length 18
    """
    f_in = z[:9]
    g_in = z[9:]
    rho = float(np.sum(f_in))

    nu_mix = alpha * nu_L + (1.0 - alpha) * nu_G
    tau_f = 3.0 * nu_mix + 0.5
    omega_f = 1.0 / tau_f
    omega_g = 1.0 / tau_g

    # Equilibrium populations
    rho_grid = np.array([[rho]])
    u_grid = u_vec[:, None, None]
    f_eq = compute_equilibrium(rho_grid, u_grid)[:, 0, 0]

    g_eq = np.zeros(9, dtype=np.float64)
    for i in range(9):
        c_u = C_X[i] * u_vec[0] + C_Y[i] * u_vec[1]
        g_eq[i] = W[i] * alpha * (1.0 + 3.0 * c_u)

    # Guo source term if force present
    S_force = np.zeros(9, dtype=np.float64)
    if force_vec is not None and (force_vec[0] != 0 or force_vec[1] != 0):
        Fx, Fy = force_vec[0], force_vec[1]
        for i in range(9):
            ci_F = C_X[i] * Fx + C_Y[i] * Fy
            ci_u = C_X[i] * u_vec[0] + C_Y[i] * u_vec[1]
            u_dot_F = u_vec[0] * Fx + u_vec[1] * Fy
            S_force[i] = (1.0 - 0.5 * omega_f) * W[i] * (3.0 * ci_F + 9.0 * ci_u * ci_F - 3.0 * u_dot_F)

    f_out = f_in - omega_f * (f_in - f_eq) + S_force
    g_out = g_in - omega_g * (g_in - g_eq)
    return np.concatenate([f_out, g_out])


class LinearizedOneNodeCollision:
    """
    Route C1: Linearized Fixed 6-Qubit Quantum Collision Dilation.
    
    Constructed around reference equilibrium (rho=1.0, u=0.0, alpha=0.5, tau=0.65).
    """

    def __init__(self, tau_0: float = 0.65, tau_g: float = 0.70):
        self.tau_0 = tau_0
        self.omega_0 = 1.0 / tau_0
        self.tau_g = tau_g
        self.omega_g = 1.0 / tau_g

        # Build 18x18 linearized matrix
        M_ff = (1.0 - self.omega_0) * np.eye(9)
        for i in range(9):
            for j in range(9):
                M_ff[i, j] += self.omega_0 * W[i] * (1.0 + 3.0 * (C_X[i] * C_X[j] + C_Y[i] * C_Y[j]))

        M_gg = (1.0 - self.omega_g) * np.eye(9)
        for i in range(9):
            for j in range(9):
                M_gg[i, j] += self.omega_g * W[i]

        self.C_matrix = np.block([[M_ff, np.zeros((9, 9))], [np.zeros((9, 9)), M_gg]])
        self.norm_C = float(la.norm(self.C_matrix, 2))
        self.alpha_C = float(1.01 * self.norm_C)
        self.p0 = float(1.0 / self.alpha_C**2)

        # 6-qubit Sz.-Nagy unitary dilation (64x64)
        C_pad = np.zeros((32, 32), dtype=np.float64)
        C_pad[:18, :18] = self.C_matrix
        C_scaled = C_pad / self.alpha_C

        D = la.sqrtm(np.eye(32) - C_scaled.T @ C_scaled)
        D_star = la.sqrtm(np.eye(32) - C_scaled @ C_scaled.T)
        self.U_C = np.block([[C_scaled, D_star], [D, -C_scaled.T]])

        # Projection operator
        self.P = np.zeros((18, 64), dtype=np.float64)
        self.P[:18, :18] = np.eye(18)

    def apply(self, z: np.ndarray) -> np.ndarray:
        """Apply linearized collision via projected block encoding."""
        z_pad = np.zeros(64, dtype=np.complex128)
        z_pad[:18] = z
        out = self.alpha_C * (self.U_C @ z_pad)
        return np.real(out[:18])


class ParameterizedOneNodeCollision:
    """
    Route C1a: State-Dependent Parameterized 6-Qubit Quantum Collision Dilation.
    
    Constructs exact C(alpha, u) and its Sz.-Nagy unitary dilation dynamically
    for any physical kinematic state.
    """

    def __init__(self, nu_L: float = 0.05, nu_G: float = 0.01, tau_g: float = 0.70):
        self.nu_L = nu_L
        self.nu_G = nu_G
        self.tau_g = tau_g
        self.omega_g = 1.0 / tau_g

    def construct_matrix(self, alpha: float, u_vec: np.ndarray) -> Tuple[np.ndarray, float, np.ndarray]:
        """
        Constructs exact parameterized C(alpha, u) in R^(18x18), its alpha_C, and 6-qubit U_C in U(64).
        """
        nu_mix = alpha * self.nu_L + (1.0 - alpha) * self.nu_G
        tau_f = 3.0 * nu_mix + 0.5
        omega_f = 1.0 / tau_f

        # Species f matrix M_f (9x9)
        E_f = np.zeros((9, 9), dtype=np.float64)
        u_sq = u_vec[0] ** 2 + u_vec[1] ** 2
        for i in range(9):
            ci_u = C_X[i] * u_vec[0] + C_Y[i] * u_vec[1]
            factor = W[i] * (1.0 + 3.0 * ci_u + 4.5 * ci_u**2 - 1.5 * u_sq)
            E_f[i, :] = factor
        M_f = (1.0 - omega_f) * np.eye(9) + omega_f * E_f

        # Species g matrix M_g (9x9)
        E_g = np.zeros((9, 9), dtype=np.float64)
        for i in range(9):
            ci_u = C_X[i] * u_vec[0] + C_Y[i] * u_vec[1]
            factor = W[i] * (1.0 + 3.0 * ci_u)
            E_g[i, :] = factor
        M_g = (1.0 - self.omega_g) * np.eye(9) + self.omega_g * E_g

        C_param = np.block([[M_f, np.zeros((9, 9))], [np.zeros((9, 9)), M_g]])
        norm_C = float(la.norm(C_param, 2))
        alpha_C = float(1.01 * norm_C)

        # 6-qubit dilation (64x64)
        C_pad = np.zeros((32, 32), dtype=np.float64)
        C_pad[:18, :18] = C_param
        C_scaled = C_pad / alpha_C

        D = la.sqrtm(np.eye(32) - C_scaled.T @ C_scaled)
        D_star = la.sqrtm(np.eye(32) - C_scaled @ C_scaled.T)
        U_C = np.block([[C_scaled, D_star], [D, -C_scaled.T]])

        return C_param, alpha_C, U_C

    def apply(self, z: np.ndarray, alpha: float, u_vec: np.ndarray) -> np.ndarray:
        """Apply exact parameterized collision via 6-qubit unitary dilation."""
        C_param, alpha_C, U_C = self.construct_matrix(alpha, u_vec)
        z_pad = np.zeros(64, dtype=np.complex128)
        z_pad[:18] = z
        out = alpha_C * (U_C @ z_pad)
        return np.real(out[:18])


class QuantumMomentReadout:
    """
    Quantum Moment Readout & Observable Extraction (Phase E4).
    
    Implements:
    1. Overlap / Hadamard test extraction for linear moments: rho, alpha, j_x, j_y.
    2. Shot-based square-root decoding from computational basis measurements.
    """

    @staticmethod
    def extract_moments_overlap(psi_18: np.ndarray, norm_z: float) -> Dict[str, float]:
        """
        Extracts macroscopic moments via quantum interference / overlap tests.
        
        |psi_18> = z / norm_z
        """
        # 1. Density rho = sum_i f_i
        probe_rho = np.zeros(18, dtype=np.float64)
        probe_rho[:9] = 1.0 / 3.0  # ||probe_rho|| = 1 since 9 * (1/3)^2 = 1
        overlap_rho = float(np.dot(probe_rho, psi_18))
        rho = 3.0 * norm_z * overlap_rho

        # 2. Phase alpha = sum_i g_i
        probe_alpha = np.zeros(18, dtype=np.float64)
        probe_alpha[9:] = 1.0 / 3.0
        overlap_alpha = float(np.dot(probe_alpha, psi_18))
        alpha = 3.0 * norm_z * overlap_alpha

        # 3. Momentum j_x = sum_i c_ix f_i
        cx_vec = np.array([C_X[i] for i in range(9)], dtype=np.float64)
        norm_cx = float(la.norm(cx_vec))  # sqrt(6)
        probe_jx = np.zeros(18, dtype=np.float64)
        probe_jx[:9] = cx_vec / norm_cx
        overlap_jx = float(np.dot(probe_jx, psi_18))
        j_x = norm_cx * norm_z * overlap_jx

        # 4. Momentum j_y = sum_i c_iy f_i
        cy_vec = np.array([C_Y[i] for i in range(9)], dtype=np.float64)
        norm_cy = float(la.norm(cy_vec))  # sqrt(6)
        probe_jy = np.zeros(18, dtype=np.float64)
        probe_jy[:9] = cy_vec / norm_cy
        overlap_jy = float(np.dot(probe_jy, psi_18))
        j_y = norm_cy * norm_z * overlap_jy

        u_x = j_x / (rho + 1e-15)
        u_y = j_y / (rho + 1e-15)

        return {
            "rho": rho,
            "alpha": alpha,
            "j_x": j_x,
            "j_y": j_y,
            "u_x": u_x,
            "u_y": u_y,
        }

    @staticmethod
    def decode_from_probabilities(
        probs_18: np.ndarray, norm_z: float
    ) -> Tuple[np.ndarray, np.ndarray, Dict[str, float]]:
        """
        Reconstructs populations and moments from computational basis probabilities P(i, p) = a_i^2 / N^2.
        
        Since kinetic populations f_i, g_i >= 0 in valid physical states:
        f_i = norm_z * sqrt(P(i, 0))
        g_i = norm_z * sqrt(P(i, 1))
        """
        f = norm_z * np.sqrt(np.maximum(probs_18[:9], 0.0))
        g = norm_z * np.sqrt(np.maximum(probs_18[9:], 0.0))

        rho = float(np.sum(f))
        alpha = float(np.sum(g))
        j_x = float(np.sum(f * C_X))
        j_y = float(np.sum(f * C_Y))
        u_x = j_x / (rho + 1e-15)
        u_y = j_y / (rho + 1e-15)

        moments = {"rho": rho, "alpha": alpha, "j_x": j_x, "j_y": j_y, "u_x": u_x, "u_y": u_y}
        return f, g, moments
