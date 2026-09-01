"""
Canonical Classical Two-Phase D2Q9 Lattice Boltzmann Dam-Break Reference Solver.

Used exclusively as the deterministic ground truth for fluid observables.
"""
import numpy as np
from classical.d2q9 import C_X, C_Y, W, OPPOSITE
from classical.equilibrium import compute_equilibrium, compute_phase_equilibrium
from classical.two_phase import (
    initialize_two_phase_dambreak,
    compute_density,
    compute_velocity,
    compute_phase_field
)
from quantum.streaming import apply_quantum_streaming
from quantum.two_phase_boundary import apply_quantum_boundary


def apply_force(f, rho, u, g_acc=-0.001, rho_gas=0.1, tau_f=0.8):
    """
    Applies buoyancy body force using Shan-Chen / Guo formulation.
    Delta f_i = 3 * w_i * (rho - rho_gas) * g_y * c_iy
    """
    f_out = np.copy(f)
    delta_rho = rho - rho_gas
    
    for i in range(9):
        f_i_force = 3.0 * W[i] * delta_rho * g_acc * C_Y[i]
        f_out[i] += f_i_force
        
    return f_out


def collision_two_phase(f, g, phi, rho, u, tau_f=0.8, tau_g=0.7, g_acc=-0.001, rho_liquid=1.0, rho_gas=0.1):
    """
    Executes coupled BGK collision for hydrodynamic and phase populations with gravitational buoyancy.
    """
    omega_f = 1.0 / tau_f
    omega_g = 1.0 / tau_g
    
    # Phase collision
    g_eq = np.zeros_like(g)
    for i in range(9):
        c_dot_u = C_X[i] * u[0] + C_Y[i] * u[1]
        g_eq[i] = W[i] * phi * (1.0 + 3.0 * c_dot_u)
    g_out = g - omega_g * (g - g_eq)
    
    # Hydrodynamic collision
    f_eq = compute_equilibrium(rho, u)
    f_out = f - omega_f * (f - f_eq)
    
    # Gravitational buoyancy forcing
    f_out = apply_force(f_out, rho, u, g_acc, rho_gas, tau_f)
        
    return f_out, g_out


def stream_two_phase(f, g=None):
    """
    Applies spatial streaming along D2Q9 velocities.
    """
    if g is not None:
        return apply_quantum_streaming(f, g)
    g_dummy = np.zeros_like(f)
    f_s, _ = apply_quantum_streaming(f, g_dummy)
    return f_s


def apply_two_phase_boundary(f_stream, g_stream, f_pre=None, g_pre=None):
    """
    Applies direction-selective half-way bounce-back on solid enclosure walls.
    """
    return apply_quantum_boundary(f_stream, g_stream)


def step_two_phase(f, g, tau_f=0.8, tau_g=0.7, g_acc=-0.001, rho_liquid=1.0, rho_gas=0.1):
    """
    Advances the two-phase system by one complete LBM time step.
    1. Collision + Body Force
    2. Streaming S
    3. Boundary B
    4. Observable moments (rho, u, phi)
    """
    phi = compute_phase_field(g)
    rho = compute_density(f)
    u = compute_velocity(f, rho)
    
    f_coll, g_coll = collision_two_phase(f, g, phi, rho, u, tau_f, tau_g, g_acc, rho_liquid, rho_gas)
    f_stream, g_stream = stream_two_phase(f_coll, g_coll)
    f_next, g_next = apply_two_phase_boundary(f_stream, g_stream)
    
    phi_next = compute_phase_field(g_next)
    rho_next = compute_density(f_next)
    u_next = compute_velocity(f_next, rho_next)
    
    return f_next, g_next, phi_next, rho_next, u_next


def run_two_phase_dambreak(nx=4, ny=4, timesteps=5, tau_f=0.8, tau_g=0.7, g_acc=-0.001):
    """
    Runs the canonical classical two-phase dam-break simulation.
    Returns:
        history: list of dicts with step snapshots (f, g, phi, rho, u, total_mass, total_liquid_mass)
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
        "total_mass": float(np.sum(rho))
    }]
    
    f_curr, g_curr = np.copy(f), np.copy(g)
    
    for t in range(1, timesteps + 1):
        f_next, g_next, phi_next, rho_next, u_next = step_two_phase(
            f_curr, g_curr, tau_f=tau_f, tau_g=tau_g, g_acc=g_acc
        )
        f_curr, g_curr = f_next, g_next
        
        history.append({
            "step": t,
            "f": np.copy(f_curr),
            "g": np.copy(g_curr),
            "phi": np.copy(phi_next),
            "rho": np.copy(rho_next),
            "u": np.copy(u_next),
            "total_liquid_mass": float(np.sum(phi_next)),
            "total_mass": float(np.sum(rho_next))
        })
        
    return history
