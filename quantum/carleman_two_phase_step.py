"""
Quantum Carleman Multi-Step Solver for Two-Phase D2Q9 Dam-Break Hydrodynamics.

Integrates:
1. Local Second-Order Carleman Linearization (Order 2, dim 342)
2. Unitary Dilation / Block Encoding with Ancilla Postselection & Scaling Tracking
3. Exact Discrete Spatial Streaming Permutations
4. Half-Way Bounce-Back Boundary Reflection
"""
import numpy as np
import scipy.linalg as la
from classical.d2q9 import C_X, C_Y, W
from classical.reference_solver import (
    initialize_two_phase_dambreak,
    compute_phase_field,
    compute_density,
    compute_velocity,
    apply_force,
    stream_two_phase,
    apply_two_phase_boundary
)
from quantum.two_phase_carleman import (
    build_two_phase_carleman_operator,
    lift_two_phase_state,
    project_two_phase_state
)
from quantum.unitary_dilation import (
    normalize_operator,
    build_unitary_dilation,
    apply_block_encoding
)


# Global cache for block-encoded Carleman dilation operators
_DILATION_CACHE = {}

def get_cached_carleman_dilation(tau_f=0.8, tau_g=0.7, rho0=1.0, order=2):
    """
    Returns (C_local, U_dilated, alpha) from cache, computing only on cache miss.
    """
    cache_key = (round(float(rho0), 3), float(tau_f), float(tau_g), int(order))
    if cache_key in _DILATION_CACHE:
        return _DILATION_CACHE[cache_key]
        
    C_local = build_two_phase_carleman_operator(tau_f=tau_f, tau_g=tau_g, rho0=rho0, order=order)
    C_scaled, alpha = normalize_operator(C_local)
    U_dilated = build_unitary_dilation(C_scaled)
    
    _DILATION_CACHE[cache_key] = (C_local, U_dilated, alpha)
    return C_local, U_dilated, alpha


def quantum_carleman_two_phase_step(nx=4, ny=4, timesteps=5,
                                    tau_f=0.8, tau_g=0.7, g_acc=-0.001,
                                    order=2, use_block_encoding=True):
    """
    Executes multi-step two-phase dam-break simulation using Local Carleman Linearization
    and Unitary Dilation / Block Encoding.
    
    Returns:
        history: list of time-step records containing (step, f, g, phi, rho, u, total_mass,
                 total_liquid_mass, p_success_mean, alpha_mean)
    """
    phi, rho, u, f, g = initialize_two_phase_dambreak(nx, ny)
    
    history = [{
        "step": 0,
        "f": np.copy(f),
        "g": np.copy(g),
        "phi": np.copy(phi),
        "rho": np.copy(rho),
        "u": np.copy(u),
        "total_liquid_mass": float(np.sum(phi)),
        "total_mass": float(np.sum(rho)),
        "p_success_mean": 1.0,
        "alpha_mean": 1.0
    }]
    
    f_curr, g_curr = np.copy(f), np.copy(g)
    
    for t in range(1, timesteps + 1):
        phi_curr = compute_phase_field(g_curr)
        rho_curr = compute_density(f_curr)
        u_curr = compute_velocity(f_curr, rho_curr)
        
        f_coll = np.zeros_like(f_curr)
        g_coll = np.zeros_like(g_curr)
        
        p_success_nodes = []
        alpha_nodes = []
        
        # 1. Local Carleman Collision with Unitary Dilation per lattice node
        for y in range(ny):
            for x in range(nx):
                f_node = f_curr[:, y, x]
                g_node = g_curr[:, y, x]
                rho_node = float(rho_curr[y, x])
                
                C_local, U_dilated, alpha = get_cached_carleman_dilation(
                    tau_f=tau_f, tau_g=tau_g, rho0=rho_node, order=order
                )
                
                if use_block_encoding:
                    Y_in = lift_two_phase_state(f_node, g_node, order=order)
                    norm_Y = float(np.linalg.norm(Y_in))
                    if norm_Y > 1e-14:
                        Y_normed = Y_in / norm_Y
                        res_block = apply_block_encoding(Y_normed, U_dilated, alpha=alpha)
                        Y_post = res_block["output_state"] * norm_Y
                        p_success_nodes.append(res_block["p_success"])
                    else:
                        Y_post = np.zeros_like(Y_in)
                        p_success_nodes.append(1.0)
                    alpha_nodes.append(alpha)
                else:
                    Y_in = lift_two_phase_state(f_node, g_node, order=order)
                    Y_post = C_local @ Y_in
                    p_success_nodes.append(1.0)
                    alpha_nodes.append(1.0)
                    
                f_star_node, g_star_node = project_two_phase_state(Y_post, order=order)
                f_coll[:, y, x] = np.maximum(f_star_node, 0.0)
                g_coll[:, y, x] = np.maximum(g_star_node, 0.0)
                
        # Apply gravitational buoyancy body forcing
        f_coll = apply_force(f_coll, rho_curr, u_curr, g_acc=g_acc, tau_f=tau_f)
        
        # 2. Exact Discrete Spatial Streaming Permutation
        f_stream, g_stream = stream_two_phase(f_coll, g_coll)
        
        # 3. Exact Half-Way Bounce-Back Boundary Reflection
        f_next, g_next = apply_two_phase_boundary(f_stream, g_stream, f_coll, g_coll)
        
        phi_next = compute_phase_field(g_next)
        rho_next = compute_density(f_next)
        u_next = compute_velocity(f_next, rho_next)
        
        f_curr, g_curr = f_next, g_next
        
        history.append({
            "step": t,
            "f": np.copy(f_next),
            "g": np.copy(g_next),
            "phi": np.copy(phi_next),
            "rho": np.copy(rho_next),
            "u": np.copy(u_next),
            "total_liquid_mass": float(np.sum(phi_next)),
            "total_mass": float(np.sum(rho_next)),
            "p_success_mean": float(np.mean(p_success_nodes)),
            "alpha_mean": float(np.mean(alpha_nodes))
        })
        
    return history
