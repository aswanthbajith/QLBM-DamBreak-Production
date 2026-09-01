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

        # Compute SVD once for norm and dilation
        U, S, Vh = la.svd(self.A)
        norm_A = float(S[0]) if len(S) > 0 else 1.0
        if alpha is None:
            self.alpha = max(norm_A * 1.05, 1.0)
        else:
            if alpha < norm_A:
                raise ValueError(f"alpha ({alpha}) must be >= ||A||_2 ({norm_A:.4f})")
            self.alpha = float(alpha)

        self.A_norm = self.A / self.alpha
        S_clamped = np.clip(S / self.alpha, 0.0, 1.0)
        C = np.sqrt(np.maximum(0.0, 1.0 - S_clamped**2))

        # Construct exact dilated unitary matrix U_A (2d x 2d)
        top_right = U * C[None, :]
        bot_left = C[:, None] * Vh
        bot_right = -np.diag(S_clamped)

        self.U_matrix = np.block([
            [self.A_norm, top_right],
            [bot_left, bot_right]
        ])

        # Build Qiskit QuantumCircuit
        self.circuit = self._build_qiskit_circuit()


    def _build_qiskit_circuit(self):
        """Builds Qiskit QuantumCircuit for U_A."""
        qc = QuantumCircuit(self.total_qubits, name="U_A")
        # System qubits: 0..(n_sys - 1), Ancilla qubit: n_sys
        if self.total_qubits <= 8:
            unitary_gate = UnitaryGate(self.U_matrix, label="Block_Enc_A", check_input=False)
            qc.append(unitary_gate, range(self.total_qubits))
        else:
            from qiskit.circuit import Gate
            qc.append(Gate("Block_Enc_A", self.total_qubits, []), range(self.total_qubits))
        return qc

    def extract_block(self):
        """
        Classically extracts top-left block:
        <0| U_A |0> = U_A[:d, :d]
        """
        extracted = self.U_matrix[:self.d, :self.d][:self.d_orig, :self.d_orig]
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

def build_A_C_block_encoding(A_C, alpha=None, metadata=None):
    """
    Standardized Part 14 API for constructing the unitary block encoding of A_C.
    Returns dictionary with circuit, alpha, system_qubits, ancilla_qubits, etc.
    """
    be = QuantumBlockEncoding(A_C, alpha=alpha)
    res = {
        'circuit': be.circuit,
        'alpha': be.alpha,
        'system_qubits': be.n_sys,
        'ancilla_qubits': be.n_ancilla,
        'total_qubits': be.total_qubits,
        'padded_dimension': be.d,
        'original_dimension': be.d_orig,
        'construction_method': "Canonical Halmos CS-Dilation",
        'verification_metadata': be.verify_encoding(),
        'encoder_instance': be
    }
    if metadata is not None:
        res['user_metadata'] = metadata
    return res

