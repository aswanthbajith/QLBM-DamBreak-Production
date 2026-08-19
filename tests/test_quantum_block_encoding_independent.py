#!/usr/bin/env python3
"""
Independent Clean-Room Test Suite for Quantum Block Encoding of Carleman Operators.
Tests unitarity, exact block extraction, padding preservation, basis actions,
and physical lifted state propagation without circular references.
"""

import unittest
import numpy as np
import scipy.linalg as la
from qiskit import QuantumCircuit
from qiskit.quantum_info import Operator

from carleman_lbm import CarlemanTwoPhaseLBM
from block_encoding import QuantumBlockEncoding, build_A_C_block_encoding

class TestQuantumBlockEncodingIndependent(unittest.TestCase):
    def setUp(self):
        self.nx = 2
        self.ny = 1
        self.N = self.nx * self.ny
        self.c_model = CarlemanTwoPhaseLBM(nx=self.nx, ny=self.ny, truncation_order=2)
        self.A_C = self.c_model.A_C.toarray()
        self.dim = self.A_C.shape[0] # 684
        self.alpha = 11.5

    def test_01_block_encoding_dimensions_and_metadata(self):
        """Verifies Part 14 build_A_C_block_encoding API and register dimensions."""
        enc_info = build_A_C_block_encoding(self.A_C, alpha=self.alpha, metadata={'test': 'true'})
        self.assertEqual(enc_info['original_dimension'], 684)
        self.assertEqual(enc_info['padded_dimension'], 1024)
        self.assertEqual(enc_info['system_qubits'], 10)
        self.assertEqual(enc_info['ancilla_qubits'], 1)
        self.assertEqual(enc_info['total_qubits'], 11)
        self.assertAlmostEqual(enc_info['alpha'], self.alpha)
        self.assertIn('verification_metadata', enc_info)

    def test_02_independent_dilation_unitarity(self):
        """Verifies that U_A is unitary to machine precision: ||U^dagger U - I||_inf < 1e-14."""
        be = QuantumBlockEncoding(self.A_C, alpha=self.alpha)
        U = be.U_matrix
        I_2d = np.eye(U.shape[0], dtype=np.complex128)
        diff = np.abs(U.conj().T @ U - I_2d)
        max_err = float(np.max(diff))
        self.assertLess(max_err, 1e-14, f"Unitarity error {max_err} exceeds 1e-14")

    def test_03_exact_block_extraction(self):
        """Verifies <0| U_A |0> == A_C / alpha to machine precision: ||B - A/alpha||_inf < 1e-14."""
        be = QuantumBlockEncoding(self.A_C, alpha=self.alpha)
        extracted = be.extract_block()
        target = self.A_C / self.alpha
        diff = np.abs(extracted - target)
        max_err = float(np.max(diff))
        self.assertLess(max_err, 1e-14, f"Block extraction error {max_err} exceeds 1e-14")

    def test_04_padding_subspace_isolation(self):
        """Verifies that padded non-physical rows/columns act as identity and do not contaminate physical subspace."""
        be = QuantumBlockEncoding(self.A_C, alpha=self.alpha)
        A_pad = be.A
        # Physical block
        np.testing.assert_allclose(A_pad[:self.dim, :self.dim], self.A_C, atol=1e-15)
        # Unused padding block should be identity
        if be.d > self.dim:
            pad_block = A_pad[self.dim:, self.dim:]
            np.testing.assert_allclose(pad_block, np.eye(be.d - self.dim), atol=1e-15)
            # Off-diagonal padding coupling must be exactly zero
            np.testing.assert_allclose(A_pad[:self.dim, self.dim:], 0.0, atol=1e-15)
            np.testing.assert_allclose(A_pad[self.dim:, :self.dim], 0.0, atol=1e-15)

    def test_05_random_state_action(self):
        """Verifies state projection: (<0| (x) I_phys) U_A (|0> (x) |psi>) == (A_C / alpha) |psi>."""
        be = QuantumBlockEncoding(self.A_C, alpha=self.alpha)
        np.random.seed(99)
        psi = np.random.uniform(-1, 1, size=self.dim) + 1j * np.random.uniform(-1, 1, size=self.dim)
        psi /= la.norm(psi)

        # Build full state |0> (x) |psi_pad>
        state_in = np.zeros(2 * be.d, dtype=np.complex128)
        state_in[:self.dim] = psi

        state_out = be.U_matrix @ state_in
        # Extract <0| (x) I_phys component
        psi_out_extracted = state_out[:be.d][:self.dim]

        psi_target = (self.A_C @ psi) / self.alpha
        err = float(la.norm(psi_out_extracted - psi_target))
        self.assertLess(err, 1e-14, f"State action error {err} exceeds 1e-14")

    def test_06_physical_lifted_dam_break_state_action(self):
        """Verifies physical Carleman lifted state action: U_A |0>|Y_phys> -> (A_C Y_phys)/alpha."""
        be = QuantumBlockEncoding(self.A_C, alpha=self.alpha)
        
        # Physical state
        psi_phys = np.zeros(18 * self.N)
        psi_phys[:9 * self.N] = 0.02 # hydro
        psi_phys[9 * self.N:] = 0.5 # phase
        Y_phys = self.c_model.lift_state(psi_phys)
        Y_norm = Y_phys / la.norm(Y_phys)

        state_in = np.zeros(2 * be.d, dtype=np.complex128)
        state_in[:self.dim] = Y_norm

        state_out = be.U_matrix @ state_in
        Y_out_extracted = state_out[:be.d][:self.dim]

        Y_target = (self.A_C @ Y_norm) / self.alpha
        err = float(la.norm(Y_out_extracted - Y_target))
        self.assertLess(err, 1e-14, f"Physical state propagation error {err} exceeds 1e-14")

if __name__ == "__main__":
    unittest.main()
