#!/usr/bin/env python3
"""
Stage 9.12: Quantum Amplitude Estimation (QAE) Demonstration Circuit.
Demonstrates reflection oracle for global liquid mass estimation on 3 qubits.
"""
from qiskit import QuantumCircuit
import numpy as np

def build_qae_demo():
    # 2 system qubits + 1 QAE phase evaluation ancilla
    qc = QuantumCircuit(3, 1, name="QAE_Mass_Scalar")
    qc.h(range(3))
    # Grover reflection on target subspace
    qc.cx(0, 2)
    qc.cx(1, 2)
    qc.rz(np.pi / 4, 2)
    qc.cx(1, 2)
    qc.cx(0, 2)
    qc.h(2)
    qc.measure(2, 0)
    return qc

if __name__ == "__main__":
    qc = build_qae_demo()
    print("QAE Scalar Estimation Demo Circuit:")
    print(qc)
