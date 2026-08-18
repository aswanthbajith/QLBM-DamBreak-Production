#!/usr/bin/env python3
"""
Exact Matrix & Tensor Formulation for Two-Phase Velocity-Based LBM.

State Vector:
Psi(t) = [g(t); h(t)] in R^(18 N)

Operators:
1. S: Linear spatial permutation & boundary reflection matrix in R^(18N x 18N) (Unitary)
2. M1: Linear collision relaxation matrix in R^(18N x 18N) (Block-Diagonal)
3. M2: Local quadratic convective and advective tensor kernel
4. b_force: Affine body force vector in R^(18N)
"""

import numpy as np
import scipy.sparse as sp
from two_phase_physics import TwoPhaseProperties

class MatrixTwoPhaseLBM2D:
    def __init__(self, nx, ny,
                 rho_L=1.0, rho_G=0.1,
                 nu_L=0.01, nu_G=0.01,
                 sigma=0.001,
                 gx=0.0, gy=-4.0e-4,
                 width=4.0, mobility=0.05,
                 enable_surface_tension=True,
                 free_slip_bottom=True):
        
        self.nx = nx
        self.ny = ny
        self.N = nx * ny
        self.Q = 9
        self.dim_single = self.Q * self.N
        self.dim_total = 2 * self.dim_single # 18 N

        self.rho_L = rho_L
        self.rho_G = rho_G
        self.nu_L = nu_L
        self.nu_G = nu_G
        self.sigma = sigma
        self.gx = gx
        self.gy = gy
        self.width = width
        self.mobility = mobility
        self.enable_surface_tension = enable_surface_tension
        self.free_slip_bottom = free_slip_bottom

        self.cs2 = 1.0 / 3.0
        self.cs4 = 1.0 / 9.0

        self.props = TwoPhaseProperties(
            rho_L=rho_L, rho_G=rho_G,
            nu_L=nu_L, nu_G=nu_G,
            sigma=sigma, width=width,
            mobility=mobility
        )

        self.c = self.props.c
        self.w = self.props.w
        self.opp = np.array([0, 3, 4, 1, 2, 7, 8, 5, 6], dtype=np.int32)
        self.refl_floor = np.array([0, 1, 4, 3, 2, 8, 7, 6, 5], dtype=np.int32)

        # Build Sparse Linear Streaming Matrix S in CSR format
        self.S = self._build_streaming_matrix()
        # Build Sparse Linear Collision Matrix M1
        self.M1 = self._build_linear_collision_matrix()

    def _node_idx(self, x, y):
        return x * self.ny + y

    def _coord(self, n):
        return n // self.ny, n % self.ny

    def _build_streaming_matrix(self):
        """
        Builds the global linear permutation and boundary reflection matrix S in R^(18N x 18N).
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
        Builds the linear relaxation operator M1 for baseline reference viscosity/mobility.
        """
        rows = []
        cols = []
        vals = []

        tau_v0 = self.nu_L / self.cs2 + 0.5
        tau_phi0 = self.mobility / self.cs2 + 0.5

        # 1. Hydrodynamic linear relaxation (g)
        for q_star in range(self.Q):
            for q in range(self.Q):
                wi_term = self.w[q_star]
                coeff = (1.0 / tau_v0) * wi_term
                if q_star == q:
                    coeff += (1.0 - 1.0 / tau_v0)

                if abs(coeff) > 1e-15:
                    for n in range(self.N):
                        rows.append(q_star * self.N + n)
                        cols.append(q * self.N + n)
                        vals.append(coeff)

        # 2. Phase-field linear relaxation (h)
        h_offset = self.dim_single
        for q_star in range(self.Q):
            for q in range(self.Q):
                coeff = (1.0 / tau_phi0) * self.w[q_star]
                if q_star == q:
                    coeff += (1.0 - 1.0 / tau_phi0)

                if abs(coeff) > 1e-15:
                    for n in range(self.N):
                        rows.append(h_offset + q_star * self.N + n)
                        cols.append(h_offset + q * self.N + n)
                        vals.append(coeff)

        M1_sparse = sp.csr_matrix((vals, (rows, cols)), shape=(self.dim_total, self.dim_total), dtype=np.float64)
        return M1_sparse

    def evaluate_collision(self, Psi, u_prev, v_prev):
        """
        Evaluates exact local collision on state vector Psi in R^(18 N).
        """
        g_arr = Psi[:self.dim_single].reshape((self.Q, self.nx, self.ny))
        h_arr = Psi[self.dim_single:].reshape((self.Q, self.nx, self.ny))

        phi = np.clip(np.sum(h_arr, axis=0), 0.0, 1.0)
        rho = self.props.density(phi)
        tau_v = self.props.relaxation_time(phi)
        tau_phi = self.mobility / self.cs2 + 0.5

        # 1. Body forces
        # Gravitational Buoyancy Force
        Fx = (rho - self.rho_G) * self.gx
        Fy = (rho - self.rho_G) * self.gy

        # Surface tension
        if self.enable_surface_tension and self.sigma > 0.0:
            Fx_s, Fy_s, _ = self.props.compute_curvature_and_csf(phi)
            Fx += Fx_s
            Fy += Fy_s

        # 2. Phase-Field Collision (Allen-Cahn with counter-gradient sharpening)
        grad_x, grad_y = self.props.compute_gradient(phi)
        grad_mag = np.sqrt(grad_x**2 + grad_y**2) + 1e-12
        nx_norm = grad_x / grad_mag
        ny_norm = grad_y / grad_mag

        bulk_factor = (1.0 - 4.0 * (phi - 0.5)**2) / self.width
        F_phi_x = self.mobility * (grad_x - bulk_factor * nx_norm)
        F_phi_y = self.mobility * (grad_y - bulk_factor * ny_norm)

        h_post = np.zeros_like(h_arr)
        for i in range(self.Q):
            wi = self.w[i]
            cx, cy = self.c[i, 0], self.c[i, 1]
            cu = cx * u_prev + cy * v_prev

            heq = wi * phi * (1.0 + cu / self.cs2)
            Si = (1.0 - 0.5 / tau_phi) * wi * (cx * F_phi_x + cy * F_phi_y) / self.cs2
            h_post[i] = h_arr[i] - (1.0 / tau_phi) * (h_arr[i] - heq) + Si

        # 3. Hydrodynamic Collision (Velocity-Based with Guo Forcing)
        sum_g = np.sum(g_arr, axis=0)
        u2 = u_prev**2 + v_prev**2

        coeff_g = 1.0 - 0.5 / tau_v
        Fx_scaled = Fx / rho
        Fy_scaled = Fy / rho

        g_post = np.zeros_like(g_arr)
        for i in range(self.Q):
            wi = self.w[i]
            cx, cy = self.c[i, 0], self.c[i, 1]
            cu = cx * u_prev + cy * v_prev

            geq = wi * (sum_g + cu / self.cs2 + 0.5 * cu**2 / self.cs4 - 0.5 * u2 / self.cs2)

            term1 = (cx - u_prev) * Fx_scaled + (cy - v_prev) * Fy_scaled
            term2 = (cu / self.cs2) * (cx * Fx_scaled + cy * Fy_scaled)
            Fi = coeff_g * wi * (term1 / self.cs2 + term2 / self.cs2)

            g_post[i] = g_arr[i] - (1.0 / tau_v) * (g_arr[i] - geq) + Fi

        Psi_post = np.zeros(self.dim_total, dtype=np.float64)
        Psi_post[:self.dim_single] = g_post.flatten()
        Psi_post[self.dim_single:] = h_post.flatten()

        return Psi_post, Fx, Fy, rho

    def step(self, Psi, u_prev, v_prev):
        """
        Executes one complete time step via operator composition:
        Psi(t+1) = S * Psi_post(Psi(t))
        """
        Psi_post, Fx, Fy, rho = self.evaluate_collision(Psi, u_prev, v_prev)
        Psi_next = self.S.dot(Psi_post)

        # Update macroscopic velocity from streamed state for next step
        g_streamed = Psi_next[:self.dim_single].reshape((self.Q, self.nx, self.ny))
        sum_gc_x = np.zeros((self.nx, self.ny), dtype=np.float64)
        sum_gc_y = np.zeros((self.nx, self.ny), dtype=np.float64)
        for i in range(self.Q):
            sum_gc_x += g_streamed[i] * self.c[i, 0]
            sum_gc_y += g_streamed[i] * self.c[i, 1]

        u_next = sum_gc_x + 0.5 * Fx / rho
        v_next = sum_gc_y + 0.5 * Fy / rho

        # Boundary enforcement
        u_next[0, :] = 0.0; u_next[-1, :] = 0.0; u_next[:, -1] = 0.0
        v_next[0, :] = 0.0; v_next[-1, :] = 0.0; v_next[:, -1] = 0.0
        if not self.free_slip_bottom:
            u_next[:, 0] = 0.0
        v_next[:, 0] = 0.0

        return Psi_next, u_next, v_next
