#!/usr/bin/env python3
"""
Stage 9.11: Small 4-Qubit QLBM State Preparation Circuit.
Encodes 2-node sub-volume density distributions into a 4-qubit normalized state.
"""
import numpy as np
from qiskit import QuantumCircuit

def build_small_qlbm_state():
    # 16-element statevector (4 qubits)
    vec = np.zeros(16, dtype=np.complex128)
    vec[0] = 0.5  # node 0 liquid
    vec[1] = 0.5  # node 0 gas
    vec[8] = 0.5  # node 1 liquid
    vec[9] = 0.5  # node 1 gas
    vec = vec / np.linalg.norm(vec)
    
    qc = QuantumCircuit(4, name="Small_QLBM_State")
    qc.initialize(vec, range(4))
    return qc

if __name__ == "__main__":
    qc = build_small_qlbm_state()
    print("4-Qubit State Preparation Circuit:")
    print(qc)
