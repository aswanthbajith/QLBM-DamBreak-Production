"""
Phase F10: Generalized Physical Boundary Masks & Multi-Node Quantum Boundary Operators.

Mathematical Architecture:
1. State Representation:
   Hilbert space H = H_x (x) H_y (x) H_vel (x) H_phase
   Total data qubits: n_total = n_x + n_y + 4_vel + 1_phase = n_x + n_y + 5
   Qubit Layout:
   - Qubit 0: Phase selector p in {0=f, 1=g}
   - Qubits 1..4: Discrete velocity i in {0..8} (9..15 idle padding)
   - Qubits 5..(4+n_y): Spatial y in {0..Ny-1}
   - Qubits (5+n_y)..(4+n_y+n_x): Spatial x in {0..Nx-1}
   Index Formula: (x << (5 + n_y)) | (y << 5) | (i << 1) | p

2. Generalized Quantum Boundary Operator B_mask:
   For solid wall nodes (solid[y, x] == True):
       B_mask |x, y, i, p> = |x, y, opp(i), p>
   For fluid domain nodes (solid[y, x] == False):
       B_mask |x, y, i, p> = |x, y, i, p>

3. Physical Properties:
   - Unitarity: B_mask† B_mask = I
   - Involution: B_mask^2 = I
   - Two-Phase Sector Isolation: p' = p (f <-> g conversion strictly 0)
   - Norm Preservation: ||B_mask |Psi>|| = |||Psi>|| = 1
   - Periodic Wrap-Around Prevention: Reflects outgoing boundary fluxes before modular streaming wraps.
"""

from typing import Tuple, Dict, Any, Optional, List
import numpy as np
import scipy.linalg as la
from qiskit import QuantumCircuit
from qiskit.quantum_info import Operator

from classical.d2q9 import C_X, C_Y, W, OPPOSITE


