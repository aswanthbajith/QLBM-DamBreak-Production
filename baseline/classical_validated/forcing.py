#!/usr/bin/env python3
"""
Hydrodynamic Forcing Module for Two-Phase Flows.

Implements:
- Surface tension continuum surface force (CSF)
- Gravitational buoyancy force with ambient gas subtraction
- Guo body forcing expansion for D2Q9 lattice
"""

import numpy as np
from two_phase_physics import TwoPhaseProperties

class TwoPhaseForcing:
    def __init__(self, props, gx=0.0, gy=-4.0e-4):
        """
        props: TwoPhaseProperties instance
        gx, gy: Gravitational acceleration vector (lattice units)
        """
        self.props = props
        self.gx = float(gx)
        self.gy = float(gy)
        self.cs2 = 1.0 / 3.0
        self.cs4 = 1.0 / 9.0

        self.c = props.c
        self.w = props.w

    def compute_total_force(self, phi, enable_surface_tension=True):
        """
        Computes total force field F = F_surface_tension + F_gravity.
        """
        rho = self.props.density(phi)

        # 1. Gravitational Buoyancy Force: (rho(phi) - rho_G) * g
        # Subtraction of background gas density eliminates spurious gas acceleration
        Fx_g = (rho - self.props.rho_G) * self.gx
        Fy_g = (rho - self.props.rho_G) * self.gy

        # 2. Surface Tension Force (CSF)
        if enable_surface_tension and self.props.sigma > 0.0:
            Fx_s, Fy_s, kappa = self.props.compute_curvature_and_csf(phi)
        else:
            Fx_s = np.zeros_like(phi)
            Fy_s = np.zeros_like(phi)

        Fx_total = Fx_g + Fx_s
        Fy_total = Fy_g + Fy_s

        return Fx_total, Fy_total

    def compute_guo_force_term(self, u, v, Fx, Fy, rho, tau_v):
        """
        Computes the discrete Guo forcing term Fi for all 9 velocities:
        Fi = (1 - 1/(2*tau_v)) * wi * [ (c_i - u).F / (rho*cs2) + (c_i.u)(c_i.F) / (rho*cs4) ]
        """
        nx, ny = u.shape
        Fi = np.zeros((9, nx, ny), dtype=np.float64)

        coeff = 1.0 - 0.5 / tau_v
        rho_safe = np.maximum(rho, 1e-12)

        Fx_scaled = Fx / rho_safe
        Fy_scaled = Fy / rho_safe

        for i in range(9):
            wi = self.w[i]
            cx, cy = self.c[i, 0], self.c[i, 1]
            cu = cx * u + cy * v

            term1 = (cx - u) * Fx_scaled + (cy - v) * Fy_scaled
            term2 = (cu / self.cs2) * (cx * Fx_scaled + cy * Fy_scaled)
            Fi[i] = coeff * wi * (term1 / self.cs2 + term2 / self.cs2)

        return Fi
