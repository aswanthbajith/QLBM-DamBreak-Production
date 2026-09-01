"""
Unitary Dilation & Block Encoding for Carleman QLBM.

Embeds rectangular Carleman step-evaluation operators:
    A_eval in R^(18 x 342)
into power-of-two quantum registers (9 state qubits + 1 block-encoding ancilla = 10 qubits):
    A_eval (18x342) -> padded A_tilde (512x512 = 2^9 x 2^9)
    A_bar = A_tilde / alpha (||A_bar||_2 <= 1)
    U_10Q in U(1024 = 2^10) via Sz.-Nagy unitary dilation.

The desired physical 18-variable post-collision state Psi' = [f'; g'] is recovered
from the |0> ancilla success branch and rescaled by alpha.
"""

import numpy as np
import scipy.linalg as la


def normalize_operator(A, safety_factor=1.01):
    """
    Normalize an operator so that ||A_scaled||_2 <= 1.
    """
    A = np.asarray(A, dtype=np.complex128)
    norm = la.norm(A, 2)
    if norm <= 1e-15:
        alpha = 1.0
    else:
        alpha = float(safety_factor * norm)
    return A / alpha, alpha


def pad_rectangular_operator(A, target_dim=512):
    """
    Embed an m x n operator into a square target_dim x target_dim
    power-of-two quantum register matrix by zero padding.

    Default target_dim=512 corresponds to 9 qubits (2^9 = 512).
    """
    A = np.asarray(A, dtype=np.complex128)
    m, n = A.shape

    if target_dim is None:
        target_dim = int(2 ** np.ceil(np.log2(max(m, n))))

    if target_dim < max(m, n):
        raise ValueError(
            f"target_dim ({target_dim}) must be >= max(A.shape) ({max(m, n)})"
        )

    padded = np.zeros((target_dim, target_dim), dtype=np.complex128)
    padded[:m, :n] = A
    return padded


def build_unitary_dilation(A_scaled):
    """
    Build the Sz.-Nagy unitary dilation on a square operator.
    For A_scaled in C^(512 x 512), returns U in U(1024 = 2^10).
    Requires ||A_scaled||_2 <= 1.
    """
    A = np.asarray(A_scaled, dtype=np.complex128)
    if A.shape[0] != A.shape[1]:
        raise ValueError(
            "build_unitary_dilation requires a square matrix. "
            "Use pad_rectangular_operator first."
        )

    n = A.shape[0]
    I = np.eye(n, dtype=np.complex128)

    left_arg = I - A @ A.conj().T
    right_arg = I - A.conj().T @ A

    # Numerical Hermitian projection
    left_arg = (left_arg + left_arg.conj().T) / 2.0
    right_arg = (right_arg + right_arg.conj().T) / 2.0

    left_sqrt = la.sqrtm(left_arg)
    right_sqrt = la.sqrtm(right_arg)

    U = np.block([
        [A, left_sqrt],
        [right_sqrt, -A.conj().T],
    ])
    return U


def verify_unitarity(U, tolerance=1e-10):
    """
    Verify U†U = I.
    """
    U = np.asarray(U, dtype=np.complex128)
    I = np.eye(U.shape[0], dtype=np.complex128)
    error = la.norm(U.conj().T @ U - I, 2)
    return bool(error < tolerance), float(error)


def apply_block_encoding(
    state,
    U,
    physical_dim=18,
    alpha=1.0,
):
    """
    Applies the block-encoded unitary to state |0>_ancilla (x) |state_padded>.
    
    The first physical_dim amplitudes of the successful ancilla branch
    correspond to A @ state / alpha, which when multiplied by alpha recovers
    the exact physical output Psi' = [f'; g'].
    """
    state = np.asarray(state, dtype=np.complex128).ravel()
    dim_in = state.shape[0]
    dim_half = U.shape[0] // 2

    if np.linalg.norm(state) <= 1e-15:
        return {
            "output_state": np.zeros(physical_dim, dtype=np.float64),
            "normalized_state": np.zeros(physical_dim, dtype=np.complex128),
            "p_success": 0.0,
            "alpha": alpha,
        }

    # Lift to full 10-qubit Hilbert space: |0>_ancilla (x) |state_padded>
    full_in = np.zeros(U.shape[0], dtype=np.complex128)
    full_in[:dim_in] = state

    # Apply 1024-dimensional unitary operator
    full_out = U @ full_in

    # Project onto ancilla |0> subspace (first dim_half components)
    success_branch = full_out[:dim_half]
    p_success = float(np.vdot(success_branch, success_branch).real)

    # Extract the physical 18 variables and rescale by alpha
    physical_scaled = success_branch[:physical_dim]
    unscaled_physical = physical_scaled * alpha

    if p_success > 1e-15:
        normalized = physical_scaled / np.sqrt(p_success)
    else:
        normalized = np.zeros(physical_dim, dtype=np.complex128)

    return {
        "output_state": unscaled_physical.real if np.all(np.isreal(state)) else unscaled_physical,
        "normalized_state": normalized,
        "p_success": p_success,
        "alpha": alpha,
    }
