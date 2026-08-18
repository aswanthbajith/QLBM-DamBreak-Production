#!/usr/bin/env python3
"""
Two-Phase Fluid Constitutive Relations, Property Interpolation, and Differential Stencils.

Provides:
- Density interpolation: rho(phi) = rho_G + phi * (rho_L - rho_G)
- Viscosity interpolation: mu(phi) = mu_G + phi * (mu_L - mu_G)
- Isotropic D2Q9 gradient, Laplacian, and curvature stencils
- Surface tension continuum surface force (CSF) and potential models
"""

import numpy as np

class TwoPhaseProperties:
    def __init__(self, rho_L=1.0, rho_G=0.1,
                 nu_L=0.01, nu_G=0.01,
                 sigma=0.001, width=4.0, mobility=0.05):
        """
        rho_L, rho_G: Liquid and gas phase densities (lattice units)
        nu_L, nu_G: Liquid and gas phase kinematic viscosities (lattice units)
        sigma: Surface tension coefficient (lattice units)
        width: Interface transition thickness (lattice nodes)
        mobility: Interface mobility parameter M
        """
        self.rho_L = float(rho_L)
        self.rho_G = float(rho_G)
        self.nu_L = float(nu_L)
        self.nu_G = float(nu_G)
        self.mu_L = self.rho_L * self.nu_L
        self.mu_G = self.rho_G * self.nu_G
        self.sigma = float(sigma)
        self.width = float(width)
        self.mobility = float(mobility)

        self.cs2 = 1.0 / 3.0
        self.cs4 = 1.0 / 9.0

        # D2Q9 lattice vectors and isotropic weights for spatial derivatives
        self.c = np.array([
            [ 0,  0], [ 1,  0], [ 0,  1], [-1,  0], [ 0, -1],
            [ 1,  1], [-1,  1], [-1, -1], [ 1, -1]
        ], dtype=np.int32)

        self.w = np.array([
            4/9, 1/9, 1/9, 1/9, 1/9, 1/36, 1/36, 1/36, 1/36
        ], dtype=np.float64)

    def density(self, phi):
        """Linear density interpolation: rho(phi) = rho_G + phi * (rho_L - rho_G)."""
        phi_clamped = np.clip(phi, 0.0, 1.0)
        return self.rho_G + phi_clamped * (self.rho_L - self.rho_G)

    def dynamic_viscosity(self, phi):
        """Linear dynamic viscosity interpolation: mu(phi) = mu_G + phi * (mu_L - mu_G)."""
        phi_clamped = np.clip(phi, 0.0, 1.0)
        return self.mu_G + phi_clamped * (self.mu_L - self.mu_G)

    def kinematic_viscosity(self, phi):
        """Kinematic viscosity: nu(phi) = mu(phi) / rho(phi)."""
        rho = self.density(phi)
        mu = self.dynamic_viscosity(phi)
        return mu / (rho + 1e-15)

    def relaxation_time(self, phi):
        """Local hydrodynamic relaxation time: tau_v(phi) = 3 * nu(phi) + 0.5."""
        nu = self.kinematic_viscosity(phi)
        return nu / self.cs2 + 0.5

    def compute_gradient(self, field):
        """
        Computes isotropic 4th-order isotropic gradient on 2D lattice:
        grad(F) = 3 * sum_i w_i c_i F(x + c_i)
        """
        grad_x = np.zeros_like(field)
        grad_y = np.zeros_like(field)

        for i in range(1, 9):
            cx, cy = self.c[i, 0], self.c[i, 1]
            wi = self.w[i]
            shifted = np.roll(field, shift=(-cx, -cy), axis=(0, 1))
            grad_x += (3.0 * wi * cx) * shifted
            grad_y += (3.0 * wi * cy) * shifted

        # Zero gradients at physical boundaries (Neumann boundary condition)
        grad_x[0, :] = grad_x[1, :]
        grad_x[-1, :] = grad_x[-2, :]
        grad_y[:, 0] = grad_y[:, 1]
        grad_y[:, -1] = grad_y[:, -2]

        return grad_x, grad_y

    def compute_laplacian(self, field):
        """
        Computes isotropic Laplacian on D2Q9 lattice:
        laplace(F) = 6 * sum_i w_i [F(x + c_i) - F(x)]
        """
        lap = np.zeros_like(field)
        for i in range(1, 9):
            cx, cy = self.c[i, 0], self.c[i, 1]
            wi = self.w[i]
            shifted = np.roll(field, shift=(-cx, -cy), axis=(0, 1))
            lap += (6.0 * wi) * (shifted - field)

        # Apply boundary condition on laplacian
        lap[0, :] = 0.0
        lap[-1, :] = 0.0
        lap[:, 0] = 0.0
        lap[:, -1] = 0.0

        return lap

    def compute_curvature_and_csf(self, phi):
        """
        Computes Continuum Surface Force (CSF):
        F_s = sigma * kappa * grad(phi)
        where kappa = -div(grad(phi) / |grad(phi)|).
        """
        grad_x, grad_y = self.compute_gradient(phi)
        grad_mag = np.sqrt(grad_x**2 + grad_y**2) + 1e-12

        # Unit interface normal
        nx = grad_x / grad_mag
        ny = grad_y / grad_mag

        # Curvature kappa = -div(n)
        div_n_x, _ = self.compute_gradient(nx)
        _, div_n_y = self.compute_gradient(ny)
        kappa = -(div_n_x + div_n_y)

        # Continuum surface force
        Fx_s = self.sigma * kappa * grad_x
        Fy_s = self.sigma * kappa * grad_y

        return Fx_s, Fy_s, kappa
