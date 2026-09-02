"""
Phase F11: Multi-Phase Coupling, Scaled Dam-Break Validation & Error Localization.

Mathematical Architecture:
1. State Representation:
   Hilbert space H = H_x (x) H_y (x) H_vel (x) H_phase (n_total = n_x + n_y + 5 data qubits)
   Qubit Layout:
   - Qubit 0: Phase selector p in {0=f, 1=g}
   - Qubits 1..4: Discrete velocity i in {0..8} (9..15 idle padding)
   - Qubits 5..(4+n_y): Spatial coordinate y in {0..Ny-1}
   - Qubits (5+n_y)..(4+n_y+n_x): Spatial coordinate x in {0..Nx-1}
   Index Formula: (x << (5 + n_y)) | (y << 5) | (i << 1) | p

2. Coupled Local Collision Operator with Guo Body Forcing:
   C(alpha, u, F/rho) = block_diag(M_f(alpha, u, F/rho), M_g(u))
   Embedded via 6-qubit Sz.-Nagy unitary dilation U_C in U(64).

3. Exact Reversible Quantum Arithmetic Streaming (S_arith):
   S_arith |x, y, i, p> = |(x + c_ix) mod Nx, (y + c_iy) mod Ny, i, p>

4. Generalized Physical Boundary Mask (B_mask):
   B_mask |x, y, i, p> = |x, y, opp(i), p> on solid perimeter nodes (B^2 = I, B†B = I).

5. Multi-Phase Dam-Break Couplings:
   - Buoyancy Gravity Force: F_buoyancy = [0, (rho - rho_G) * g_acc]
   - Continuum Surface Force (CSF): F_s = sigma * kappa * grad(alpha)
   - Viscosity Relaxation: nu_mix(alpha) = alpha * nu_L + (1 - alpha) * nu_G, tau_f = 3*nu_mix + 0.5
"""

from typing import Tuple, Dict, Any, Optional, List
import numpy as np
import scipy.linalg as la

from classical.d2q9 import C_X, C_Y, W, OPPOSITE
from classical.equilibrium import compute_equilibrium
from classical.streaming import stream
from classical.level4_two_phase import Level4TwoPhaseLBM
from quantum.physical_boundary_mask import PhysicalBoundaryMask
from quantum.parameterized_collision_oracle import (
    build_parameterized_collision_matrix,
    ParameterizedQuantumCollisionOracle,
)


def build_coupled_collision_matrix(
    alpha: float,
    u_vec: np.ndarray,
    rho: float,
    F_vec: np.ndarray,
    alpha_raw: Optional[float] = None,
    nu_L: float = 0.05,
    nu_G: float = 0.05,
    tau_g: float = 0.70,
) -> Tuple[np.ndarray, float, np.ndarray, Dict[str, Any]]:
    """
    Constructs the exact 18x18 parameterized collision matrix C(alpha, u, F/rho)
    including Guo body-force source term, and its 6-qubit Sz.-Nagy dilation U_C in U(64).
    """
    nu_mix = alpha * nu_L + (1.0 - alpha) * nu_G
    tau_f = 3.0 * nu_mix + 0.5
    omega_f = 1.0 / tau_f
    omega_g = 1.0 / tau_g

    u2 = float(u_vec[0]**2 + u_vec[1]**2)
    u_dot_F = float(u_vec[0] * F_vec[0] + u_vec[1] * F_vec[1])

    M_f = np.zeros((9, 9), dtype=np.float64)
    M_g = np.zeros((9, 9), dtype=np.float64)

    raw_val = alpha_raw if alpha_raw is not None else alpha
    ratio_g = (alpha / (raw_val + 1e-15)) if abs(raw_val) > 1e-12 else 1.0

    for i in range(9):
        c_dot_u = float(C_X[i] * u_vec[0] + C_Y[i] * u_vec[1])
        c_dot_F = float(C_X[i] * F_vec[0] + C_Y[i] * F_vec[1])

        eq_factor_f = 1.0 + 3.0 * c_dot_u + 4.5 * (c_dot_u**2) - 1.5 * u2
        eq_factor_g = (1.0 + 3.0 * c_dot_u) * ratio_g

        guo_term = 0.0
        if rho > 1e-12:
            term_force = 3.0 * c_dot_F + 9.0 * c_dot_u * c_dot_F - 3.0 * u_dot_F
            guo_term = (1.0 - 0.5 * omega_f) * (term_force / rho)

        for j in range(9):
            delta_ij = 1.0 if i == j else 0.0
            M_f[i, j] = (1.0 - omega_f) * delta_ij + omega_f * W[i] * eq_factor_f + W[i] * guo_term
            M_g[i, j] = (1.0 - omega_g) * delta_ij + omega_g * W[i] * eq_factor_g

    C_mat = np.block([[M_f, np.zeros((9, 9))], [np.zeros((9, 9)), M_g]])

    # 6-qubit Sz.-Nagy dilation
    norm_C = float(la.norm(C_mat, 2))
    alpha_C = max(1.01 * norm_C, 1.001)

    C_scaled = C_mat / alpha_C
    D = la.sqrtm(np.eye(18) - C_scaled.T @ C_scaled)
    D_star = la.sqrtm(np.eye(18) - C_scaled @ C_scaled.T)

    U_C = np.zeros((64, 64), dtype=np.complex128)
    U_C[:18, :18] = C_scaled
    U_C[:18, 32:50] = D_star
    U_C[32:50, :18] = D
    U_C[32:50, 32:50] = -C_scaled.T
    U_C[18:32, 18:32] = np.eye(14)
    U_C[50:, 50:] = np.eye(14)

    p0 = 1.0 / (alpha_C**2)
    diag_info = {
        "alpha_C": alpha_C,
        "norm_C": norm_C,
        "p0": p0,
        "tau_f": tau_f,
        "omega_f": omega_f,
    }
    return C_mat, alpha_C, U_C, diag_info


