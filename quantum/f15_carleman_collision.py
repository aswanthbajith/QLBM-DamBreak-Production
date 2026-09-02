"""
Phase F15: Autonomous Nonlinear Quantum Collision via Carleman Linearization.

Mathematical Formulation:
State vector at each node: z in R^18 = [f_0..f_8, g_0..g_8]^T.
Lifted Carleman state (K=2):
Y = [ z ; z (x) z ] in R^(18 + 324) = R^342.

Nonlinear Two-Phase LBM Collision Map:
z* = M1 z + M2 (z (x) z) + s_0

Carleman Matrix A_C in R^(342 x 342):
A_C = [[ M1,         M2 ],
       [ 0,  M1 (x) M1 ]]

Unitary Block-Encoding via Sz.-Nagy Dilation:
U_A in U(1024) such that <0| U_A |0> = A_C / alpha_C.
"""

from typing import Tuple, Dict, Any, Optional, List
import numpy as np
import scipy.linalg as la

from classical.d2q9 import C_X, C_Y, W, OPPOSITE


class CarlemanTwoPhaseCollision:
    """
    Second-order (K=2) Carleman Linearization engine for autonomous two-phase LBM collision.
    Constructs fixed linear matrices M1, M2 and the global Carleman block-encoded unitary U_A.
    """

    def __init__(
        self,
        nu_L: float = 0.05,
        nu_G: float = 0.05,
        tau_phi: float = 0.70,
        g_acc: float = -0.0005,
        rho_G: float = 0.1,
    ):
        self.nu_L = nu_L
        self.nu_G = nu_G
        self.tau_phi = tau_phi
        self.g_acc = g_acc
        self.rho_G = rho_G

        self.dim_z = 18
        self.dim_z2 = 324
        self.dim_Y = self.dim_z + self.dim_z2  # 342

        # Build fixed polynomial collision matrices
        self._build_carleman_matrices()

    def _build_carleman_matrices(self):
        """Constructs fixed M1 (18x18), M2 (18x324), and Carleman matrix A_C (342x342)."""
        # Average reference relaxation rates
        nu_0 = 0.5 * (self.nu_L + self.nu_G)
        tau_f0 = 3.0 * nu_0 + 0.5
        omega_f0 = 1.0 / tau_f0
        omega_g0 = 1.0 / self.tau_phi

        # 1. Linear matrix M1 (18x18)
        M_f1 = (1.0 - omega_f0) * np.eye(9) + omega_f0 * np.outer(W, np.ones(9))
        M_g1 = (1.0 - omega_g0) * np.eye(9) + omega_g0 * np.outer(W, np.ones(9))
        M1 = la.block_diag(M_f1, M_g1)

        # 2. Quadratic coupling matrix M2 (18x324)
        # Encodes nonlinear velocity terms u = j / rho and alpha*u coupling
        M2 = np.zeros((self.dim_z, self.dim_z2), dtype=np.float64)

        for i in range(9):
            for j in range(9):
                for k in range(9):
                    idx_jk = j * 18 + k
                    # Hydrodynamic velocity correction: 3 * w_i * c_i . (c_j f_j)
                    c_dot_c = float(C_X[i] * C_X[j] + C_Y[i] * C_Y[j])
                    term_f = 3.0 * omega_f0 * W[i] * c_dot_c
                    M2[i, idx_jk] += term_f * 0.1

                    # Phase-field velocity advection: 3 * w_i * c_i . (c_j g_k)
                    idx_g_jk = (9 + j) * 18 + (9 + k)
                    term_g = 3.0 * omega_g0 * W[i] * c_dot_c
                    M2[9 + i, idx_g_jk] += term_g * 0.1

        # 3. Assemble K=2 Carleman Matrix A_C (342x342)
        A_C = np.zeros((self.dim_Y, self.dim_Y), dtype=np.float64)
        A_C[:self.dim_z, :self.dim_z] = M1
        A_C[:self.dim_z, self.dim_z:] = M2
        A_C[self.dim_z:, self.dim_z:] = np.kron(M1, M1)

        self.M1 = M1
        self.M2 = M2
        self.A_C = A_C

        # 4. Sz.-Nagy Unitary Dilation of A_C (embedded into 512x512, dilated into 1024x1024)
        pad_dim = 512
        A_padded = np.zeros((pad_dim, pad_dim), dtype=np.complex128)
        A_padded[:self.dim_Y, :self.dim_Y] = self.A_C

        norm_A = float(la.norm(A_padded, 2))
        alpha_A = max(1.05 * norm_A, 1.0)
        A_scaled = A_padded / alpha_A

        D = la.sqrtm(np.eye(pad_dim, dtype=np.complex128) - A_scaled.conj().T @ A_scaled)
        D_star = la.sqrtm(np.eye(pad_dim, dtype=np.complex128) - A_scaled @ A_scaled.conj().T)
        U_A = np.block([[A_scaled, D_star], [D, -A_scaled.conj().T]])

        self.alpha_A = alpha_A
        self.U_A = U_A
        self.p0_success = 1.0 / (alpha_A**2)

    def lift_state(self, z: np.ndarray) -> np.ndarray:
        """Lifts 18-element state vector z to 342-element Carleman vector Y = [z; z (x) z]."""
        z2 = np.kron(z, z)
        return np.concatenate([z, z2])

    def evaluate_carleman_collision(self, z: np.ndarray) -> Tuple[np.ndarray, Dict[str, float]]:
        """
        Executes autonomous Carleman collision on local node state z:
        Y = [z; z (x) z]
        Y* = A_C Y
        z* = Y*[:18]
        """
        Y = self.lift_state(z)
        Y_post = self.A_C @ Y
        z_post = Y_post[:self.dim_z]

        # Check tensor manifold consistency
        z2_expected = np.kron(z_post, z_post)
        z2_actual = Y_post[self.dim_z:]
        norm_exp = float(la.norm(z2_expected)) + 1e-14
        manifold_defect = float(la.norm(z2_actual - z2_expected) / norm_exp)

        unitarity_err = float(la.norm(self.U_A.conj().T @ self.U_A - np.eye(1024), 2))

        meta = {
            "manifold_defect": manifold_defect,
            "unitarity_error": unitarity_err,
            "alpha_A": self.alpha_A,
            "p0_success": self.p0_success,
        }
        return z_post, meta
