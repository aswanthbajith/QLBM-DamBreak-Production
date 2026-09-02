"""
Parameterized Quantum Collision Oracle & Coherent Moment Oracle (Phases F2, F3, F4, F5).

Mathematical Architecture:
1. Exact Parameterized Collision Matrix C(alpha, u) in R^(18x18):
   - M_f(alpha, u)[i, j] = (1 - omega_f(alpha)) delta_ij + omega_f(alpha) w_i [1 + 3(c_i . u) + 4.5(c_i . u)^2 - 1.5 |u|^2]
   - M_g(u)[i, j] = (1 - omega_g) delta_ij + omega_g w_i [1 + 3(c_i . u)]
   - C(alpha, u) = block_diag(M_f, M_g)

2. 6-Qubit Sz.-Nagy Unitary Dilation U_C(alpha, u) in U(64):
   - Embedded into 5 system qubits (4 vel + 1 phase) + 1 dilation ancilla:
     U_C = [[C/alpha_C, D_*], [D, -C^T/alpha_C]], where D = sqrt(I - C^T C / alpha_C^2).

3. Coherent Fixed-Point Moment Oracle (Phase F4):
   - Reversible fixed-point arithmetic model evaluating rho, alpha, j, u with word length B in {8, 10, 12, 16}.

4. Oblivious Amplitude Amplification (OAA):
   - Grover angle theta = arcsin(1 / alpha_C), p_m = sin^2((2m+1)theta).
"""

from typing import Tuple, Dict, Any, Optional, List
import numpy as np
import scipy.linalg as la
from classical.d2q9 import C_X, C_Y, W, CS2
from classical.equilibrium import compute_equilibrium
from quantum.reference_collision import reference_one_node_level4_collision


def build_parameterized_collision_matrix(
    alpha: float,
    u_vec: np.ndarray,
    nu_L: float = 0.05,
    nu_G: float = 0.01,
    tau_g: float = 0.70,
) -> Tuple[np.ndarray, float, np.ndarray, Dict[str, Any]]:
    """
    Constructs exact C(alpha, u), its normalization alpha_C, and 6-qubit Sz.-Nagy unitary dilation U_C.
    
    Returns:
    - C_matrix: 18x18 real matrix
    - alpha_C: dilation scaling factor
    - U_C: 64x64 unitary matrix (6 qubits)
    - diag_info: dictionary containing singular values, condition number, p0, optimal m, p_m
    """
    alpha_clipped = float(np.clip(alpha, 0.0, 1.0))
    ux, uy = float(u_vec[0]), float(u_vec[1])
    u_sq = ux**2 + uy**2

    nu_mix = alpha_clipped * nu_L + (1.0 - alpha_clipped) * nu_G
    tau_f = 3.0 * nu_mix + 0.5
    omega_f = 1.0 / tau_f
    omega_g = 1.0 / tau_g

    # 1. Species f matrix M_f (9x9)
    E_f = np.zeros((9, 9), dtype=np.float64)
    for i in range(9):
        ci_u = C_X[i] * ux + C_Y[i] * uy
        factor = W[i] * (1.0 + 3.0 * ci_u + 4.5 * ci_u**2 - 1.5 * u_sq)
        E_f[i, :] = factor
    M_f = (1.0 - omega_f) * np.eye(9) + omega_f * E_f

    # 2. Species g matrix M_g (9x9)
    E_g = np.zeros((9, 9), dtype=np.float64)
    for i in range(9):
        ci_u = C_X[i] * ux + C_Y[i] * uy
        factor = W[i] * (1.0 + 3.0 * ci_u)
        E_g[i, :] = factor
    M_g = (1.0 - omega_g) * np.eye(9) + omega_g * E_g

    # 3. Full 18x18 block-diagonal collision matrix
    C_matrix = np.block([[M_f, np.zeros((9, 9))], [np.zeros((9, 9)), M_g]])

    # 4. Spectral analysis
    singular_values = la.svdvals(C_matrix)
    norm_C = float(singular_values[0])
    min_sv = float(singular_values[-1])
    cond_num = norm_C / (min_sv + 1e-15)

    alpha_C = float(1.01 * norm_C)
    p0 = float(1.0 / alpha_C**2)
    theta = float(np.arcsin(np.sqrt(p0)))

    # Find optimal small m for OAA (m in {1, 2, 3})
    oaa_probs = [(m, float(np.sin((2 * m + 1) * theta) ** 2)) for m in range(1, 4)]
    best_m, best_p_m = max(oaa_probs, key=lambda item: item[1])

    # 5. Construct 6-qubit Sz.-Nagy unitary dilation U_C in U(64)
    C_pad = np.zeros((32, 32), dtype=np.float64)
    C_pad[:18, :18] = C_matrix
    C_scaled = C_pad / alpha_C

    D = la.sqrtm(np.eye(32) - C_scaled.T @ C_scaled)
    D_star = la.sqrtm(np.eye(32) - C_scaled @ C_scaled.T)
    U_C = np.block([[C_scaled, D_star], [D, -C_scaled.T]])

    diag_info = {
        "norm_C": norm_C,
        "min_singular_value": min_sv,
        "condition_number": cond_num,
        "alpha_C": alpha_C,
        "p0": p0,
        "theta_deg": float(np.degrees(theta)),
        "optimal_m": best_m,
        "best_p_m": best_p_m,
        "oaa_probs": dict(oaa_probs),
        "tau_f": tau_f,
        "omega_f": omega_f,
    }
    return C_matrix, alpha_C, U_C, diag_info


