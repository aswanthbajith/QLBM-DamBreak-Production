#!/usr/bin/env python3
"""
Unit Tests for Step 9: Quantum Block Encoding Module.
"""

import sys
import os
sys.path.append(os.path.join(os.path.dirname(__file__), '../quantum'))

import unittest
import numpy as np
import scipy.linalg as la
from qiskit.quantum_info import Operator
from block_encoding import QuantumBlockEncoding
from carleman_lbm import CarlemanTwoPhaseLBM

class TestBlockEncoding(unittest.TestCase):
    def setUp(self):
        self.c_model = CarlemanTwoPhaseLBM(nx=2, ny=1, truncation_order=1)
        self.A = self.c_model.A_C.toarray()
        self.be = QuantumBlockEncoding(self.A)

    def test_01_dilation_unitarity(self):
        """Verify that dilated operator U_A is strictly unitary (U_A^dag * U_A = I)."""
        U = self.be.U_matrix
        dim = U.shape[0]
        identity = np.eye(dim, dtype=np.complex128)
        diff = U.conj().T @ U - identity
        err = la.norm(diff, 2)
        self.assertLess(err, 1e-14, "Dilated operator must be unitary within 1e-14")

    def test_02_block_encoding_accuracy(self):
        """Verify that top-left block reproduces A / alpha to machine precision."""
        res = self.be.verify_encoding()
        self.assertLess(res['linf_error'], 1e-14)
        self.assertLess(res['frob_error'], 1e-14)

    def test_03_qiskit_circuit_operator(self):
        """Verify that Qiskit QuantumCircuit operator matches dilated matrix U_A."""
        op = Operator(self.be.circuit)
        u_sim = op.data
        diff = la.norm(u_sim - self.be.U_matrix, 2)
        self.assertLess(diff, 1e-14)

if __name__ == "__main__":
    unittest.main()
