"""
Quantum Collision Operator for Reduced Two-Phase Lattice Boltzmann.

Provides two mathematically grounded collision constructions:
1. Static Unitary (Polar SVD Projection): For single-step / short-time NISQ circuits.
2. State-Dependent Adaptive Unitary (Exact Subspace Rotation): For multi-step exact non-linear BGK relaxation.
"""
import numpy as np
import scipy.linalg as la
from qiskit import QuantumCircuit
from qiskit.circuit.library import UnitaryGate
from classical.d2q9 import W, C_X, C_Y
from classical.equilibrium import compute_equilibrium


def get_bgk_collision_unitary_16x16(omega=1.25, dt=0.5):
    """
    Computes 16x16 unitary matrix representation of D2Q9 BGK relaxation on 4 velocity qubits
    using polar factor SVD decomposition for unconditional numerical stability across all omega.
    """
    # 9x9 Linear BGK matrix
    M = (1.0 - omega) * np.eye(9, dtype=np.complex128) + omega * np.outer(W, np.ones(9))
    
    # SVD polar factor: M = U Sigma V^H -> Unitary V_unit = U V^H
    u_svd, _, vh_svd = la.svd(M)
    U9 = u_svd @ vh_svd
    
    # Fractional power via Schur / Eigendecomposition with explicit re-unitarization
    if dt != 1.0:
        T, Z = la.schur(U9, output='complex')
        diag_T = np.diag(T)
        phases = np.angle(diag_T)
        T_dt = np.diag(np.exp(1j * phases * dt))
        U9 = Z @ T_dt @ Z.conj().T
        # Final SVD projection ensures strict machine-precision unitarity
        u_svd, _, vh_svd = la.svd(U9)
        U9 = u_svd @ vh_svd
    
    U16 = np.eye(16, dtype=np.complex128)
    U16[:9, :9] = U9
    return U16


def build_two_phase_collision_unitary(tau_liquid=0.8, tau_gas=0.65, dt=0.5):
    """
    Constructs the full 32x32 5-qubit unitary (4 velocity qubits + 1 phase qubit).
    """
    omega_l = 1.0 / tau_liquid
    omega_g = 1.0 / tau_gas
    
    U_liq = get_bgk_collision_unitary_16x16(omega=omega_l, dt=dt)
    U_gas = get_bgk_collision_unitary_16x16(omega=omega_g, dt=dt)
    
    dim_5q = 32
    U_combined = np.eye(dim_5q, dtype=np.complex128)
    U_combined[:16, :16] = U_gas
    U_combined[16:, 16:] = U_liq
    return U_combined


def build_node_adaptive_collision_unitary_9x9(f_in, rho, u, phi, tau_liquid=0.8, tau_gas=0.65):
    """
    Constructs an exact 9x9 unitary rotation for a single lattice node that maps
    amplitude state |psi_in> = sqrt(f_in/rho) to exact post-collision state |psi_out> = sqrt(f_star/rho).
    """
    omega = (1.0 / tau_liquid) if phi >= 0.5 else (1.0 / tau_gas)
    
    # Equilibrium populations
    f_eq = np.zeros(9)
    ux, uy = u[0], u[1]
    for i in range(9):
        c_dot_u = C_X[i] * ux + C_Y[i] * uy
        u_sq = ux**2 + uy**2
        f_eq[i] = W[i] * rho * (1.0 + 3.0 * c_dot_u + 4.5 * c_dot_u**2 - 1.5 * u_sq)
        
    f_star = (1.0 - omega) * f_in + omega * f_eq
    f_star = np.maximum(f_star, 1e-12)
    f_star = f_star * (rho / np.sum(f_star)) # preserve exact mass
    
    psi = np.sqrt(np.maximum(f_in, 0.0) / (rho + 1e-14))
    phi_vec = np.sqrt(np.maximum(f_star, 0.0) / (rho + 1e-14))
    
    psi_norm = np.linalg.norm(psi)
    phi_norm = np.linalg.norm(phi_vec)
    if psi_norm < 1e-12 or phi_norm < 1e-12:
        return np.eye(9, dtype=np.complex128)
        
    psi /= psi_norm
    phi_vec /= phi_norm
    
    cos_theta = float(np.dot(psi, phi_vec))
    if cos_theta > 0.99999999:
        return np.eye(9, dtype=np.complex128)
        
    v2 = phi_vec - cos_theta * psi
    v2_norm = np.linalg.norm(v2)
    if v2_norm < 1e-12:
        return np.eye(9, dtype=np.complex128)
    v2 /= v2_norm
    
    theta = float(np.arccos(np.clip(cos_theta, -1.0, 1.0)))
    R2 = np.array([[np.cos(theta), -np.sin(theta)],
                   [np.sin(theta),  np.cos(theta)]], dtype=np.complex128)
    
    P_sub = np.column_stack((psi, v2))
    U_node = np.eye(9, dtype=np.complex128) - P_sub @ P_sub.conj().T + P_sub @ R2 @ P_sub.conj().T
    
    # Ensure exact machine precision unitarity
    u_svd, _, vh_svd = la.svd(U_node)
    return u_svd @ vh_svd


def build_two_phase_collision_circuit(layout, tau_liquid=0.8, tau_gas=0.65, dt=0.5):
    """
    Builds the static two-phase collision circuit operating on velocity qubits
    conditioned by the phase qubit (liquid vs gas relaxation rates).
    """
    total_qubits = layout["total_qubits"]
    q_phase = layout["registers"]["phase"][0]
    q_vel = layout["registers"]["velocity"]
    
    U_combined = build_two_phase_collision_unitary(tau_liquid=tau_liquid, tau_gas=tau_gas, dt=dt)
    
    qc = QuantumCircuit(total_qubits, name="TwoPhaseCollision")
    gate_5q = UnitaryGate(U_combined, label="BGK_TwoPhase_Coll")
    
    # Target registers: [q_vel[0], q_vel[1], q_vel[2], q_vel[3], q_phase]
    target_qubits = q_vel + [q_phase]
    qc.append(gate_5q, target_qubits)
    
    return qc