class CoherentFixedPointMomentOracle:
    """
    Phase F4: Coherent Reversible Fixed-Point Moment Arithmetic Emulator.
    
    Models fixed-point registers:
    - B: total word length (e.g. 8, 10, 12, 16 bits)
    - F_bits: fractional bits (e.g. 4 for 8-bit, 6 for 10-bit, 10 for 16-bit)
    """

    def __init__(self, total_bits: int = 16, frac_bits: int = 10):
        self.total_bits = total_bits
        self.frac_bits = frac_bits
        self.scale = 2.0**frac_bits
        self.max_val = (2.0 ** (total_bits - 1) - 1.0) / self.scale
        self.min_val = -(2.0 ** (total_bits - 1)) / self.scale

    def quantize(self, val: float) -> float:
        """Fixed-point truncation / quantization."""
        clipped = np.clip(val, self.min_val, self.max_val)
        integer_rep = np.round(clipped * self.scale)
        return float(integer_rep / self.scale)

    def quantize_vector(self, vec: np.ndarray) -> np.ndarray:
        """Fixed-point quantization for vector."""
        return np.array([self.quantize(v) for v in vec], dtype=np.float64)

    def evaluate_moments(self, z: np.ndarray) -> Dict[str, float]:
        """
        Coherent fixed-point moment calculation:
        rho = sum(f_i), alpha = sum(g_i), j_x = sum(c_ix f_i), j_y = sum(c_iy f_i), u = j / rho.
        """
        z_q = self.quantize_vector(z)
        f_q = z_q[:9]
        g_q = z_q[9:]

        # Fixed-point additions
        rho_q = self.quantize(float(np.sum(f_q)))
        alpha_q = self.quantize(float(np.sum(g_q)))

        jx_q = self.quantize(float(np.sum(f_q * C_X)))
        jy_q = self.quantize(float(np.sum(f_q * C_Y)))

        # Fixed-point reciprocal division
        if rho_q > 0.0:
            ux_q = self.quantize(jx_q / (rho_q + 1e-15))
            uy_q = self.quantize(jy_q / (rho_q + 1e-15))
        else:
            ux_q, uy_q = 0.0, 0.0

        return {
            "rho": rho_q,
            "alpha": alpha_q,
            "j_x": jx_q,
            "j_y": jy_q,
            "u_x": ux_q,
            "u_y": uy_q,
            "word_length": self.total_bits,
            "frac_bits": self.frac_bits,
        }


