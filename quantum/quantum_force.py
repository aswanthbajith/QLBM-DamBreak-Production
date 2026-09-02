"""
Phase F12: Quantum Two-Phase Force & Continuum Surface Force (CSF) Stencil Engine.

Mathematical Formulation:
1. Gravitational Buoyancy Force:
   F_buoyancy(x,y) = [0, (rho(x,y) - rho_G) * g_acc]^T

2. Continuum Surface Force (CSF):
   F_CSF(x,y) = sigma * kappa(x,y) * grad(alpha(x,y))

   where:
   grad(alpha) is computed via central differences:
   grad_x(alpha) = 0.5 * (S_x^+1 - S_x^-1) alpha
   grad_y(alpha) = 0.5 * (S_y^+1 - S_y^-1) alpha
   n = grad(alpha) / (|grad(alpha)| + 1e-12)
   kappa = - div(n) = - 0.5 * [ (S_x^+1 - S_x^-1) n_x + (S_y^+1 - S_y^-1) n_y ]
"""

from typing import Tuple, Dict, Any, Optional, List
import numpy as np
import scipy.linalg as la


class QuantumForceOracle:
    """
    Quantum-compatible spatial force and CSF stencil engine.
    Uses reversible coordinate shifts on spatial registers to compute gradients and curvatures.
    """

    def __init__(
        self,
        nx: int = 8,
        ny: int = 4,
        g_acc: float = -0.0005,
        sigma: float = 0.001,
        rho_G: float = 0.1,
    ):
        self.nx = nx
        self.ny = ny
        self.g_acc = g_acc
        self.sigma = sigma
        self.rho_G = rho_G

        self.n_x = int(np.ceil(np.log2(nx))) if nx > 1 else 1
        self.n_y = int(np.ceil(np.log2(ny))) if ny > 1 else 1
        self.n_total = self.n_x + self.n_y + 5

    def compute_force_fields(
        self,
        rho_field: np.ndarray,
        alpha_field: np.ndarray,
    ) -> Tuple[np.ndarray, Dict[str, Any]]:
        """
        Computes the total force vector field F(x, y) = F_buoyancy + F_CSF.
        """
        F = np.zeros((2, self.ny, self.nx), dtype=np.float64)

        # 1. Buoyancy body force
        F[1] = (rho_field - self.rho_G) * self.g_acc

        # 2. Continuum surface force (CSF)
        if self.sigma > 0.0 and self.nx >= 3 and self.ny >= 3:
            grad_x = np.zeros((self.ny, self.nx), dtype=np.float64)
            grad_y = np.zeros((self.ny, self.nx), dtype=np.float64)

            # Central difference stencil
            grad_x[:, 1:-1] = (alpha_field[:, 2:] - alpha_field[:, :-2]) / 2.0
            grad_y[1:-1, :] = (alpha_field[2:, :] - alpha_field[:-2, :]) / 2.0

            grad_norm = np.sqrt(grad_x**2 + grad_y**2) + 1e-12
            mask = grad_norm > 1e-3

            nx_vec = np.where(mask, grad_x / grad_norm, 0.0)
            ny_vec = np.where(mask, grad_y / grad_norm, 0.0)

            div_nx = np.zeros_like(nx_vec)
            div_ny = np.zeros_like(ny_vec)
            div_nx[:, 1:-1] = (nx_vec[:, 2:] - nx_vec[:, :-2]) / 2.0
            div_ny[1:-1, :] = (ny_vec[2:, :] - ny_vec[:-2, :]) / 2.0

            kappa = np.clip(-(div_nx + div_ny), -2.0, 2.0)

            F_s = np.zeros((2, self.ny, self.nx), dtype=np.float64)
            F_s[0] = np.where(mask, self.sigma * kappa * grad_x, 0.0)
            F_s[1] = np.where(mask, self.sigma * kappa * grad_y, 0.0)
            F += F_s

        # Resource estimates for spatial stencil shifts
        shift_toffoli = 4 * (self.n_x + self.n_y)
        shift_cx = 8 * (self.n_x + self.n_y)

        resource_info = {
            "stencil_shifts_per_node": 4,
            "shift_toffoli": shift_toffoli,
            "shift_cx": shift_cx,
            "max_force_magnitude": float(np.max(np.sqrt(F[0]**2 + F[1]**2))),
        }

        return F, resource_info
