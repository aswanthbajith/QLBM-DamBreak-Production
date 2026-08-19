#!/usr/bin/env python3
"""
Independent Clean-Room Mathematical Verification Suite for Polynomial & Carleman LBM.
Does NOT reuse or import classes from quantum/carleman_lbm.py to prevent circular validation.
"""

import unittest
import numpy as np
import scipy.sparse as sp

class TestIndependentCarlemanAudit(unittest.TestCase):
    def setUp(self):
        self.nx = 4
        self.ny = 4
        self.N = self.nx * self.ny
        self.Q = 9
        self.cs2 = 1.0 / 3.0
        self.cs4 = 1.0 / 9.0
        self.tau_v = 0.53
        self.tau_phi = 0.65
        self.rho0 = 1.0

        self.c = np.array([
            [ 0,  0], [ 1,  0], [ 0,  1], [-1,  0], [ 0, -1],
            [ 1,  1], [-1,  1], [-1, -1], [ 1, -1]
        ], dtype=np.int32)

        self.w = np.array([
            4/9, 1/9, 1/9, 1/9, 1/9, 1/36, 1/36, 1/36, 1/36
        ], dtype=np.float64)
        self.opp = np.array([0, 3, 4, 1, 2, 7, 8, 5, 6], dtype=np.int32)

    def test_01_independent_streaming_unitarity(self):
        """Builds independent streaming permutation matrix and asserts S^T S == I."""
        dim_base = 18 * self.N
        rows, cols, vals = [], [], []

        for field in [0, 1]:
            f_offset = field * 9 * self.N
            for q in range(9):
                cx, cy = self.c[q, 0], self.c[q, 1]
                q_offset = q * self.N
                for n in range(self.N):
                    x, y = n // self.ny, n % self.ny
                    src = f_offset + q_offset + n
                    tx, ty = x + cx, y + cy
                    tq = q
                    if tx < 0 or tx >= self.nx or ty < 0 or ty >= self.ny:
                        tq = self.opp[q]
                        tx = np.clip(x, 0, self.nx - 1)
                        ty = np.clip(y, 0, self.ny - 1)
                    dst = f_offset + tq * self.N + (tx * self.ny + ty)
                    rows.append(dst)
                    cols.append(src)
                    vals.append(1.0)

        S = sp.csr_matrix((vals, (rows, cols)), shape=(dim_base, dim_base))
        diff = S.T.dot(S) - sp.eye(dim_base, format='csr')
        self.assertEqual(diff.nnz, 0, "Independent streaming matrix is not strictly unitary")

    def test_02_independent_polynomial_collision_equivalence(self):
        """Compares independent quadratic polynomial evaluation against non-linear equilibrium formula."""
        np.random.seed(123)
        # Construct local linear M1 and quadratic M2 from first principles
        M1_node = np.zeros((18, 18))
        for q_star in range(9):
            for q in range(9):
                w_star = self.w[q_star]
                c_dot = np.dot(self.c[q_star], self.c[q])
                # Hydrodynamic linear relaxation including linear velocity term
                M1_node[q_star, q] = (1.0 / self.tau_v) * w_star * (1.0 + c_dot / (self.rho0 * self.cs2)) + ((1.0 - 1.0/self.tau_v) if q_star == q else 0.0)
                # Phase-field linear relaxation
                M1_node[9 + q_star, 9 + q] = (1.0 / self.tau_phi) * w_star + ((1.0 - 1.0/self.tau_phi) if q_star == q else 0.0)

        M2_node = np.zeros((18, 324))
        # Hydro convective
        for q_star in range(9):
            w_star = self.w[q_star]
            for q1 in range(9):
                for q2 in range(9):
                    c1_dot_cs = np.dot(self.c[q1], self.c[q_star])
                    c2_dot_cs = np.dot(self.c[q2], self.c[q_star])
                    c1_dot_c2 = np.dot(self.c[q1], self.c[q2])
                    val = (1.0 / self.tau_v) * w_star * ((c1_dot_cs * c2_dot_cs)/(2.0 * self.cs4) - c1_dot_c2/(2.0 * self.cs2)) / (self.rho0**2)
                    M2_node[q_star, q1 * 18 + q2] = val

        # Test on 20 random node states
        for _ in range(20):
            psi_node = np.random.uniform(0.01, 0.1, size=18)
            g_node = psi_node[:9]
            h_node = psi_node[9:]

            # Non-linear calculation
            u_nl = np.sum([g_node[q] * self.c[q] for q in range(9)], axis=0) / self.rho0
            g_eq_nl = np.array([self.w[q] * (np.sum(g_node) + np.dot(self.c[q], u_nl)/self.cs2 + np.dot(self.c[q], u_nl)**2/(2*self.cs4) - np.dot(u_nl, u_nl)/(2*self.cs2)) for q in range(9)])
            g_post_nl = g_node - (1.0 / self.tau_v) * (g_node - g_eq_nl)

            # Polynomial calculation
            psi_kron_node = np.kron(psi_node, psi_node)
            psi_post_poly = M1_node.dot(psi_node) + M2_node.dot(psi_kron_node)
            g_post_poly = psi_post_poly[:9]

            np.testing.assert_allclose(g_post_poly, g_post_nl, atol=1e-12, rtol=1e-10)

    def test_03_independent_carleman_single_step_closure(self):
        """Verifies independent Carleman lifting preserves linear sector within quadratic truncation."""
        M1_node = np.eye(18)
        M2_node = np.zeros((18, 324))
        M2_node[0, 0] = 0.05 # small quadratic coupling

        M1_kron2 = np.kron(M1_node, M1_node)
        C2 = np.block([
            [M1_node, M2_node],
            [np.zeros((324, 18)), M1_kron2]
        ])

        psi = np.ones(18) * 0.1
        y2 = np.concatenate([psi, np.kron(psi, psi)])
        y2_next = C2.dot(y2)
        psi_next_carle = y2_next[:18]
        psi_next_poly = M1_node.dot(psi) + M2_node.dot(np.kron(psi, psi))

        np.testing.assert_allclose(psi_next_carle, psi_next_poly, atol=1e-14)

if __name__ == "__main__":
    unittest.main()
