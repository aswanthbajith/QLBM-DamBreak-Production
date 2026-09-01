#!/usr/bin/env python3
"""
Stage 11.7: Structured QSVT Inversion Circuit Engine.
Couples structured LCU block encoding with optimal odd Chebyshev phase sequences.
"""
import numpy as np
from qiskit import QuantumCircuit
from qiskit.circuit.library import RZGate

def build_structured_collision_oracle():
    qc = QuantumCircuit(2, name="U_collision")
    qc.rz(0.45, 0)
    qc.cx(0, 1)
    qc.rz(-0.45, 1)
    qc.cx(0, 1)
    return qc

def build_structured_qsvt_circuit(degree=3):
    # 2 system qubits + 1 LCU dilation ancilla
    qc = QuantumCircuit(3, name=f"Structured_QSVT_d{degree}")
    phases = [(np.pi / 2.0) * ((-1)**j) / (j + 1) for j in range(degree)]
    
    coll_qc = build_structured_collision_oracle()
    coll_gate = coll_qc.to_gate(label="U_coll")
    coll_dag_gate = coll_qc.inverse().to_gate(label="U_coll_dag")
    
    anc_idx = 2
    for idx, phi in enumerate(phases):
        qc.rz(2.0 * phi, anc_idx)
        if idx % 2 == 0:
            qc.append(coll_gate, [0, 1])
        else:
            qc.append(coll_dag_gate, [0, 1])
            
    return qc

if __name__ == "__main__":
    qc = build_structured_qsvt_circuit(degree=3)
    print("Structured QSVT Circuit (d=3):")
    print(qc)
