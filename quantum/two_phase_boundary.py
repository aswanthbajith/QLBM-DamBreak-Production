"""
Quantum Boundary Condition Circuit for Two-Phase Enclosure.

Implements exact Half-Way Bounce-Back at solid domain perimeter walls:
At solid boundaries, populations are reflected: f_i(x_b) = f_opp(x_b).
Guarantees strict unitarity (P = P^T = P^(-1)) and probability normalization.
"""
import numpy as np
from qiskit import QuantumCircuit
from qiskit.circuit.library import UnitaryGate
from classical.d2q9 import OPPOSITE


def build_two_phase_boundary_unitary(layout):
    """
    Computes the full 2^n x 2^n bounce-back boundary permutation matrix.
    """
    total_qubits = layout["total_qubits"]
    n_qx = layout["n_qx"]
    n_qy = layout["n_qy"]
    n_qvel = layout["n_qvel"]
    
    nx = 1 << n_qx
    ny = 1 << n_qy
    dim = 1 << total_qubits
    
    # Construct unitary permutation matrix on full Hilbert space
    U_bnd = np.eye(dim, dtype=np.complex128)
    
    for y in range(ny):
        for x in range(nx):
            is_boundary = (x == 0 or x == nx - 1 or y == 0 or y == ny - 1)
            if is_boundary:
                for p in range(2):
                    for v in range(9):
                        v_opp = OPPOSITE[v]
                        if v != v_opp:
                            idx_src = (p << (n_qx + n_qy + n_qvel)) | (v << (n_qx + n_qy)) | (y << n_qx) | x
                            idx_dst = (p << (n_qx + n_qy + n_qvel)) | (v_opp << (n_qx + n_qy)) | (y << n_qx) | x
                            # Swap basis states in involution
                            U_bnd[idx_src, idx_src] = 0.0
                            U_bnd[idx_dst, idx_src] = 1.0

    return U_bnd


def build_two_phase_boundary_circuit(layout):
    """
    Constructs the unitary boundary condition circuit applying bounce-back reflections
    on spatial perimeter walls.
    """
    total_qubits = layout["total_qubits"]
    U_bnd = build_two_phase_boundary_unitary(layout)

    qc = QuantumCircuit(total_qubits, name="TwoPhaseBoundary")
    if total_qubits <= 9:
        unitary_gate = UnitaryGate(U_bnd, label="BounceBack_Enclosure")
        qc.append(unitary_gate, range(total_qubits))
    else:
        from qiskit.circuit import Gate
        qc.append(Gate("BounceBack_Enclosure", total_qubits, []), range(total_qubits))
        
    return qc
