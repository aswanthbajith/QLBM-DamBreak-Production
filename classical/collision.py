"""
BGK Collision Operator for D2Q9.
"""
import numpy as np
from classical.equilibrium import compute_macroscopic, compute_equilibrium

def collide_bgk(f, omega, force=None):
    """
    Single-relaxation-time (BGK) collision step:
    f_i^* = f_i - omega * (f_i - f_i^eq) + S_i(force)
    """
    rho, u = compute_macroscopic(f)
    f_eq = compute_equilibrium(rho, u)
    f_out = f - omega * (f - f_eq)
    
    if force is not None:
        # Guo external forcing scheme or standard force term
        # S_i = (1 - 0.5*omega) * w_i * [ 3*(c_i - u) + 9*(c_i . u)*c_i ] . F
        from classical.d2q9 import C_X, C_Y, W
        fx, fy = force[0], force[1]
        for i in range(9):
            c_dot_u = C_X[i] * u[0] + C_Y[i] * u[1]
            c_minus_u_x = C_X[i] - u[0]
            c_minus_u_y = C_Y[i] - u[1]
            term = 3.0 * (c_minus_u_x * fx + c_minus_u_y * fy) + 9.0 * c_dot_u * (C_X[i] * fx + C_Y[i] * fy)
            source_i = (1.0 - 0.5 * omega) * W[i] * term
            f_out[i] += source_i
            
    return f_out
