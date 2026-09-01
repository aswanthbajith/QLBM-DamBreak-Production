#!/usr/bin/env python3
"""
Stage 9.12: Minimal Hardware-Safe Block-Encoding Demonstration Circuit.
Encodes a 2x2 local collision primitive into a 2-qubit exact unitary dilation U_A.
"""
import numpy as np
import scipy.linalg as la
from qiskit import QuantumCircuit
from qiskit.circuit.library import UnitaryGate

def build_2q_block_encoding():
    # 2x2 matrix representing local LBM relaxation primitive
    A = np.array([[0.85, 0.15], [0.10, 0.75]], dtype=np.complex128)
    U_svd, S, Vh = la.svd(A)
    alpha = max(float(S[0]) * 1.05, 1.0) # subnormalization
    
    A_norm = A / alpha
    S_clamped = np.clip(S / alpha, 0.0, 1.0)
    C = np.sqrt(np.maximum(0.0, 1.0 - S_clamped**2))
    
    top_right = U_svd * C[None, :]
    bot_left = C[:, None] * Vh
    bot_right = -np.diag(S_clamped)
    
    U_mat = np.block([[A_norm, top_right], [bot_left, bot_right]])
    
    # 2-qubit circuit: q0 = system, q1 = dilation ancilla
    qc = QuantumCircuit(2, name="Block_Enc_2Q")
    u_gate = UnitaryGate(U_mat, label="U_A")
    qc.append(u_gate, [0, 1])
    
    return qc, A, alpha, U_mat

if __name__ == "__main__":
    qc, A, alpha, U_mat = build_2q_block_encoding()
    print("Block Encoding 2Q Circuit:")
    print(qc)
    print(f"Alpha: {alpha:.4f} | Unitarity error: {np.max(np.abs(U_mat.conj().T @ U_mat - np.eye(4))):.2e}")
