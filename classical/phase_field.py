#!/usr/bin/env python3
"""
Conservative Phase-Field Interface Capturing Module.

Implements:
- Conservative Allen-Cahn and Order-Parameter Advection-Diffusion on D2Q9 lattice
- Functional API for phase gradient, laplacian, evolution, boundary, and validation
- PhaseFieldLBM2D class for continuous multi-step phase evolution
"""

import numpy as np
from classical.d2q9 import C_X, C_Y, W, CS2, OPPOSITE
try:
    from classical.two_phase_physics import TwoPhaseProperties
except ImportError:
    from two_phase_physics import TwoPhaseProperties


def initialize_phase_field(nx=4, ny=4, dam_w=None, dam_h=None, width=1.0, smooth=False):
    """
    Initializes the phase field phi in [0, 1] for a dam-break configuration.
    
    Args:
        nx, ny: Grid dimensions in X and Y
        dam_w: Width of liquid column (default: nx // 2)
        dam_h: Height of liquid column (default: ny // 2)
        width: Interface thickness parameter
        smooth: If True, uses tanh diffuse interface; otherwise sharp step.
        
    Returns:
        phi: (ny, nx) array with phi in [0, 1] (1 for liquid, 0 for gas)
    """
    if dam_w is None:
        dam_w = max(1, nx // 2)
    if dam_h is None:
        dam_h = max(1, ny // 2)
        
    phi = np.zeros((ny, nx), dtype=np.float64)
    
    if not smooth:
        phi[:dam_h, :dam_w] = 1.0
    else:
        for y in range(ny):
            for x in range(nx):
                if x <= dam_w and y <= dam_h:
                    d = min(dam_w - x, dam_h - y)
                    phi[y, x] = 0.5 + 0.5 * np.tanh(2.0 * d / max(width, 0.1))
                else:
                    d = max(x - dam_w, y - dam_h)
                    phi[y, x] = 0.5 - 0.5 * np.tanh(2.0 * d / max(width, 0.1))
                    
    return np.clip(phi, 0.0, 1.0)


def compute_phase_gradient(phi):
    """
    Computes spatial gradient nabla phi = (dphi/dx, dphi/dy) using 2nd-order central differences
    with one-sided differences at boundaries.
    
    Returns:
        grad_x, grad_y: (ny, nx) arrays
    """
    ny, nx = phi.shape
    grad_x = np.zeros_like(phi)
    grad_y = np.zeros_like(phi)
    
    # X gradient
    if nx > 1:
        grad_x[:, 1:-1] = (phi[:, 2:] - phi[:, :-2]) / 2.0
        grad_x[:, 0] = phi[:, 1] - phi[:, 0]
        grad_x[:, -1] = phi[:, -1] - phi[:, -2]
        
    # Y gradient
    if ny > 1:
        grad_y[1:-1, :] = (phi[2:, :] - phi[:-2, :]) / 2.0
        grad_y[0, :] = phi[1, :] - phi[0, :]
        grad_y[-1, :] = phi[-1, :] - phi[-2, :]
        
    return grad_x, grad_y


def compute_phase_laplacian(phi):
    """
    Computes spatial Laplacian nabla^2 phi using standard 5-point discrete stencil.
    """
    ny, nx = phi.shape
    lap = np.zeros_like(phi)
    
    if nx > 2 and ny > 2:
        lap[1:-1, 1:-1] = (
            phi[1:-1, 2:] + phi[1:-1, :-2] +
            phi[2:, 1:-1] + phi[:-2, 1:-1] -
            4.0 * phi[1:-1, 1:-1]
        )
    return lap


def apply_phase_boundary(phi, boundary_type="neumann"):
    """
    Applies zero-gradient (Neumann) or constant contact angle boundary condition on domain perimeter.
    """
    phi_b = np.copy(phi)
    if phi_b.shape[1] > 1:
        phi_b[:, 0] = phi_b[:, 1]
        phi_b[:, -1] = phi_b[:, -2]
    if phi_b.shape[0] > 1:
        phi_b[0, :] = phi_b[1, :]
        phi_b[-1, :] = phi_b[-2, :]
    return np.clip(phi_b, 0.0, 1.0)


def update_phase_field(phi, u, tau_phi=0.7, mobility=0.05):
    """
    Advances the order-parameter phase field by one time step via kinetic LBM advection-diffusion.
    
    Args:
        phi: (ny, nx) current phase field
        u: (2, ny, nx) macroscopic velocity (ux, uy)
        tau_phi: Phase relaxation time
        mobility: Phase mobility M
        
    Returns:
        phi_next: (ny, nx) updated phase field bounded in [0, 1]
    """
    ny, nx = phi.shape
    g = np.zeros((9, ny, nx), dtype=np.float64)
    omega_g = 1.0 / tau_phi
    
    # 1. Equilibrium
    for i in range(9):
        c_dot_u = C_X[i] * u[0] + C_Y[i] * u[1]
        g[i] = W[i] * phi * (1.0 + 3.0 * c_dot_u)
        
    # 2. Collision
    g_coll = np.zeros_like(g)
    for i in range(9):
        c_dot_u = C_X[i] * u[0] + C_Y[i] * u[1]
        g_eq = W[i] * phi * (1.0 + 3.0 * c_dot_u)
        g_coll[i] = g[i] - omega_g * (g[i] - g_eq)
        
    # 3. Streaming (periodic shift)
    g_stream = np.zeros_like(g_coll)
    for i in range(9):
        g_stream[i] = np.roll(g_coll[i], shift=(int(C_Y[i]), int(C_X[i])), axis=(0, 1))
        
    # 4. Boundary bounce-back
    from classical.boundary import apply_noslip_box
    g_next = apply_noslip_box(g_stream, g_coll)
    
    # 5. Extract new phase field
    phi_next = np.sum(g_next, axis=0)
    return np.clip(phi_next, 0.0, 1.0)


def validate_phase_field(phi):
    """
    Validates physical consistency of phase field:
    - Boundedness in [0, 1]
    - Total mass positivity
    - Finite interface gradient
    
    Returns:
        dict of validation metrics and status boolean
    """
    in_bounds = bool(np.all(phi >= -1e-12) and np.all(phi <= 1.0 + 1e-12))
    total_liquid = float(np.sum(phi))
    min_val = float(np.min(phi))
    max_val = float(np.max(phi))
    grad_x, grad_y = compute_phase_gradient(phi)
    max_grad = float(np.max(np.sqrt(grad_x**2 + grad_y**2)))
    
    return {
        "valid": in_bounds and (total_liquid > 0),
        "min": min_val,
        "max": max_val,
        "total_liquid_volume": total_liquid,
        "max_interface_gradient": max_grad
    }


class PhaseFieldLBM2D:
    """
    Class-based interface preserving full backward-compatibility with Phase 15 test suite.
    """
    def __init__(self, nx, ny, width=4.0, mobility=0.05, contact_angle=90.0, free_slip_bottom=True):
        self.nx = nx
        self.ny = ny
        self.width = float(width)
        self.mobility = float(mobility)
        self.theta_w = float(contact_angle) * np.pi / 180.0
        self.free_slip_bottom = free_slip_bottom
        self.cs2 = 1.0 / 3.0
        self.tau_phi = self.mobility / self.cs2 + 0.5

        self.c = np.array([
            [ 0,  0], [ 1,  0], [ 0,  1], [-1,  0], [ 0, -1],
            [ 1,  1], [-1,  1], [-1, -1], [ 1, -1]
        ], dtype=np.int32)

        self.w = np.array([
            4/9, 1/9, 1/9, 1/9, 1/9, 1/36, 1/36, 1/36, 1/36
        ], dtype=np.float64)

        self.opp = np.array([0, 3, 4, 1, 2, 7, 8, 5, 6], dtype=np.int32)
        self.refl_floor = np.array([0, 1, 4, 3, 2, 8, 7, 6, 5], dtype=np.int32)
        self.props = TwoPhaseProperties(width=self.width, mobility=self.mobility)

        self.phi = np.zeros((nx, ny), dtype=np.float64)
        self.h = np.zeros((9, nx, ny), dtype=np.float64)
        self.h_post = np.zeros((9, nx, ny), dtype=np.float64)

    def initialize_column(self, dam_w, dam_h):
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

        self.phi = np.clip(self.phi, 0.0, 1.0)
        for i in range(9):
            self.h[i] = self.w[i] * self.phi

    def step(self, u, v):
        grad_x, grad_y = self.props.compute_gradient(self.phi)
        grad_mag = np.sqrt(grad_x**2 + grad_y**2) + 1e-12
        nx_norm = grad_x / grad_mag
        ny_norm = grad_y / grad_mag

        bulk_factor = (1.0 - 4.0 * (self.phi - 0.5)**2) / self.width
        F_phi_x = self.mobility * (grad_x - bulk_factor * nx_norm)
        F_phi_y = self.mobility * (grad_y - bulk_factor * ny_norm)

        for i in range(9):
            wi = self.w[i]
            cx, cy = self.c[i, 0], self.c[i, 1]
            cu = cx * u + cy * v
            heq = wi * self.phi * (1.0 + cu / self.cs2)
            Si = (1.0 - 0.5 / self.tau_phi) * wi * (cx * F_phi_x + cy * F_phi_y) / self.cs2
            self.h_post[i] = self.h[i] - (1.0 / self.tau_phi) * (self.h[i] - heq) + Si

        for i in range(9):
            cx, cy = self.c[i, 0], self.c[i, 1]
            self.h[i] = np.roll(self.h_post[i], shift=(cx, cy), axis=(0, 1))

        for i in range(1, 9):
            opp_i = self.opp[i]
            cx, cy = self.c[i, 0], self.c[i, 1]
            if cx > 0: self.h[opp_i, -1, :] = self.h_post[i, -1, :]
            if cx < 0: self.h[opp_i, 0, :] = self.h_post[i, 0, :]
            if cy > 0: self.h[opp_i, :, -1] = self.h_post[i, :, -1]
            if cy < 0:
                if self.free_slip_bottom:
                    refl_i = self.refl_floor[i]
                    self.h[refl_i, :, 0] = self.h_post[i, :, 0]
                else:
                    self.h[opp_i, :, 0] = self.h_post[i, :, 0]

        self.phi = np.clip(np.sum(self.h, axis=0), 0.0, 1.0)
