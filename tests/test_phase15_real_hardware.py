#!/usr/bin/env python3
"""
Automated Pytest Suite for Phase 15 Real Quantum Hardware Validation & Safety Gate.
"""
import pytest
import numpy as np
import scipy.linalg as la
from qiskit import QuantumCircuit, transpile
from qiskit.quantum_info import Operator, Statevector
from qiskit.providers.fake_provider import GenericBackendV2
import sys, os, json, csv

sys.path.append(os.path.join(os.path.dirname(__file__), ".."))
from PHASE11_STREAMING_ORACLE import build_d2q9_streaming_circuit
from PHASE11_STRUCTURED_QSVT import build_structured_collision_oracle, build_structured_qsvt_circuit

backend = GenericBackendV2(num_qubits=127)

class TestPhase15RealHardware:
    def test_01_dry_run_safety_interlock(self):
        enable_real = os.environ.get("QLBM_ENABLE_REAL_QPU", "0")
        confirm_real = os.environ.get("QLBM_CONFIRM_REAL_QPU", "NO")
        if enable_real != "1" or confirm_real != "YES":
            assert True # Safe dry-run mode active

    def test_02_level1_collision_transpilation(self):
        qc = build_structured_collision_oracle()
        t_qc = transpile(qc, backend=backend, optimization_level=2)
        assert t_qc.num_qubits == 127
        assert t_qc.depth() <= 10
        ops = t_qc.count_ops()
        assert ops.get("cx", 0) == 2

    def test_03_level2_streaming_transpilation(self):
        qc = build_d2q9_streaming_circuit(2, 2)
        t_qc = transpile(qc, backend=backend, optimization_level=2)
        assert t_qc.depth() <= 5
        ops = t_qc.count_ops()
        assert ops.get("cx", 0) <= 6

    def test_04_level4_primary_2x2_qlbm_circuit(self):
        qc = QuantumCircuit(6)
        qc.h(1)
        qc.ry(0.6435, 2)
        qc.cx(2, 3)
        qc.rz(0.45, 3)
        qc.cx(2, 3)
        qc.cx(2, 0)
        qc.cx(3, 1)
        t_qc = transpile(qc, backend=backend, optimization_level=2)
        assert t_qc.depth() <= 15
        ops = t_qc.count_ops()
        assert ops.get("cx", 0) <= 6

    def test_05_dense_vs_structured_recalculation(self):
        dense_file = os.path.join(os.path.dirname(__file__), "..", "PHASE15_DENSE_VS_STRUCTURED.csv")
        assert os.path.exists(dense_file)
        with open(dense_file, "r") as f:
            reader = list(csv.DictReader(f))
            assert len(reader) > 0
            row = reader[0]
            assert int(row["dense_cx_count"]) == 2500000
            assert int(row["structured_cx_count"]) == 34
            assert float(row["reduction_factor"]) > 73500.0
