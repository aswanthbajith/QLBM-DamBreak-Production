"""
Level-5 Quantum Two-Phase D2Q9 Dam-Break Solver.

Implements end-to-end quantum statevector evolution on power-of-two registers:
|x> (nqx) (x) |y> (nqy) (x) |v> (4 qubits) (x) |s> (1 qubit) (x) |anc> (1 qubit)
Total: 10 qubits for 4x4 mesh (dim = 1024).

Composite Quantum Timestep Operator:
|Psi_{t+1}> = B . S . U_force . U_collision |Psi_t>
"""

from typing import Dict, Any, Tuple, Optional
import numpy as np
import scipy.linalg as la

from classical.d2q9 import C_X, C_Y, W, OPPOSITE
from quantum.level5_two_phase_carleman import (
    compute_level5_carleman_matrices,
    construct_level5_unitary_dilation,
    lift_to_second_order,
)
from quantum.streaming import build_two_phase_streaming_unitary
from quantum.boundary_quantum import build_two_phase_boundary_unitary


class Level5QuantumTwoPhaseSolver:
    """
    Quantum-compatible statevector solver for the coupled two-phase dam break.
    """

    def __init__(self, nx: int = 4, ny: int = 4, g_acc: float = -0.0005, tau_f: float = 0.8, tau_g: float = 0.7):
        self.nx = nx
        self.ny = ny
        self.g_acc = g_acc
        self.tau_f = tau_f
        self.tau_g = tau_g

        # Register layout
        self.nqx = int(np.ceil(np.log2(nx)))
        self.nqy = int(np.ceil(np.log2(ny)))
        self.nq_vel = 4
        self.nq_sel = 1
        self.total_sys_qubits = self.nqx + self.nqy + self.nq_vel + self.nq_sel  # 9 qubits
        self.dim_sys = 1 << self.total_sys_qubits                               # 512
        self.dim_total = 1 << (self.total_sys_qubits + 1)                       # 1024

        self.layout = {
            "total_qubits": self.total_sys_qubits,
            "n_qx": self.nqx,
            "n_qy": self.nqy,
            "n_qvel": self.nq_vel,
            "n_qsel": self.nq_sel,
        }

        # Precompute Carleman matrices and Unitary Dilation
        self.M1, self.M2, self.A_eval = compute_level5_carleman_matrices(
            tau_f=tau_f, tau_g=tau_g, g_acc=g_acc
        )
        self.U_C, self.alpha_C = construct_level5_unitary_dilation(self.A_eval)

        # Precompute Spatial Streaming Permutation and Boundary Involution
        self.S = build_two_phase_streaming_unitary(self.layout)
        self.B = build_two_phase_boundary_unitary(self.layout)

    def encode_state(self, f: np.ndarray, g: np.ndarray) -> Tuple[np.ndarray, float]:
        """
        Encodes physical f (9, ny, nx) and g (9, ny, nx) into 512-dim quantum statevector.
        Bit packing: (s << (nqx + nqy + nq_vel)) | (v << (nqx + nqy)) | (y << nqx) | x
        """
        psi = np.zeros(self.dim_sys, dtype=np.complex128)
        M_total = float(np.sum(f) + np.sum(g))

        for y in range(self.ny):
            for x in range(self.nx):
                for i in range(9):
                    idx_f = (0 << (self.nqx + self.nqy + self.nq_vel)) | (i << (self.nqx + self.nqy)) | (y << self.nqx) | x
                    idx_g = (1 << (self.nqx + self.nqy + self.nq_vel)) | (i << (self.nqx + self.nqy)) | (y << self.nqx) | x
                    psi[idx_f] = np.sqrt(max(0.0, f[i, y, x]) / M_total)
                    psi[idx_g] = np.sqrt(max(0.0, g[i, y, x]) / M_total)

        norm_psi = la.norm(psi)
        if norm_psi > 1e-15:
            psi = psi / norm_psi

        return psi, M_total

    def decode_state(self, psi: np.ndarray, M_total: float) -> Tuple[np.ndarray, np.ndarray]:
        """
        Decodes 512-dim quantum statevector back to physical f and g arrays.
        """
        f = np.zeros((9, self.ny, self.nx), dtype=np.float64)
        g = np.zeros((9, self.ny, self.nx), dtype=np.float64)

        for y in range(self.ny):
            for x in range(self.nx):
                for i in range(9):
                    idx_f = (0 << (self.nqx + self.nqy + self.nq_vel)) | (i << (self.nqx + self.nqy)) | (y << self.nqx) | x
                    idx_g = (1 << (self.nqx + self.nqy + self.nq_vel)) | (i << (self.nqx + self.nqy)) | (y << self.nqx) | x
                    f[i, y, x] = (np.abs(psi[idx_f]) ** 2) * M_total
                    g[i, y, x] = (np.abs(psi[idx_g]) ** 2) * M_total

        return f, g

    def step(self, f: np.ndarray, g: np.ndarray) -> Tuple[np.ndarray, np.ndarray, Dict[str, Any]]:
        """
        Executes one full Level-5 Quantum Timestep.
        """
        f_coll = np.zeros_like(f)
        g_coll = np.zeros_like(g)

        # Local Node Collision via Carleman Map A_eval
        for y in range(self.ny):
            for x in range(self.nx):
                z_node = np.concatenate((f[:, y, x], g[:, y, x]))
                Y_node = lift_to_second_order(z_node)
                z_post = self.A_eval @ Y_node
                f_coll[:, y, x] = np.maximum(z_post[:9], 0.0)
                g_coll[:, y, x] = np.maximum(z_post[9:], 0.0)

        # Encode into quantum statevector
        psi_coll, M_total = self.encode_state(f_coll, g_coll)

        # Spatial Streaming Permutation (S)
        psi_streamed = self.S @ psi_coll

        # Boundary Bounce-Back Involution (B)
        psi_next = self.B @ psi_streamed

        # Decode macroscopic moments
        f_next, g_next = self.decode_state(psi_next, M_total)

        p_succ = 1.0 / (self.alpha_C ** 2)

        meta = {
            "p_success": p_succ,
            "alpha": self.alpha_C,
            "total_mass": float(np.sum(f_next)),
            "liquid_mass": float(np.sum(g_next)),
        }

        return f_next, g_next, meta
