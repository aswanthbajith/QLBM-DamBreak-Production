#!/usr/bin/env python3
"""
Level 6: Grand Linear System Assembly, Final-State Idling, and Quantum Block Encoding Oracle.

Theoretical Basis:
- Jennings et al. (PsiQuantum/Airbus 2025) & Ueno et al. (QunaSys/Univ Tokyo 2026)
- Discrete time-marching Carleman grand linear system: A * Y = B
- Final-state idling stabilization against amplitude decay
- (alpha, a, epsilon)-Block encoding of A into unitary oracle U_A
"""

import numpy as np
import scipy.sparse as sp
import scipy.sparse.linalg as spla

class QuantumBlockEncoding:
    def __init__(self, A_step, y_init, b_force=None,
                 T_sim=10, T_idle=5):
        """
        A_step: Sparse one-step Carleman evolution matrix in R^(D x D)
        y_init: Initial state vector in R^D
        b_force: Constant/affine forcing vector in R^D
        T_sim: Number of physical simulation steps
        T_idle: Number of final-state idling steps (Ueno 2026)
        """
        self.A_step = A_step
        self.D = A_step.shape[0]
        self.y_init = y_init
        self.b_force = b_force if b_force is not None else np.zeros(self.D, dtype=np.float64)
        self.T_sim = T_sim
        self.T_idle = T_idle
        self.T_total = T_sim + T_idle
        self.dim_grand = (self.T_total + 1) * self.D

        print(f"Constructing Grand Linear System: T_sim={T_sim}, T_idle={T_idle} (Total Steps={self.T_total})")
        print(f"One-Step State Dimension D = {self.D} | Grand Matrix Dimension N_grand = {self.dim_grand}")

        # Assemble grand sparse matrix A_grand
        self.A_grand = self._build_grand_matrix()
        # Assemble right-hand side vector B_grand
        self.B_grand = self._build_rhs_vector()

        # Compute block encoding parameters
        self.alpha_A, self.n_state_qubits, self.n_ancilla_qubits = self._compute_block_encoding_parameters()

    def _build_grand_matrix(self):
        """
        Assembles block lower-triangular matrix A_grand:
        [ I          0          0      ...   0 ]
        [ -A^(1)     I          0      ...   0 ]
        [ 0         -A^(1)      I      ...   0 ]
        [ ...       ...        ...     ...   0 ]
        [ 0          0         -I_idle ...   I ]
        """
        I_block = sp.eye(self.D, dtype=np.float64, format='csr')

        block_rows = []
        for t in range(self.T_total + 1):
            row_blocks = [None] * (self.T_total + 1)
            # Diagonal identity
            row_blocks[t] = I_block
            
            if t > 0:
                if t <= self.T_sim:
                    # Physical transition step: -A_step
                    row_blocks[t - 1] = -self.A_step
                else:
                    # Idling transition step: -I (Ueno 2026)
                    row_blocks[t - 1] = -I_block
                    
            block_rows.append(row_blocks)

        A_grand = sp.bmat(block_rows, format='csr', dtype=np.float64)
        return A_grand

    def _build_rhs_vector(self):
        """
        Assembles right-hand side vector B_grand in R^dim_grand:
        B = [ y_init; b_force; b_force; ... ; 0 ]
        """
        B = np.zeros(self.dim_grand, dtype=np.float64)
        # Initial condition at t=0
        B[:self.D] = self.y_init

        # Body force injections at physical time steps
        for t in range(1, self.T_sim + 1):
            B[t * self.D : (t + 1) * self.D] = self.b_force

        return B

    def _compute_block_encoding_parameters(self):
        """
        Computes (alpha, a, epsilon) quantum block encoding specifications:
        - alpha: Subnormalization constant (1-norm / maximum absolute row sum)
        - n_state_qubits: ceil(log2(dim_grand))
        - n_ancilla_qubits: Ancilla qubits required for sparse oracle encoding
        """
        # Maximum absolute row sum (infinity norm) as block encoding subnormalization
        row_sums = np.array(np.abs(self.A_grand).sum(axis=1)).flatten()
        alpha = float(np.max(row_sums))

        # Qubit counts
        n_state = int(np.ceil(np.log2(self.dim_grand)))
        # Sparsity per row (at most 1 from I + max_row from A_step)
        max_row_nnz = max(self.A_grand[i].nnz for i in range(min(100, self.dim_grand)))
        n_ancilla = int(np.ceil(np.log2(max_row_nnz))) + 2

        return alpha, n_state, n_ancilla

    def solve_exact(self):
        """
        Solves the grand linear system A_grand * Y = B_grand classically
        to obtain the exact ground-truth state trajectory.
        """
        Y_sol = spla.spsolve(self.A_grand, self.B_grand)
        return Y_sol

    def compute_condition_number_estimate(self):
        """
        Computes condition number estimate kappa(A_grand).
        """
        # 1-norm condition number estimate
        norm_A = spla.norm(self.A_grand, 1)
        # Approximate norm(A^-1) via power iteration on inverse
        v = np.random.randn(self.dim_grand)
        v /= np.linalg.norm(v)
        for _ in range(5):
            w = spla.spsolve(self.A_grand, v)
            norm_w = np.linalg.norm(w)
            v = w / norm_w
        inv_norm_est = norm_w
        kappa_est = norm_A * inv_norm_est
        return kappa_est
