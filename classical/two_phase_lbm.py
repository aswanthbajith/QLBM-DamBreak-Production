#!/usr/bin/env python3
"""
Production Two-Phase Velocity-Based Lattice Boltzmann Method (LBM)
Coupled with Conservative Phase-Field Interface Capturing.

Theoretical Basis:
- Hydrodynamics: Incompressible Velocity-Based LBM (Jennings et al. 2025 / Watanabe & Hu 2026)
- Interface Tracking: Conservative Phase-Field / Allen-Cahn Formulation
- Lattice: D2Q9 (9 discrete velocities)
- Boundaries: Half-way bounce-back on solid walls, with free-slip floor option
"""

import numpy as np

class TwoPhaseLBM2D:
    def __init__(self, nx, ny,
                 rho0=1.0, nu=0.01,
                 gy=-3.0e-4, gx=0.0,
                 width=3.0, tau_phi=0.6,
                 free_slip_bottom=True):
        """
        nx, ny: Lattice grid dimensions
        rho0: Reference fluid density
        nu: Kinematic shear viscosity
        gy, gx: Gravitational acceleration vector
        width: Interface transition thickness
        tau_phi: Phase field relaxation time
        free_slip_bottom: Whether floor uses free-slip or no-slip bounce-back
        """
        self.nx = nx
        self.ny = ny
        self.rho0 = rho0
        self.nu = nu
        self.gx = gx
        self.gy = gy
        self.g_abs = np.sqrt(gx**2 + gy**2)
        self.width = width
        self.tau_phi = tau_phi
        self.free_slip_bottom = free_slip_bottom

        # D2Q9 Lattice constants
        self.Q = 9
        self.cs2 = 1.0 / 3.0
        self.cs4 = 1.0 / 9.0
        self.tau_v = self.nu / self.cs2 + 0.5

        # Lattice velocity vectors c[i] = [cx, cy]
        self.c = np.array([
            [ 0,  0],  # 0: rest
            [ 1,  0],  # 1: +x
            [ 0,  1],  # 2: +y
            [-1,  0],  # 3: -x
            [ 0, -1],  # 4: -y
            [ 1,  1],  # 5: +x+y
            [-1,  1],  # 6: -x+y
            [-1, -1],  # 7: -x-y
            [ 1, -1]   # 8: +x-y
        ], dtype=np.int32)

        # Lattice weights w[i]
        self.w = np.array([
            4.0/9.0,
            1.0/9.0, 1.0/9.0, 1.0/9.0, 1.0/9.0,
            1.0/36.0, 1.0/36.0, 1.0/36.0, 1.0/36.0
        ], dtype=np.float64)

        # Opposite directions for bounce-back
        self.opp = np.array([0, 3, 4, 1, 2, 7, 8, 5, 6], dtype=np.int32)
        
        # Mirror reflections for floor free-slip
        self.refl_floor = np.array([0, 1, 4, 3, 2, 8, 7, 6, 5], dtype=np.int32)

        # Macroscopic fields
        self.phi = np.zeros((nx, ny), dtype=np.float64)
        self.u = np.zeros((nx, ny), dtype=np.float64)
        self.v = np.zeros((nx, ny), dtype=np.float64)
        self.p = np.zeros((nx, ny), dtype=np.float64)

        # Mesoscopic distribution populations
        self.g = np.zeros((self.Q, nx, ny), dtype=np.float64)
        self.h = np.zeros((self.Q, nx, ny), dtype=np.float64)

    def initialize_dam(self, dam_w, dam_h):
        """Initialize water column of dimensions dam_w x dam_h at bottom-left corner."""
        self.dam_w = dam_w
        self.dam_h = dam_h
        
        for x in range(self.nx):
            for y in range(self.ny):
                if x <= dam_w and y <= dam_h:
                    d = min(dam_w - x, dam_h - y)
                    self.phi[x, y] = 0.5 + 0.5 * np.tanh(2.0 * d / self.width)
                elif x > dam_w and y <= dam_h:
                    d = x - dam_w
                    self.phi[x, y] = 0.5 - 0.5 * np.tanh(2.0 * d / self.width)
                elif x <= dam_w and y > dam_h:
                    d = y - dam_h
                    self.phi[x, y] = 0.5 - 0.5 * np.tanh(2.0 * d / self.width)
                else:
                    d = np.sqrt((x - dam_w)**2 + (y - dam_h)**2)
                    self.phi[x, y] = 0.5 - 0.5 * np.tanh(2.0 * d / self.width)

        self.u.fill(0.0)
        self.v.fill(0.0)
        self.p.fill(0.0)

        # Set equilibrium distributions at rest
        for i in range(self.Q):
            cu = self.c[i, 0] * self.u + self.c[i, 1] * self.v
            u2 = self.u**2 + self.v**2
            self.g[i] = (self.p / (self.rho0 * self.cs2)) * self.w[i] + self.rho0 * self.w[i] * (cu / self.cs2 + 0.5 * cu**2 / self.cs4 - 0.5 * u2 / self.cs2)
            self.h[i] = self.w[i] * self.phi * (1.0 + cu / self.cs2)

    def step(self):
        """Execute one complete time step of the coupled two-phase system."""
        # 1. Update order parameter from distributions
        self.phi = np.clip(np.sum(self.h, axis=0), 0.0, 1.0)

        # 2. Gravity body force driving the liquid phase
        Fx = self.phi * self.rho0 * self.gx
        Fy = self.phi * self.rho0 * self.gy

        # 3. Collision Step for Phase Field (h)
        h_post = np.zeros_like(self.h)
        for i in range(self.Q):
            cu = self.c[i, 0] * self.u + self.c[i, 1] * self.v
            heq = self.w[i] * self.phi * (1.0 + cu / self.cs2)
            h_post[i] = self.h[i] - (1.0 / self.tau_phi) * (self.h[i] - heq)

        # 4. Collision Step for Hydrodynamics (g) with Guo Body Forcing (Jennings et al. 2025)
        g_post = np.zeros_like(self.g)
        for i in range(self.Q):
            cu = self.c[i, 0] * self.u + self.c[i, 1] * self.v
            u2 = self.u**2 + self.v**2
            geq = (self.p / (self.rho0 * self.cs2)) * self.w[i] + self.rho0 * self.w[i] * (cu / self.cs2 + 0.5 * cu**2 / self.cs4 - 0.5 * u2 / self.cs2)
            
            term1 = (self.c[i, 0] - self.u) * (Fx / self.rho0) + (self.c[i, 1] - self.v) * (Fy / self.rho0)
            term2 = (cu / self.cs2) * (self.c[i, 0] * (Fx / self.rho0) + self.c[i, 1] * (Fy / self.rho0))
            Fi = (1.0 - 0.5 / self.tau_v) * self.w[i] * (term1 / self.cs2 + term2 / self.cs2)
            
            g_post[i] = self.g[i] - (1.0 / self.tau_v) * (self.g[i] - geq) + Fi

        # 5. Streaming Step (Exact Linear Permutation Shift)
        for i in range(self.Q):
            cx = self.c[i, 0]
            cy = self.c[i, 1]
            self.h[i] = np.roll(h_post[i], shift=(cx, cy), axis=(0, 1))
            self.g[i] = np.roll(g_post[i], shift=(cx, cy), axis=(0, 1))

        # 6. Solid Wall Boundary Conditions
        for i in range(1, self.Q):
            opp_i = self.opp[i]
            cx = self.c[i, 0]
            cy = self.c[i, 1]
            
            if cx > 0: # Right wall bounce-back
                self.g[opp_i, -1, :] = g_post[i, -1, :]
                self.h[opp_i, -1, :] = h_post[i, -1, :]
            if cx < 0: # Left wall bounce-back
                self.g[opp_i, 0, :] = g_post[i, 0, :]
                self.h[opp_i, 0, :] = h_post[i, 0, :]
            if cy > 0: # Top wall bounce-back
                self.g[opp_i, :, -1] = g_post[i, :, -1]
                self.h[opp_i, :, -1] = h_post[i, :, -1]
            if cy < 0: # Bottom floor
                if self.free_slip_bottom:
                    refl_i = self.refl_floor[i]
                    self.g[refl_i, :, 0] = g_post[i, :, 0]
                    self.h[refl_i, :, 0] = h_post[i, :, 0]
                else:
                    self.g[opp_i, :, 0] = g_post[i, :, 0]
                    self.h[opp_i, :, 0] = h_post[i, :, 0]

        # 7. Macroscopic Hydrodynamic Moments
        self.p = self.cs2 * np.sum(self.g, axis=0)
        
        sum_gc_x = np.zeros((self.nx, self.ny), dtype=np.float64)
        sum_gc_y = np.zeros((self.nx, self.ny), dtype=np.float64)
        for i in range(self.Q):
            sum_gc_x += self.g[i] * self.c[i, 0]
            sum_gc_y += self.g[i] * self.c[i, 1]
            
        self.u = (1.0 / self.rho0) * sum_gc_x + 0.5 * Fx / self.rho0
        self.v = (1.0 / self.rho0) * sum_gc_y + 0.5 * Fy / self.rho0

        # Enforce no-slip on left, right, top walls
        self.u[0, :] = 0.0; self.u[-1, :] = 0.0; self.u[:, -1] = 0.0
        self.v[0, :] = 0.0; self.v[-1, :] = 0.0; self.v[:, -1] = 0.0
        if not self.free_slip_bottom:
            self.u[:, 0] = 0.0
        self.v[:, 0] = 0.0

    def get_wavefront_x(self, threshold=0.5):
        """Extract leading liquid surge position along floor."""
        floor_phi = self.phi[:, 1]
        liquid_idx = np.where(floor_phi > threshold)[0]
        if len(liquid_idx) > 0:
            return float(np.max(liquid_idx))
        return float(self.dam_w)

    def get_column_height(self, threshold=0.5):
        """Extract remaining column height along back wall."""
        wall_phi = self.phi[1, :]
        liquid_idx = np.where(wall_phi > threshold)[0]
        if len(liquid_idx) > 0:
            return float(np.max(liquid_idx))
        return float(self.dam_h)

    def get_sensor_pressure(self, x, y):
        """Extract pressure at sensor node (x, y)."""
        return float(self.p[x, y])
