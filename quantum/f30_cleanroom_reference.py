"""
Phase F30: Completely Independent Clean-Room Multi-Lattice LBM Reference Engine.

Strict Anti-Circularity Implementation:
- ZERO imports from quantum/
- Implements exact discrete D2Q9 two-phase BGK, coordinate streaming, and solid bounce-back from first principles
- Supports arbitrary Nx x Ny lattices and multi-step evaluation.
"""

from typing import Dict, Any, List, Tuple
import numpy as np


class F30CleanRoomScalableReference:
    """
    Independent scalable reference engine for multi-lattice discrete QLBM validation.
    """

    C_X = [0, 1, 0, -1, 0, 1, -1, -1, 1]
    C_Y = [0, 0, 1, 0, -1, 1, 1, -1, -1]
    OPPOSITE = [0, 3, 4, 1, 2, 7, 8, 5, 6]
    W = [4.0 / 9.0] + [1.0 / 9.0] * 4 + [1.0 / 36.0] * 4

    def __init__(self, nx: int = 4, ny: int = 4, frac_bits: int = 12):
        self.nx = nx
        self.ny = ny
        self.frac_bits = frac_bits
        self.scale = 1 << frac_bits
        self.w_fixed = [int(round(w * self.scale)) for w in self.W]

        self.solid_mask = np.zeros((self.ny, self.nx), dtype=bool)
        self.solid_mask[0, :] = True
        self.solid_mask[-1, :] = True
        self.solid_mask[:, 0] = True
        self.solid_mask[:, -1] = True

    def step(
        self,
        f_in: np.ndarray,
        g_in: np.ndarray,
        omega_f_fixed: int = 4096,
        omega_g_fixed: int = 5851,
        g_acc_fixed: int = -2,
    ) -> Tuple[np.ndarray, np.ndarray]:
        """
        Executes one full independent timestep: BGK -> Streaming -> Boundary.
        """
        ny, nx = self.ny, self.nx
        f_coll = np.zeros_like(f_in)
        g_coll = np.zeros_like(g_in)

        # 1. Local BGK Collision at each node
        for y in range(ny):
            for x in range(nx):
                f_node = [int(f_in[i, y, x]) for i in range(9)]
                g_node = [int(g_in[i, y, x]) for i in range(9)]

                rho = sum(f_node)
                alpha = sum(g_node)

                jx = sum(f_node[i] * self.C_X[i] for i in range(9))
                jy = sum(f_node[i] * self.C_Y[i] for i in range(9))
                jy += (((rho * g_acc_fixed) >> self.frac_bits)) // 2

                ux = (jx << self.frac_bits) // max(rho, 1)
                uy = (jy << self.frac_bits) // max(rho, 1)

                ux2 = (ux * ux) >> self.frac_bits
                uy2 = (uy * uy) >> self.frac_bits
                u2 = ux2 + uy2
                term_u2 = (3 * u2) // 2

                u_diag1 = ux + uy
                u_diag2 = -ux + uy
                u_diag1_sq = (u_diag1 * u_diag1) >> self.frac_bits
                u_diag2_sq = (u_diag2 * u_diag2) >> self.frac_bits

                c_dot_u = [0, ux, uy, -ux, -uy, u_diag1, u_diag2, -u_diag1, -u_diag2]
                c_dot_u_sq = [0, ux2, uy2, ux2, uy2, u_diag1_sq, u_diag2_sq, u_diag1_sq, u_diag2_sq]

                f_out = [0] * 9
                g_out = [0] * 9

                for i in range(1, 9):
                    cu = c_dot_u[i]
                    cu2 = c_dot_u_sq[i]

                    bracket_f = self.scale + 3 * cu + (9 * cu2) // 2 - term_u2
                    term_f = (rho * bracket_f) >> self.frac_bits
                    f_eq = (self.w_fixed[i] * term_f) >> self.frac_bits

                    bracket_g = self.scale + 3 * cu
                    term_g = (alpha * bracket_g) >> self.frac_bits
                    g_eq = (self.w_fixed[i] * term_g) >> self.frac_bits

                    f_out[i] = f_node[i] + (((f_eq - f_node[i]) * omega_f_fixed) >> self.frac_bits)
                    g_out[i] = g_node[i] + (((g_eq - g_node[i]) * omega_g_fixed) >> self.frac_bits)

                f_out[0] = rho - sum(f_out[1:9])
                g_out[0] = alpha - sum(g_out[1:9])

                for i in range(9):
                    f_coll[i, y, x] = f_out[i]
                    g_coll[i, y, x] = g_out[i]

        # 2. Coordinate Streaming Permutation
        f_streamed = np.zeros_like(f_coll)
        g_streamed = np.zeros_like(g_coll)
        for i in range(9):
            dx = self.C_X[i]
            dy = self.C_Y[i]
            f_streamed[i] = np.roll(np.roll(f_coll[i], dx, axis=1), dy, axis=0)
            g_streamed[i] = np.roll(np.roll(g_coll[i], dx, axis=1), dy, axis=0)

        # 3. Bounce-Back Boundary Involution
        f_next = np.copy(f_streamed)
        g_next = np.copy(g_streamed)
        for i in range(9):
            opp_i = self.OPPOSITE[i]
            f_next[opp_i, self.solid_mask] = f_streamed[i, self.solid_mask]
            g_next[opp_i, self.solid_mask] = g_streamed[i, self.solid_mask]

        return f_next, g_next
