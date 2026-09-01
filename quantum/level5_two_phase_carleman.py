"""
Level-5 Coupled Two-Phase Second-Order Carleman Linearization Module.

Constructs:
1. Linear collision matrix M1 in R^(18x18)
2. Quadratic convective tensor M2 in R^(18x324)
3. Local evaluation operator A_eval = [M1, M2] in R^(18x342)
4. Autonomous closed Carleman operator C2 in R^(342x342)
5. Power-of-two Sz.-Nagy unitary dilation U_C in U(1024) (10 qubits)
6. Truncation error and spectral property evaluators
"""

from typing import Tuple, Dict, Any
import numpy as np
import scipy.linalg as la
from classical.d2q9 import C_X, C_Y, W, CS2


def compute_level5_carleman_matrices(
    tau_f: float = 0.8,
    tau_g: float = 0.7,
    rho_0: float = 1.0,
    g_acc: float = -0.0005,
    rho_gas: float = 0.1,
) -> Tuple[np.ndarray, np.ndarray, np.ndarray]:
    """
    Computes exact coupled Level-5 Carleman matrices M1, M2, and A_eval.
    
    State vector: z = [f_0..f_8, g_0..g_8]^T in R^18 (indices 0..8: f, indices 9..17: g)
    Lifted state: Y2 = [z; z (x) z] in R^342
    
    Returns:
        M1: (18, 18) linear collision + forcing matrix
        M2: (18, 324) quadratic convection matrix
        A_eval: (18, 342) evaluation operator [M1, M2]
    """
    omega_f = 1.0 / tau_f
    omega_g = 1.0 / tau_g

    cx = C_X
    cy = C_Y
    w = W

    # 1. Linear Matrix M1 (18 x 18)
    M1 = np.zeros((18, 18), dtype=np.float64)

    # Hydrodynamic block (0..8 -> 0..8)
    for i in range(9):
        for k in range(9):
            c_dot_c = cx[i] * cx[k] + cy[i] * cy[k]
            E1_ik_f = w[i] * (1.0 + 3.0 * c_dot_c)
            # Body force linear contribution: (rho - rho_G) * g_acc
            # F_y = (sum_k f_k - rho_G) * g_acc
            F_linear_term = (1.0 - 0.5 * omega_f) * w[i] * 3.0 * cy[i] * g_acc
            delta_ik = 1.0 if i == k else 0.0
            M1[i, k] = (1.0 - omega_f) * delta_ik + omega_f * E1_ik_f + F_linear_term

    # Phase block (9..17 -> 9..17)
    for i in range(9):
        for k in range(9):
            E1_ik_g = w[i]
            delta_ik = 1.0 if i == k else 0.0
            M1[9 + i, 9 + k] = (1.0 - omega_g) * delta_ik + omega_g * E1_ik_g

    # 2. Quadratic Matrix M2 (18 x 324)
    # The quadratic basis is z (x) z of length 18 * 18 = 324
    # Index for (a, b) where a, b in 0..17 is: idx = a * 18 + b
    M2 = np.zeros((18, 324), dtype=np.float64)

    # Hydrodynamic convective block (f_j * f_k, j,k in 0..8 -> idx = j * 18 + k)
    for i in range(9):
        for j in range(9):
            for k in range(9):
                idx = j * 18 + k
                ci_cj = cx[i] * cx[j] + cy[i] * cy[j]
                ci_ck = cx[i] * cx[k] + cy[i] * cy[k]
                cj_ck = cx[j] * cx[k] + cy[j] * cy[k]
                E2_ijk_f = (w[i] / rho_0) * (4.5 * ci_cj * ci_ck - 1.5 * cj_ck)
                M2[i, idx] = omega_f * E2_ijk_f

    # Phase-Momentum coupling block (g_j * f_k, j in 9..17, k in 0..8 -> idx = j * 18 + k)
    for i in range(9):
        for j_g in range(9):
            for k_f in range(9):
                j_idx = 9 + j_g
                k_idx = k_f
                idx = j_idx * 18 + k_idx
                ci_ck = cx[i] * cx[k_f] + cy[i] * cy[k_f]
                E2_ijk_g = (3.0 * w[i] / rho_0) * ci_ck
                M2[9 + i, idx] = omega_g * E2_ijk_g

    # 3. Combined Evaluation Operator A_eval (18 x 342)
    A_eval = np.hstack((M1, M2))

    return M1, M2, A_eval


