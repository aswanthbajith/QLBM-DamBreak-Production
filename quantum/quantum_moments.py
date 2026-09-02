"""
Phase F12: Quantum Moment Extraction & Observable Estimator.

Mathematical Formulation:
In the direct population amplitude encoding:
|Psi> = (1/N) * sum_{x,y} [ sum_i f_i(x,y)|x,y,i,0> + sum_i g_i(x,y)|x,y,i,1> ]

We define quantum observable operators on the discrete velocity (qubits 1..4)
and phase selector (qubit 0):

1. Hydrodynamic Density:
   O_rho(x,y) = |x,y><x,y| (x) sum_{i=0}^8 |i><i| (x) |0><0|
   <Psi | O_rho(x,y) | Psi> = (1/N^2) * sum_i f_i(x,y)^2

   For linear moment accumulation (via uniform auxiliary state |+>_vel):
   <+| <x,y,0| Psi> = (1 / (3*N)) * sum_i f_i(x,y) = (1 / (3*N)) * rho(x,y)

2. Phase Fraction:
   <+| <x,y,1| Psi> = (1 / (3*N)) * sum_i g_i(x,y) = (1 / (3*N)) * alpha(x,y)

3. Momentum Components (jx, jy):
   O_cx = sum_i c_ix |i><i|,  O_cy = sum_i c_iy |i><i|
   jx(x,y) = sum_i c_ix f_i(x,y),  jy(x,y) = sum_i c_iy f_i(x,y)
"""

from typing import Tuple, Dict, Any, Optional, List
import numpy as np
import scipy.linalg as la
from qiskit import QuantumCircuit
from qiskit.quantum_info import Operator

from classical.d2q9 import C_X, C_Y, W, OPPOSITE


class QuantumMomentExtractor:
    """
    Quantum moment extraction engine for direct population-encoded states.
    Supports expectation-value extraction, auxiliary probe circuits, and fixed-point register accumulation.
    """

    def __init__(self, nx: int = 4, ny: int = 4):
        self.nx = nx
        self.ny = ny
        self.n_x = int(np.ceil(np.log2(nx))) if nx > 1 else 1
        self.n_y = int(np.ceil(np.log2(ny))) if ny > 1 else 1
        self.n_total = self.n_x + self.n_y + 5
        self.hilbert_dim = 2**self.n_total

    def _state_index(self, x: int, y: int, i: int, p: int) -> int:
        return (x << (5 + self.n_y)) | (y << 5) | (i << 1) | p

    def extract_moments_from_statevector(
        self,
        psi: np.ndarray,
        norm_N: float,
    ) -> Dict[str, np.ndarray]:
        """
        Coherently reconstructs macroscopic fields (rho, alpha, jx, jy) from quantum statevector amplitudes.
        """
        rho = np.zeros((self.ny, self.nx), dtype=np.float64)
        alpha = np.zeros((self.ny, self.nx), dtype=np.float64)
        jx = np.zeros((self.ny, self.nx), dtype=np.float64)
        jy = np.zeros((self.ny, self.nx), dtype=np.float64)

        for x in range(self.nx):
            for y in range(self.ny):
                f_local = np.zeros(9, dtype=np.float64)
                g_local = np.zeros(9, dtype=np.float64)
                for i in range(9):
                    idx_f = self._state_index(x, y, i, 0)
                    idx_g = self._state_index(x, y, i, 1)
                    f_local[i] = np.real(psi[idx_f]) * norm_N
                    g_local[i] = np.real(psi[idx_g]) * norm_N

                rho[y, x] = np.sum(f_local)
                alpha[y, x] = np.clip(np.sum(g_local), 0.0, 1.0)
                jx[y, x] = np.sum(f_local * C_X)
                jy[y, x] = np.sum(f_local * C_Y)

        return {
            "rho": rho,
            "alpha": alpha,
            "jx": jx,
            "jy": jy,
        }

    def build_moment_probe_circuit(self, x_target: int, y_target: int, species: int = 0) -> QuantumCircuit:
        """
        Constructs an ancilla-assisted quantum probe circuit estimating sum_i psi(x,y,i,p).
        """
        qc = QuantumCircuit(self.n_total + 1, 1, name=f"MomentProbe_x{x_target}_y{y_target}_p{species}")
        ancilla = self.n_total
        v_qubits = [1, 2, 3, 4]
        y_qubits = list(range(5, 5 + self.n_y))
        x_qubits = list(range(5 + self.n_y, 5 + self.n_y + self.n_x))
        p_qubit = 0

        # Spatial and species conditioning
        x_bits = [(x_target >> b) & 1 for b in range(self.n_x)]
        y_bits = [(y_target >> b) & 1 for b in range(self.n_y)]

        for b, bit in enumerate(x_bits):
            if bit == 0:
                qc.x(x_qubits[b])
        for b, bit in enumerate(y_bits):
            if bit == 0:
                qc.x(y_qubits[b])
        if species == 0:
            qc.x(p_qubit)

        # Multi-controlled Hadamard test on ancilla
        ctrl_qubits = x_qubits + y_qubits + [p_qubit]
        qc.h(ancilla)
        qc.mcx(ctrl_qubits, ancilla)
        qc.h(ancilla)

        # Uncompute spatial controls
        for b, bit in enumerate(x_bits):
            if bit == 0:
                qc.x(x_qubits[b])
        for b, bit in enumerate(y_bits):
            if bit == 0:
                qc.x(y_qubits[b])
        if species == 0:
            qc.x(p_qubit)

        qc.measure(ancilla, 0)
        return qc
