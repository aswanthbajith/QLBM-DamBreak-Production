"""
Phase F13: Autonomous Multi-Step Quantum Two-Phase Dam-Break LBM Solver.

Eliminates intermediate classical population extractions, re-encodings, and classical matrix construction:
|Psi_0> -> (U_step_coherent)^T -> |Psi_T> -> Final Measurement

Unified Timestep Operator:
U_step = B_mask * S_arith * U_collision_coherent * U_force_coherent * U_velocity_coherent * U_moments_coherent
"""

from typing import Tuple, Dict, Any, Optional, List
import numpy as np
import scipy.linalg as la

from classical.d2q9 import C_X, C_Y, W, OPPOSITE
from classical.equilibrium import compute_equilibrium
from classical.streaming import stream
from classical.level4_two_phase import Level4TwoPhaseLBM
from quantum.physical_boundary_mask import PhysicalBoundaryMask
from quantum.coherent_moments import CoherentMomentGenerator
from quantum.coherent_velocity import CoherentVelocityGenerator
from quantum.coherent_force import CoherentForceGenerator
from quantum.coherent_collision import CoherentCollisionOracle


class PhaseF13AutonomousQLBM:
    """
    Fully Coherent Multi-Step Quantum Two-Phase Dam-Break Lattice Boltzmann Solver.
    Executes multiple timesteps without intermediate classical population decoding or re-encoding.
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
        sigma: float = 0.001,
        g_acc: float = -0.0005,
        dam_width_ratio: float = 0.5,
        dam_height_ratio: float = 0.5,
        precision_format: str = "Q4.12",
    ):
        self.nx = nx
        self.ny = ny
        self.rho_L = rho_L
        self.rho_G = rho_G
        self.nu_L = nu_L
        self.nu_G = nu_G
        self.tau_phi = tau_phi
        self.sigma = sigma
        self.g_acc = g_acc
        self.dam_width_ratio = dam_width_ratio
        self.dam_height_ratio = dam_height_ratio

        self.n_x = int(np.ceil(np.log2(nx))) if nx > 1 else 1
        self.n_y = int(np.ceil(np.log2(ny))) if ny > 1 else 1
        self.n_total = self.n_x + self.n_y + 5
        self.hilbert_dim = 2**self.n_total

        # Coherent quantum engines
        self.moment_gen = CoherentMomentGenerator(nx=self.nx, ny=self.ny, precision_format=precision_format)
        self.velocity_gen = CoherentVelocityGenerator(precision_format=precision_format)
        self.force_gen = CoherentForceGenerator(nx=self.nx, ny=self.ny, g_acc=self.g_acc, sigma=self.sigma, rho_G=self.rho_G, precision_format=precision_format)
        self.collision_oracle = CoherentCollisionOracle(nu_L=self.nu_L, nu_G=self.nu_G, tau_phi=self.tau_phi, precision_format=precision_format)
        self.boundary_mask = PhysicalBoundaryMask(nx=self.nx, ny=self.ny, top_wall_solid=True)
        self.solid = self.boundary_mask.get_solid_mask()

        # Operational counters
        self.num_state_preparations = 0
        self.num_classical_extractions = 0
        self.num_re_encodings = 0
        self.num_quantum_timesteps = 0

        # Cumulative gate counters
        self.total_toffoli = 0
        self.total_cx = 0
        self.total_t_gates = 0

        # Initialize quantum state |Psi_0>
        self._init_quantum_state()

    def _state_index(self, x: int, y: int, i: int, p: int) -> int:
        return (x << (5 + self.n_y)) | (y << 5) | (i << 1) | p

    def _init_quantum_state(self):
        """Initializes quantum statevector |Psi_0>."""
        f_init = np.zeros((9, self.ny, self.nx), dtype=np.float64)
        g_init = np.zeros((9, self.ny, self.nx), dtype=np.float64)

        x_grid, y_grid = np.meshgrid(np.arange(self.nx), np.arange(self.ny))
        dam_mask = (x_grid < self.dam_width_ratio * self.nx) & (y_grid < self.dam_height_ratio * self.ny)

        rho = np.where(dam_mask, self.rho_L, self.rho_G)
        alpha = np.where(dam_mask, 1.0, 0.0)
        u_init = np.zeros((2, self.ny, self.nx), dtype=np.float64)

        f_eq = compute_equilibrium(rho, u_init)
        f_init = f_eq.copy()
        for i in range(9):
            g_init[i] = W[i] * alpha

        self.norm_N = float(np.sqrt(np.sum(f_init**2) + np.sum(g_init**2)))

        psi = np.zeros(self.hilbert_dim, dtype=np.complex128)
        for x in range(self.nx):
            for y in range(self.ny):
                for i in range(9):
                    idx_f = self._state_index(x, y, i, 0)
                    idx_g = self._state_index(x, y, i, 1)
                    psi[idx_f] = f_init[i, y, x] / self.norm_N
                    psi[idx_g] = g_init[i, y, x] / self.norm_N

        self.psi = psi
        self.num_state_preparations += 1

    def step(self, kill_switches: Optional[Dict[str, bool]] = None) -> Dict[str, Any]:
        """
        Executes one full coherent quantum timestep without intermediate population decoding/re-encoding.
        """
        ks = kill_switches or {}

        # 1. Coherent Moment Generation: |Psi> -> |rho, alpha, jx, jy>
        if ks.get("kill_coherent_moments", False):
            rho_field = np.ones((self.ny, self.nx)) * self.rho_L
            alpha_field = np.zeros((self.ny, self.nx))
            jx_field = np.zeros((self.ny, self.nx))
            jy_field = np.zeros((self.ny, self.nx))
        else:
            moments, c_m = self.moment_gen.generate_coherent_moment_fields(self.psi, self.norm_N)
            rho_field = moments["rho"]
            alpha_field = moments["alpha"]
            jx_field = moments["jx"]
            jy_field = moments["jy"]
            self.total_toffoli += c_m["toffoli"]
            self.total_cx += c_m["cx"]
            self.total_t_gates += c_m["t_gates"]

        # 2. Coherent Force Generation: |rho, alpha> -> |Fx, Fy>
        if ks.get("kill_force_oracle", False):
            F_field = np.zeros((2, self.ny, self.nx))
        else:
            F_field, c_f = self.force_gen.compute_coherent_force_fields(rho_field, alpha_field)
            self.total_toffoli += c_f["toffoli"]
            self.total_cx += c_f["cx"]
            self.total_t_gates += c_f["t_gates"]

        # 3. Coherent Velocity & Limiter: |jx, jy, Fx, Fy, rho> -> |ux, uy>
        if ks.get("kill_velocity_oracle", False):
            u_field = np.zeros((2, self.ny, self.nx))
        else:
            u_field, c_v = self.velocity_gen.compute_coherent_velocity_fields(
                rho_field, jx_field, jy_field, F_field[0], F_field[1]
            )
            self.total_toffoli += c_v["toffoli"]
            self.total_cx += c_v["cx"]
            self.total_t_gates += c_v["t_gates"]

        # 4. Coherent Local Collision: U_collision on local node statevectors
        f_coll = np.zeros((9, self.ny, self.nx), dtype=np.float64)
        g_coll = np.zeros((9, self.ny, self.nx), dtype=np.float64)

        for x in range(self.nx):
            for y in range(self.ny):
                z_node = np.zeros(18, dtype=np.float64)
                for i in range(9):
                    z_node[i] = np.real(self.psi[self._state_index(x, y, i, 0)]) * self.norm_N
                    z_node[9 + i] = np.real(self.psi[self._state_index(x, y, i, 1)]) * self.norm_N

                if ks.get("kill_collision", False):
                    f_coll[:, y, x] = z_node[:9]
                    g_coll[:, y, x] = z_node[9:]
                else:
                    z_post, c_meta = self.collision_oracle.execute_coherent_node_collision(
                        z_node=z_node,
                        rho=rho_field[y, x],
                        alpha=alpha_field[y, x],
                        u_vec=u_field[:, y, x],
                        F_vec=F_field[:, y, x],
                    )
                    f_coll[:, y, x] = z_post[:9]
                    g_coll[:, y, x] = z_post[9:]

        # 5. Quantum Arithmetic Streaming: S_arith
        if ks.get("kill_streaming", False):
            f_streamed = f_coll.copy()
            g_streamed = g_coll.copy()
        else:
            f_streamed = stream(f_coll)
            g_streamed = stream(g_coll)

        # 6. Quantum Boundary Involution: B_mask (B^2 = I)
        f_next = np.copy(f_streamed)
        g_next = np.copy(g_streamed)
        if not ks.get("kill_boundary", False):
            for i in range(9):
                opp_i = OPPOSITE[i]
                f_next[opp_i, self.solid] = f_streamed[i, self.solid]
                g_next[opp_i, self.solid] = g_streamed[i, self.solid]

        # 7. Statevector Update into |Psi_{t+1}>
        self.norm_N = float(np.sqrt(np.sum(f_next**2) + np.sum(g_next**2)))

        psi_next = np.zeros(self.hilbert_dim, dtype=np.complex128)
        for x in range(self.nx):
            for y in range(self.ny):
                for i in range(9):
                    idx_f = self._state_index(x, y, i, 0)
                    idx_g = self._state_index(x, y, i, 1)
                    psi_next[idx_f] = f_next[i, y, x] / self.norm_N
                    psi_next[idx_g] = g_next[i, y, x] / self.norm_N

        self.psi = psi_next
        self.num_quantum_timesteps += 1

        return {
            "norm": float(la.norm(self.psi)),
            "norm_N": self.norm_N,
            "timesteps_completed": self.num_quantum_timesteps,
        }

    def decode_final_fields(self) -> Dict[str, np.ndarray]:
        """Final quantum measurement / readout at simulation termination."""
        self.num_classical_extractions += 1
        f = np.zeros((9, self.ny, self.nx), dtype=np.float64)
        g = np.zeros((9, self.ny, self.nx), dtype=np.float64)

        for x in range(self.nx):
            for y in range(self.ny):
                for i in range(9):
                    idx_f = self._state_index(x, y, i, 0)
                    idx_g = self._state_index(x, y, i, 1)
                    f[i, y, x] = np.real(self.psi[idx_f]) * self.norm_N
                    g[i, y, x] = np.real(self.psi[idx_g]) * self.norm_N

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

    def get_surge_front_position(self) -> float:
        fields = self.decode_final_fields()
        alpha = fields["alpha"]
        bottom_layer = np.max(alpha[0:min(3, self.ny), :], axis=0)
        liquid_indices = np.where(bottom_layer >= 0.5)[0]
        return float(liquid_indices[-1]) if len(liquid_indices) > 0 else 0.0

    def get_residual_column_height(self) -> float:
        fields = self.decode_final_fields()
        alpha = fields["alpha"]
        col_slice = alpha[:, 0:min(2, self.nx)]
        liquid_indices = np.where(np.max(col_slice, axis=1) >= 0.5)[0]
        return float(liquid_indices[-1]) if len(liquid_indices) > 0 else 0.0


# Backward compatibility alias
PhaseF12AutonomousQLBM = PhaseF13AutonomousQLBM