def lift_to_second_order(z: np.ndarray) -> np.ndarray:
    """
    Lifts state vector z in R^18 to second-order Carleman vector Y2 = [z; z (x) z] in R^342.
    """
    z = np.asarray(z, dtype=np.float64).flatten()
    z_kron_z = np.kron(z, z)
    return np.concatenate((z, z_kron_z))


def compute_closed_carleman_matrix_order2(M1: np.ndarray, M2: np.ndarray) -> np.ndarray:
    """
    Constructs the autonomous closed Carleman evolution matrix C2 in R^(342 x 342).
    
    C2 = [ M1         M2             ]
         [ 0          M1 (x) M1      ]
    """
    M1_kron_M1 = np.kron(M1, M1)  # (324, 324)
    C2 = np.zeros((342, 342), dtype=np.float64)
    C2[:18, :18] = M1
    C2[:18, 18:] = M2
    C2[18:, 18:] = M1_kron_M1
    return C2


def analyze_carleman_operator_properties(
    tau_f: float = 0.8, tau_g: float = 0.7
) -> Dict[str, Any]:
    """
    Computes spectral, norm, and conditioning properties of the Level-5 Carleman operator.
    """
    M1, M2, A_eval = compute_level5_carleman_matrices(tau_f=tau_f, tau_g=tau_g)
    C2 = compute_closed_carleman_matrix_order2(M1, M2)

    # Spectral properties
    eigenvalues_M1 = la.eigvals(M1)
    eigenvalues_C2 = la.eigvals(C2)
    spectral_radius_M1 = float(np.max(np.abs(eigenvalues_M1)))
    spectral_radius_C2 = float(np.max(np.abs(eigenvalues_C2)))

    # Norms
    norm_M1 = float(la.norm(M1, 2))
    norm_A_eval = float(la.norm(A_eval, 2))
    norm_C2 = float(la.norm(C2, 2))

    # Condition number
    s_M1 = la.svdvals(M1)
    cond_M1 = float(s_M1[0] / (s_M1[-1] + 1e-15))

    # Sparsity
    nnz_A_eval = int(np.count_nonzero(A_eval))
    sparsity_A_eval = float(1.0 - nnz_A_eval / A_eval.size)

    return {
        "dim_M1": M1.shape,
        "dim_M2": M2.shape,
        "dim_A_eval": A_eval.shape,
        "dim_C2": C2.shape,
        "spectral_radius_M1": spectral_radius_M1,
        "spectral_radius_C2": spectral_radius_C2,
        "norm_M1": norm_M1,
        "norm_A_eval": norm_A_eval,
        "norm_C2": norm_C2,
        "cond_M1": cond_M1,
        "nnz_A_eval": nnz_A_eval,
        "sparsity_A_eval": sparsity_A_eval,
    }


def construct_level5_unitary_dilation(
    A_eval: np.ndarray, alpha: float = None
) -> Tuple[np.ndarray, float]:
    """
    Constructs 10-qubit Sz.-Nagy unitary dilation U_C in U(1024) of padded A_eval.
    
    Zero-pads A_eval (18 x 342) to A_pad (512 x 512 = 2^9) and embeds into 1024 x 1024 (2^10).
    """
    dim_target = 512  # 2^9
    A_pad = np.zeros((dim_target, dim_target), dtype=np.float64)
    A_pad[:18, :342] = A_eval

    if alpha is None:
        norm_A = float(la.norm(A_pad, 2))
        alpha = 1.01 * norm_A

    A_bar = A_pad / alpha

    # Sz.-Nagy dilation: U_C = [ A_bar, sqrt(I - A_bar A_bar^dagger) ]
    #                           [ sqrt(I - A_bar^dagger A_bar), -A_bar^dagger ]
    dim = dim_target
    I_dim = np.eye(dim, dtype=np.float64)

    D_A = I_dim - A_bar.T @ A_bar
    D_A_adj = I_dim - A_bar @ A_bar.T

    evals_A, V_A = la.eigh(D_A)
    sqrt_D_A = V_A @ np.diag(np.sqrt(np.maximum(evals_A, 0.0))) @ V_A.T

    evals_adj, V_adj = la.eigh(D_A_adj)
    sqrt_D_A_adj = V_adj @ np.diag(np.sqrt(np.maximum(evals_adj, 0.0))) @ V_adj.T

    U_C = np.zeros((2 * dim, 2 * dim), dtype=np.float64)
    U_C[:dim, :dim] = A_bar
    U_C[:dim, dim:] = sqrt_D_A_adj
    U_C[dim:, :dim] = sqrt_D_A
    U_C[dim:, dim:] = -A_bar.T

    return U_C, float(alpha)
