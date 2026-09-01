"""
Two-Phase Coupled Carleman Linearization Module for D2Q9 Dam-Break Hydrodynamics.

Couples hydrodynamic populations f and phase-order populations g:
Psi = [ f0..f8, g0..g8 ] in R^18

Second-Order Lifted Carleman state:
Y_2 = [ Psi; Psi (x) Psi ] in R^(18 + 324) = R^342
"""
import numpy as np
import scipy.linalg as la
from classical.d2q9 import C_X, C_Y, W


def build_two_phase_carleman_basis(order=2):
    """
    Returns basis dimensions for two-phase Carleman lifting.
    Linear base: 18
    Order 2: 18 + 324 = 342
    """
    dim_base = 18
    if order == 1:
        return {"dim_base": 18, "order": 1, "layer_dims": [18], "total_dim": 18}
    elif order == 2:
        return {"dim_base": 18, "order": 2, "layer_dims": [18, 324], "total_dim": 342}
    else:
        raise ValueError(f"Unsupported order: {order}")


def build_two_phase_linear_collision_matrix_18x18(tau_f=0.8, tau_g=0.7):
    """
    Builds the 18x18 linear collision matrix M1 for coupled (f, g):
    M1 = block_diag(M1_f, M1_g)
    """
    omega_f = 1.0 / tau_f
    omega_g = 1.0 / tau_g
    
    # 1. Hydrodynamic linear part (f)
    M1_f = np.zeros((9, 9), dtype=np.float64)
    for i in range(9):
        for j in range(9):
            ci_dot_cj = C_X[i] * C_X[j] + C_Y[i] * C_Y[j]
            linear_eq = W[i] * (1.0 + 3.0 * ci_dot_cj)
            M1_f[i, j] = omega_f * linear_eq
            if i == j:
                M1_f[i, j] += (1.0 - omega_f)
                
    # 2. Phase-field linear part (g)
    # g_eq = w_i * phi * (1 + 3 (c_i . u)) -> linear part is w_i * phi = w_i * sum_j g_j
    M1_g = np.zeros((9, 9), dtype=np.float64)
    for i in range(9):
        for j in range(9):
            M1_g[i, j] = omega_g * W[i]
            if i == j:
                M1_g[i, j] += (1.0 - omega_g)
                
    M1 = np.zeros((18, 18), dtype=np.float64)
    M1[:9, :9] = M1_f
    M1[9:, 9:] = M1_g
    return M1


def build_two_phase_quadratic_collision_tensor_18x324(tau_f=0.8, tau_g=0.7, rho0=1.0):
    """
    Builds the 18x324 quadratic contraction tensor M2:
    Contracts Psi (x) Psi in R^324 into R^18.
    
    1. Hydrodynamic convective flux:
       Q_i(f) = omega_f * w_i / rho0 * [ 9/2 (c_i.j)^2 - 3/2 |j|^2 ]
    2. Phase-field advective flux:
       A_i(f, g) = omega_g * w_i / rho0 * [ 3 phi (c_i.j) ]
       where phi = sum_q1 g_q1 and j = sum_q2 c_q2 f_q2
    """
    omega_f = 1.0 / tau_f
    omega_g = 1.0 / tau_g
    cs2 = 1.0 / 3.0
    cs4 = 1.0 / 9.0
    
    M2 = np.zeros((18, 324), dtype=np.float64)
    
    # 1. Hydrodynamic block (rows 0..8)
    for i in range(9):
        wi = W[i]
        for q1 in range(9): # f index
            for q2 in range(9): # f index
                c1_dot_ci = C_X[q1] * C_X[i] + C_Y[q1] * C_Y[i]
                c2_dot_ci = C_X[q2] * C_X[i] + C_Y[q2] * C_Y[i]
                c1_dot_c2 = C_X[q1] * C_X[q2] + C_Y[q1] * C_Y[q2]
                
                term_conv = (c1_dot_ci * c2_dot_ci) / (2.0 * cs4)
                term_trace = c1_dot_c2 / (2.0 * cs2)
                
                coeff = (omega_f * wi / rho0) * (term_conv - term_trace)
                col = q1 * 18 + q2 # in Psi(18) (x) Psi(18)
                M2[i, col] = coeff
                
    # 2. Phase-field advection block (rows 9..17)
    # A_i = 3 omega_g w_i / rho0 * (c_i . j) * phi
    # phi = sum_q1 g_q1 (index 9 + q1), j = sum_q2 c_q2 f_q2 (index q2)
    for i in range(9):
        wi = W[i]
        for q1 in range(9): # g index (9 + q1 in Psi)
            for q2 in range(9): # f index (q2 in Psi)
                ci_dot_c2 = C_X[i] * C_X[q2] + C_Y[i] * C_Y[q2]
                coeff = (omega_g * wi / rho0) * (3.0 * ci_dot_c2)
                
                # Ordered pair (9 + q1, q2)
                col = (9 + q1) * 18 + q2
                M2[9 + i, col] = coeff
                
    return M2


def build_two_phase_carleman_operator(tau_f=0.8, tau_g=0.7, rho0=1.0, order=2):
    """
    Assembles the complete 342x342 block upper-triangular Carleman matrix C_2.
    """
    M1 = build_two_phase_linear_collision_matrix_18x18(tau_f=tau_f, tau_g=tau_g)
    
    if order == 1:
        return M1
        
    elif order == 2:
        M2 = build_two_phase_quadratic_collision_tensor_18x324(tau_f=tau_f, tau_g=tau_g, rho0=rho0)
        M1_kron2 = np.kron(M1, M1) # 324 x 324
        
        dim_total = 18 + 324
        C2 = np.zeros((dim_total, dim_total), dtype=np.float64)
        C2[:18, :18] = M1
        C2[:18, 18:] = M2
        C2[18:, 18:] = M1_kron2
        return C2
        
    else:
        raise ValueError(f"Unsupported order: {order}")


def lift_two_phase_state(f, g, order=2):
    """
    Lifts hydrodynamic f (9,) and phase g (9,) to Carleman state Y:
    Order 1: Psi = [f; g] in R^18
    Order 2: Y = [Psi; Psi (x) Psi] in R^342
    """
    f = np.asarray(f, dtype=np.float64).ravel()
    g = np.asarray(g, dtype=np.float64).ravel()
    Psi = np.concatenate([f, g])
    
    if order == 1:
        return Psi
    elif order == 2:
        Psi_kron2 = np.kron(Psi, Psi)
        return np.concatenate([Psi, Psi_kron2])
    else:
        raise ValueError(f"Unsupported order: {order}")


def project_two_phase_state(Y, order=2):
    """
    Projects lifted Carleman state Y back to physical populations f (9,) and g (9,).
    """
    Psi = np.asarray(Y, dtype=np.float64)[:18]
    f = Psi[:9].copy()
    g = Psi[9:].copy()
    return f, g


def apply_two_phase_carleman(f, g, C_op, order=2):
    """
    Applies the two-phase Carleman operator to local populations (f, g).
    """
    Y = lift_two_phase_state(f, g, order=order)
    Y_next = C_op @ Y
    return project_two_phase_state(Y_next, order=order)
