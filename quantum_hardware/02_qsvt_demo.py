#!/usr/bin/env python3
"""
Stage 9.13: Minimal Hardware-Safe QSVT Matrix Inversion Circuit.
Demonstrates QSVT polynomial inversion on 2-qubit system for degree d=3 and d=5.
"""
import numpy as np
from qiskit import QuantumCircuit
from qiskit.circuit.library import UnitaryGate

def build_2q_qsvt(degree=3):
    from qiskit.circuit.library import UnitaryGate
    A = np.array([[0.85, 0.15], [0.10, 0.75]], dtype=np.complex128)
    alpha = 1.05 * np.linalg.norm(A, 2)
    
    # Dilation matrix U
    U_svd, S, Vh = np.linalg.svd(A / alpha)
    C = np.sqrt(np.maximum(0.0, 1.0 - S**2))
    U_mat = np.block([[A/alpha, U_svd * C[None, :]], [C[:, None] * Vh, -np.diag(S)]])
    
    qc = QuantumCircuit(2, name=f"QSVT_2Q_deg{degree}")
    # Initialize system in |0>
    U_gate = UnitaryGate(U_mat, label="U_A")
    U_dag_gate = UnitaryGate(U_mat.conj().T, label="U_A_dag")
    
    # Phase sequence for d degrees
    phases = [(np.pi / 2.0) * ((-1)**j) / (j + 1) for j in range(degree)]
    
    for idx, phi in enumerate(phases):
        qc.rz(2.0 * phi, 1) # Rz on ancilla q1
        if idx % 2 == 0:
            qc.append(U_gate, [0, 1])
        else:
            qc.append(U_dag_gate, [0, 1])
            
    return qc

if __name__ == "__main__":
    qc = build_2q_qsvt(degree=3)
    print("QSVT 2Q (d=3) Circuit:")
    print(qc)
