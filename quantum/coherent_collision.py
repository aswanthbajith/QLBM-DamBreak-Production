"""
Phase F13: Coherent Collision Oracle & Sz.-Nagy Unitary Dilation.

Mathematical Formulation:
1. Hydrodynamic & Phase-Field Collision:
   f_i^* = (1 - omega_f) f_i + omega_f f_i^eq(rho, u) + S_i(F, u)
   g_i^* = (1 - omega_g) g_i + omega_g g_i^eq(alpha, u)

2. Linear Block-Matrix Synthesis:
   C(alpha, u, F/rho) = block_diag(M_f(alpha, u, F/rho), M_g(u))

3. 6-Qubit Sz.-Nagy Unitary Dilation U_C in U(64):
   U_C = [[ C/alpha_C,  D_* ],
          [ D,         -C†/alpha_C ]]
   where D = sqrt(I - C†C/alpha_C^2), D_* = sqrt(I - CC†/alpha_C^2).
"""

from typing import Tuple, Dict, Any, Optional, List
import numpy as np
import scipy.linalg as la

from classical.d2q9 import C_X, C_Y, W, OPPOSITE
from quantum.coherent_parameter_oracle import FixedPointArithmetic, build_coupled_collision_matrix


class CoherentCollisionOracle:
    """
    Coherent quantum collision engine.
    Synthesizes unitary block-encoded collision operators directly from coherent parameter registers.
    """

    def __init__(
        self,
        nu_L: float = 0.05,
        nu_G: float = 0.05,
        tau_phi: float = 0.70,
        precision_format: str = "Q4.12",
    ):
        self.nu_L = nu_L
        self.nu_G = nu_G
        self.tau_phi = tau_phi
        self.fp = FixedPointArithmetic(m=4, n=12) if precision_format == "Q4.12" else FixedPointArithmetic(m=4, n=8)

    def execute_coherent_node_collision(
        self,
        z_node: np.ndarray,
        rho: float,
        alpha: float,
        u_vec: np.ndarray,
        F_vec: np.ndarray,
    ) -> Tuple[np.ndarray, Dict[str, Any]]:
        """
        Applies local unitary collision dilation to 18-element state vector z_node = [f_0..f_8, g_0..g_8].
        """
        C_mat, alpha_C, U_C, diag = build_coupled_collision_matrix(
            alpha=alpha,
            u_vec=u_vec,
            rho=rho,
            F_vec=F_vec,
            alpha_raw=alpha,
            nu_L=self.nu_L,
            nu_G=self.nu_G,
            tau_g=self.tau_phi,
        )

        z_pad = np.zeros(64, dtype=np.complex128)
        z_pad[:18] = z_node

        psi_out = alpha_C * (U_C @ z_pad)
        z_post = np.real(psi_out[:18])

        unitarity_err = float(la.norm(U_C.conj().T @ U_C - np.eye(64), 2))

        meta = {
            "alpha_C": alpha_C,
            "p0_success": 1.0 / (alpha_C**2),
            "unitarity_error": unitarity_err,
            "tau_f": diag["tau_f"],
            "omega_f": diag["omega_f"],
        }
        return z_post, meta
