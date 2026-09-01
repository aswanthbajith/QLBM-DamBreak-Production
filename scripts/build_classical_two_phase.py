import os

repo_dir = "/home/aswa/Research/QLBM-DamBreak"
classical_dir = os.path.join(repo_dir, "classical")
tests_dir = os.path.join(repo_dir, "tests")

# 1. classical/two_phase.py
with open(os.path.join(classical_dir, "two_phase.py"), "w") as f:
    f.write("""\"\"\"
Classical Reference Solver for Reduced Two-Phase Lattice Boltzmann Dam-Break Hydrodynamics.
\"\"\"
import numpy as np
from classical.d2q9 import C_X, C_Y, W, CS2, OPPOSITE
from classical.equilibrium import compute_macroscopic, compute_equilibrium
from classical.streaming import stream
from classical.boundary import apply_noslip_box

def initialize_two_phase_dambreak(nx=4, ny=4, rho_liquid=1.0, rho_gas=0.1):
    \"\"\"
    Initializes a dam-break column of liquid on the left and gas on the right.
    Returns:
        phi: (Ny, Nx) phase field (1.0 for liquid, 0.0 for gas)
        rho: (Ny, Nx) macroscopic density
        u: (2, Ny, Nx) velocity field (initially zero)
        f: (9, Ny, Nx) hydrodynamic populations
        g: (9, Ny, Nx) order-parameter populations
    \"\"\"
    phi = np.zeros((ny, nx), dtype=np.float64)
    # Liquid column occupies left half (and lower half if specified)
    col_w = max(1, nx // 2)
    col_h = max(1, ny // 2)
    phi[:col_h, :col_w] = 1.0
    
    rho = phi * rho_liquid + (1.0 - phi) * rho_gas
    u = np.zeros((2, ny, nx), dtype=np.float64)
    
    f = compute_equilibrium(rho, u)
    
    # Order-parameter equilibrium
    g = np.zeros((9, ny, nx), dtype=np.float64)
    for i in range(9):
        c_dot_u = C_X[i] * u[0] + C_Y[i] * u[1]
        g[i] = W[i] * phi * (1.0 + 3.0 * c_dot_u)
        
    return phi, rho, u, f, g

def compute_phase_field(g):
    \"\"\"
    Extracts phase indicator phi = sum_i g_i. Clamped to [0, 1].
    \"\"\"
    phi = np.sum(g, axis=0)
    return np.clip(phi, 0.0, 1.0)

def compute_density(f):
    \"\"\"
    Extracts macroscopic density rho = sum_i f_i.
    \"\"\"
    return np.sum(f, axis=0)

def compute_velocity(f, rho):
    \"\"\"
    Extracts macroscopic velocity u = (sum_i c_i f_i) / rho.
    \"\"\"
    rho_safe = np.where(rho > 1e-14, rho, 1.0)
    ux = np.sum(C_X[:, None, None] * f, axis=0) / rho_safe
    uy = np.sum(C_Y[:, None, None] * f, axis=0) / rho_safe
    return np.stack((ux, uy), axis=0)

def collision_two_phase(f, g, phi, rho, u, tau_f=0.8, tau_g=0.7, g_acc=-0.001, rho_liquid=1.0, rho_gas=0.1):
    \"\"\"
    Executes coupled BGK collision for hydrodynamic and phase populations with gravitational buoyancy.
    \"\"\"
    omega_f = 1.0 / tau_f
    omega_g = 1.0 / tau_g
    
    # Phase collision
    g_eq = np.zeros_like(g)
    for i in range(9):
        c_dot_u = C_X[i] * u[0] + C_Y[i] * u[1]
        g_eq[i] = W[i] * phi * (1.0 + 3.0 * c_dot_u)
    g_out = g - omega_g * (g - g_eq)
    
    # Hydrodynamic collision with buoyancy force: F = (0, g_acc * (rho - rho_gas))
    f_eq = compute_equilibrium(rho, u)
    f_out = f - omega_f * (f - f_eq)
    
    fy = g_acc * (rho - rho_gas)
    for i in range(9):
        c_minus_u_y = C_Y[i] - u[1]
        c_dot_u = C_X[i] * u[0] + C_Y[i] * u[1]
        term = 3.0 * (c_minus_u_y * fy) + 9.0 * c_dot_u * (C_Y[i] * fy)
        source_i = (1.0 - 0.5 * omega_f) * W[i] * term
        f_out[i] += source_i
        
    return f_out, g_out

def stream_two_phase(f, g):
    \"\"\"
    Streams both hydrodynamic and phase populations along D2Q9 velocities.
    \"\"\"
    return stream(f), stream(g)

def apply_two_phase_boundary(f_post, g_post, f_pre, g_pre):
    \"\"\"
    Applies half-way bounce back on all domain enclosure walls.
    \"\"\"
    f_b = apply_noslip_box(f_post, f_pre)
    g_b = apply_noslip_box(g_post, g_pre)
    return f_b, g_b

def step_two_phase(f, g, tau_f=0.8, tau_g=0.7, g_acc=-0.001, rho_liquid=1.0, rho_gas=0.1):
    \"\"\"
    Advances the two-phase system by one complete LBM time step.
    \"\"\"
    phi = compute_phase_field(g)
    rho = compute_density(f)
    u = compute_velocity(f, rho)
    
    f_coll, g_coll = collision_two_phase(f, g, phi, rho, u, tau_f, tau_g, g_acc, rho_liquid, rho_gas)
    f_stream, g_stream = stream_two_phase(f_coll, g_coll)
    f_next, g_next = apply_two_phase_boundary(f_stream, g_stream, f_coll, g_coll)
    
    phi_next = compute_phase_field(g_next)
    rho_next = compute_density(f_next)
    u_next = compute_velocity(f_next, rho_next)
    
    return f_next, g_next, phi_next, rho_next, u_next

def run_two_phase_dambreak(nx=4, ny=4, timesteps=5, tau_f=0.8, tau_g=0.7, g_acc=-0.001):
    \"\"\"
    Runs the classical two-phase dam-break simulation for given number of timesteps.
    \"\"\"
    phi, rho, u, f, g = initialize_two_phase_dambreak(nx, ny)
    history = [{
        "step": 0,
        "phi": np.copy(phi),
        "rho": np.copy(rho),
        "u": np.copy(u),
        "total_liquid_mass": float(np.sum(phi)),
        "total_mass": float(np.sum(rho))
    }]
    
    for t in range(1, timesteps + 1):
        f, g, phi, rho, u = step_two_phase(f, g, tau_f, tau_g, g_acc)
        history.append({
            "step": t,
            "phi": np.copy(phi),
            "rho": np.copy(rho),
            "u": np.copy(u),
            "total_liquid_mass": float(np.sum(phi)),
            "total_mass": float(np.sum(rho))
        })
        
    return history
""")

