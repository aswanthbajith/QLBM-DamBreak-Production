#!/usr/bin/env python3
"""
Unit Tests for Quantum Circuit Resource Estimation & Logarithmic Scaling.
"""

import sys
import os
sys.path.append(os.path.join(os.path.dirname(__file__), '../quantum'))

import unittest
import numpy as np
from carleman_lbm import CarlemanTwoPhaseLBM
from block_encoding import QuantumBlockEncoding

class TestQuantumResources(unittest.TestCase):
    def test_01_logarithmic_qubit_scaling(self):
        """Verify that total qubits scale logarithmically with lattice nodes N."""
        for N in [1, 2, 4, 8, 16]:
            c_model = CarlemanTwoPhaseLBM(nx=N, ny=1, truncation_order=1)
            A = c_model.A_C.toarray()
            be = QuantumBlockEncoding(A)
            expected_qubits = int(np.ceil(np.log2(18 * N))) + 1
            self.assertEqual(be.total_qubits, expected_qubits)

    def test_02_circuit_depth_scaling(self):
        """Verify that block encoding circuit has well-defined unitary depth."""
        c_model = CarlemanTwoPhaseLBM(nx=2, ny=1, truncation_order=1)
        A = c_model.A_C.toarray()
        be = QuantumBlockEncoding(A)
        self.assertGreater(be.circuit.depth(), 0)

if __name__ == "__main__":
    unittest.main()
