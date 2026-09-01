import os

repo_dir = "/home/aswa/Research/QLBM-DamBreak"
classical_dir = os.path.join(repo_dir, "classical")
os.makedirs(classical_dir, exist_ok=True)

# 1. classical/d2q9.py
with open(os.path.join(classical_dir, "d2q9.py"), "w") as f:
    f.write("""\"\"\"
D2Q9 Lattice Constants, Velocity Vectors, and Weights.
\"\"\"
import numpy as np

# D2Q9 Discrete Velocities (c_x, c_y)
# c0 = (0, 0)
# c1 = (1, 0), c2 = (0, 1), c3 = (-1, 0), c4 = (0, -1)
# c5 = (1, 1), c6 = (-1, 1), c7 = (-1, -1), c8 = (1, -1)
C_X = np.array([0, 1, 0, -1, 0, 1, -1, -1, 1], dtype=np.int32)
C_Y = np.array([0, 0, 1, 0, -1, 1, 1, -1, -1], dtype=np.int32)
C = np.column_stack((C_X, C_Y))

# D2Q9 Lattice Weights
W = np.array([
    4.0 / 9.0,                                      # c0
    1.0 / 9.0, 1.0 / 9.0, 1.0 / 9.0, 1.0 / 9.0,    # c1, c2, c3, c4
    1.0 / 36.0, 1.0 / 36.0, 1.0 / 36.0, 1.0 / 36.0 # c5, c6, c7, c8
], dtype=np.float64)

# Speed of sound squared in lattice units
CS2 = 1.0 / 3.0

# Opposite direction indices for bounce-back
# 0->0, 1->3, 2->4, 3->1, 4->2, 5->7, 6->8, 7->5, 8->6
OPPOSITE = np.array([0, 3, 4, 1, 2, 7, 8, 5, 6], dtype=np.int32)
""")

# 2. classical/equilibrium.py
with open(os.path.join(classical_dir, "equilibrium.py"), "w") as f:
    f.write("""\"\"\"
Exact BGK Polynomial Equilibrium for D2Q9 Lattice.
\"\"\"
import numpy as np
from classical.d2q9 import C_X, C_Y, W, CS2

def compute_macroscopic(f):
    \"\"\"
    Compute macroscopic density rho and velocity field u from populations f.
    f shape: (9, Ny, Nx)
    Returns:
        rho: (Ny, Nx)
        u: (2, Ny, Nx)
    \"\"\"
    rho = np.sum(f, axis=0)
    # Avoid division by zero
    rho_safe = np.where(rho > 1e-14, rho, 1.0)
    ux = np.sum(C_X[:, None, None] * f, axis=0) / rho_safe
    uy = np.sum(C_Y[:, None, None] * f, axis=0) / rho_safe
    u = np.stack((ux, uy), axis=0)
    return rho, u

def compute_equilibrium(rho, u):
    \"\"\"
    Compute standard second-order BGK polynomial equilibrium:
    f_i^eq = w_i * rho * [1 + 3*(c_i . u) + 4.5*(c_i . u)^2 - 1.5*(u . u)]
    \"\"\"
    Ny, Nx = rho.shape
    f_eq = np.zeros((9, Ny, Nx), dtype=np.float64)
    u_sq = u[0]**2 + u[1]**2
    
    for i in range(9):
        c_dot_u = C_X[i] * u[0] + C_Y[i] * u[1]
        f_eq[i] = W[i] * rho * (1.0 + 3.0 * c_dot_u + 4.5 * (c_dot_u**2) - 1.5 * u_sq)
        
    return f_eq
""")

# 3. classical/collision.py
with open(os.path.join(classical_dir, "collision.py"), "w") as f:
    f.write("""\"\"\"
BGK Collision Operator for D2Q9.
\"\"\"
import numpy as np
from classical.equilibrium import compute_macroscopic, compute_equilibrium

def collide_bgk(f, omega, force=None):
    \"\"\"
    Single-relaxation-time (BGK) collision step:
    f_i^* = f_i - omega * (f_i - f_i^eq) + S_i(force)
    \"\"\"
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
""")

# 4. classical/streaming.py
with open(os.path.join(classical_dir, "streaming.py"), "w") as f:
    f.write("""\"\"\"
Exact Spatial Streaming Permutation for D2Q9 Lattice.
\"\"\"
import numpy as np
from classical.d2q9 import C_X, C_Y

def stream(f):
    \"\"\"
    Stream populations along discrete velocity directions:
    f_i(x + c_i, t + dt) = f_i^*(x, t)
    f shape: (9, Ny, Nx)
    \"\"\"
    f_streamed = np.zeros_like(f)
    for i in range(9):
        # Shift along y by C_Y[i], shift along x by C_X[i]
        f_streamed[i] = np.roll(np.roll(f[i], shift=C_Y[i], axis=0), shift=C_X[i], axis=1)
    return f_streamed
""")

# 5. classical/boundary.py
with open(os.path.join(classical_dir, "boundary.py"), "w") as f:
    f.write("""\"\"\"
Boundary Conditions for D2Q9 LBM (Periodic, Half-Way Bounce-Back, Walls, Obstacles).
\"\"\"
import numpy as np
from classical.d2q9 import OPPOSITE

def apply_periodic(f):
    \"\"\"
    Periodic boundary conditions are natively handled by np.roll in streaming.
    \"\"\"
    return f

def apply_bounce_back_walls(f_post_stream, f_pre_stream, solid_mask):
    \"\"\"
    Half-way bounce-back on solid obstacle nodes:
    Populations hitting solid nodes are reflected back in opposite direction:
    f_i(fluid) = f_opposite(solid)
    \"\"\"
    f_out = np.copy(f_post_stream)
    for i in range(9):
        opp = OPPOSITE[i]
        f_out[i, solid_mask] = f_pre_stream[opp, solid_mask]
    return f_out

def apply_noslip_box(f, f_coll):
    \"\"\"
    Enforce half-way bounce-back on all four domain perimeter walls (bottom, top, left, right).
    \"\"\"
    Ny, Nx = f.shape[1], f.shape[2]
    solid_mask = np.zeros((Ny, Nx), dtype=bool)
    solid_mask[0, :] = True
    solid_mask[-1, :] = True
    solid_mask[:, 0] = True
    solid_mask[:, -1] = True
    return apply_bounce_back_walls(f, f_coll, solid_mask)
""")

# 6. classical/dambreak.py
with open(os.path.join(classical_dir, "dambreak.py"), "w") as f:
    f.write("""\"\"\"
Classical Dam-Break Benchmark Solver using D2Q9 BGK LBM.
\"\"\"
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
        \"\"\"
        Execute one complete classical LBM timestep:
        1. Collision with gravity
        2. Streaming
        3. No-slip boundary reflection
        4. Macroscopic reconstruction
        \"\"\"
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
""")

print("Successfully generated all Phase 4 classical D2Q9 modules.")
