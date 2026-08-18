#!/usr/bin/env python3
"""
Production Two-Phase Velocity-Based Lattice Boltzmann Method (LBM) Solver.

Couples:
- Hydrodynamics: Incompressible velocity-based D2Q9 LBM with variable density and viscosity
- Interface Capturing: Conservative Allen-Cahn phase field with counter-gradient sharpening
- Forcing: Continuum Surface Force (CSF) + Gravitational buoyancy + Guo body forcing scheme
"""

import numpy as np
from two_phase_physics import TwoPhaseProperties
from phase_field import PhaseFieldLBM2D
from forcing import TwoPhaseForcing

class TwoPhaseLBM2D:
    def __init__(self, nx, ny,
                 rho_L=1.0, rho_G=0.1,
                 nu_L=0.01, nu_G=0.01,
                 sigma=0.001,
                 gx=0.0, gy=-4.0e-4,
                 width=4.0, mobility=0.05,
                 contact_angle=90.0,
                 enable_surface_tension=True,
                 free_slip_bottom=True):
        """
        nx, ny: Lattice grid dimensions
        rho_L, rho_G: Liquid and gas phase densities
        nu_L, nu_G: Liquid and gas phase kinematic viscosities
        sigma: Surface tension coefficient
        gx, gy: Gravitational acceleration vector
        width: Interface transition width W
        mobility: Interface mobility M
        contact_angle: Wall static contact angle in degrees
        enable_surface_tension: Whether surface tension force is evaluated
        free_slip_bottom: Whether bottom floor uses free-slip reflection
        """
        self.nx = nx
        self.ny = ny
        self.enable_surface_tension = enable_surface_tension
        self.free_slip_bottom = free_slip_bottom

        # Lattice constants
        self.Q = 9
        self.cs2 = 1.0 / 3.0
        self.cs4 = 1.0 / 9.0

        # Physical properties & differential stencils
        self.props = TwoPhaseProperties(
            rho_L=rho_L, rho_G=rho_G,
            nu_L=nu_L, nu_G=nu_G,
            sigma=sigma, width=width,
            mobility=mobility
        )

        # Sub-modules
        self.phase_field = PhaseFieldLBM2D(
            nx=nx, ny=ny,
            width=width, mobility=mobility,
            contact_angle=contact_angle,
            free_slip_bottom=free_slip_bottom
        )

        self.forcing = TwoPhaseForcing(
            props=self.props,
            gx=gx, gy=gy
        )

        # Lattice velocities & weights
        self.c = self.props.c
        self.w = self.props.w
        self.opp = np.array([0, 3, 4, 1, 2, 7, 8, 5, 6], dtype=np.int32)
        self.refl_floor = np.array([0, 1, 4, 3, 2, 8, 7, 6, 5], dtype=np.int32)

        # Macroscopic fields
        self.u = np.zeros((nx, ny), dtype=np.float64)
        self.v = np.zeros((nx, ny), dtype=np.float64)
        self.p = np.zeros((nx, ny), dtype=np.float64)
        self.rho = np.ones((nx, ny), dtype=np.float64) * rho_G
        self.tau_v = np.ones((nx, ny), dtype=np.float64) * (nu_G / self.cs2 + 0.5)

        # Hydrodynamic distribution populations
        self.g = np.zeros((9, nx, ny), dtype=np.float64)
        self.g_post = np.zeros((9, nx, ny), dtype=np.float64)

    @property
    def phi(self):
        """Shortcut property for phase field order parameter."""
        return self.phase_field.phi

    @phi.setter
    def phi(self, value):
        self.phase_field.phi = value

    @property
    def h(self):
        """Shortcut property for phase field distribution."""
        return self.phase_field.h

    def initialize_dam(self, dam_w, dam_h):
        """Initializes the liquid water column and equilibrium distributions."""
        self.dam_w = dam_w
        self.dam_h = dam_h

        # 1. Initialize phase-field
        self.phase_field.initialize_column(dam_w, dam_h)

        # 2. Compute initial density and viscosity fields
        self.rho = self.props.density(self.phi)
        self.tau_v = self.props.relaxation_time(self.phi)

        # 3. Initialize velocity and pressure at rest
        self.u.fill(0.0)
        self.v.fill(0.0)
        self.p.fill(0.0)

        # 4. Initialize hydrodynamic distribution g_i at equilibrium
        for i in range(9):
            self.g[i] = self.w[i] * (self.p / (self.rho * self.cs2))

    def step(self):
        """Executes one complete time step of the coupled two-phase system."""
        # 1. Update fluid properties from current phase field
        self.rho = self.props.density(self.phi)
        self.tau_v = self.props.relaxation_time(self.phi)

        # 2. Compute total body forces (Surface Tension + Gravity)
        Fx, Fy = self.forcing.compute_total_force(
            self.phi,
            enable_surface_tension=self.enable_surface_tension
        )

        # 3. Phase-field evolution step (Conservative Allen-Cahn)
        self.phase_field.step(self.u, self.v)

        # 4. Compute Guo body forcing terms
        Fi = self.forcing.compute_guo_force_term(
            self.u, self.v, Fx, Fy, self.rho, self.tau_v
        )

        # 5. Hydrodynamic collision step
        u2 = self.u**2 + self.v**2
        p_star = self.p / (self.rho * self.cs2)

        for i in range(9):
            wi = self.w[i]
            cx, cy = self.c[i, 0], self.c[i, 1]
            cu = cx * self.u + cy * self.v

            geq = wi * (p_star + cu / self.cs2 + 0.5 * cu**2 / self.cs4 - 0.5 * u2 / self.cs2)
            self.g_post[i] = self.g[i] - (1.0 / self.tau_v) * (self.g[i] - geq) + Fi[i]

        # 6. Hydrodynamic streaming step
        for i in range(9):
            cx, cy = self.c[i, 0], self.c[i, 1]
            self.g[i] = np.roll(self.g_post[i], shift=(cx, cy), axis=(0, 1))

        # 7. Solid wall bounce-back boundary conditions
        for i in range(1, 9):
            opp_i = self.opp[i]
            cx, cy = self.c[i, 0], self.c[i, 1]

            if cx > 0: self.g[opp_i, -1, :] = self.g_post[i, -1, :]
            if cx < 0: self.g[opp_i, 0, :] = self.g_post[i, 0, :]
            if cy > 0: self.g[opp_i, :, -1] = self.g_post[i, :, -1]
            if cy < 0:
                if self.free_slip_bottom:
                    refl_i = self.refl_floor[i]
                    self.g[refl_i, :, 0] = self.g_post[i, :, 0]
                else:
                    self.g[opp_i, :, 0] = self.g_post[i, :, 0]

        # 8. Macroscopic hydrodynamic moments update
        self.p = self.rho * self.cs2 * np.sum(self.g, axis=0)

        sum_gc_x = np.zeros((self.nx, self.ny), dtype=np.float64)
        sum_gc_y = np.zeros((self.nx, self.ny), dtype=np.float64)
        for i in range(9):
            sum_gc_x += self.g[i] * self.c[i, 0]
            sum_gc_y += self.g[i] * self.c[i, 1]

        self.u = sum_gc_x + 0.5 * Fx / self.rho
        self.v = sum_gc_y + 0.5 * Fy / self.rho

        # Enforce no-slip on boundaries
        self.u[0, :] = 0.0; self.u[-1, :] = 0.0; self.u[:, -1] = 0.0
        self.v[0, :] = 0.0; self.v[-1, :] = 0.0; self.v[:, -1] = 0.0
        if not self.free_slip_bottom:
            self.u[:, 0] = 0.0
        self.v[:, 0] = 0.0

    def get_wavefront_x(self, threshold=0.5):
        """Extracts leading liquid surge front position along floor."""
        floor_phi = self.phi[:, 1]
        liq_idx = np.where(floor_phi > threshold)[0]
        if len(liq_idx) > 0:
            return float(np.max(liq_idx))
        return float(self.dam_w)

    def get_column_height(self, threshold=0.5):
        """Extracts remaining liquid column height along back wall."""
        wall_phi = self.phi[1, :]
        liq_idx = np.where(wall_phi > threshold)[0]
        if len(liq_idx) > 0:
            return float(np.max(liq_idx))
        return float(self.dam_h)

    def get_sensor_pressure(self, x, y):
        """Extracts pressure at sensor coordinate (x, y)."""
        return float(self.p[x, y])
