"""
Direct Spatial/Population Quantum State Encoding for Two-Phase D2Q9 Lattice Boltzmann.

Mathematical Architecture:
1. Hilbert Space:
   H = H_x (x) H_y (x) H_vel (x) H_phase
   - H_x: n_x = ceil(log2(Nx)) qubits
   - H_y: n_y = ceil(log2(Ny)) qubits
   - H_vel: 4 qubits (states |0>..|8> encode D2Q9 velocities, |9>..|15> idle)
   - H_phase: 1 qubit (|0> = hydrodynamic f, |1> = phase-field g)
   Total data logical qubits = n_x + n_y + 5

2. Quantum State Representation:
   |Psi> = (1/N_norm) * [ sum_{x,y,i} f_i(x,y) |x,y,i,0> + sum_{x,y,i} g_i(x,y) |x,y,i,1> ]

3. Unitary Quantum Streaming Operator S:
   S |x, y, i, p> = |(x + c_ix) mod Nx, (y + c_iy) mod Ny, i, p>
   Permutation unitary satisfying S^dag S = I unconditionally.
   Eliminates the Level-6A spatial tensor de-correlation obstruction.

4. Unitary Boundary Involution B:
   B |x, y, i, p> = |x, y, opp(i), p> for (x,y) in boundary, identity otherwise.
   Satisfies B^dag = B and B^2 = I.

5. Collision Operator U_coll:
   Locally maps populations via block-encoded dynamic collision or hybrid quantum-classical update.
"""

from typing import Dict, Tuple, Optional
import numpy as np
import scipy.linalg as la
from qiskit import QuantumCircuit, QuantumRegister
from qiskit.circuit.library import UnitaryGate

from classical.d2q9 import C_X, C_Y, W, OPPOSITE, CS2
from classical.equilibrium import compute_equilibrium
from classical.streaming import stream


