"""
Quantum Carleman Linearization Module for Two-Phase D2Q9 Lattice Boltzmann.

Mathematical Architecture:
1. State Vector: Psi = [f_0..f_8, g_0..g_8]^T in R^18
2. Quadratic Lift: Y_2 = [Psi; Psi (x) Psi] in R^342
3. Second-Order Truncated Polynomial Map:
   Psi' = M_1 Psi + M_2 (Psi (x) Psi) = A_eval Y_2
   where M_1 in R^(18 x 18), M_2 in R^(18 x 324), A_eval in R^(18 x 342)

Formulations:
- Formulation A (Observable-Evaluation / Hybrid Mode):
  Evaluates Psi' = A_eval Y_2 at each timestep and reconstructs Y_2 from measured physical state.
- Formulation B (Closed Autonomous Carleman Linear System):
  Evolves Y_{t+1} = C_2 Y_t where C_2 = [[M_1, M_2], [0, M_1 (x) M_1]] in R^(342 x 342).
  Characterizes truncation error E = ||Psi' (x) Psi' - (M_1 (x) M_1)(Psi (x) Psi)||.

10-Qubit Power-of-Two Unitary Dilation:
- Zero-pads A_eval in R^(18 x 342) to A_tilde in R^(512 x 512) (2^9)
- Normalizes A_bar = A_tilde / alpha (alpha = 1.01 * ||A_tilde||_2)
- Embeds into Sz.-Nagy Unitary Dilation U_C in U(1024 = 2^10) acting on 9 system qubits + 1 ancilla qubit
"""

import numpy as np
import scipy.linalg as la
from qiskit import QuantumCircuit
from qiskit.circuit.library import UnitaryGate
from classical.d2q9 import C_X, C_Y, W


def build_second_order_carleman_matrices(tau_f=0.8, tau_g=0.7, rho0=1.0):
    """
    Constructs the linear collision matrix M_1 and quadratic contraction tensor M_2.
    """
    from quantum.two_phase_carleman import (
        build_two_phase_linear_collision_matrix_18x18,
        build_two_phase_quadratic_collision_tensor_18x324
    )
    M1 = build_two_phase_linear_collision_matrix_18x18(tau_f=tau_f, tau_g=tau_g)
    M2 = build_two_phase_quadratic_collision_tensor_18x324(tau_f=tau_f, tau_g=tau_g, rho0=rho0)
    return M1, M2


def build_second_order_evaluation_operator(tau_f=0.8, tau_g=0.7, rho0=1.0):
    """
    Builds the rectangular step-evaluation operator A_eval = [M_1, M_2] in R^(18 x 342).
    """
    M1, M2 = build_second_order_carleman_matrices(tau_f, tau_g, rho0)
    A_eval = np.hstack([M1, M2])
    return A_eval


def lift_two_phase_state(f_node, g_node, order=2):
    """
    Constructs the polynomial lifted state vector Y_2 = [Psi; Psi (x) Psi] in R^342.
    """
    f_node = np.asarray(f_node, dtype=np.float64)
    g_node = np.asarray(g_node, dtype=np.float64)
    psi = np.concatenate([f_node, g_node]) # dim 18

    if order == 1:
        return psi
    elif order == 2:
        psi_psi = np.kron(psi, psi) # dim 324
        return np.concatenate([psi, psi_psi]) # dim 342
    else:
        raise ValueError("Only order 1 and 2 are currently supported.")


def build_closed_carleman_matrix(tau_f=0.8, tau_g=0.7, rho0=1.0):
    """
    Constructs the autonomous closed 2nd-order Carleman evolution matrix C_2 in R^(342 x 342):
    C_2 = [[M_1, M_2],
           [0,   M_1 (x) M_1]]
    """
    M1, M2 = build_second_order_carleman_matrices(tau_f, tau_g, rho0)
    dim1 = 18
    dim2 = 324
    total_dim = dim1 + dim2

    C2 = np.zeros((total_dim, total_dim), dtype=np.float64)
    C2[:dim1, :dim1] = M1
    C2[:dim1, dim1:] = M2
    C2[dim1:, dim1:] = np.kron(M1, M1)

    return C2


def analyze_carleman_truncation_error(f_node, g_node, tau_f=0.8, tau_g=0.7, rho0=1.0):
    """
    Compares Formulation A (exact re-lifted polynomial) vs Formulation B (closed Carleman matrix)
    and computes the quadratic truncation error E.
    """
    A_eval = build_second_order_evaluation_operator(tau_f, tau_g, rho0)
    C2 = build_closed_carleman_matrix(tau_f, tau_g, rho0)
    Y_in = lift_two_phase_state(f_node, g_node, order=2)

    # Formulation A
    psi_next_A = A_eval @ Y_in
    Y_next_exact = lift_two_phase_state(psi_next_A[:9], psi_next_A[9:18], order=2)

    # Formulation B
    Y_next_B = C2 @ Y_in
    psi_next_B = Y_next_B[:18]

    err_psi = np.linalg.norm(psi_next_A - psi_next_B)
    err_quadratic_layer = np.linalg.norm(Y_next_exact[18:] - Y_next_B[18:])

    return {
        "psi_A": psi_next_A,
        "psi_B": psi_next_B,
        "psi_difference": float(err_psi),
        "quadratic_layer_truncation_error": float(err_quadratic_layer),
        "recommendation": "Formulation A (Hybrid Re-lifting) preserves exact multi-step physics."
    }


def build_carleman_unitary_dilation(A_eval, target_dim=512):
    """
    Pads A_eval to target_dim x target_dim and constructs Sz.-Nagy unitary dilation U_C in U(2*target_dim).
    For target_dim = 512, U_C in U(1024) (10 qubits).
    """
    from quantum.unitary_dilation import pad_rectangular_operator, normalize_operator, build_unitary_dilation, verify_unitarity
    A_padded = pad_rectangular_operator(A_eval, target_dim=target_dim)
    A_scaled, alpha = normalize_operator(A_padded)
    U = build_unitary_dilation(A_scaled)
    is_unitary, err = verify_unitarity(U)
    return U, alpha, err


def build_carleman_collision_circuit(U_dilated, num_qubits=10):
    """
    Constructs the 10-qubit quantum collision circuit representing U_C.
    """
    qc = QuantumCircuit(num_qubits, name="QuantumCarlemanCollision")
    unitary_gate = UnitaryGate(U_dilated, label="Carleman_U_10Q", check_input=False)
    qc.append(unitary_gate, range(num_qubits))
    return qc
