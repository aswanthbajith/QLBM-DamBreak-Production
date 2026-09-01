"""
Quantum Observable Estimation Module for Two-Phase D2Q9 Lattice Boltzmann.

Mathematical Formulation:
Given quantum state |psi> on 9 qubits with global normalization scalar M:
- Macroscopic Density:
  rho(x,y) = M * <psi| Pi_rho(x,y) |psi>
  where Pi_rho(x,y) = |x,y><x,y| (x) (sum_{i=0}^8 |i><i|) (x) |0><0|

- Macroscopic Phase Field:
  phi(x,y) = M * <psi| Pi_phi(x,y) |psi>
  where Pi_phi(x,y) = |x,y><x,y| (x) (sum_{i=0}^8 |i><i|) (x) |1><1|

- Macroscopic Velocity Field:
  u_x(x,y) = (M / rho(x,y)) * <psi| C_hat_x(x,y) |psi>
  u_y(x,y) = (M / rho(x,y)) * <psi| C_hat_y(x,y) |psi>
  where C_hat_x(x,y) = |x,y><x,y| (x) (sum_{i=0}^8 c_ix |i><i|) (x) |0><0|
        C_hat_y(x,y) = |x,y><x,y| (x) (sum_{i=0}^8 c_iy |i><i|) (x) |0><0|

Methods:
1. Exact Quantum Expectation Values / Statevector Reduction (Noise-free quantum baseline)
2. Statistical Shot Sampling (Emulating QPU projective measurement with shot noise O(1/sqrt(N)))
3. Hadamard Test / Amplitude Estimation Interfaces
"""

import numpy as np
from classical.d2q9 import C_X, C_Y


def compute_quantum_expectation_observables(statevector, total_mass, layout):
    """
    Computes exact macroscopic fields (rho, u, phi) directly from quantum expectation values
    without constructing intermediate classical f, g arrays.
    """
    statevector = np.asarray(statevector, dtype=np.complex128)
    n_qx = layout["n_qx"]
    n_qy = layout["n_qy"]
    n_qvel = layout["n_qvel"]
    nx = layout["nx"]
    ny = layout["ny"]
    selector_shift = n_qx + n_qy + n_qvel

    rho = np.zeros((ny, nx), dtype=np.float64)
    phi = np.zeros((ny, nx), dtype=np.float64)
    momentum_x = np.zeros((ny, nx), dtype=np.float64)
    momentum_y = np.zeros((ny, nx), dtype=np.float64)

    for y in range(ny):
        for x in range(nx):
            for i in range(9):
                idx_common = (i << (n_qx + n_qy)) | (y << n_qx) | x
                idx_f = idx_common
                idx_g = (1 << selector_shift) | idx_common

                prob_f = float(np.abs(statevector[idx_f]) ** 2)
                prob_g = float(np.abs(statevector[idx_g]) ** 2)

                f_val = total_mass * prob_f
                g_val = total_mass * prob_g

                rho[y, x] += f_val
                phi[y, x] += g_val
                momentum_x[y, x] += f_val * C_X[i]
                momentum_y[y, x] += f_val * C_Y[i]

    # Safe velocity division
    rho_safe = np.where(rho > 1e-14, rho, 1.0)
    ux = momentum_x / rho_safe
    uy = momentum_y / rho_safe
    u = np.stack([ux, uy], axis=0)

    return rho, u, phi


def estimate_observables_from_shots(counts, total_shots, total_mass, layout):
    """
    Estimates macroscopic observables (rho, u, phi) from shot measurement counts.
    """
    from quantum.state_preparation import decode_counts_to_distributions
    f_est, g_est = decode_counts_to_distributions(counts, total_shots, total_mass, layout)

    rho = np.sum(f_est, axis=0)
    phi = np.sum(g_est, axis=0)

    rho_safe = np.where(rho > 1e-14, rho, 1.0)
    ux = np.sum(C_X[:, None, None] * f_est, axis=0) / rho_safe
    uy = np.sum(C_Y[:, None, None] * f_est, axis=0) / rho_safe
    u = np.stack([ux, uy], axis=0)

    return rho, u, phi


def build_velocity_observable_operator(axis, layout):
    """
    Constructs the 512 x 512 diagonal velocity observable matrix C_hat_x or C_hat_y.
    """
    total_qubits = layout["total_qubits"]
    n_qx = layout["n_qx"]
    n_qy = layout["n_qy"]
    n_qvel = layout["n_qvel"]
    nx = layout["nx"]
    ny = layout["ny"]
    dim = 1 << total_qubits

    C_matrix = np.zeros((dim, dim), dtype=np.complex128)
    c_vec = C_X if axis == 'x' else C_Y

    for y in range(ny):
        for x in range(nx):
            for i in range(9):
                # Hydrodynamic distribution (s=0)
                idx_f = (0 << (n_qx + n_qy + n_qvel)) | (i << (n_qx + n_qy)) | (y << n_qx) | x
                C_matrix[idx_f, idx_f] = c_vec[i]

    return C_matrix