class DirectTwoPhaseQLBM:
    """
    Direct Spatial/Population Quantum Two-Phase D2Q9 LBM Solver.
    
    Encodes the full lattice distribution directly into a unified quantum state vector.
    """

    def __init__(
        self,
        nx: int = 2,
        ny: int = 2,
        rho_L: float = 1.0,
        rho_G: float = 0.1,
        nu_L: float = 0.05,
        nu_G: float = 0.05,
        sigma: float = 0.0,
        g_acc: float = -0.0005,
        tau_phi: float = 0.7,
        dam_width_ratio: float = 0.5,
        dam_height_ratio: float = 0.5,
    ):
        self.nx = nx
        self.ny = ny
        self.rho_L = rho_L
        self.rho_G = rho_G
        self.nu_L = nu_L
        self.nu_G = nu_G
        self.sigma = sigma
        self.g_acc = g_acc
        self.tau_phi = tau_phi

        self.col_w = max(1, int(nx * dam_width_ratio))
        self.col_h = max(1, int(ny * dam_height_ratio))

        # Discrete velocity constants
        self.cx = C_X
        self.cy = C_Y
        self.w = W
        self.opp = OPPOSITE
        self.cs2 = CS2

        # Quantum register sizing
        self.n_x = int(np.ceil(np.log2(nx))) if nx > 1 else 1
        self.n_y = int(np.ceil(np.log2(ny))) if ny > 1 else 1
        self.n_vel = 4      # 16 states >= 9 velocities
        self.n_phase = 1    # 2 states: 0=f, 1=g
        self.n_data = self.n_x + self.n_y + self.n_vel + self.n_phase
        self.dim_hilbert = 2 ** self.n_data

        # Physical macroscopic fields
        self.alpha = np.zeros((ny, nx), dtype=np.float64)
        self.alpha[: self.col_h, : self.col_w] = 1.0

        self.rho = self.alpha * self.rho_L + (1.0 - self.alpha) * self.rho_G
        self.u = np.zeros((2, ny, nx), dtype=np.float64)

        # Classical reference distributions: shape (9, ny, nx)
        self.f = np.zeros((9, ny, nx), dtype=np.float64)
        self.g = np.zeros((9, ny, nx), dtype=np.float64)
        self._initialize_distributions()

        # Build quantum state vector and operators
        self.psi = np.zeros(self.dim_hilbert, dtype=np.complex128)
        self.norm_factor = 1.0
        self.encode_state()

        # Build global unitary operators
        self.S_matrix = self._build_streaming_matrix()
        self.B_matrix = self._build_boundary_matrix()

    def _initialize_distributions(self):
        """Initialize equilibrium distributions for hydrodynamic and phase-field lattices."""
        self.f = compute_equilibrium(self.rho, self.u)
        self.g = np.zeros((9, self.ny, self.nx), dtype=np.float64)
        for i in range(9):
            c_dot_u = self.cx[i] * self.u[0] + self.cy[i] * self.u[1]
            self.g[i] = self.w[i] * self.alpha * (1.0 + 3.0 * c_dot_u)

    def _state_index(self, x: int, y: int, i: int, p: int) -> int:
        """
        Calculates flat computational basis index for |x>|y>|i>|p>.
        Bit layout: [ x (n_x bits) | y (n_y bits) | i (4 bits) | p (1 bit) ]
        """
        idx = (x << (self.n_y + self.n_vel + self.n_phase)) | \
              (y << (self.n_vel + self.n_phase)) | \
              (i << self.n_phase) | \
              p
        return idx

    def encode_state(self) -> np.ndarray:
        """
        Encodes physical f and g arrays into the normalized quantum statevector |Psi>.
        """
        self.psi = np.zeros(self.dim_hilbert, dtype=np.complex128)
        sum_sq = 0.0

        for x in range(self.nx):
            for y in range(self.ny):
                for i in range(9):
                    f_val = self.f[i, y, x]
                    g_val = self.g[i, y, x]
                    sum_sq += f_val ** 2 + g_val ** 2

        self.norm_factor = np.sqrt(sum_sq)
        inv_norm = 1.0 / (self.norm_factor + 1e-15)

        for x in range(self.nx):
            for y in range(self.ny):
                for i in range(9):
                    idx_f = self._state_index(x, y, i, 0)
                    idx_g = self._state_index(x, y, i, 1)
                    self.psi[idx_f] = self.f[i, y, x] * inv_norm
                    self.psi[idx_g] = self.g[i, y, x] * inv_norm

        return self.psi

    def decode_state(self) -> Tuple[np.ndarray, np.ndarray]:
        """
        Decodes physical f and g arrays from quantum statevector |Psi>.
        """
        f_decoded = np.zeros((9, self.ny, self.nx), dtype=np.float64)
        g_decoded = np.zeros((9, self.ny, self.nx), dtype=np.float64)

        for x in range(self.nx):
            for y in range(self.ny):
                for i in range(9):
                    idx_f = self._state_index(x, y, i, 0)
                    idx_g = self._state_index(x, y, i, 1)
                    f_decoded[i, y, x] = np.real(self.psi[idx_f]) * self.norm_factor
                    g_decoded[i, y, x] = np.real(self.psi[idx_g]) * self.norm_factor

        self.f = f_decoded
        self.g = g_decoded
        return f_decoded, g_decoded

    def _build_streaming_matrix(self) -> np.ndarray:
        """
        Constructs the exact unitary streaming permutation matrix S in U(2^n_data).
        S |x, y, i, p> = |(x + c_ix) mod Nx, (y + c_iy) mod Ny, i, p>
        """
        dim = self.dim_hilbert
        S = np.zeros((dim, dim), dtype=np.complex128)

        # Map each valid state to its streamed target state
        for x in range(2 ** self.n_x):
            for y in range(2 ** self.n_y):
                for i in range(2 ** self.n_vel):
                    for p in range(2 ** self.n_phase):
                        src_idx = (x << (self.n_y + self.n_vel + self.n_phase)) | \
                                  (y << (self.n_vel + self.n_phase)) | \
                                  (i << self.n_phase) | p

                        if x < self.nx and y < self.ny and i < 9:
                            # Valid physical lattice node & velocity
                            new_x = (x + self.cx[i]) % self.nx
                            new_y = (y + self.cy[i]) % self.ny
                            tgt_idx = (new_x << (self.n_y + self.n_vel + self.n_phase)) | \
                                      (new_y << (self.n_vel + self.n_phase)) | \
                                      (i << self.n_phase) | p
                            S[tgt_idx, src_idx] = 1.0
                        else:
                            # Idle/padding subspace maps identically to itself
                            S[src_idx, src_idx] = 1.0

        return S

    def _build_boundary_matrix(self) -> np.ndarray:
        """
        Constructs the exact unitary bounce-back boundary involution B in U(2^n_data).
        B |x, y, i, p> = |x, y, opp(i), p> on solid walls, identity elsewhere.
        """
        dim = self.dim_hilbert
        B = np.zeros((dim, dim), dtype=np.complex128)

        solid_mask = np.zeros((self.ny, self.nx), dtype=bool)
        solid_mask[0, :] = True
        solid_mask[-1, :] = True
        solid_mask[:, 0] = True
        solid_mask[:, -1] = True

        for x in range(2 ** self.n_x):
            for y in range(2 ** self.n_y):
                for i in range(2 ** self.n_vel):
                    for p in range(2 ** self.n_phase):
                        src_idx = (x << (self.n_y + self.n_vel + self.n_phase)) | \
                                  (y << (self.n_vel + self.n_phase)) | \
                                  (i << self.n_phase) | p

                        if x < self.nx and y < self.ny and i < 9:
                            if solid_mask[y, x]:
                                opp_i = self.opp[i]
                                tgt_idx = (x << (self.n_y + self.n_vel + self.n_phase)) | \
                                          (y << (self.n_vel + self.n_phase)) | \
                                          (opp_i << self.n_phase) | p
                                B[tgt_idx, src_idx] = 1.0
                            else:
                                B[src_idx, src_idx] = 1.0
                        else:
                            B[src_idx, src_idx] = 1.0

        return B

    def apply_quantum_streaming(self):
        """Applies exact unitary quantum streaming S on the statevector |Psi>."""
        self.psi = self.S_matrix @ self.psi

    def apply_quantum_boundary(self):
        """Applies exact unitary quantum bounce-back involution B on the statevector |Psi>."""
        self.psi = self.B_matrix @ self.psi

    def compute_surface_tension_force(self) -> np.ndarray:
        """Continuum surface force F_s = sigma * kappa * grad(alpha)."""
        if self.sigma <= 0.0:
            return np.zeros((2, self.ny, self.nx), dtype=np.float64)

        grad_x = np.zeros((self.ny, self.nx), dtype=np.float64)
        grad_y = np.zeros((self.ny, self.nx), dtype=np.float64)

        if self.nx > 2:
            grad_x[:, 1:-1] = (self.alpha[:, 2:] - self.alpha[:, :-2]) / 2.0
        if self.ny > 2:
            grad_y[1:-1, :] = (self.alpha[2:, :] - self.alpha[:-2, :]) / 2.0

        grad_norm = np.sqrt(grad_x ** 2 + grad_y ** 2) + 1e-12
        mask = grad_norm > 1e-3
        nx_vec = np.where(mask, grad_x / grad_norm, 0.0)
        ny_vec = np.where(mask, grad_y / grad_norm, 0.0)

        div_nx = np.zeros_like(nx_vec)
        div_ny = np.zeros_like(ny_vec)
        if self.nx > 2:
            div_nx[:, 1:-1] = (nx_vec[:, 2:] - nx_vec[:, :-2]) / 2.0
        if self.ny > 2:
            div_ny[1:-1, :] = (ny_vec[2:, :] - ny_vec[:-2, :]) / 2.0

        kappa = np.clip(-(div_nx + div_ny), -2.0, 2.0)
        F_s = np.zeros((2, self.ny, self.nx), dtype=np.float64)
        F_s[0] = np.where(mask, self.sigma * kappa * grad_x, 0.0)
        F_s[1] = np.where(mask, self.sigma * kappa * grad_y, 0.0)
        return F_s

    def compute_total_force(self) -> np.ndarray:
        """Total force F = F_buoyancy + F_surface."""
        F = np.zeros((2, self.ny, self.nx), dtype=np.float64)
        F[1] = (self.rho - self.rho_G) * self.g_acc
        if self.sigma > 0.0:
            F += self.compute_surface_tension_force()
        return F

    def execute_collision_step(self):
        """
        Executes hydrodynamic and phase-field collision on physical populations.
        """
        self.decode_state()

        # 1. Macroscopic moments
        self.rho = np.sum(self.f, axis=0)
        self.alpha = np.clip(np.sum(self.g, axis=0), 0.0, 1.0)

        # 2. Total force
        F = self.compute_total_force()

        # 3. Shifted velocity
        rho_safe = np.where(self.rho > 1e-6, self.rho, self.rho_G)
        ux = (np.sum(self.cx[:, None, None] * self.f, axis=0) + 0.5 * F[0]) / rho_safe
        uy = (np.sum(self.cy[:, None, None] * self.f, axis=0) + 0.5 * F[1]) / rho_safe

        u_mag = np.sqrt(ux**2 + uy**2)
        max_u = 0.15
        scale = np.where(u_mag > max_u, max_u / (u_mag + 1e-12), 1.0)
        self.u = np.stack((ux * scale, uy * scale), axis=0)

        # 4. Phase-dependent viscosity & relaxation
        nu_mix = self.alpha * self.nu_L + (1.0 - self.alpha) * self.nu_G
        tau_f = 3.0 * nu_mix + 0.5
        omega_f = 1.0 / tau_f
        omega_g = 1.0 / self.tau_phi

        # 5. Equilibria
        f_eq = compute_equilibrium(self.rho, self.u)
        g_eq = np.zeros_like(self.g)
        for i in range(9):
            c_dot_u = self.cx[i] * self.u[0] + self.cy[i] * self.u[1]
            g_eq[i] = self.w[i] * self.alpha * (1.0 + 3.0 * c_dot_u)

        # 6. Post-collision populations
        f_coll = np.zeros_like(self.f)
        g_coll = np.zeros_like(self.g)
        u_dot_F = self.u[0] * F[0] + self.u[1] * F[1]

        for i in range(9):
            ci_u = self.cx[i] * self.u[0] + self.cy[i] * self.u[1]
            ci_F = self.cx[i] * F[0] + self.cy[i] * F[1]
            term = 3.0 * ci_F + 9.0 * ci_u * ci_F - 3.0 * u_dot_F
            S_i = (1.0 - 0.5 * omega_f) * self.w[i] * term
            f_coll[i] = self.f[i] - omega_f * (self.f[i] - f_eq[i]) + S_i
            g_coll[i] = self.g[i] - omega_g * (self.g[i] - g_eq[i])

        self.f = f_coll
        self.g = g_coll
        self.encode_state()

    def step(self):
        """
        Advances the direct-encoded quantum two-phase state by one full timestep:
        1. Local quantum collision
        2. Reversible quantum streaming S |Psi>
        3. Quantum boundary bounce-back involution B |Psi>
        """
        # Step 1: Local Collision
        self.execute_collision_step()

        # Step 2: Quantum Unitary Streaming
        self.apply_quantum_streaming()

        # Step 3: Quantum Unitary Boundary Involution
        self.apply_quantum_boundary()

        # Decode final physical fields
        self.decode_state()
        self.rho = np.sum(self.f, axis=0)
        self.alpha = np.clip(np.sum(self.g, axis=0), 0.0, 1.0)

    def build_qiskit_circuit(self) -> QuantumCircuit:
        """
        Builds the explicit Qiskit QuantumCircuit implementing the 2x2 quantum step:
        Registers: q_x (1), q_y (1), q_vel (4), q_phase (1) = 7 qubits.
        """
        qr = QuantumRegister(self.n_data, name="q_lattice")
        qc = QuantumCircuit(qr, name="DirectTwoPhaseQLBM_2x2")

        # 1. State preparation
        qc.initialize(self.psi, qr)

        # 2. Streaming gate
        streaming_gate = UnitaryGate(self.S_matrix, label="U_Stream_D2Q9")
        qc.append(streaming_gate, qr)

        # 3. Boundary gate
        boundary_gate = UnitaryGate(self.B_matrix, label="U_BounceBack_Wall")
        qc.append(boundary_gate, qr)

        return qc
