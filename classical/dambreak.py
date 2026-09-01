"""
Classical Dam-Break Benchmark Solver using D2Q9 BGK LBM.
"""
import numpy as np
from classical.d2q9 import W
from classical.equilibrium import compute_macroscopic, compute_equilibrium
from classical.collision import collide_bgk
from classical.streaming import stream
from classical.boundary import apply_noslip_box

class ClassicalDamBreakSolver:
    def __init__(self, nx=8, ny=8, rho_liquid=1.0, rho_gas=0.1, tau=0.8, g=-0.001):
        self.nx = nx
        self.ny = ny
        self.rho_l = rho_liquid
        self.rho_g = rho_gas
        self.tau = tau
        self.omega = 1.0 / tau
        self.g = g
        
        # Initialize domain
        self.rho = np.ones((ny, nx), dtype=np.float64) * rho_gas
        # Column of water in bottom-left corner
        col_w = max(1, nx // 2)
        col_h = max(1, ny // 2)
        self.rho[:col_h, :col_w] = rho_liquid
        
        self.u = np.zeros((2, ny, nx), dtype=np.float64)
        self.f = compute_equilibrium(self.rho, self.u)
        self.initial_mass = np.sum(self.rho)
        self.time = 0

    def step(self):
        """
        Execute one complete classical LBM timestep:
        1. Collision with gravity
        2. Streaming
        3. No-slip boundary reflection
        4. Macroscopic reconstruction
        """
        force = np.zeros((2, self.ny, self.nx))
        force[1] = self.g * (self.rho - self.rho_g) # buoyancy / gravity
        
        f_coll = collide_bgk(self.f, self.omega, force=force)
        f_stream = stream(f_coll)
        self.f = apply_noslip_box(f_stream, f_coll)
        
        self.rho, self.u = compute_macroscopic(self.f)
        self.time += 1
        
        current_mass = np.sum(self.rho)
        mass_drift = abs(current_mass - self.initial_mass) / self.initial_mass
        return {
            "time": self.time,
            "mean_density": np.mean(self.rho),
            "max_velocity": np.max(np.sqrt(self.u[0]**2 + self.u[1]**2)),
            "mass_drift": mass_drift
        }
