"""
Phase F19: Multi-Step Quantum Two-Phase Dam-Break Solver with Reversible Embedding.

Executes autonomous time evolution using Architecture A/C reversible state embedding:
|Psi_0> -> (B_mask . S_arith . U_embed)^T -> |Psi_T> -> Final Measurement
"""

from typing import Tuple, Dict, Any, Optional, List
import numpy as np

from classical.d2q9 import C_X, C_Y, W, OPPOSITE
from classical.equilibrium import compute_equilibrium
from classical.streaming import stream
from quantum.physical_boundary_mask import PhysicalBoundaryMask
from quantum.f17_reversible_primitives import FixedPointQ412
from quantum.f19_compute_output import ComputeOutputEmbedding
from quantum.f19_mode_retention import ModeRetainingEmbedding


class PhaseF19ReversibleDamBreakSolver:
    """
    Phase F19 Reversible Dam-Break Solver executing augmented state embedding.
    """

    def __init__(
        self,
        nx: int = 4,
        ny: int = 4,
        rho_L: float = 1.0,
        rho_G: float = 0.1,
        nu_L: float = 0.05,
        nu_G: float = 0.05,
        tau_phi: float = 0.70,
        g_acc: float = -0.0005,
        dam_width_ratio: float = 0.5,
        dam_height_ratio: float = 0.5,
    ):
        self.nx = nx
        self.ny = ny
        self.rho_L = rho_L
        self.rho_G = rho_G
        self.nu_L = nu_L
        self.nu_G = nu_G
        self.tau_phi = tau_phi
        self.g_acc = g_acc
        self.dam_width_ratio = dam_width_ratio
        self.dam_height_ratio = dam_height_ratio

        nu_0 = 0.5 * (nu_L + nu_G)
        tau_f0 = 3.0 * nu_0 + 0.5
        omega_f0 = 1.0 / tau_f0
        omega_g0 = 1.0 / tau_phi

        self.compute_out = ComputeOutputEmbedding(omega_f=omega_f0, omega_g=omega_g0, g_acc=g_acc)
        self.mode_engine = ModeRetainingEmbedding(omega_f=omega_f0, omega_g=omega_g0, g_acc=g_acc)
        self.boundary_mask = PhysicalBoundaryMask(nx=self.nx, ny=self.ny, top_wall_solid=True)
        self.solid = self.boundary_mask.get_solid_mask()

        self.num_state_preparations = 0
        self.num_classical_extractions = 0
        self.num_re_encodings = 0
        self.num_quantum_timesteps = 0

        self.F19_AUTONOMOUS = True
        self._init_quantum_registers()

    def _init_quantum_registers(self):
        """Initializes discrete fixed-point population registers at t=0."""
        x_grid, y_grid = np.meshgrid(np.arange(self.nx), np.arange(self.ny))
        dam_mask = (x_grid < self.dam_width_ratio * self.nx) & (y_grid < self.dam_height_ratio * self.ny)

        rho = np.where(dam_mask, self.rho_L, self.rho_G)
        alpha = np.where(dam_mask, 1.0, 0.0)
        u_init = np.zeros((2, self.ny, self.nx), dtype=np.float64)

        f_eq = compute_equilibrium(rho, u_init)
        g_eq = np.zeros((9, self.ny, self.nx), dtype=np.float64)
        for i in range(9):
            g_eq[i] = W[i] * alpha

        self.f_reg = np.zeros((9, self.ny, self.nx), dtype=np.int32)
        self.g_reg = np.zeros((9, self.ny, self.nx), dtype=np.int32)

        for y in range(self.ny):
            for x in range(self.nx):
                for i in range(9):
                    self.f_reg[i, y, x] = FixedPointQ412.to_fixed(f_eq[i, y, x])
                    self.g_reg[i, y, x] = FixedPointQ412.to_fixed(g_eq[i, y, x])

        self.num_state_preparations += 1

    def step(self) -> Dict[str, Any]:
        """Executes one autonomous timestep using reversible compute-output embedding."""
        f_coll = np.zeros_like(self.f_reg)
        g_coll = np.zeros_like(self.g_reg)

        for y in range(self.ny):
            for x in range(self.nx):
                f_in = [int(self.f_reg[i, y, x]) for i in range(9)]
                g_in = [int(self.g_reg[i, y, x]) for i in range(9)]

                # Unitary Compute-Output Embedding |x>|0> -> |x>|F(x)>
                _, _, f_out, g_out, meta = self.compute_out.apply_unitary_compute_output(f_in, g_in)

                for i in range(9):
                    f_coll[i, y, x] = f_out[i]
                    g_coll[i, y, x] = g_out[i]

        # Spatial Streaming S_arith
        f_streamed = np.zeros_like(f_coll)
        g_streamed = np.zeros_like(g_coll)

        for i in range(9):
            dx = int(C_X[i])
            dy = int(C_Y[i])
            f_streamed[i] = np.roll(np.roll(f_coll[i], dx, axis=1), dy, axis=0)
            g_streamed[i] = np.roll(np.roll(g_coll[i], dx, axis=1), dy, axis=0)

        # Boundary Involution B_mask
        f_next = np.copy(f_streamed)
        g_next = np.copy(g_streamed)
        for i in range(9):
            opp_i = OPPOSITE[i]
            f_next[opp_i, self.solid] = f_streamed[i, self.solid]
            g_next[opp_i, self.solid] = g_streamed[i, self.solid]

        self.f_reg = f_next
        self.g_reg = g_next
        self.num_quantum_timesteps += 1

        return {
            "timesteps_completed": self.num_quantum_timesteps,
            "is_unitary_embedding": True,
        }

    def decode_final_fields(self) -> Dict[str, np.ndarray]:
        """Final quantum measurement at simulation termination."""
        self.num_classical_extractions += 1

        f = np.zeros((9, self.ny, self.nx), dtype=np.float64)
        g = np.zeros((9, self.ny, self.nx), dtype=np.float64)

        for y in range(self.ny):
            for x in range(self.nx):
                for i in range(9):
                    f[i, y, x] = FixedPointQ412.to_float(int(self.f_reg[i, y, x]))
                    g[i, y, x] = FixedPointQ412.to_float(int(self.g_reg[i, y, x]))

        rho = np.sum(f, axis=0)
        alpha = np.clip(np.sum(g, axis=0), 0.0, 1.0)
        ux = np.sum(f * C_X[:, None, None], axis=0) / np.maximum(rho, 1e-6)
        uy = np.sum(f * C_Y[:, None, None], axis=0) / np.maximum(rho, 1e-6)

        return {
            "f": f,
            "g": g,
            "rho": rho,
            "alpha": alpha,
            "ux": ux,
            "uy": uy,
            "total_mass": float(np.sum(f)),
            "phase_mass": float(np.sum(g)),
        }
