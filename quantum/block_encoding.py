#!/usr/bin/env python3
"""
Quantum Block Encoding Module for Carleman LBM Matrices using Qiskit.

Given matrix A in C^(d x d):
Constructs unitary U_A in C^(2d x 2d) on (a=1 + n) qubits such that:
<0| U_A |0> = A / alpha
within machine precision.
"""

import numpy as np
import scipy.linalg as la
from qiskit import QuantumCircuit
from qiskit.circuit.library import UnitaryGate
from qiskit.quantum_info import Operator

class QuantumBlockEncoding:
    def __init__(self, A, alpha=None):
        """
        A: Real or complex matrix (d x d)
        alpha: Subnormalization constant (if None, set to 1.05 * ||A||_2)
        """
        self.A_orig = np.array(A, dtype=np.complex128)
        self.d_orig = self.A_orig.shape[0]

        # Pad to next power of 2: d = 2^n
        self.n_sys = int(np.ceil(np.log2(max(self.d_orig, 2))))
        self.d = 1 << self.n_sys
        self.n_ancilla = 1
        self.total_qubits = self.n_ancilla + self.n_sys

        # Padded matrix A_pad
        self.A = np.zeros((self.d, self.d), dtype=np.complex128)
        self.A[:self.d_orig, :self.d_orig] = self.A_orig
        # Identity padding for unused subspace
        if self.d > self.d_orig:
            for i in range(self.d_orig, self.d):
                self.A[i, i] = 1.0

        # Spectral norm and subnormalization alpha
        norm_A = float(la.norm(self.A, 2))
        if alpha is None:
            self.alpha = max(norm_A * 1.05, 1.0)
        else:
            if alpha < norm_A:
                raise ValueError(f"alpha ({alpha}) must be >= ||A||_2 ({norm_A:.4f})")
            self.alpha = float(alpha)

        self.A_norm = self.A / self.alpha

        # Construct exact dilated unitary matrix U_A (2d x 2d)
        self.U_matrix = self._build_dilated_unitary()

        # Build Qiskit QuantumCircuit
        self.circuit = self._build_qiskit_circuit()

    def _build_dilated_unitary(self):
        """
        Constructs canonical CS-decomposition / Halmos dilation:
        U_A = [[ A_norm,           sqrt(I - A_norm * A_norm^dagger) ],
               [ sqrt(I - A_norm^dagger * A_norm), -A_norm^dagger ]]
        """
        d = self.d
        I_d = np.eye(d, dtype=np.complex128)

        # Singular Value Decomposition: A_norm = U * S * Vh
        U, S, Vh = la.svd(self.A_norm)
        # S is array of singular values in [0, 1]
        S_clamped = np.clip(S, 0.0, 1.0)
        C = np.sqrt(np.maximum(0.0, 1.0 - S_clamped**2))

        # Dilation components
        Sigma = np.diag(S_clamped)
        Cosine = np.diag(C)

        R_sigma = np.block([
            [Sigma, Cosine],
            [Cosine, -Sigma]
        ])

        U_ext = la.block_diag(U, np.eye(d, dtype=np.complex128))
        Vh_ext = la.block_diag(Vh, np.eye(d, dtype=np.complex128))

        U_A = U_ext @ R_sigma @ Vh_ext
        return U_A

    def _build_qiskit_circuit(self):
        """Builds Qiskit QuantumCircuit for U_A."""
        qc = QuantumCircuit(self.total_qubits, name="U_A")
        # System qubits: 0..(n_sys - 1), Ancilla qubit: n_sys
        unitary_gate = UnitaryGate(self.U_matrix, label="Block_Enc_A")
        qc.append(unitary_gate, range(self.total_qubits))
        return qc

    def extract_block(self):
        """
        Classically extracts top-left block:
        <0| U_A |0> = U_A[:d, :d]
        """
        op = Operator(self.circuit)
        u_sim = op.data
        extracted = u_sim[:self.d, :self.d][:self.d_orig, :self.d_orig]
        return extracted

    def verify_encoding(self):
        """
        Calculates L_inf error and Frobenius relative error against A / alpha.
        """
        extracted = self.extract_block()
        target = self.A_orig / self.alpha

        diff = np.abs(extracted - target)
        linf_err = float(np.max(diff))
        frob_err = float(la.norm(diff, 'fro') / (la.norm(target, 'fro') + 1e-15))

        return {
            'linf_error': linf_err,
            'frob_error': frob_err,
            'alpha': self.alpha,
            'd_orig': self.d_orig,
            'n_qubits': self.total_qubits,
            'gate_count': len(self.circuit.data),
            'depth': self.circuit.depth()
        }
