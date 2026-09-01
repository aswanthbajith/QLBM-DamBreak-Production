"""
Local Carleman Linearization Module for D2Q9 Lattice Boltzmann Collision.

Transforms the nonlinear BGK collision operator into an enlarged linear system:
Y(t+1) = C_CL * Y(t)

Supported truncation orders:
- Order 1: Linear BGK (dim = 9)
- Order 2: Complete Quadratic Carleman (dim = 9 + 81 = 90)
- Order 3: Cubic Carleman (dim = 9 + 81 + 729 = 819)
"""
import numpy as np
import scipy.linalg as la
from classical.d2q9 import C_X, C_Y, W


def build_carleman_basis(dim_base=9, order=2):
    """
    Returns the basis configuration and dimensions for the given truncation order.
    """
    dims = [dim_base**k for k in range(1, order + 1)]
    total_dim = sum(dims)
    return {
        "dim_base": dim_base,
        "order": order,
        "layer_dims": dims,
        "total_dim": total_dim
    }


def build_local_linear_collision_matrix_9x9(omega=1.25):
    """
    Builds the 9x9 linear part M1 of the BGK collision operator:
    (M1 f)_i = (1 - omega) f_i + omega * w_i * [ sum_j f_j + 3 * sum_j (c_i . c_j) f_j ]
    """
    M1 = np.zeros((9, 9), dtype=np.float64)
    for i in range(9):
        for j in range(9):
            ci_dot_cj = C_X[i] * C_X[j] + C_Y[i] * C_Y[j]
            linear_eq = W[i] * (1.0 + 3.0 * ci_dot_cj)
            M1[i, j] = omega * linear_eq
            if i == j:
                M1[i, j] += (1.0 - omega)
    return M1


def build_local_quadratic_collision_tensor_9x81(omega=1.25, rho0=1.0):
    """
    Builds the 9x81 quadratic contraction tensor M2:
    Contracts f (x) f in R^81 into R^9 representing convective flux:
    Q_i(f) = omega * w_i / rho0 * [ 9/2 (c_i.j)^2 - 3/2 |j|^2 ]
    """
    M2 = np.zeros((9, 81), dtype=np.float64)
    
    for i in range(9):
        wi = W[i]
        for q1 in range(9):
            for q2 in range(9):
                c1_dot_ci = C_X[q1] * C_X[i] + C_Y[q1] * C_Y[i]
                c2_dot_ci = C_X[q2] * C_X[i] + C_Y[q2] * C_Y[i]
                c1_dot_c2 = C_X[q1] * C_X[q2] + C_Y[q1] * C_Y[q2]
                
                term_conv = 4.5 * (c1_dot_ci * c2_dot_ci)
                term_trace = 1.5 * c1_dot_c2
                
                coeff = (omega * wi / rho0) * (term_conv - term_trace)
                col = q1 * 9 + q2
                M2[i, col] = coeff
                
    return M2


def build_local_carleman_operator(omega=1.25, rho0=1.0, order=2):
    """
    Assembles the block upper-triangular Carleman matrix C_CL for local D2Q9 collision.
    For Order 1: C = M1 in R^(9x9)
    For Order 2: C = [[ M1, M2 ], [ 0, M1 (x) M1 ]] in R^(90x90)
    For Order 3: C in R^(819x819)
    """
    M1 = build_local_linear_collision_matrix_9x9(omega=omega)
    
    if order == 1:
        return M1
        
    elif order == 2:
        M2 = build_local_quadratic_collision_tensor_9x81(omega=omega, rho0=rho0)
        M1_kron2 = np.kron(M1, M1) # 81 x 81
        
        dim_total = 9 + 81
        C2 = np.zeros((dim_total, dim_total), dtype=np.float64)
        C2[:9, :9] = M1
        C2[:9, 9:] = M2
        C2[9:, 9:] = M1_kron2
        return C2
        
    elif order == 3:
        M2 = build_local_quadratic_collision_tensor_9x81(omega=omega, rho0=rho0)
        M1_kron2 = np.kron(M1, M1) # 81 x 81
        M1_kron3 = np.kron(M1, M1_kron2) # 729 x 729
        
        M2_kron_I = np.kron(M2, np.eye(9)) # 81 x 729
        
        dim_total = 9 + 81 + 729
        C3 = np.zeros((dim_total, dim_total), dtype=np.float64)
        C3[:9, :9] = M1
        C3[:9, 9:90] = M2
        C3[9:90, 9:90] = M1_kron2
        C3[9:90, 90:] = M2_kron_I
        C3[90:, 90:] = M1_kron3
        return C3
        
    else:
        raise ValueError(f"Unsupported Carleman order: {order}")


def lift_state(f, order=2):
    """
    Lifts 9-population vector f to Carleman state Y:
    Order 1: Y = f (dim 9)
    Order 2: Y = [f; f (x) f] (dim 90)
    Order 3: Y = [f; f (x) f; f (x) f (x) f] (dim 819)
    """
    f = np.asarray(f, dtype=np.float64).ravel()
    if order == 1:
        return f.copy()
    elif order == 2:
        f_kron2 = np.kron(f, f)
        return np.concatenate([f, f_kron2])
    elif order == 3:
        f_kron2 = np.kron(f, f)
        f_kron3 = np.kron(f, f_kron2)
        return np.concatenate([f, f_kron2, f_kron3])
    else:
        raise ValueError(f"Unsupported Carleman order: {order}")


def project_state(Y, order=2):
    """
    Projects lifted Carleman state Y back to physical 9-population state f.
    """
    return np.asarray(Y, dtype=np.float64)[:9].copy()


def apply_carleman_operator(f, C_op, order=2):
    """
    Applies the Carleman linear operator to population f:
    f_next = project( C_op * lift(f) )
    """
    Y = lift_state(f, order=order)
    Y_next = C_op @ Y
    return project_state(Y_next, order=order)
