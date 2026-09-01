"""
Quantum Gravitational Body Forcing Module for Two-Phase D2Q9 Lattice Boltzmann.

Mathematical Formulation:
Shan-Chen / Guo buoyancy forcing for two-phase fluid under gravity:
    Delta f_i(x, y) = 3 * w_i * (rho(x,y) - rho_gas) * g_acc * c_iy

Notice that for D2Q9:
- c_iy = +1 for i in {2, 5, 6} (North, North-East, North-West)
- c_iy = -1 for i in {4, 7, 8} (South, South-East, South-West)
- c_iy =  0 for i in {0, 1, 3} (Center, East, West)

Quantum Embedding Options:
1. Block-Encoded Affine Scaling / Shift Operator:
   Represented as a diagonal perturbation matrix D_force on the 512-dim state space
   where (I + Delta_F) is embedded into a unitary dilation U_force.
2. Direct Amplitude Perturbation / Hybrid Interface.
"""

import numpy as np
import scipy.linalg as la
from qiskit import QuantumCircuit
from qiskit.circuit.library import UnitaryGate
from classical.d2q9 import C_Y, W


def compute_buoyancy_force_increment(rho, g_acc=-0.001, rho_gas=0.1):
    """
    Computes delta f_i array of shape (9, ny, nx).
    """
    rho = np.asarray(rho, dtype=np.float64)
    ny, nx = rho.shape
    delta_f = np.zeros((9, ny, nx), dtype=np.float64)
    delta_rho = rho - rho_gas

    for i in range(9):
        delta_f[i] = 3.0 * W[i] * delta_rho * g_acc * C_Y[i]

    return delta_f


def apply_quantum_force(f, rho, u=None, g_acc=-0.001, rho_gas=0.1, tau_f=0.8):
    """
    Applies buoyancy forcing to hydrodynamic distribution f.
    g (phase field) is unaffected by gravitational buoyancy.
    """
    f_out = np.array(f, copy=True, dtype=np.float64)
    delta_f = compute_buoyancy_force_increment(rho, g_acc=g_acc, rho_gas=rho_gas)
    f_out += delta_f
    return f_out


def build_forcing_operator_matrix(rho, layout, g_acc=-0.001, rho_gas=0.1):
    """
    Builds the 512 x 512 linear operator F representing identity + buoyancy perturbation
    on the 9-qubit quantum state space.
    """
    total_qubits = layout["total_qubits"]
    n_qx = layout["n_qx"]
    n_qy = layout["n_qy"]
    n_qvel = layout["n_qvel"]
    nx = layout["nx"]
    ny = layout["ny"]
    dim = 1 << total_qubits

    F = np.eye(dim, dtype=np.complex128)
    delta_f = compute_buoyancy_force_increment(rho, g_acc=g_acc, rho_gas=rho_gas)

    for y in range(ny):
        for x in range(nx):
            for v in range(9):
                # Only hydrodynamic selector (s=0) is modified
                idx = (0 << (n_qx + n_qy + n_qvel)) | (v << (n_qx + n_qy)) | (y << n_qx) | x
                # Local scaling representation
                f_denom = max(float(rho[y, x]) * float(W[v]), 1e-12)
                scaling = 1.0 + delta_f[v, y, x] / f_denom
                F[idx, idx] = scaling

    return F


def build_forcing_unitary_dilation(F):
    """
    Constructs a 10-qubit Sz.-Nagy unitary dilation U_force in U(1024) for the forcing operator.
    """
    from quantum.unitary_dilation import normalize_operator, build_unitary_dilation, verify_unitarity
    F_scaled, alpha_force = normalize_operator(F)
    U_force = build_unitary_dilation(F_scaled)
    is_unitary, err = verify_unitarity(U_force)
    return U_force, alpha_force, err


def build_forcing_circuit(U_force, num_qubits=10):
    """
    Constructs the 10-qubit quantum circuit applying U_force.
    """
    qc = QuantumCircuit(num_qubits, name="QuantumBuoyancyForcing")
    gate = UnitaryGate(U_force, label="Forcing_U_10Q", check_input=False)
    qc.append(gate, range(num_qubits))
    return qc