# 2. tests/test_two_phase_classical.py
with open(os.path.join(tests_dir, "test_two_phase_classical.py"), "w") as f:
    f.write("""import pytest
import numpy as np
from classical.two_phase import (
    initialize_two_phase_dambreak,
    step_two_phase,
    run_two_phase_dambreak,
    compute_phase_field,
    compute_density,
    compute_velocity
)

class TestTwoPhaseClassical:
    def test_01_initialization_bounds(self):
        phi, rho, u, f, g = initialize_two_phase_dambreak(4, 4)
        assert phi.shape == (4, 4)
        assert np.all(phi >= 0.0) and np.all(phi <= 1.0)
        assert np.all(rho >= 0.1) and np.all(rho <= 1.0)
        assert np.allclose(u, 0.0)

    def test_02_mass_conservation_and_phase_bounds(self):
        history = run_two_phase_dambreak(nx=4, ny=4, timesteps=5)
        initial_mass = history[0]["total_mass"]
        initial_liq = history[0]["total_liquid_mass"]
        
        for record in history:
            phi = record["phi"]
            rho = record["rho"]
            u = record["u"]
            # Phase bounded in [0, 1]
            assert np.all(phi >= -1e-12) and np.all(phi <= 1.0 + 1e-12)
            # Density bounded
            assert np.all(rho > 0.0)
            # Mass conservation
            mass_drift = abs(record["total_mass"] - initial_mass) / initial_mass
            assert mass_drift < 0.05 # small domain boundary drift bound

    def test_03_grid_8x4_stability(self):
        history = run_two_phase_dambreak(nx=8, ny=4, timesteps=3)
        assert len(history) == 4
        assert history[-1]["step"] == 3
""")

print("Successfully generated classical two-phase reference solver and unit test.")
