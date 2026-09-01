#!/usr/bin/env python3
"""
Automated Pytest Suite for Phase 13 Quantum Hardware Validation.
"""
import pytest
import numpy as np
import scipy.linalg as la
from qiskit import QuantumCircuit, transpile
from qiskit.quantum_info import Operator, Statevector
from qiskit.providers.fake_provider import GenericBackendV2
import sys, os

sys.path.append(os.path.join(os.path.dirname(__file__), ".."))
from PHASE11_STREAMING_ORACLE import build_d2q9_streaming_circuit
from PHASE11_STRUCTURED_QSVT import build_structured_collision_oracle, build_structured_qsvt_circuit

backend = GenericBackendV2(num_qubits=127)

class TestPhase13Hardware:
    def test_01_primary_2x2_qlbm_circuit(self):
        qc = QuantumCircuit(6)
        qc.h(1)
        qc.ry(0.6435, 2)
        qc.cx(2, 3)
        qc.rz(0.45, 3)
        qc.cx(2, 3)
        qc.cx(2, 0)
        qc.cx(3, 1)
        t_qc = transpile(qc, backend=backend, optimization_level=2)
        assert t_qc.num_qubits == 127
        assert t_qc.depth() <= 15
        ops = t_qc.count_ops()
        assert ops.get("cx", 0) <= 6

    def test_02_structured_streaming_unitarity(self):
        qc = build_d2q9_streaming_circuit(2, 2)
        op = Operator(qc)
        assert op.is_unitary(atol=1e-12)

    def test_03_structured_collision_unitarity(self):
        qc = build_structured_collision_oracle()
        op = Operator(qc)
        assert op.is_unitary(atol=1e-12)

    def test_04_qsvt_circuit_validity(self):
        qc = build_structured_qsvt_circuit(3)
        assert qc.num_qubits == 3
        assert qc.depth() > 0
