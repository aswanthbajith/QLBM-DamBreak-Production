"""
Quantum Carleman Multi-Step Solver for Two-Phase D2Q9 Dam-Break Hydrodynamics.

Integrates:
1. Local Second-Order Carleman Truncated Step Evaluation A_eval in R^(18 x 342)
2. 10-Qubit Power-of-Two Unitary Dilation U_C in U(1024) with Ancilla Postselection
3. Physical Positivity Guard (Classical numerical admissibility)
4. Gravitational Body Forcing (Buoyancy)
5. Reversible Spatial Streaming Permutation S (S† S = I_512)
6. Direction-Selective Half-Way Bounce-Back Involution B (B† B = B² = I_512)
7. Macroscopic Observable Decoding and Re-Encoding (Hybrid Architecture)
"""
import numpy as np
from classical.reference_solver import (
    initialize_two_phase_dambreak,
    compute_phase_field,
    compute_density,
    compute_velocity,
    apply_force,
)
from quantum.two_phase_carleman import (
    lift_two_phase_state,
    build_second_order_evaluation_operator,
    apply_second_order_carleman,
)
from quantum.unitary_dilation import (
    normalize_operator,
    pad_rectangular_operator,
    build_unitary_dilation,
    apply_block_encoding,
)
from quantum.streaming import apply_quantum_streaming
from quantum.two_phase_boundary import apply_quantum_boundary


# Global cache for block-encoded Carleman dilation operators
_DILATION_CACHE = {}

def get_cached_carleman_dilation(tau_f=0.8, tau_g=0.7, rho0=1.0):
    """
    Returns (A_eval, U_dilated, alpha) from cache, computing only on cache miss.
    Embeds 18x342 evaluation operator into 512x512 square operator, dilated to 1024x1024 unitary.
    """
    cache_key = (round(float(rho0), 3), float(tau_f), float(tau_g))
    if cache_key in _DILATION_CACHE:
        return _DILATION_CACHE[cache_key]
        
    A_eval = build_second_order_evaluation_operator(tau_f=tau_f, tau_g=tau_g, rho0=rho0)
    A_padded = pad_rectangular_operator(A_eval, target_dim=512)
    A_scaled, alpha = normalize_operator(A_padded)
    U_dilated = build_unitary_dilation(A_scaled)
    
    _DILATION_CACHE[cache_key] = (A_eval, U_dilated, alpha)
    return A_eval, U_dilated, alpha


def quantum_carleman_two_phase_step(nx=4, ny=4, timesteps=5,
                                    tau_f=0.8, tau_g=0.7, g_acc=-0.001,
                                    order=2, use_block_encoding=True):
    """
    Executes multi-step hybrid two-phase dam-break simulation using Local Carleman Linearization,
    10-Qubit Unitary Dilation, Quantum Streaming S, and Boundary Bounce-Back B.
    
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
        # 1. Macroscopic moments
        phi_curr = compute_phase_field(g_curr)
        rho_curr = compute_density(f_curr)
        u_curr = compute_velocity(f_curr, rho_curr)
        
        f_coll = np.zeros_like(f_curr)
        g_coll = np.zeros_like(g_curr)
        
        p_success_nodes = []
        alpha_nodes = []
        
        # 2. Local Second-Order Carleman Collision with 10-Qubit Unitary Dilation per node
        for y in range(ny):
            for x in range(nx):
                f_node = f_curr[:, y, x]
                g_node = g_curr[:, y, x]
                local_rho = max(float(rho_curr[y, x]), 1e-12)
                
                if use_block_encoding:
                    A_eval, U_dilated, alpha = get_cached_carleman_dilation(
                        tau_f=tau_f, tau_g=tau_g, rho0=local_rho
                    )
                    Y_in = lift_two_phase_state(f_node, g_node, order=order)
                    res_block = apply_block_encoding(
                        Y_in, U_dilated, physical_dim=18, alpha=alpha
                    )
                    psi_next = res_block["output_state"]
                    f_next = psi_next[:9]
                    g_next = psi_next[9:18]
                    p_success_nodes.append(res_block["p_success"])
                    alpha_nodes.append(alpha)
                else:
                    f_next, g_next = apply_second_order_carleman(
                        f_node, g_node, tau_f=tau_f, tau_g=tau_g, rho0=local_rho
                    )
                    p_success_nodes.append(1.0)
                    alpha_nodes.append(1.0)
                    
                # Physical positivity guard (numerical admissibility)
                f_coll[:, y, x] = np.maximum(f_next, 0.0)
                g_coll[:, y, x] = np.maximum(g_next, 0.0)
                
        # 3. Gravitational buoyancy body forcing
        f_forced = apply_force(f_coll, rho_curr, u_curr, g_acc=g_acc, tau_f=tau_f)
        
        # 4. Reversible Spatial Streaming Permutation S
        f_stream, g_stream = apply_quantum_streaming(f_forced, g_coll)
        
        # 5. Direction-Selective Half-Way Bounce-Back Boundary Involution B
        f_next_step, g_next_step = apply_quantum_boundary(f_stream, g_stream)
        
        # 6. Reconstruct physical observables
        phi_next = compute_phase_field(g_next_step)
        rho_next = compute_density(f_next_step)
        u_next = compute_velocity(f_next_step, rho_next)
        
        # 7. Re-encoding occurs implicitly for next timestep
        f_curr, g_curr = f_next_step, g_next_step
        
        history.append({
            "step": t,
            "f": np.copy(f_curr),
            "g": np.copy(g_curr),
            "phi": np.copy(phi_next),
            "rho": np.copy(rho_next),
            "u": np.copy(u_next),
            "total_liquid_mass": float(np.sum(phi_next)),
            "total_mass": float(np.sum(rho_next)),
            "p_success_mean": float(np.mean(p_success_nodes)),
            "alpha_mean": float(np.mean(alpha_nodes))
        })
        
    return history


def run_hybrid_carleman_two_phase(nx=4, ny=4, timesteps=10,
                                  tau_f=0.8, tau_g=0.7, g_acc=-0.001):
    """Alias for direct execution with default parameters."""
    return quantum_carleman_two_phase_step(
        nx=nx, ny=ny, timesteps=timesteps,
        tau_f=tau_f, tau_g=tau_g, g_acc=g_acc,
        order=2, use_block_encoding=True
    )