class ParameterizedQuantumCollisionOracle:
    """
    Phase F5: Parameterized Quantum Collision Oracle.
    
    Executes the 6-qubit Sz.-Nagy unitary dilation U_C(alpha, u) on computational statevectors.
    """

    def __init__(self, nu_L: float = 0.05, nu_G: float = 0.01, tau_g: float = 0.70):
        self.nu_L = nu_L
        self.nu_G = nu_G
        self.tau_g = tau_g
        self.P = np.zeros((18, 64), dtype=np.float64)
        self.P[:18, :18] = np.eye(18)

    def execute_collision(
        self,
        z: np.ndarray,
        alpha: Optional[float] = None,
        u_vec: Optional[np.ndarray] = None,
        apply_oaa: bool = False,
    ) -> Tuple[np.ndarray, Dict[str, Any]]:
        """
        Applies parameterized 6-qubit quantum collision dilation to population vector z.
        
        Returns:
        - z_post: post-collision population vector (length 18)
        - exec_metrics: execution metrics including unitarity, precision, and success probability
        """
        f_in = z[:9]
        g_in = z[9:]
        rho = float(np.sum(f_in))
        alpha_val = float(np.sum(g_in)) if alpha is None else float(alpha)

        if u_vec is None:
            ux = float(np.sum(f_in * C_X)) / (rho + 1e-15)
            uy = float(np.sum(f_in * C_Y)) / (rho + 1e-15)
            u_actual = np.array([ux, uy], dtype=np.float64)
        else:
            u_actual = np.asarray(u_vec, dtype=np.float64)

        C_mat, alpha_C, U_C, diag_info = build_parameterized_collision_matrix(
            alpha=alpha_val,
            u_vec=u_actual,
            nu_L=self.nu_L,
            nu_G=self.nu_G,
            tau_g=self.tau_g,
        )

        # Unitarity and projection precision verification
        unitarity_err = float(la.norm(U_C.conj().T @ U_C - np.eye(64), 2))
        proj_block_err = float(la.norm(self.P @ (alpha_C * U_C) @ self.P.T - C_mat, 2))

        # Apply dilation to state
        z_pad = np.zeros(64, dtype=np.complex128)
        z_pad[:18] = z

        if apply_oaa and diag_info["optimal_m"] == 1:
            R_0 = np.eye(64, dtype=np.complex128)
            R_0[32:, 32:] = -np.eye(32)

            R_tar = np.eye(64, dtype=np.complex128)
            R_tar[:18, :18] = -np.eye(18)

            psi_0 = U_C @ z_pad
            psi_amplified = -U_C @ (R_0 @ (U_C.conj().T @ (R_tar @ psi_0)))
            gain_factor = np.sqrt(diag_info["best_p_m"] / (diag_info["p0"] + 1e-15))
            z_post = np.real(psi_amplified[:18]) * (alpha_C / gain_factor)
        else:
            psi_out = alpha_C * (U_C @ z_pad)
            z_post = np.real(psi_out[:18])

        # Validate against Level-4 canonical reference
        z_ref, ref_meta = reference_one_node_level4_collision(
            z=z,
            nu_L=self.nu_L,
            nu_G=self.nu_G,
            tau_g=self.tau_g,
            alpha_override=alpha_val,
        )

        abs_err = float(la.norm(z_post - z_ref))
        rel_err = float(abs_err / (la.norm(z_ref) + 1e-15))

        exec_metrics = {
            "unitarity_error": unitarity_err,
            "proj_block_error": proj_block_err,
            "absolute_error_vs_level4": abs_err,
            "relative_error_vs_level4": rel_err,
            "alpha_C": alpha_C,
            "p0_base_success": diag_info["p0"],
            "oaa_m": diag_info["optimal_m"],
            "oaa_success_prob": diag_info["best_p_m"],
            "spectral_condition": diag_info["condition_number"],
            "u_evaluated": u_actual,
        }
        return z_post, exec_metrics