class PhysicalBoundaryMask:
    """
    Generalized physical boundary mask and quantum boundary operator generator for QLBM.
    """

    def __init__(
        self,
        nx: int = 4,
        ny: int = 4,
        top_wall_solid: bool = True,
        custom_solid_mask: Optional[np.ndarray] = None,
    ):
        self.nx = nx
        self.ny = ny
        self.top_wall_solid = top_wall_solid

        self.n_x = int(np.ceil(np.log2(nx))) if nx > 1 else 1
        self.n_y = int(np.ceil(np.log2(ny))) if ny > 1 else 1
        self.n_total = self.n_x + self.n_y + 5
        self.hilbert_dim = 2**self.n_total

        if custom_solid_mask is not None:
            assert custom_solid_mask.shape == (ny, nx), f"Mask shape {custom_solid_mask.shape} != ({ny}, {nx})"
            self.solid = np.asarray(custom_solid_mask, dtype=bool)
        else:
            self.solid = np.zeros((ny, nx), dtype=bool)
            self.solid[0, :] = True   # Bottom wall
            self.solid[:, 0] = True   # Left wall
            self.solid[:, -1] = True  # Right wall
            if self.top_wall_solid:
                self.solid[-1, :] = True  # Top wall

        self.fluid = ~self.solid
        self._B_matrix: Optional[np.ndarray] = None

    def _state_index(self, x: int, y: int, i: int, p: int) -> int:
        """Calculates basis state integer index matching direct qubit layout."""
        return (x << (5 + self.n_y)) | (y << 5) | (i << 1) | p

    def get_solid_mask(self) -> np.ndarray:
        """Returns boolean array (ny, nx) of solid wall nodes."""
        return self.solid.copy()

    def get_fluid_mask(self) -> np.ndarray:
        """Returns boolean array (ny, nx) of fluid domain nodes."""
        return self.fluid.copy()

    def build_boundary_matrix(self) -> np.ndarray:
        """
        Constructs the exact 2^n_total x 2^n_total unitary permutation matrix B_mask.
        """
        if self._B_matrix is not None:
            return self._B_matrix

        B = np.eye(self.hilbert_dim, dtype=np.complex128)

        for x in range(self.nx):
            for y in range(self.ny):
                if self.solid[y, x]:
                    for p in range(2):
                        for i in range(9):
                            opp_i = OPPOSITE[i]
                            if i < opp_i:
                                idx_i = self._state_index(x, y, i, p)
                                idx_opp = self._state_index(x, y, opp_i, p)
                                B[idx_i, idx_i] = 0.0
                                B[idx_opp, idx_opp] = 0.0
                                B[idx_i, idx_opp] = 1.0
                                B[idx_opp, idx_i] = 1.0

        self._B_matrix = B
        return self._B_matrix

    def apply_boundary_matrix(self, psi: np.ndarray) -> np.ndarray:
        """Applies generalized quantum boundary operator to statevector."""
        B = self.build_boundary_matrix()
        return B @ psi

    def verify_unitarity_and_involution(self) -> Dict[str, float]:
        """Verifies ||B† B - I|| and ||B^2 - I||."""
        B = self.build_boundary_matrix()
        I = np.eye(self.hilbert_dim, dtype=np.complex128)
        unitarity_err = float(la.norm(B.conj().T @ B - I, 2))
        involution_err = float(la.norm(B @ B - I, 2))
        return {
            "unitarity_error": unitarity_err,
            "involution_error": involution_err,
        }

    def build_boundary_circuit(self) -> QuantumCircuit:
        """
        Constructs an explicit gate-level Qiskit quantum circuit for the boundary operator.
        """
        qc = QuantumCircuit(self.n_total, name=f"BoundaryMask_{self.nx}x{self.ny}")
        v_qubits = [1, 2, 3, 4]
        y_qubits = list(range(5, 5 + self.n_y))
        x_qubits = list(range(5 + self.n_y, 5 + self.n_y + self.n_x))

        # Local velocity swap matrix V_swap on 4 velocity qubits
        V_swap = np.eye(16, dtype=np.complex128)
        for i in range(9):
            V_swap[:, i] = 0
            V_swap[OPPOSITE[i], i] = 1.0

        # For each solid node (x, y), condition on spatial qubits and apply V_swap
        for x in range(self.nx):
            for y in range(self.ny):
                if self.solid[y, x]:
                    x_bits = [(x >> b) & 1 for b in range(self.n_x)]
                    y_bits = [(y >> b) & 1 for b in range(self.n_y)]

                    # Flip 0-controls
                    for b, bit in enumerate(x_bits):
                        if bit == 0:
                            qc.x(x_qubits[b])
                    for b, bit in enumerate(y_bits):
                        if bit == 0:
                            qc.x(y_qubits[b])

                    # Multi-controlled unitary on velocity register
                    ctrl_qubits = x_qubits + y_qubits
                    custom_gate = Operator(V_swap).to_instruction()
                    ctrl_gate = custom_gate.control(len(ctrl_qubits))
                    qc.append(ctrl_gate, ctrl_qubits + v_qubits)

                    # Uncompute flips
                    for b, bit in enumerate(x_bits):
                        if bit == 0:
                            qc.x(x_qubits[b])
                    for b, bit in enumerate(y_bits):
                        if bit == 0:
                            qc.x(y_qubits[b])

        return qc

    def audit_single_wall(self, wall_type: str, p_sector: int = 0) -> Dict[str, Any]:
        """
        Tests isolated wall reflection for left, right, bottom, or top wall.
        """
        B = self.build_boundary_matrix()

        if wall_type == "left":
            x_test, y_test = 0, self.ny // 2
            inc_dir = 3  # West moving into left wall
            exp_ref = 1  # East reflected
        elif wall_type == "right":
            x_test, y_test = self.nx - 1, self.ny // 2
            inc_dir = 1  # East moving into right wall
            exp_ref = 3  # West reflected
        elif wall_type == "bottom":
            x_test, y_test = self.nx // 2, 0
            inc_dir = 4  # South moving into bottom wall
            exp_ref = 2  # North reflected
        elif wall_type == "top":
            x_test, y_test = self.nx // 2, self.ny - 1
            inc_dir = 2  # North moving into top wall
            exp_ref = 4  # South reflected
        else:
            raise ValueError(f"Unknown wall type {wall_type}")

        idx_inc = self._state_index(x_test, y_test, inc_dir, p_sector)
        idx_exp = self._state_index(x_test, y_test, exp_ref, p_sector)

        psi_in = np.zeros(self.hilbert_dim, dtype=np.complex128)
        psi_in[idx_inc] = 1.0

        psi_out = B @ psi_in

        reflection_acc = float(abs(psi_out[idx_exp] - 1.0))
        residual_inc = float(abs(psi_out[idx_inc]))
        norm_err = float(abs(la.norm(psi_out) - 1.0))

        # Check that opposing species sector is 0
        p_other = 1 - p_sector
        idx_other = self._state_index(x_test, y_test, exp_ref, p_other)
        cross_talk = float(abs(psi_out[idx_other]))

        return {
            "wall_type": wall_type,
            "p_sector": p_sector,
            "reflection_error": reflection_acc,
            "residual_incident_error": residual_inc,
            "norm_error": norm_err,
            "cross_talk_error": cross_talk,
            "passed": reflection_acc < 1e-14 and residual_inc < 1e-14 and cross_talk < 1e-14,
        }

    def audit_periodic_wrap_around_prevention(self) -> Dict[str, Any]:
        """
        Validates that boundary reflection prevents modular coordinate streaming from wrapping around.
        """
        from quantum.arithmetic_streaming import build_direct_streaming_circuit
        qc_stream = build_direct_streaming_circuit(self.nx, self.ny)
        U_stream = Operator(qc_stream).data
        B = self.build_boundary_matrix()

        # Place fluid population next to right wall (nx-2, ny//2) moving East (i=1)
        x_fluid = self.nx - 2
        y_fluid = self.ny // 2
        psi_init = np.zeros(self.hilbert_dim, dtype=np.complex128)
        idx_fluid = self._state_index(x_fluid, y_fluid, 1, 0)
        psi_init[idx_fluid] = 1.0

        # Step 1: Streaming moves fluid to right wall (nx-1, ny//2)
        psi_streamed = U_stream @ psi_init
        idx_wall_east = self._state_index(self.nx - 1, y_fluid, 1, 0)
        arrived_at_wall = bool(abs(psi_streamed[idx_wall_east] - 1.0) < 1e-12)

        # Step 2: Boundary operator reflects i=1 -> i=3 (West) on right wall
        psi_reflected = B @ psi_streamed
        idx_wall_west = self._state_index(self.nx - 1, y_fluid, 3, 0)
        reflected_on_wall = bool(abs(psi_reflected[idx_wall_west] - 1.0) < 1e-12)

        # Step 3: Next streaming moves reflected population back to (nx-2, ny//2) moving West (i=3)
        psi_next_stream = U_stream @ psi_reflected
        idx_back_fluid = self._state_index(x_fluid, y_fluid, 3, 0)
        returned_to_fluid = bool(abs(psi_next_stream[idx_back_fluid] - 1.0) < 1e-12)

        # Check that NO population wrapped around to x=0
        idx_wrapped = self._state_index(0, y_fluid, 1, 0)
        wrap_around_leakage = float(abs(psi_next_stream[idx_wrapped]))

        return {
            "arrived_at_wall": arrived_at_wall,
            "reflected_on_wall": reflected_on_wall,
            "returned_to_fluid": returned_to_fluid,
            "wrap_around_leakage": wrap_around_leakage,
            "passed": arrived_at_wall and reflected_on_wall and returned_to_fluid and wrap_around_leakage < 1e-12,
        }
