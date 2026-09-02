"""
Exact One-Node Classical Level-4 Two-Phase Collision Reference Oracle (Phase F1 Gold Standard).

Mathematical Formulation:
Local state: z = [f_0..f_8, g_0..g_8]^T in R^18.
1. Moments:
   rho = sum_{i=0}^8 f_i
   alpha = sum_{i=0}^8 g_i
   j_x = sum_{i=0}^8 c_ix f_i
   j_y = sum_{i=0}^8 c_iy f_i
2. Effective Velocity:
   u = [j + 0.5 F] / rho
3. Phase-Dependent Kinematic Viscosity and Relaxation:
   nu(alpha) = alpha * nu_L + (1 - alpha) * nu_G
   tau_f(alpha) = 3 * nu(alpha) + 0.5
   omega_f(alpha) = 1 / tau_f(alpha)
   omega_g = 1 / tau_g
4. Maxwellian Equilibrium Distributions:
   f_i^eq(rho, u) = w_i * rho * [1 + 3(c_i . u) + 4.5(c_i . u)^2 - 1.5 |u|^2]
   g_i^eq(alpha, u) = w_i * alpha * [1 + 3(c_i . u)]
5. Guo Forcing Source Term:
   S_i = (1 - 0.5*omega_f) * w_i * [3(c_i . F) + 9(c_i . u)(c_i . F) - 3(u . F)]
6. Post-Collision Populations:
   f_i' = f_i - omega_f(alpha) * (f_i - f_i^eq) + S_i
   g_i' = g_i - omega_g * (g_i - g_i^eq)
"""

from typing import Tuple, Dict, Any, Optional
import numpy as np
from classical.d2q9 import C_X, C_Y, W, CS2
from classical.equilibrium import compute_equilibrium


def reference_one_node_level4_collision(
    z: np.ndarray,
    nu_L: float = 0.05,
    nu_G: float = 0.01,
    tau_g: float = 0.70,
    force_vec: Optional[np.ndarray] = None,
    alpha_override: Optional[float] = None,
) -> Tuple[np.ndarray, Dict[str, Any]]:
    """
    Exact local Level-4 classical collision reference for one spatial node.
    
    Inputs:
    - z: input population vector of length 18 [f_0..f_8, g_0..g_8]
    - nu_L, nu_G: liquid and gas kinematic viscosities
    - tau_g: phase-field relaxation time
    - force_vec: external body force [Fx, Fy] (e.g. buoyancy, gravity, surface tension)
    - alpha_override: optional explicit phase fraction (if None, evaluated as sum(g))
    
    Returns:
    - z_prime: post-collision population vector of length 18
    - metadata: dict containing computed moments, equilibria, and relaxation times
    """
    z = np.asarray(z, dtype=np.float64)
    if z.shape != (18,):
        raise ValueError(f"Input state z must have shape (18,), got {z.shape}")

    f_in = z[:9].copy()
    g_in = z[9:].copy()

    # 1. Macroscopic moments
    rho = float(np.sum(f_in))
    if rho <= 0.0:
        raise ValueError(f"Non-physical non-positive density rho = {rho}")

    alpha = float(np.sum(g_in)) if alpha_override is None else float(alpha_override)
    alpha_clipped = float(np.clip(alpha, 0.0, 1.0))

    jx_raw = float(np.sum(f_in * C_X))
    jy_raw = float(np.sum(f_in * C_Y))

    # 2. Forcing and shifted fluid velocity
    if force_vec is None:
        Fx, Fy = 0.0, 0.0
    else:
        Fx, Fy = float(force_vec[0]), float(force_vec[1])

    ux = (jx_raw + 0.5 * Fx) / rho
    uy = (jy_raw + 0.5 * Fy) / rho
    u_vec = np.array([ux, uy], dtype=np.float64)

    # 3. Phase-dependent viscosity and relaxation time
    nu_mix = alpha_clipped * nu_L + (1.0 - alpha_clipped) * nu_G
    tau_f = 3.0 * nu_mix + 0.5
    omega_f = 1.0 / tau_f
    omega_g = 1.0 / tau_g

    # 4. Maxwellian equilibrium distributions
    rho_grid = np.array([[rho]])
    u_grid = u_vec[:, None, None]
    f_eq = compute_equilibrium(rho_grid, u_grid)[:, 0, 0]

    g_eq = np.zeros(9, dtype=np.float64)
    for i in range(9):
        c_dot_u = C_X[i] * ux + C_Y[i] * uy
        g_eq[i] = W[i] * alpha_clipped * (1.0 + 3.0 * c_dot_u)

    # 5. Guo forcing source term
    S_force = np.zeros(9, dtype=np.float64)
    if Fx != 0.0 or Fy != 0.0:
        u_dot_F = ux * Fx + uy * Fy
        for i in range(9):
            ci_F = C_X[i] * Fx + C_Y[i] * Fy
            ci_u = C_X[i] * ux + C_Y[i] * uy
            S_force[i] = (1.0 - 0.5 * omega_f) * W[i] * (3.0 * ci_F + 9.0 * ci_u * ci_F - 3.0 * u_dot_F)

    # 6. Post-collision populations
    f_out = f_in - omega_f * (f_in - f_eq) + S_force
    g_out = g_in - omega_g * (g_in - g_eq)

    z_prime = np.concatenate([f_out, g_out])

    metadata = {
        "rho": rho,
        "alpha": alpha,
        "alpha_clipped": alpha_clipped,
        "u": u_vec,
        "nu_mix": nu_mix,
        "tau_f": tau_f,
        "omega_f": omega_f,
        "omega_g": omega_g,
        "f_eq": f_eq,
        "g_eq": g_eq,
        "S_force": S_force,
        "force_vec": np.array([Fx, Fy]),
    }
    return z_prime, metadata
