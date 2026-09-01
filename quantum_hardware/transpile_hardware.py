#!/usr/bin/env python3
"""
Transpilation Tool for Quantum Hardware Deployment on IBM Eagle/Heron.
"""
from qiskit import transpile
from qiskit.providers.fake_provider import GenericBackendV2
import sys, os

sys.path.append(os.path.dirname(__file__))
from importlib import import_module

demo1 = import_module("01_block_encoding_demo").build_2q_block_encoding()[0]
demo2 = import_module("02_qsvt_demo").build_2q_qsvt(degree=3)
demo3 = import_module("03_measurement_demo").build_measured_circuit()
demo5 = import_module("05_qae_scalar_demo").build_qae_demo()

backend = GenericBackendV2(num_qubits=127)

circuits = [
    ("01_Block_Encoding_2Q", demo1),
    ("02_QSVT_2Q_deg3", demo2),
    ("03_Measurement_Demo", demo3),
    ("05_QAE_Mass_Scalar", demo5)
]

print("="*75)
print("TRANSPILING DEMONSTRATION CIRCUITS TO 127Q HEAVY-HEX ARCHITECTURE")
print("="*75)

for name, qc in circuits:
    t_qc = transpile(qc, backend=backend, optimization_level=2)
    ops = t_qc.count_ops()
    cx_count = ops.get("cx", 0)
    print(f"Circuit: {name:<22} | Qubits: {qc.num_qubits:2d} | Depth: {t_qc.depth():3d} | CX: {cx_count:2d} | Ops: {dict(ops)}")
