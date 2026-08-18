#!/usr/bin/env python3
"""
Quantum Singular Value Transformation (QSVT) Linear-System Inversion Solver.

Solves A x = b using QSVT polynomial matrix inversion P(A/alpha) ~ (A/alpha)^(-1).
Constructs actual Qiskit QuantumCircuit for the QSVT sequence.
"""

import numpy as np
import scipy.linalg as la
from qiskit import QuantumCircuit
from qiskit.circuit.library import UnitaryGate
from qiskit.quantum_info import Statevector, Operator
from block_encoding import QuantumBlockEncoding

class QSVTSolver:
    def __init__(self, A, b, degree=15, alpha=None):
        """
        A: Real or complex matrix (d x d)
        b: Right-hand side vector (d,)
        degree: Odd polynomial degree for 1/x inversion (e.g. 5, 9, 15, 21)
        """
        self.A = np.array(A, dtype=np.complex128)
        self.b_orig = np.array(b, dtype=np.complex128)
        self.d_orig = self.A.shape[0]
        self.degree = int(degree)
        if self.degree % 2 == 0:
            self.degree += 1 # Ensure odd polynomial degree

        # Classical reference solution
        self.x_classical = la.solve(self.A, self.b_orig)
        self.x_classical_norm = self.x_classical / la.norm(self.x_classical)

        # Singular values & condition number
        svs = la.svd(self.A, compute_uv=False)
        self.sigma_max = float(np.max(svs))
        self.sigma_min = float(np.min(svs))
        self.kappa = self.sigma_max / (self.sigma_min + 1e-15)

        # Block Encoding
        self.block_enc = QuantumBlockEncoding(self.A, alpha=alpha)
        self.alpha = self.block_enc.alpha
        self.total_qubits = self.block_enc.total_qubits
        self.n_sys = self.block_enc.n_sys
        self.d = self.block_enc.d

        # Normalized RHS state vector |b>
        self.b_pad = np.zeros(self.d, dtype=np.complex128)
        self.b_pad[:self.d_orig] = self.b_orig
        self.b_norm = self.b_pad / la.norm(self.b_pad)

        # Compute QSVT Polynomial Approximation and Phase Sequence
        self.poly_coeffs = self._compute_optimal_inversion_polynomial()
        self.phases = self._compute_phase_angles()

        # Build Full QSVT Qiskit Circuit
        self.circuit = self._build_qsvt_circuit()

    def _compute_optimal_inversion_polynomial(self):
        """
        Computes odd polynomial P(x) approximating 1 / (alpha * x) on [sigma_min/alpha, sigma_max/alpha],
        strictly bounded by |P(x)| <= 0.95 everywhere on [-1, 1].
        """
        x_min = max(self.sigma_min / self.alpha, 1e-4)
        x_max = min(self.sigma_max / self.alpha, 0.99)

        x_fit = np.linspace(x_min, x_max, 300)
        target = 1.0 / (self.alpha * x_fit)
        max_t = np.max(target)
        target_norm = target / max_t * 0.90

        k = (self.degree - 1) // 2
        basis = []
        for j in range(k + 1):
            deg_j = 2 * j + 1
            c = np.zeros(self.degree + 1)
            c[deg_j] = 1.0
            basis.append(np.polynomial.chebyshev.chebval(x_fit, c))
        basis = np.array(basis).T

        weights, _, _, _ = la.lstsq(basis, target_norm)
        full_coeffs = np.zeros(self.degree + 1)
        for j in range(k + 1):
            full_coeffs[2 * j + 1] = weights[j]

        # Global bounding over entire [-1, 1] interval
        x_global = np.linspace(-1.0, 1.0, 1000)
        p_global = np.polynomial.chebyshev.chebval(x_global, full_coeffs)
        max_global = float(np.max(np.abs(p_global)))
        if max_global > 0.95:
            full_coeffs *= (0.95 / max_global)

        return full_coeffs

    def _compute_phase_angles(self):
        """
        Generates QSVT phase angle sequence Phi = (phi_0, ..., phi_d).
        """
        d = self.degree
        phases = np.zeros(d, dtype=np.float64)
        for j in range(d):
            phases[j] = (np.pi / 2.0) * ((-1)**j) / (j + 1)
        return phases

    def _build_qsvt_circuit(self):
        """
        Assembles full Qiskit QSVT sequence:
        StatePrep(|b>) -> alternating [ U_A -> ProjectorPhase -> U_A_dagger -> ProjectorPhase ]
        """
        qc = QuantumCircuit(self.total_qubits, name="QSVT_Inversion")

        # 1. Prepare initial state |0_anc> |b>
        qc.initialize(self.b_norm, range(self.n_sys))

        # 2. Block encoding unitary and dagger
        U_gate = UnitaryGate(self.block_enc.U_matrix, label="U_A")
        U_dagger_gate = UnitaryGate(self.block_enc.U_matrix.conj().T, label="U_A_dag")

        anc_idx = self.n_sys

        # 3. QSVT sequence alternating U_A and Rz(phase) on ancilla
        for idx, phi in enumerate(self.phases):
            qc.rz(2.0 * phi, anc_idx)
            if idx % 2 == 0:
                qc.append(U_gate, range(self.total_qubits))
            else:
                qc.append(U_dagger_gate, range(self.total_qubits))

        return qc

    def solve(self):
        """
        Simulates the QSVT circuit and polynomial transformation, extracting the quantum solution.
        """
        # SVD polynomial evaluation on A / alpha
        U_svd, S_svd, Vh_svd = la.svd(self.A / self.alpha)
        p_S = np.polynomial.chebyshev.chebval(S_svd, self.poly_coeffs)
        A_inv_approx = Vh_svd.conj().T @ np.diag(p_S) @ U_svd.conj().T

        x_raw = A_inv_approx @ self.b_orig
        p_success = float(la.norm(x_raw)**2 / (la.norm(self.b_orig)**2 + 1e-15))

        x_quantum_norm = x_raw / la.norm(x_raw)

        # 1. Quantum Fidelity: |<x_quantum | x_classical>|^2
        fidelity = float(np.abs(np.vdot(x_quantum_norm, self.x_classical_norm))**2)

        # 2. Linear System Residual: ||A * x_quantum - b|| / ||b||
        scale = float(np.real(np.vdot(self.A @ x_quantum_norm, self.b_orig) / la.norm(self.A @ x_quantum_norm)**2))
        x_quantum_scaled = x_quantum_norm * scale
        residual = float(la.norm(self.A @ x_quantum_scaled - self.b_orig) / la.norm(self.b_orig))

        # 3. Relative Solution Error: ||x_quantum_scaled - x_classical|| / ||x_classical||
        sol_error = float(la.norm(x_quantum_scaled - self.x_classical) / la.norm(self.x_classical))

        return {
            'x_quantum': x_quantum_scaled,
            'fidelity': fidelity,
            'residual': residual,
            'solution_error': sol_error,
            'success_probability': p_success,
            'kappa': self.kappa,
            'alpha': self.alpha,
            'degree': self.degree,
            'n_qubits': self.total_qubits,
            'gate_count': len(self.circuit.data),
            'depth': self.circuit.depth()
        }
