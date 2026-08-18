#!/usr/bin/env python3
"""
Unit Tests for Step 9: QSVT Polynomial Inversion & Circuit Sequence.
"""

import sys
import os
sys.path.append(os.path.join(os.path.dirname(__file__), '../quantum'))

import unittest
import numpy as np
from carleman_lbm import CarlemanTwoPhaseLBM
from qsvt_solver import QSVTSolver

class TestQSVT(unittest.TestCase):
    def setUp(self):
        self.c_model = CarlemanTwoPhaseLBM(nx=1, ny=1, truncation_order=1)
        self.A = self.c_model.A_C.toarray()
        dim = self.A.shape[0]
        self.M = np.eye(dim) + 0.1 * self.A
        self.b = np.ones(dim)

    def test_01_polynomial_boundedness(self):
        """Verify that QSVT polynomial satisfies |P(x)| <= 1.0."""
        qsvt = QSVTSolver(self.M, self.b, degree=15)
        x_eval = np.linspace(-1.0, 1.0, 500)
        p_vals = np.polynomial.chebyshev.chebval(x_eval, qsvt.poly_coeffs)
        max_val = np.max(np.abs(p_vals))
        self.assertLessEqual(max_val, 1.0, "Polynomial must be bounded by 1 for unitary QSVT")

    def test_02_circuit_structure(self):
        """Verify Qiskit QSVT circuit depth and qubit allocations."""
        qsvt = QSVTSolver(self.M, self.b, degree=15)
        self.assertEqual(qsvt.circuit.num_qubits, qsvt.total_qubits)
        self.assertGreater(len(qsvt.circuit.data), 10)

if __name__ == "__main__":
    unittest.main()
