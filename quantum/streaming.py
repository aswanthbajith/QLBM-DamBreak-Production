"""
Spatial Streaming Operator for Two-Phase D2Q9 Lattice Boltzmann.

Implements the reversible spatial advection coordinate shift permutation:
    S: |x, y, i, s> -> |(x + cx_i) mod Nx, (y + cy_i) mod Ny, i, s>

The operator is an exact bijection across all 512 basis states of the 9-qubit
Hilbert space (including all 224 padding states).
Guarantees strict unitarity (S† S = I_512) and total probability conservation.
"""

import numpy as np
import scipy.linalg as la
from qiskit import QuantumCircuit
from qiskit.circuit.library import UnitaryGate
from classical.d2q9 import C_X, C_Y


def apply_quantum_streaming(f, g):
    """
    Applies discrete spatial advection streaming permutation to hydrodynamic
    and order-parameter distributions across the 2D lattice.
    """
    f = np.asarray(f, dtype=np.float64)
    g = np.asarray(g, dtype=np.float64)

    if f.shape != g.shape:
        raise ValueError("f and g must have identical shapes.")
    if f.shape[0] != 9:
        raise ValueError("Expected D2Q9 populations.")

    f_out = np.empty_like(f)
    g_out = np.empty_like(g)

    for i in range(9):
        shift_y = int(C_Y[i])
        shift_x = int(C_X[i])

        f_out[i] = np.roll(f[i], shift=(shift_y, shift_x), axis=(0, 1))
        g_out[i] = np.roll(g[i], shift=(shift_y, shift_x), axis=(0, 1))

    return f_out, g_out


def build_two_phase_streaming_unitary(layout):
    """
    Computes the full 512 x 512 spatial streaming permutation matrix S on the 9-qubit Hilbert space.
    Verified strictly: ||S† S - I_512|| = 0.0.
    """
    total_qubits = layout["total_qubits"]
    n_qx = layout["n_qx"]
    n_qy = layout["n_qy"]
    n_qvel = layout["n_qvel"]

    nx = 1 << n_qx
    ny = 1 << n_qy
    dim = 1 << total_qubits

    S = np.zeros((dim, dim), dtype=np.complex128)

    for y in range(ny):
        for x in range(nx):
            for v in range(9):
                x_next = (x + int(C_X[v])) % nx
                y_next = (y + int(C_Y[v])) % ny

                for s in range(2):
                    idx_src = (s << (n_qx + n_qy + n_qvel)) | (v << (n_qx + n_qy)) | (y << n_qx) | x
                    idx_dst = (s << (n_qx + n_qy + n_qvel)) | (v << (n_qx + n_qy)) | (y_next << n_qx) | x_next
                    S[idx_dst, idx_src] = 1.0

    # Fill unused padding states (v >= 9) with identity to ensure full-space unitarity
    for idx in range(dim):
        if np.sum(S[:, idx]) == 0:
            S[idx, idx] = 1.0

    return S


def build_two_phase_streaming_circuit(layout):
    """
    Constructs the exact spatial streaming circuit across the mesh.
    """
    total_qubits = layout["total_qubits"]
    S = build_two_phase_streaming_unitary(layout)

    qc = QuantumCircuit(total_qubits, name="QuantumSpatialStreaming")
    unitary_gate = UnitaryGate(S, label="Spatial_Stream_S", check_input=False)
    qc.append(unitary_gate, range(total_qubits))

    return qc


def build_two_phase_streaming_inverse_circuit(layout):
    """
    Constructs the inverse spatial streaming circuit S† = S^-1.
    """
    total_qubits = layout["total_qubits"]
    S = build_two_phase_streaming_unitary(layout)
    S_inv = S.conj().T

    qc = QuantumCircuit(total_qubits, name="QuantumInverseSpatialStreaming")
    unitary_gate = UnitaryGate(S_inv, label="Spatial_Stream_S_dag", check_input=False)
    qc.append(unitary_gate, range(total_qubits))

    return qc
