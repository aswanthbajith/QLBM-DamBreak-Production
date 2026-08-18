#!/usr/bin/env python3
"""
Unit Tests for Step 9: Carleman State Lifting & Matrix Dimensions.
"""

import sys
import os
sys.path.append(os.path.join(os.path.dirname(__file__), '../quantum'))

import unittest
import numpy as np
from carleman_lbm import CarlemanTwoPhaseLBM

class TestCarlemanLifting(unittest.TestCase):
    def setUp(self):
        self.nx, self.ny = 6, 4
        self.N = self.nx * self.ny
        self.c1 = CarlemanTwoPhaseLBM(nx=self.nx, ny=self.ny, truncation_order=1)
        self.c2 = CarlemanTwoPhaseLBM(nx=self.nx, ny=self.ny, truncation_order=2)

    def test_01_dimensions(self):
        """Verify analytical dimensions: N_C=1 (18N) and N_C=2 (342N)."""
        self.assertEqual(self.c1.dim_carleman, 18 * self.N)
        self.assertEqual(self.c2.dim_carleman, 342 * self.N)
        self.assertEqual(self.c2.A_C.shape, (342 * self.N, 342 * self.N))

    def test_02_state_lifting_and_projection(self):
        """Verify that state lifting and subsequent projection preserves the base state."""
        Psi = np.random.randn(18 * self.N)
        Y2 = self.c2.lift_state(Psi)
        self.assertEqual(Y2.shape, (342 * self.N,))
        
        Psi_proj = self.c2.project_state(Y2)
        np.testing.assert_allclose(Psi_proj, Psi, rtol=1e-14, atol=1e-14)

    def test_03_local_kronecker_structure(self):
        """Verify that Y2 contains exact ordered quadratic products per node."""
        Psi = np.arange(18 * self.N, dtype=np.float64)
        Y2 = self.c2.lift_state(Psi)
        
        # Check node 0: Psi(18) -> Psi(18) (x) Psi(18) (dim 324)
        psi_node0 = Psi.reshape((18, self.N))[:, 0]
        expected_kron = np.kron(psi_node0, psi_node0)
        actual_kron = Y2[18 * self.N :].reshape((324, self.N))[:, 0]
        np.testing.assert_allclose(actual_kron, expected_kron, rtol=1e-14)

if __name__ == "__main__":
    unittest.main()
