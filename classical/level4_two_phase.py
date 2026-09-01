"""
High-Fidelity Level-4 Two-Phase D2Q9 Lattice Boltzmann Solver.

Coupled weakly-compressible hydrodynamic lattice (f_i) with conservative
phase-field interface capturing (g_i), phase-dependent density/viscosity,
interfacial surface tension, and gravitational buoyancy.
"""

from typing import Dict, Tuple, Optional
import numpy as np
from classical.d2q9 import C_X, C_Y, W, OPPOSITE, CS2
from classical.equilibrium import compute_equilibrium
from classical.streaming import stream
from classical.boundary import apply_noslip_box


class Level4TwoPhaseLBM:
    """
    High-fidelity two-phase D2Q9 LBM solver with surface tension and density contrast.
    
    Fields are stored in (ny, nx) spatial ordering for consistent D2Q9 index compatibility.
    """

    def __init__(
        self,
        nx: int = 64,
        ny: int = 32,
        rho_L: float = 1.0,
        rho_G: float = 0.1,
        nu_L: float = 0.05,
        nu_G: float = 0.05,
        sigma: float = 0.001,
        interface_width: float = 3.0,
        g_acc: float = -0.0005,
        tau_phi: float = 0.7,
        dam_width_ratio: float = 0.25,
        dam_height_ratio: float = 0.5,
    ):
        self.nx = nx
        self.ny = ny
        self.rho_L = rho_L
        self.rho_G = rho_G
        self.nu_L = nu_L
        self.nu_G = nu_G
        self.sigma = sigma
        self.W_int = interface_width
        self.g_acc = g_acc
        self.tau_phi = tau_phi
        self.col_w = max(1, int(nx * dam_width_ratio))
        self.col_h = max(1, int(ny * dam_height_ratio))
        self.dam_width = self.col_w
        self.dam_height = self.col_h

        # Discrete velocity constants
        self.cx = C_X
        self.cy = C_Y
        self.w = W
        self.opp = OPPOSITE
        self.cs2 = CS2

        # Initialize physical fields: (ny, nx)
        self.alpha = np.zeros((ny, nx), dtype=np.float64)  # 1=liquid, 0=gas
        self.alpha[: self.col_h, : self.col_w] = 1.0

        # Density and velocity
        self.rho = self.alpha * self.rho_L + (1.0 - self.alpha) * self.rho_G
        self.u = np.zeros((2, ny, nx), dtype=np.float64)

        # Initialize population arrays: (9, ny, nx)
        self.f = np.zeros((9, ny, nx), dtype=np.float64)
        self.g = np.zeros((9, ny, nx), dtype=np.float64)
        self._initialize_distributions()

        # Initial liquid volume
        self.initial_liquid_volume = float(np.sum(self.alpha))

    def _initialize_distributions(self):
        """Set initial f and g distributions to equilibrium."""
        self.f = compute_equilibrium(self.rho, self.u)
        self.g = np.zeros((9, self.ny, self.nx), dtype=np.float64)
        for i in range(9):
            c_dot_u = self.cx[i] * self.u[0] + self.cy[i] * self.u[1]
            self.g[i] = self.w[i] * self.alpha * (1.0 + 3.0 * c_dot_u)

    def compute_surface_tension_force(self) -> np.ndarray:
        """
        Compute continuum surface force F_s = sigma * kappa * grad(alpha).
        Using internal stencils with zero-gradient solid walls.
        """
        if self.sigma <= 0.0:
            return np.zeros((2, self.ny, self.nx), dtype=np.float64)

        # Gradient of alpha with zero-flux boundaries
        grad_x = np.zeros((self.ny, self.nx), dtype=np.float64)
        grad_y = np.zeros((self.ny, self.nx), dtype=np.float64)

        grad_x[:, 1:-1] = (self.alpha[:, 2:] - self.alpha[:, :-2]) / 2.0
        grad_y[1:-1, :] = (self.alpha[2:, :] - self.alpha[:-2, :]) / 2.0

        grad_norm = np.sqrt(grad_x ** 2 + grad_y ** 2) + 1e-12

        # Mask unit normal to interface zone only
        mask = grad_norm > 1e-3
        nx_vec = np.where(mask, grad_x / grad_norm, 0.0)
        ny_vec = np.where(mask, grad_y / grad_norm, 0.0)

        # Curvature kappa = -div(n)
        div_nx = np.zeros_like(nx_vec)
        div_ny = np.zeros_like(ny_vec)
        div_nx[:, 1:-1] = (nx_vec[:, 2:] - nx_vec[:, :-2]) / 2.0
        div_ny[1:-1, :] = (ny_vec[2:, :] - ny_vec[:-2, :]) / 2.0
        kappa = np.clip(-(div_nx + div_ny), -2.0, 2.0)

        F_s = np.zeros((2, self.ny, self.nx), dtype=np.float64)
        F_s[0] = np.where(mask, self.sigma * kappa * grad_x, 0.0)
        F_s[1] = np.where(mask, self.sigma * kappa * grad_y, 0.0)
        return F_s

    def compute_total_force(self) -> np.ndarray:
        """Compute total force F = F_buoyancy + F_surface."""
        F = np.zeros((2, self.ny, self.nx), dtype=np.float64)
        # Gravitational buoyancy in negative y-direction
        F[1] = (self.rho - self.rho_G) * self.g_acc

        if self.sigma > 0.0:
            F += self.compute_surface_tension_force()
        return F

    def step(self):
        """Advance the coupled two-phase state by one timestep."""
        # 1. Macroscopic moments
        self.rho = np.sum(self.f, axis=0)
        self.alpha = np.clip(np.sum(self.g, axis=0), 0.0, 1.0)

        # Total force
        F = self.compute_total_force()

        # Shifted velocity: u = (sum c_i f_i + 0.5 F) / rho
        rho_safe = np.where(self.rho > 1e-6, self.rho, self.rho_G)
        ux = (np.sum(self.cx[:, None, None] * self.f, axis=0) + 0.5 * F[0]) / rho_safe
        uy = (np.sum(self.cy[:, None, None] * self.f, axis=0) + 0.5 * F[1]) / rho_safe

        # Velocity limit for weakly-compressible low-Mach stability
        u_mag = np.sqrt(ux**2 + uy**2)
        max_u = 0.15
        scale = np.where(u_mag > max_u, max_u / (u_mag + 1e-12), 1.0)
        self.u = np.stack((ux * scale, uy * scale), axis=0)

        # Phase-dependent viscosity relaxation
        nu_mix = self.alpha * self.nu_L + (1.0 - self.alpha) * self.nu_G
        tau_f = 3.0 * nu_mix + 0.5
        omega_f = 1.0 / tau_f
        omega_g = 1.0 / self.tau_phi

        # 2. Equilibria
        f_eq = compute_equilibrium(self.rho, self.u)
        g_eq = np.zeros_like(self.g)
        for i in range(9):
            c_dot_u = self.cx[i] * self.u[0] + self.cy[i] * self.u[1]
            g_eq[i] = self.w[i] * self.alpha * (1.0 + 3.0 * c_dot_u)

        # 3. Collision with Guo Forcing
        f_coll = np.zeros_like(self.f)
        g_coll = np.zeros_like(self.g)

        u_dot_F = self.u[0] * F[0] + self.u[1] * F[1]

        for i in range(9):
            ci_u = self.cx[i] * self.u[0] + self.cy[i] * self.u[1]
            ci_F = self.cx[i] * F[0] + self.cy[i] * F[1]
            # Guo source term
            term = 3.0 * ci_F + 9.0 * ci_u * ci_F - 3.0 * u_dot_F
            S_i = (1.0 - 0.5 * omega_f) * self.w[i] * term
            f_coll[i] = self.f[i] - omega_f * (self.f[i] - f_eq[i]) + S_i
            g_coll[i] = self.g[i] - omega_g * (self.g[i] - g_eq[i])

        # 4. Reversible Spatial Streaming
        f_streamed = stream(f_coll)
        g_streamed = stream(g_coll)

        # 5. Boundary Exact Involution Bounce-Back on Solid Walls
        solid_mask = np.zeros((self.ny, self.nx), dtype=bool)
        solid_mask[0, :] = True
        solid_mask[-1, :] = True
        solid_mask[:, 0] = True
        solid_mask[:, -1] = True

        self.f = np.copy(f_streamed)
        self.g = np.copy(g_streamed)
        for i in range(9):
            opp = self.opp[i]
            self.f[opp, solid_mask] = f_streamed[i, solid_mask]
            self.g[opp, solid_mask] = g_streamed[i, solid_mask]

    def get_surge_front_position(self, threshold: float = 0.5) -> float:
        """Extract the rightmost x-coordinate of the liquid front along bottom fluid layer."""
        bottom_layer = np.max(self.alpha[0:3, :], axis=0)
        liquid_indices = np.where(bottom_layer >= threshold)[0]
        if len(liquid_indices) > 0:
            return float(liquid_indices[-1])
        return 0.0

    def get_column_height(self, threshold: float = 0.5) -> float:
        """Extract the highest y-coordinate of the liquid column along left wall layer."""
        left_layer = np.max(self.alpha[:, 0:3], axis=1)
        liquid_indices = np.where(left_layer >= threshold)[0]
        if len(liquid_indices) > 0:
            return float(liquid_indices[-1])
        return 0.0

    def get_total_liquid_volume(self) -> float:
        """Integral of liquid volume fraction over domain."""
        return float(np.sum(self.alpha))

    def get_kinetic_energy(self) -> float:
        """Total kinetic energy 0.5 * sum(rho * (u_x^2 + u_y^2))."""
        u_sq = self.u[0] ** 2 + self.u[1] ** 2
        return float(0.5 * np.sum(self.rho * u_sq))
