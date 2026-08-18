#!/usr/bin/env python3
"""
Complete Carleman Linearization & State Space Lifting for Two-Phase LBM.

State Representation (Order N_C = 2):
Y_2(t) = [ Psi(t); Psi_local^(x)2(t) ] in R^(18 N + 324 N) = R^(342 N)

Complete Carleman Linear System:
Y_2(t+1) = A_C * Y_2(t) + b_C

where:
A_C = S_C * C_2 in R^(342 N x 342 N)
- S_C = block_diag(S, S_kron2) is the complete (342N x 342N) unitary streaming permutation.
- C_2 = [[ M1, M2 ], [ 0, M1_kron2 ]] is the block upper-triangular collision matrix.
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
        """
        nx, ny: Grid nodes
        truncation_order: 1 (Linear 18N) or 2 (Complete Quadratic 342N)
        """
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

        # Dimension calculation
        if truncation_order == 1:
            self.dim_carleman = self.dim_base # 18 N
        elif truncation_order == 2:
            self.dim_carleman = self.dim_base + 324 * self.N # 342 N
        else:
            raise ValueError("Truncation order > 2 not implemented.")

        print(f"Constructing Carleman Model: Grid {nx}x{ny} (N={self.N}) | Order N_C={truncation_order} | Dimension D_C={self.dim_carleman}")

        # Build Full Operators
        self.S = self._build_streaming_matrix_base()
        self.M1_node = self._build_local_linear_collision()
        self.M2_node = self._build_local_quadratic_tensor()

        # Build Full Carleman Matrix A_C (342N x 342N)
        self.A_C = self._build_full_carleman_matrix()

    def _node_idx(self, x, y):
        return x * self.ny + y

    def _coord(self, n):
        return n // self.ny, n % self.ny

    def _build_streaming_matrix_base(self):
        """Builds 18N x 18N base streaming permutation matrix S."""
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

        return sp.csr_matrix((vals, (rows, cols)), shape=(self.dim_base, self.dim_base), dtype=np.float64)

    def _build_local_linear_collision(self):
        """Builds local 18x18 linear collision matrix M1_node."""
        M1 = np.zeros((18, 18), dtype=np.float64)

        # 1. Hydrodynamic block (g, indices 0..8)
        for q_star in range(9):
            for q in range(9):
                wi = self.w[q_star]
                val = (1.0 / self.tau_v) * wi
                if q_star == q:
                    val += (1.0 - 1.0 / self.tau_v)
                M1[q_star, q] = val

        # 2. Phase-field block (h, indices 9..17)
        for q_star in range(9):
            for q in range(9):
                wi = self.w[q_star]
                val = (1.0 / self.tau_phi) * wi
                if q_star == q:
                    val += (1.0 - 1.0 / self.tau_phi)
                M1[9 + q_star, 9 + q] = val

        return M1

    def _build_local_quadratic_tensor(self):
        """
        Builds local 18x324 quadratic collision matrix M2_node.
        Contracts local Kronecker monomial Psi(18) (x) Psi(18) (dim 324) into Psi(18).
        """
        M2 = np.zeros((18, 324), dtype=np.float64)

        # Hydrodynamic convective flux: w_i * [ (c_i.u)^2 / (2 cs4) - |u|^2 / (2 cs2) ]
        # u = sum_q g_q c_q / rho0
        for q_star in range(9):
            wi = self.w[q_star]
            for q1 in range(9): # g index
                for q2 in range(9): # g index
                    c1_dot_cstar = self.c[q1, 0] * self.c[q_star, 0] + self.c[q1, 1] * self.c[q_star, 1]
                    c2_dot_cstar = self.c[q2, 0] * self.c[q_star, 0] + self.c[q2, 1] * self.c[q_star, 1]
                    c1_dot_c2 = self.c[q1, 0] * self.c[q2, 0] + self.c[q1, 1] * self.c[q2, 1]

                    term_conv = (c1_dot_cstar * c2_dot_cstar) / (2.0 * self.cs4)
                    term_trace = c1_dot_c2 / (2.0 * self.cs2)
                    coeff = (1.0 / self.tau_v) * wi * (term_conv - term_trace) / (self.rho0**2)

                    col = q1 * 18 + q2
                    M2[q_star, col] = coeff

        # Phase-field advective flux: w_i * phi * (c_i.u) / cs2
        # phi = sum_q1 h_q1, u = sum_q2 g_q2 c_q2 / rho0
        for q_star in range(9):
            wi = self.w[q_star]
            for q1 in range(9): # h index (9 + q1)
                for q2 in range(9): # g index (q2)
                    c_star_dot_c2 = self.c[q_star, 0] * self.c[q2, 0] + self.c[q_star, 1] * self.c[q2, 1]
                    coeff = (1.0 / self.tau_phi) * wi * (c_star_dot_c2 / (self.cs2 * self.rho0))

                    col = (9 + q1) * 18 + q2
                    M2[9 + q_star, col] = coeff

        return M2

    def _build_full_carleman_matrix(self):
        """
        Assembles the complete Carleman matrix A_C in CSR format:
        For N_C = 1: A_C in R^(18N x 18N)
        For N_C = 2: A_C in R^(342N x 342N)
        """
        if self.truncation_order == 1:
            # A_C = S * M1
            # Build global M1
            rows = []
            cols = []
            vals = []
            for n in range(self.N):
                for i in range(18):
                    for j in range(18):
                        val = self.M1_node[i, j]
                        if abs(val) > 1e-15:
                            rows.append(i * self.N + n)
                            cols.append(j * self.N + n)
                            vals.append(val)
            M1_global = sp.csr_matrix((vals, (rows, cols)), shape=(self.dim_base, self.dim_base), dtype=np.float64)
            return self.S.dot(M1_global)

        elif self.truncation_order == 2:
            # Build Block Upper-Triangular Collision Matrix C_2 (342N x 342N)
            # C_2 = [[ M1_global (18N x 18N), M2_global (18N x 324N) ],
            #        [ 0,                     M1_kron2_global (324N x 324N) ]]
            
            # 1. M1_global (18N x 18N)
            r_m1, c_m1, v_m1 = [], [], []
            for n in range(self.N):
                for i in range(18):
                    for j in range(18):
                        val = self.M1_node[i, j]
                        if abs(val) > 1e-15:
                            r_m1.append(i * self.N + n)
                            c_m1.append(j * self.N + n)
                            v_m1.append(val)
            M1_global = sp.csr_matrix((v_m1, (r_m1, c_m1)), shape=(self.dim_base, self.dim_base), dtype=np.float64)

            # 2. M2_global (18N x 324N)
            r_m2, c_m2, v_m2 = [], [], []
            for n in range(self.N):
                for i in range(18):
                    for j in range(324):
                        val = self.M2_node[i, j]
                        if abs(val) > 1e-15:
                            r_m2.append(i * self.N + n)
                            c_m2.append(j * self.N + n)
                            v_m2.append(val)
            M2_global = sp.csr_matrix((v_m2, (r_m2, c_m2)), shape=(self.dim_base, 324 * self.N), dtype=np.float64)

            # 3. M1_kron2_global (324N x 324N) = (M1 (x) M1)_node
            M1_kron2_node = np.kron(self.M1_node, self.M1_node) # 324 x 324
            r_mk, c_mk, v_mk = [], [], []
            for n in range(self.N):
                for i in range(324):
                    for j in range(324):
                        val = M1_kron2_node[i, j]
                        if abs(val) > 1e-15:
                            r_mk.append(i * self.N + n)
                            c_mk.append(j * self.N + n)
                            v_mk.append(val)
            M1_kron2_global = sp.csr_matrix((v_mk, (r_mk, c_mk)), shape=(324 * self.N, 324 * self.N), dtype=np.float64)

            # Block assemble C_2
            C_2 = sp.bmat([
                [M1_global, M2_global],
                [None, M1_kron2_global]
            ], format='csr', dtype=np.float64)

            # Build Full S_C = block_diag(S, S_kron2)
            # S_kron2 permutations for ordered pairs (q1, q2)
            r_sk, c_sk, v_sk = [], [], []
            for q1 in range(18):
                q1_dir = q1 % 9
                q1_field = q1 // 9
                cx1, cy1 = self.c[q1_dir, 0], self.c[q1_dir, 1]

                for q2 in range(18):
                    q2_dir = q2 % 9
                    q2_field = q2 // 9
                    cx2, cy2 = self.c[q2_dir, 0], self.c[q2_dir, 1]

                    # Combined ordered pair index k = q1 * 18 + q2 (0..323)
                    k = q1 * 18 + q2
                    k_offset = k * self.N

                    # Directional displacement is dominated by primary velocity
                    cx = cx1
                    cy = cy1

                    for n in range(self.N):
                        x, y = self._coord(n)
                        src_idx = k_offset + n

                        tx = x + cx
                        ty = y + cy

                        target_q1 = q1_dir
                        if tx < 0 or tx >= self.nx or ty < 0 or ty >= self.ny:
                            if ty < 0 and self.free_slip_bottom:
                                target_q1 = self.refl_floor[q1_dir]
                                tx = x
                                ty = 0
                            else:
                                target_q1 = self.opp[q1_dir]
                                tx = np.clip(x, 0, self.nx - 1)
                                ty = np.clip(y, 0, self.ny - 1)

                        target_k = (q1_field * 9 + target_q1) * 18 + q2
                        target_n = self._node_idx(tx, ty)
                        dst_idx = target_k * self.N + target_n

                        r_sk.append(dst_idx)
                        c_sk.append(src_idx)
                        v_sk.append(1.0)

            S_kron2 = sp.csr_matrix((v_sk, (r_sk, c_sk)), shape=(324 * self.N, 324 * self.N), dtype=np.float64)

            S_C = sp.bmat([
                [self.S, None],
                [None, S_kron2]
            ], format='csr', dtype=np.float64)

            A_C = S_C.dot(C_2)
            return A_C

    def lift_state(self, Psi):
        """
        Lifts state vector Psi in R^(18 N) to Carleman vector Y_2 in R^(342 N):
        Y_2 = [ Psi; Psi_local^(x)2 ]
        """
        if self.truncation_order == 1:
            return Psi.copy()

        # Reshape Psi to (18, N)
        psi_mat = Psi.reshape((18, self.N))
        # Compute local Kronecker square per node: (18, 18, N) -> (324, N)
        psi_kron2 = np.einsum('in,jn->ijn', psi_mat, psi_mat).reshape((324 * self.N,))
        
        Y_2 = np.concatenate([Psi, psi_kron2])
        return Y_2

    def project_state(self, Y):
        """Projects Carleman vector Y back to physical state Psi in R^(18 N)."""
        return Y[:self.dim_base].copy()

    def step(self, Y):
        """Executes one Carleman step: Y(t+1) = A_C * Y(t)."""
        return self.A_C.dot(Y)
