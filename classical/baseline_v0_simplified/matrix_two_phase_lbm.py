#!/usr/bin/env python3
"""
Level 3 & 4: Sparse Matrix and Quadratic Tensor Representation of Two-Phase LBM.

State Vector:
Psi(t) = [g(t); h(t)] in R^(2 * Q * N)

Operators:
1. S: Linear spatial permutation & reflection matrix in R^(2QN x 2QN) (Unitary)
2. M1: Linear relaxation matrix in R^(2QN x 2QN) (Block-Diagonal)
3. M2: Quadratic convection & advection tensor kernel
4. b_force: Affine gravitational body force vector in R^(2QN)
"""

import numpy as np
import scipy.sparse as sp

class MatrixTwoPhaseLBM2D:
    def __init__(self, nx, ny,
                 rho0=1.0, nu=0.01,
                 gy=-3.0e-4, gx=0.0,
                 tau_phi=0.6,
                 free_slip_bottom=True):
        
        self.nx = nx
        self.ny = ny
        self.N = nx * ny
        self.Q = 9
        self.dim_single = self.Q * self.N
        self.dim_total = 2 * self.dim_single

        self.rho0 = rho0
        self.nu = nu
        self.gx = gx
        self.gy = gy
        self.tau_phi = tau_phi
        self.free_slip_bottom = free_slip_bottom

        self.cs2 = 1.0 / 3.0
        self.cs4 = 1.0 / 9.0
        self.tau_v = self.nu / self.cs2 + 0.5

        # D2Q9 Velocity Set
        self.c = np.array([
            [ 0,  0], [ 1,  0], [ 0,  1], [-1,  0], [ 0, -1],
            [ 1,  1], [-1,  1], [-1, -1], [ 1, -1]
        ], dtype=np.int32)

        self.w = np.array([
            4/9, 1/9, 1/9, 1/9, 1/9, 1/36, 1/36, 1/36, 1/36
        ], dtype=np.float64)

        self.opp = np.array([0, 3, 4, 1, 2, 7, 8, 5, 6], dtype=np.int32)
        self.refl_floor = np.array([0, 1, 4, 3, 2, 8, 7, 6, 5], dtype=np.int32)

        # Build Sparse Linear Matrix Operators
        self.S = self._build_streaming_matrix()
        self.M1 = self._build_linear_collision_matrix()

    def _node_idx(self, x, y):
        return x * self.ny + y

    def _coord(self, n):
        return n // self.ny, n % self.ny

    def _build_streaming_matrix(self):
        """
        Builds the global linear permutation streaming matrix S.
        Property: S^T * S = I (strictly unitary permutation).
        """
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

        S_sparse = sp.csr_matrix((vals, (rows, cols)), shape=(self.dim_total, self.dim_total), dtype=np.float64)
        return S_sparse

    def _build_linear_collision_matrix(self):
        """
        Builds the linear relaxation matrix M1 for both g and h.
        """
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

        M1_sparse = sp.csr_matrix((vals, (rows, cols)), shape=(self.dim_total, self.dim_total), dtype=np.float64)
        return M1_sparse

    def evaluate_collision(self, Psi):
        """
        Evaluates exact local collision on state vector Psi.
        """
        g_arr = Psi[:self.dim_single].reshape((self.Q, self.N))
        h_arr = Psi[self.dim_single:].reshape((self.Q, self.N))

        phi = np.clip(np.sum(h_arr, axis=0), 0.0, 1.0)
        p = self.cs2 * np.sum(g_arr, axis=0)

        sum_gc_x = np.zeros(self.N, dtype=np.float64)
        sum_gc_y = np.zeros(self.N, dtype=np.float64)
        for q in range(self.Q):
            sum_gc_x += g_arr[q] * self.c[q, 0]
            sum_gc_y += g_arr[q] * self.c[q, 1]

        Fx = phi * self.rho0 * self.gx
        Fy = phi * self.rho0 * self.gy

        u = (1.0 / self.rho0) * sum_gc_x + 0.5 * Fx / self.rho0
        v = (1.0 / self.rho0) * sum_gc_y + 0.5 * Fy / self.rho0

        u_2d = u.reshape((self.nx, self.ny))
        v_2d = v.reshape((self.nx, self.ny))
        u_2d[0, :] = 0.0; u_2d[-1, :] = 0.0; u_2d[:, -1] = 0.0
        v_2d[0, :] = 0.0; v_2d[-1, :] = 0.0; v_2d[:, -1] = 0.0
        if not self.free_slip_bottom:
            u_2d[:, 0] = 0.0
        v_2d[:, 0] = 0.0

        u_flat = u_2d.flatten()
        v_flat = v_2d.flatten()
        u2 = u_flat**2 + v_flat**2

        g_post = np.zeros_like(g_arr)
        h_post = np.zeros_like(h_arr)

        for q in range(self.Q):
            wi = self.w[q]
            cx, cy = self.c[q, 0], self.c[q, 1]
            cu = cx * u_flat + cy * v_flat

            heq = wi * phi * (1.0 + cu / self.cs2)
            h_post[q] = h_arr[q] - (1.0 / self.tau_phi) * (h_arr[q] - heq)

            geq = (p / (self.rho0 * self.cs2)) * wi + self.rho0 * wi * (cu / self.cs2 + 0.5 * cu**2 / self.cs4 - 0.5 * u2 / self.cs2)

            term1 = (cx - u_flat) * (Fx / self.rho0) + (cy - v_flat) * (Fy / self.rho0)
            term2 = (cu / self.cs2) * (cx * (Fx / self.rho0) + cy * (Fy / self.rho0))
            Fi = (1.0 - 0.5 / self.tau_v) * wi * (term1 / self.cs2 + term2 / self.cs2)

            g_post[q] = g_arr[q] - (1.0 / self.tau_v) * (g_arr[q] - geq) + Fi

        Psi_post = np.zeros(self.dim_total, dtype=np.float64)
        Psi_post[:self.dim_single] = g_post.flatten()
        Psi_post[self.dim_single:] = h_post.flatten()
        return Psi_post

    def step(self, Psi):
        Psi_post = self.evaluate_collision(Psi)
        Psi_next = self.S.dot(Psi_post)
        return Psi_next
