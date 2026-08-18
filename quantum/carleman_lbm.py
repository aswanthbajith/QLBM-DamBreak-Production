#!/usr/bin/env python3
"""
Level 5: Carleman Linearization and State Space Lifting for Two-Phase LBM.

State Representation:
For order N_C = 2 (exact quadratic truncation):
y_2(t) = [Psi(t); Psi_local^(x)2(t)] in R^(18 N + 324 N) = R^(342 N)

Carleman Update Equation:
y_2(t+1) = M_C * y_2(t) + b_C
where:
M_C = S_C * C_C
- C_C = [[ M1, M2 ], [ 0, M1_kron2 ]] is the block upper-triangular Carleman collision matrix.
- S_C = [[ S, 0 ], [ 0, S_kron2 ]] is the Carleman streaming matrix (Unitary Permutation).
"""

import numpy as np
import scipy.sparse as sp

class CarlemanTwoPhaseLBM:
    def __init__(self, nx, ny,
                 rho0=1.0, nu=0.02,
                 gy=-2.0e-4, gx=0.0,
                 tau_phi=0.65,
                 truncation_order=2,
                 free_slip_bottom=True):
        
        self.nx = nx
        self.ny = ny
        self.N = nx * ny
        self.Q = 9
        self.dim_single = self.Q * self.N
        self.dim_base = 2 * self.dim_single # 18 N
        self.truncation_order = truncation_order

        self.rho0 = rho0
        self.nu = nu
        self.gx = gx
        self.gy = gy
        self.tau_phi = tau_phi
        self.free_slip_bottom = free_slip_bottom

        self.cs2 = 1.0 / 3.0
        self.cs4 = 1.0 / 9.0
        self.tau_v = self.nu / self.cs2 + 0.5

        # D2Q9 velocities and weights
        self.c = np.array([
            [ 0,  0], [ 1,  0], [ 0,  1], [-1,  0], [ 0, -1],
            [ 1,  1], [-1,  1], [-1, -1], [ 1, -1]
        ], dtype=np.int32)

        self.w = np.array([
            4/9, 1/9, 1/9, 1/9, 1/9, 1/36, 1/36, 1/36, 1/36
        ], dtype=np.float64)

        self.opp = np.array([0, 3, 4, 1, 2, 7, 8, 5, 6], dtype=np.int32)
        self.refl_floor = np.array([0, 1, 4, 3, 2, 8, 7, 6, 5], dtype=np.int32)

        # Dimension of Carleman state
        # Order 1: 18 N
        # Order 2: 18 N + (18^2) N = 18 N + 324 N = 342 N
        if truncation_order == 1:
            self.dim_carleman = self.dim_base
        elif truncation_order == 2:
            self.dim_carleman = self.dim_base + (18**2) * self.N
        else:
            raise ValueError("Truncation order > 2 not required for quadratic LBM.")

        print(f"Initializing Carleman Two-Phase LBM: Grid {nx}x{ny} (N={self.N}) | Order N_C={truncation_order} | Carleman Dim D_C={self.dim_carleman}")

        # Build Sparse Linear Streaming Matrix S
        self.S = self._build_streaming_matrix()
        # Build Block Linear Collision Matrix M1
        self.M1 = self._build_linear_collision_matrix()

    def _node_idx(self, x, y):
        return x * self.ny + y

    def _coord(self, n):
        return n // self.ny, n % self.ny

    def _build_streaming_matrix(self):
        rows = []
        cols = []
        vals = []

        for field in [0, 1]:
            field_offset = field * self.dim_single
            for q in range(self.Q):
                cx, cy = self.c[q, 0], self.c[q, 1]
                q_offset = q * self.N

                for n in range(self.N):
                    x, y = self._coord(n)
                    src_idx = field_offset + q_offset + n

                    tx = x + cx
                    ty = y + cy

                    target_q = q

                    if tx < 0 or tx >= self.nx or ty < 0 or ty >= self.ny:
                        if ty < 0 and self.free_slip_bottom:
                            target_q = self.refl_floor[q]
                            tx = x
                            ty = 0
                        else:
                            target_q = self.opp[q]
                            tx = np.clip(x, 0, self.nx - 1)
                            ty = np.clip(y, 0, self.ny - 1)

                    target_n = self._node_idx(tx, ty)
                    dst_idx = field_offset + target_q * self.N + target_n

                    rows.append(dst_idx)
                    cols.append(src_idx)
                    vals.append(1.0)

        S_sparse = sp.csr_matrix((vals, (rows, cols)), shape=(self.dim_base, self.dim_base), dtype=np.float64)
        return S_sparse

    def _build_linear_collision_matrix(self):
        rows = []
        cols = []
        vals = []

        # 1. Hydrodynamic linear relaxation (g)
        for q_star in range(self.Q):
            for q in range(self.Q):
                wi_term = self.w[q_star] * (1.0 + (self.c[q_star, 0] * self.c[q, 0] + self.c[q_star, 1] * self.c[q, 1]) / self.cs2)
                coeff = (1.0 / self.tau_v) * wi_term
                if q_star == q:
                    coeff += (1.0 - 1.0 / self.tau_v)

                if abs(coeff) > 1e-15:
                    for n in range(self.N):
                        rows.append(q_star * self.N + n)
                        cols.append(q * self.N + n)
                        vals.append(coeff)

        # 2. Phase-field linear relaxation (h)
        h_offset = self.dim_single
        for q_star in range(self.Q):
            for q in range(self.Q):
                coeff = (1.0 / self.tau_phi) * self.w[q_star]
                if q_star == q:
                    coeff += (1.0 - 1.0 / self.tau_phi)

                if abs(coeff) > 1e-15:
                    for n in range(self.N):
                        rows.append(h_offset + q_star * self.N + n)
                        cols.append(h_offset + q * self.N + n)
                        vals.append(coeff)

        M1_sparse = sp.csr_matrix((vals, (rows, cols)), shape=(self.dim_base, self.dim_base), dtype=np.float64)
        return M1_sparse

    def lift_state(self, Psi):
        """
        Lifts base physical state Psi in R^(18 N) to Carleman state y_2 in R^(342 N):
        y_2 = [ Psi; Psi (x)_local Psi ]
        """
        if self.truncation_order == 1:
            return Psi.copy()

        # Compute local tensor square at each node
        # Reshape to (18, N)
        psi_mat = Psi.reshape((18, self.N))
        # Outer product per node: (18, 18, N) -> (324, N)
        psi_kron2 = np.einsum('in,jn->ijn', psi_mat, psi_mat).reshape((324 * self.N,))
        
        y = np.concatenate([Psi, psi_kron2])
        return y

    def project_state(self, y):
        """
        Projects Carleman state y back to physical hydrodynamic state Psi in R^(18 N).
        """
        return y[:self.dim_base].copy()

    def build_carleman_one_step_matrix(self):
        """
        Constructs the linear Carleman one-step transition matrix A^(1) such that:
        y(t+1) = A^(1) y(t) + b_force
        """
        # For N_C = 1: A^(1) = S * M1
        A1 = self.S.dot(self.M1)
        return A1
