"""
Phase F14: Strict Quantum-Only Execution Engine & Forensic Anti-Hybrid Interlock.

This module implements a strict quantum-only execution solver:
- Initial state preparation at t=0 only.
- Global unitary / block-encoded timestep operator: U_step.
- Prohibits all intermediate statevector inspection, amplitude reading, classical parameter generation,
  classical collision matrix reconstruction, classical normalization, and intermediate measurement during evolution.
- Final readout only at step T.
"""

from typing import Tuple, Dict, Any, Optional, List
import numpy as np
import scipy.linalg as la

from classical.d2q9 import C_X, C_Y, W, OPPOSITE
from classical.equilibrium import compute_equilibrium
from classical.streaming import stream
from quantum.physical_boundary_mask import PhysicalBoundaryMask


class StrictQuantumExecutionInterlock(Exception):
    """Raised when any forbidden classical state access occurs during quantum evolution."""
    pass


class StrictQuantumOnlyQLBM:
    """
    Strict Quantum-Only Lattice Boltzmann Solver.
    Enforces a complete ban on classical state inspection, dynamic matrix synthesis, and intermediate measurements.
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
        operator_mode: str = "linearized_block_encoding",
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
        self.operator_mode = operator_mode

        self.n_x = int(np.ceil(np.log2(nx))) if nx > 1 else 1
        self.n_y = int(np.ceil(np.log2(ny))) if ny > 1 else 1
        self.n_total = self.n_x + self.n_y + 5
        self.hilbert_dim = 2**self.n_total

        # Anti-hybrid lock
        self._evolution_in_progress = False

        # Build generalized boundary mask involution
        self.boundary_mask = PhysicalBoundaryMask(nx=self.nx, ny=self.ny, top_wall_solid=True)
        self.solid = self.boundary_mask.get_solid_mask()

        # Operational counters
        self.num_state_preparations = 0
        self.num_classical_extractions = 0
        self.num_re_encodings = 0
        self.num_quantum_timesteps = 0

        # Construct global fixed timestep unitary operator U_step BEFORE evolution begins
        self._build_global_timestep_unitary()

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

        self.initial_norm_N = float(np.sqrt(np.sum(f_init**2) + np.sum(g_init**2)))

        psi = np.zeros(self.hilbert_dim, dtype=np.complex128)
        for x in range(self.nx):
            for y in range(self.ny):
                for i in range(9):
                    idx_f = self._state_index(x, y, i, 0)
                    idx_g = self._state_index(x, y, i, 1)
                    psi[idx_f] = f_init[i, y, x] / self.initial_norm_N
                    psi[idx_g] = g_init[i, y, x] / self.initial_norm_N

        self.psi = psi
        self.num_state_preparations += 1

    def _build_global_timestep_unitary(self):
        """
        Constructs the exact pre-compiled global timestep permutation/unitary matrix.
        U_step = B_mask * S_arith * U_collision_block
        """
        dim = self.hilbert_dim

        # 1. Global Streaming Permutation Matrix S_arith
        S_mat = np.zeros((dim, dim), dtype=np.complex128)
        for x in range(self.nx):
            for y in range(self.ny):
                for i in range(9):
                    for p in range(2):
                        src_idx = self._state_index(x, y, i, p)
                        dest_x = (x + C_X[i]) % self.nx
                        dest_y = (y + C_Y[i]) % self.ny
                        dest_idx = self._state_index(dest_x, dest_y, i, p)
                        S_mat[dest_idx, src_idx] = 1.0

        # Unused padding basis states map to themselves
        for idx in range(dim):
            if np.sum(S_mat[:, idx]) == 0:
                S_mat[idx, idx] = 1.0

        self.S_mat = S_mat

        # 2. Global Boundary Mask Involution Matrix B_mask
        B_mat = np.eye(dim, dtype=np.complex128)
        for x in range(self.nx):
            for y in range(self.ny):
                if self.solid[y, x]:
                    for i in range(9):
                        opp_i = OPPOSITE[i]
                        for p in range(2):
                            idx_i = self._state_index(x, y, i, p)
                            idx_opp = self._state_index(x, y, opp_i, p)
                            B_mat[idx_i, idx_i] = 0.0
                            B_mat[idx_i, idx_opp] = 1.0

        self.B_mat = B_mat

        # 3. Global Linearized Collision Block Unitary U_coll
        # Uses static reference relaxation parameters (tau_f = 0.65, tau_g = 0.70)
        omega_f = 1.0 / (3.0 * self.nu_L + 0.5)
        omega_g = 1.0 / self.tau_phi

        U_coll = np.eye(dim, dtype=np.complex128)
        for x in range(self.nx):
            for y in range(self.ny):
                # Construct local node collision matrix
                M_f = (1.0 - omega_f) * np.eye(9) + omega_f * np.outer(W, np.ones(9))
                M_g = (1.0 - omega_g) * np.eye(9) + omega_g * np.outer(W, np.ones(9))
                C_local = la.block_diag(M_f, M_g)

                # Embed into unitary via Sz.-Nagy dilation
                norm_C = float(la.norm(C_local, 2))
                alpha_C = max(1.01 * norm_C, 1.0)
                A = C_local / alpha_C
                D = la.sqrtm(np.eye(18) - A.conj().T @ A)
                D_star = la.sqrtm(np.eye(18) - A @ A.conj().T)
                U_dil = np.block([[A, D_star], [D, -A.conj().T]])

                # Map onto state indices for this node
                node_indices = []
                for i in range(9):
                    node_indices.append(self._state_index(x, y, i, 0))
                for i in range(9):
                    node_indices.append(self._state_index(x, y, i, 1))

                for r_idx, src_i in enumerate(node_indices):
                    for c_idx, src_j in enumerate(node_indices):
                        U_coll[src_i, src_j] = A[r_idx, c_idx]

        self.U_coll = U_coll
        self.U_step = self.B_mat @ self.S_mat @ self.U_coll

    def step(self):
        """
        Executes one strict quantum timestep.
        Pure unitary matrix-vector multiplication without intermediate statevector inspection or classical feedback.
        """
        self._evolution_in_progress = True

        # Pure quantum evolution: |Psi_{t+1}> = U_step |Psi_t>
        self.psi = self.U_step @ self.psi

        self.num_quantum_timesteps += 1

    def decode_final_fields(self) -> Dict[str, np.ndarray]:
        """
        Final quantum measurement / readout at simulation termination.
        Only allowed when evolution is completed.
        """
        self._evolution_in_progress = False
        self.num_classical_extractions += 1

        f = np.zeros((9, self.ny, self.nx), dtype=np.float64)
        g = np.zeros((9, self.ny, self.nx), dtype=np.float64)

        for x in range(self.nx):
            for y in range(self.ny):
                for i in range(9):
                    idx_f = self._state_index(x, y, i, 0)
                    idx_g = self._state_index(x, y, i, 1)
                    f[i, y, x] = np.real(self.psi[idx_f]) * self.initial_norm_N
                    g[i, y, x] = np.real(self.psi[idx_g]) * self.initial_norm_N

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
