"""
Exact BGK Polynomial Equilibrium for D2Q9 Lattice.
"""
import numpy as np
from classical.d2q9 import C_X, C_Y, W, CS2

def compute_macroscopic(f):
    """
    Compute macroscopic density rho and velocity field u from populations f.
    f shape: (9, Ny, Nx)
    Returns:
        rho: (Ny, Nx)
        u: (2, Ny, Nx)
    """
    rho = np.sum(f, axis=0)
    # Avoid division by zero
    rho_safe = np.where(rho > 1e-14, rho, 1.0)
    ux = np.sum(C_X[:, None, None] * f, axis=0) / rho_safe
    uy = np.sum(C_Y[:, None, None] * f, axis=0) / rho_safe
    u = np.stack((ux, uy), axis=0)
    return rho, u

def compute_equilibrium(rho, u):
    """
    Compute standard second-order BGK polynomial equilibrium:
    f_i^eq = w_i * rho * [1 + 3*(c_i . u) + 4.5*(c_i . u)^2 - 1.5*(u . u)]
    """
    Ny, Nx = rho.shape
    f_eq = np.zeros((9, Ny, Nx), dtype=np.float64)
    u_sq = u[0]**2 + u[1]**2
    
    for i in range(9):
        c_dot_u = C_X[i] * u[0] + C_Y[i] * u[1]
        f_eq[i] = W[i] * rho * (1.0 + 3.0 * c_dot_u + 4.5 * (c_dot_u**2) - 1.5 * u_sq)
        
    return f_eq
