#!/usr/bin/env python3
"""
Unit Tests for Step 9: End-to-End Quantum Linear System Solver.
"""

import sys
import os
sys.path.append(os.path.join(os.path.dirname(__file__), '../quantum'))

import unittest
import numpy as np
from carleman_lbm import CarlemanTwoPhaseLBM
from qsvt_solver import QSVTSolver

class TestQuantumSolver(unittest.TestCase):
    def setUp(self):
        self.c_model = CarlemanTwoPhaseLBM(nx=2, ny=1, truncation_order=1)
        self.A = self.c_model.A_C.toarray()
        dim = self.A.shape[0]
        self.M = np.eye(dim) + 0.1 * self.A
        np.random.seed(123)
        self.b = np.random.randn(dim)

    def test_01_high_fidelity_solve(self):
        """Verify that QSVT solver achieves fidelity > 0.99 with direct classical solve."""
        qsvt = QSVTSolver(self.M, self.b, degree=15)
        res = qsvt.solve()
        self.assertGreater(res['fidelity'], 0.99, f"Fidelity {res['fidelity']:.6f} must exceed 0.99")

    def test_02_residual_bound(self):
        """Verify that QSVT linear residual is bounded below 1e-3."""
        qsvt = QSVTSolver(self.M, self.b, degree=15)
        res = qsvt.solve()
        self.assertLess(res['residual'], 1e-3, f"Residual {res['residual']:.2e} must be < 1e-3")

if __name__ == "__main__":
    unittest.main()
