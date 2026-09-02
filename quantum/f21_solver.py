"""
Phase F21: Quantum Two-Phase Dam-Break Solver with Reversible CSF Surface Tension.

Executes autonomous multi-step time evolution with active interfacial surface tension:
rho_0, alpha_0 -> [ CSF -> Guo Force -> Collision -> Streaming -> Boundary ]^T -> Final Measurement
"""

from typing import Dict, Any, List
import numpy as np

from classical.d2q9 import C_X, C_Y, W, OPPOSITE
from classical.equilibrium import compute_equilibrium
from quantum.physical_boundary_mask import PhysicalBoundaryMask
from quantum.f17_reversible_primitives import FixedPointQ412
from quantum.f20_fixed_point import F20FixedPointBGKEngine
from quantum.f21_csf import F21ReversibleCSFPipeline
from quantum.f21_fixed_point import F21FixedPointCSFMath


class PhaseF21ReversibleCSFSolver:
    """
    Phase F21 Quantum Two-Phase Solver with reversible CSF channel.
    """

    def __init__(
        self,
        nx: int = 4,
        ny: int = 4,
        rho_L: float = 1.0,
        rho_G: float = 0.1,
        nu_L: float = 0.05,
        nu_G: float = 0.05,
        sigma: float = 0.001,
        tau_phi: float = 0.70,
        g_acc: float = -0.0005,
        dam_width_ratio: float = 0.5,
        dam_height_ratio: float = 0.5,
        frac_bits: int = 12,
    ):
        self.nx = nx
        self.ny = ny
        self.rho_L = rho_L
        self.rho_G = rho_G
        self.nu_L = nu_L
        self.nu_G = nu_G
        self.sigma = sigma
        self.tau_phi = tau_phi
        self.g_acc = g_acc
        self.dam_width_ratio = dam_width_ratio
        self.dam_height_ratio = dam_height_ratio
        self.frac_bits = frac_bits

        nu_0 = 0.5 * (nu_L + nu_G)
        tau_f0 = 3.0 * nu_0 + 0.5
        omega_f0 = 1.0 / tau_f0
        omega_g0 = 1.0 / tau_phi

        self.math = F21FixedPointCSFMath(frac_bits=frac_bits)
        self.bgk_engine = F20FixedPointBGKEngine(omega_f=omega_f0, omega_g=omega_g0, g_acc=g_acc)
        self.csf_pipeline = F21ReversibleCSFPipeline(nx, ny, sigma=sigma, frac_bits=frac_bits)
        self.boundary_mask = PhysicalBoundaryMask(nx=self.nx, ny=self.ny, top_wall_solid=True)
        self.solid = self.boundary_mask.get_solid_mask()

        self.num_state_preparations = 0
        self.num_classical_extractions = 0
        self.num_re_encodings = 0
        self.num_quantum_timesteps = 0

        self.F21_AUTONOMOUS = True
        self._init_state()

    def _init_state(self):
        """Initializes discrete population registers at t=0."""
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
                    self.f_reg[i, y, x] = self.math.to_fixed(f_eq[i, y, x])
                    self.g_reg[i, y, x] = self.math.to_fixed(g_eq[i, y, x])

        self.num_state_preparations += 1

    def step(self) -> Dict[str, Any]:
        """Executes one autonomous quantum step with reversible CSF surface tension."""
        ny, nx = self.ny, self.nx

        # 1. Recover alpha register internally from g_reg
        alpha_reg = np.zeros((ny, nx), dtype=np.int32)
        for y in range(ny):
            for x in range(nx):
                sum_g = sum(int(self.g_reg[i, y, x]) for i in range(9))
                alpha_reg[y, x] = self.math.fixed_clip(sum_g, 0.0, 1.0)

        # 2. Reversible CSF Force Calculation
        F_sx, F_sy, csf_meta = self.csf_pipeline.execute_reversible_csf(alpha_reg)

        # 3. Collision with combined gravity + CSF forcing
        f_coll = np.zeros_like(self.f_reg)
        g_coll = np.zeros_like(self.g_reg)

        for y in range(ny):
            for x in range(nx):
                f_in = [int(self.f_reg[i, y, x]) for i in range(9)]
                g_in = [int(self.g_reg[i, y, x]) for i in range(9)]
                f_ext_node = (int(F_sx[y, x]), int(F_sy[y, x]))

                # Add CSF force to momentum evaluation in BGK
                f_out, g_out, meta = self.bgk_engine.evaluate_bgk_map(f_in, g_in, F_ext=f_ext_node)

                for i in range(9):
                    f_coll[i, y, x] = f_out[i]
                    g_coll[i, y, x] = g_out[i]

        # 4. Spatial Streaming Permutation S_arith
        f_streamed = np.zeros_like(f_coll)
        g_streamed = np.zeros_like(g_coll)

        for i in range(9):
            dx = int(C_X[i])
            dy = int(C_Y[i])
            f_streamed[i] = np.roll(np.roll(f_coll[i], dx, axis=1), dy, axis=0)
            g_streamed[i] = np.roll(np.roll(g_coll[i], dx, axis=1), dy, axis=0)

        # 5. Boundary Mask Involution B_mask
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
            "csf_is_uncomputed": csf_meta["is_uncomputed"],
            "is_autonomous": True,
        }

    def decode_final_fields(self) -> Dict[str, np.ndarray]:
        """Final quantum readout at simulation termination."""
        self.num_classical_extractions += 1

        f = np.zeros((9, self.ny, self.nx), dtype=np.float64)
        g = np.zeros((9, self.ny, self.nx), dtype=np.float64)

        for y in range(self.ny):
            for x in range(self.nx):
                for i in range(9):
                    f[i, y, x] = self.math.to_float(int(self.f_reg[i, y, x]))
                    g[i, y, x] = self.math.to_float(int(self.g_reg[i, y, x]))

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
