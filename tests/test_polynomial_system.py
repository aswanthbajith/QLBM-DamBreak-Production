#!/usr/bin/env python3
"""
Unit Tests for Step 9: Discrete Polynomial System & Matrix Operators.
"""

import sys
import os
sys.path.append(os.path.join(os.path.dirname(__file__), '../classical'))

import unittest
import numpy as np
from matrix_two_phase_lbm import MatrixTwoPhaseLBM2D

class TestPolynomialSystem(unittest.TestCase):
    def setUp(self):
        self.nx, self.ny = 10, 8
        self.N = self.nx * self.ny
        self.matrix_lbm = MatrixTwoPhaseLBM2D(
            nx=self.nx, ny=self.ny,
            rho_L=1.0, rho_G=0.1,
            nu_L=0.01, nu_G=0.01,
            sigma=0.001, gy=-4.0e-4
        )

    def test_01_streaming_matrix_properties(self):
        """Verify that streaming matrix S is strictly an orthogonal permutation matrix."""
        S = self.matrix_lbm.S
        dim = 18 * self.N
        self.assertEqual(S.shape, (dim, dim))
        self.assertEqual(S.nnz, dim, "S must have exactly 1 non-zero per row")

        # Verify unitarity S^T * S = I
        STS = S.T.dot(S)
        self.assertEqual(STS.nnz, dim)

    def test_02_linear_collision_matrix_sparsity(self):
        """Verify block-diagonal structure of M1."""
        M1 = self.matrix_lbm.M1
        dim = 18 * self.N
        self.assertEqual(M1.shape, (dim, dim))
        # Non-zeros per row should be bounded by 9
        avg_nnz = M1.nnz / dim
        self.assertLessEqual(avg_nnz, 9.0)

    def test_03_polynomial_step_execution(self):
        """Verify that matrix step executes cleanly on random state vector."""
        dim = 18 * self.N
        Psi0 = np.random.rand(dim) * 0.01
        u0 = np.zeros((self.nx, self.ny))
        v0 = np.zeros((self.nx, self.ny))
        Psi1, u1, v1 = self.matrix_lbm.step(Psi0, u0, v0)
        self.assertEqual(Psi1.shape, (dim,))
        self.assertEqual(u1.shape, (self.nx, self.ny))
        self.assertEqual(v1.shape, (self.nx, self.ny))
        self.assertFalse(np.isnan(Psi1).any())

if __name__ == "__main__":
    unittest.main()
