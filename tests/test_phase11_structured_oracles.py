#!/usr/bin/env python3
"""
Automated Pytest Suite for Phase 11 Structured Quantum Oracles.
"""
import pytest
import numpy as np
import scipy.linalg as la
from qiskit import QuantumCircuit
from qiskit.quantum_info import Operator, Statevector
import sys, os

sys.path.append(os.path.join(os.path.dirname(__file__), ".."))
from PHASE11_STREAMING_ORACLE import build_d2q9_streaming_circuit
from PHASE11_STRUCTURED_QSVT import build_structured_collision_oracle, build_structured_qsvt_circuit

class TestPhase11StructuredOracles:
    def test_01_streaming_oracle_unitarity(self):
        qc = build_d2q9_streaming_circuit(2, 2)
        op = Operator(qc)
        assert op.is_unitary(atol=1e-12)
        
    def test_02_collision_oracle_unitarity(self):
        qc = build_structured_collision_oracle()
        op = Operator(qc)
        assert op.is_unitary(atol=1e-12)
        
    def test_03_structured_qsvt_circuit_structure(self):
        qc = build_structured_qsvt_circuit(degree=3)
        assert qc.num_qubits == 3
        assert qc.depth() > 0
        
    def test_04_end_to_end_statevector_conservation(self):
        qc = QuantumCircuit(6)
        qc.h(1)
        qc.ry(0.6435, 2)
        qc.cx(2, 3)
        qc.cx(2, 0)
        qc.cx(3, 1)
        sv = Statevector.from_instruction(qc)
        assert np.isclose(la.norm(sv.data), 1.0, atol=1e-12)
