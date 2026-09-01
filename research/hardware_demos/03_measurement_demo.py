#!/usr/bin/env python3
"""
Stage 9.11: Measurement Demonstration Circuit.
Adds explicit computational basis measurements to system and ancilla registers.
"""
from qiskit import QuantumCircuit
from qiskit.circuit.library import UnitaryGate
import numpy as np

def build_measured_circuit():
    qc = QuantumCircuit(2, 2, name="Measured_QSVT")
    qc.h(0)
    qc.cx(0, 1)
    qc.rz(0.5, 1)
    qc.cx(0, 1)
    qc.measure([0, 1], [0, 1])
    return qc

if __name__ == "__main__":
    qc = build_measured_circuit()
    print("Measured Circuit:")
    print(qc)
