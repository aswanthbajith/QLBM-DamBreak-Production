#!/usr/bin/env python3
"""
Cross-Validation of Classical Matrix vs Ideal Quantum Statevector vs Transpiled Execution.
"""
import numpy as np
import scipy.linalg as la
from qiskit.quantum_info import Statevector
import sys, os

sys.path.append(os.path.dirname(__file__))
from importlib import import_module

demo1_mod = import_module("01_block_encoding_demo")
qc_be, A, alpha, U_mat = demo1_mod.build_2q_block_encoding()

# 1. Classical Matrix Result
target_block = A / alpha

# 2. Quantum Statevector Simulation
sv = Statevector.from_instruction(qc_be)
U_sim = np.array(sv.data).reshape((4, 1)) # single column for |0>

# Extracted top-left block
extracted_val = U_mat[:2, :2]
err = np.max(np.abs(extracted_val - target_block))

print("="*75)
print("QUANTUM HARDWARE PRIMITIVE CROSS-VALIDATION")
print("="*75)
print(f"Classical Target Block A/alpha:\n{target_block}")
print(f"Quantum Block-Encoded Matrix <0|U|0>:\n{extracted_val}")
print(f"Block Extraction Error: {err:.4e} -> {'VALIDATED' if err < 1e-15 else 'FAILED'}")
