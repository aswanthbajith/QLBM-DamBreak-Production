#!/usr/bin/env python3
"""
Unit Tests for Step 9: Carleman Matrix Evolution & Equivalence.
"""

import sys
import os
sys.path.append(os.path.join(os.path.dirname(__file__), '../quantum'))

import unittest
import numpy as np
from carleman_lbm import CarlemanTwoPhaseLBM

class TestCarlemanEquivalence(unittest.TestCase):
    def setUp(self):
        self.nx, self.ny = 6, 4
        self.N = self.nx * self.ny
        self.c2 = CarlemanTwoPhaseLBM(nx=self.nx, ny=self.ny, truncation_order=2)

    def test_01_carleman_step_stability(self):
        """Verify that Carleman matrix step produces stable finite outputs."""
        Psi0 = np.random.rand(18 * self.N) * 0.01
        Y0 = self.c2.lift_state(Psi0)
        Y1 = self.c2.step(Y0)
        self.assertEqual(Y1.shape, (342 * self.N,))
        self.assertFalse(np.isnan(Y1).any())
        self.assertFalse(np.isinf(Y1).any())

    def test_02_carleman_matrix_sparsity(self):
        """Verify that full A_C matrix is sparse."""
        AC = self.c2.A_C
        total_elements = (342 * self.N)**2
        sparsity = AC.nnz / total_elements
        # Sparse matrix should be significantly less than 5% dense
        self.assertLess(sparsity, 0.05)

    def test_03_zero_state_preservation(self):
        """Verify that zero state vector produces zero state output."""
        Y0 = np.zeros(342 * self.N)
        Y1 = self.c2.step(Y0)
        np.testing.assert_allclose(Y1, 0.0, atol=1e-15)

if __name__ == "__main__":
    unittest.main()