class PhaseF11ScaledTwoPhaseQLBM:
    """
    Scalable Multi-Node Quantum Two-Phase Dam-Break Lattice Boltzmann Solver.
    """

    def __init__(
        self,
        nx: int = 4,
        ny: int = 4,
        rho_L: float = 1.0,
        rho_G: float = 0.1,
        nu_L: float = 0.05,
        nu_G: float = 0.05,
        tau_phi: float = 0.70,
        sigma: float = 0.0,
        g_acc: float = 0.0,
        dam_width_ratio: float = 0.5,
        dam_height_ratio: float = 0.5,
    ):
        self.nx = nx
        self.ny = ny
        self.rho_L = rho_L
        self.rho_G = rho_G
        self.nu_L = nu_L
        self.nu_G = nu_G
        self.tau_phi = tau_phi
        self.sigma = sigma
        self.g_acc = g_acc
        self.dam_width_ratio = dam_width_ratio
        self.dam_height_ratio = dam_height_ratio

        self.n_x = int(np.ceil(np.log2(nx))) if nx > 1 else 1
        self.n_y = int(np.ceil(np.log2(ny))) if ny > 1 else 1
        self.n_total = self.n_x + self.n_y + 5
        self.hilbert_dim = 2**self.n_total

        # Generalized boundary mask
        self.boundary_mask = PhysicalBoundaryMask(nx=self.nx, ny=self.ny, top_wall_solid=True)
        self.solid = self.boundary_mask.get_solid_mask()

        # Initialize distributions matching Level 4 setup
        self._init_distributions()
        self.norm_N = float(np.sqrt(np.sum(self.f**2) + np.sum(self.g**2)))

    def _state_index(self, x: int, y: int, i: int, p: int) -> int:
        return (x << (5 + self.n_y)) | (y << 5) | (i << 1) | p

    def _init_distributions(self):
        self.f = np.zeros((9, self.ny, self.nx), dtype=np.float64)
        self.g = np.zeros((9, self.ny, self.nx), dtype=np.float64)

        x_grid, y_grid = np.meshgrid(np.arange(self.nx), np.arange(self.ny))
        dam_mask = (x_grid < self.dam_width_ratio * self.nx) & (y_grid < self.dam_height_ratio * self.ny)

        rho = np.where(dam_mask, self.rho_L, self.rho_G)
        alpha = np.where(dam_mask, 1.0, 0.0)
        u_init = np.zeros((2, self.ny, self.nx), dtype=np.float64)

        f_eq = compute_equilibrium(rho, u_init)
        self.f = f_eq.copy()
        for i in range(9):
            self.g[i] = W[i] * alpha

    def compute_surface_tension_force(self, alpha_field: np.ndarray) -> np.ndarray:
        """Computes continuum surface force F_s = sigma * kappa * grad(alpha)."""
        if self.sigma <= 0.0 or self.nx < 3 or self.ny < 3:
            return np.zeros((2, self.ny, self.nx), dtype=np.float64)

        grad_x = np.zeros((self.ny, self.nx), dtype=np.float64)
        grad_y = np.zeros((self.ny, self.nx), dtype=np.float64)
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
        return F_s

    def compute_total_force(self, rho_field: np.ndarray, alpha_field: np.ndarray) -> np.ndarray:
        """Computes total body + surface tension force."""
        F = np.zeros((2, self.ny, self.nx), dtype=np.float64)
        F[1] = (rho_field - self.rho_G) * self.g_acc
        if self.sigma > 0.0:
            F += self.compute_surface_tension_force(alpha_field)
        return F

    def compute_macroscopic_fields(self) -> Dict[str, np.ndarray]:
        """Computes moments and velocity matching Level 4 formulation."""
        rho = np.sum(self.f, axis=0)
        alpha = np.clip(np.sum(self.g, axis=0), 0.0, 1.0)
        F = self.compute_total_force(rho, alpha)

        rho_safe = np.where(rho > 1e-6, rho, self.rho_G)
        ux = (np.sum(self.f * C_X[:, None, None], axis=0) + 0.5 * F[0]) / rho_safe
        uy = (np.sum(self.f * C_Y[:, None, None], axis=0) + 0.5 * F[1]) / rho_safe

        u_mag = np.sqrt(ux**2 + uy**2)
        scale = np.where(u_mag > 0.15, 0.15 / (u_mag + 1e-12), 1.0)
        u = np.stack((ux * scale, uy * scale), axis=0)

        return {
            "rho": rho,
            "alpha": alpha,
            "F": F,
            "u": u,
        }

    def step(self, kill_switches: Optional[Dict[str, bool]] = None) -> Dict[str, Any]:
        """
        Executes one full coupled QLBM timestep with support for differential kill switches.
        """
        ks = kill_switches or {}

        # 1. Parameter and Force Extraction
        fields = self.compute_macroscopic_fields()
        rho = fields["rho"]
        alpha_raw = np.sum(self.g, axis=0)
        alpha = fields["alpha"] if not ks.get("kill_phase_coupling", False) else np.zeros_like(fields["alpha"])
        F = fields["F"]
        if ks.get("kill_gravity", False):
            F[1] = 0.0
        if ks.get("kill_csf", False) and self.sigma > 0.0:
            F -= self.compute_surface_tension_force(alpha)
        u = fields["u"]

        # 2. Local Quantum Collision
        f_coll = np.zeros_like(self.f)
        g_coll = np.zeros_like(self.g)

        if ks.get("kill_collision", False):
            f_coll = self.f.copy()
            g_coll = self.g.copy()
        else:
            for x in range(self.nx):
                for y in range(self.ny):
                    z_node = np.concatenate([self.f[:, y, x], self.g[:, y, x]])
                    C_mat, alpha_C, U_C, _ = build_coupled_collision_matrix(
                        alpha=alpha[y, x],
                        u_vec=u[:, y, x],
                        rho=rho[y, x],
                        F_vec=F[:, y, x],
                        alpha_raw=alpha_raw[y, x],
                        nu_L=self.nu_L,
                        nu_G=self.nu_G,
                        tau_g=self.tau_phi,
                    )
                    z_pad = np.zeros(64, dtype=np.complex128)
                    z_pad[:18] = z_node
                    psi_coll_node = alpha_C * (U_C @ z_pad)
                    f_coll[:, y, x] = np.real(psi_coll_node[:9])
                    g_coll[:, y, x] = np.real(psi_coll_node[9:18])

        # 3. Spatial Streaming
        if ks.get("kill_streaming", False):
            f_streamed = f_coll.copy()
            g_streamed = g_coll.copy()
        else:
            f_streamed = stream(f_coll)
            g_streamed = stream(g_coll)

        # 4. Physical Boundary Involution Bounce-Back
        f_next = np.copy(f_streamed)
        g_next = np.copy(g_streamed)

        if not ks.get("kill_boundary", False):
            for i in range(9):
                opp_i = OPPOSITE[i]
                f_next[opp_i, self.solid] = f_streamed[i, self.solid]
                g_next[opp_i, self.solid] = g_streamed[i, self.solid]

        self.f = f_next
        self.g = g_next

        # Normalization
        if not ks.get("kill_normalization", False):
            self.norm_N = float(np.sqrt(np.sum(self.f**2) + np.sum(self.g**2)))

        return {
            "total_mass": float(np.sum(self.f)),
            "phase_mass": float(np.sum(self.g)),
            "max_u": float(np.max(np.sqrt(u[0]**2 + u[1]**2))),
        }

    def get_surge_front_position(self, threshold: float = 0.5) -> float:
        """Extracts rightmost x-coordinate of the liquid front along bottom fluid layer."""
        alpha = np.clip(np.sum(self.g, axis=0), 0.0, 1.0)
        bottom_layer = np.max(alpha[0:min(3, self.ny), :], axis=0)
        liquid_indices = np.where(bottom_layer >= threshold)[0]
        return float(liquid_indices[-1]) if len(liquid_indices) > 0 else 0.0

    def get_residual_column_height(self, threshold: float = 0.5) -> float:
        """Extracts topmost y-coordinate of the liquid column at left wall."""
        alpha = np.clip(np.sum(self.g, axis=0), 0.0, 1.0)
        col_slice = alpha[:, 0:min(2, self.nx)]
        liquid_indices = np.where(np.max(col_slice, axis=1) >= threshold)[0]
        return float(liquid_indices[-1]) if len(liquid_indices) > 0 else 0.0
