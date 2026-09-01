"""
Unitary Dilation & Block Encoding Module for Non-Unitary Carleman Operators.

Embeds any general linear / dissipative contraction A (||A|| <= 1)
into an exact unitary operator acting on an enlarged Hilbert space:
U_A = [[ A,               sqrt(I - A A^H) ],
       [ sqrt(I - A^H A), -A^H            ]]
"""
import numpy as np
import scipy.linalg as la


def normalize_operator(A, safety_factor=1.01):
    """
    Computes spectral norm ||A||_2 and returns the contractive normalized
    matrix A_scaled = A / alpha such that ||A_scaled||_2 <= 1.
    
    Returns:
        A_scaled: Contractive matrix with ||A_scaled||_2 < 1.0
        alpha: Exact scaling factor (spectral norm * safety_factor)
    """
    A = np.asarray(A, dtype=np.complex128)
    s_max = float(la.svdvals(A)[0])
    alpha = max(1.0, s_max * safety_factor)
    A_scaled = A / alpha
    return A_scaled, alpha


def matrix_sqrt_hermitian(M):
    """
    Computes the principal matrix square root for positive semi-definite Hermitian matrix M.
    """
    # Force strict Hermitian symmetry
    M_herm = 0.5 * (M + M.conj().T)
    eigvals, eigvecs = la.eigh(M_herm)
    # Clip small negative numerical eigenvalues
    eigvals_pos = np.maximum(eigvals, 0.0)
    sqrt_M = eigvecs @ np.diag(np.sqrt(eigvals_pos)) @ eigvecs.conj().T
    return sqrt_M


def build_unitary_dilation(A_scaled):
    """
    Constructs the 2D x 2D unitary dilation (block encoding) of contractive matrix A_scaled:
    U_A = [[ A_scaled,               sqrt(I - A_scaled A_scaled^H) ],
           [ sqrt(I - A_scaled^H A_scaled), -A_scaled^H            ]]
    """
    A_scaled = np.asarray(A_scaled, dtype=np.complex128)
    dim = A_scaled.shape[0]
    eye = np.eye(dim, dtype=np.complex128)
    
    # Blocks
    I_minus_AAH = eye - A_scaled @ A_scaled.conj().T
    I_minus_AHA = eye - A_scaled.conj().T @ A_scaled
    
    D1 = matrix_sqrt_hermitian(I_minus_AAH)
    D2 = matrix_sqrt_hermitian(I_minus_AHA)
    
    U = np.zeros((2 * dim, 2 * dim), dtype=np.complex128)
    U[:dim, :dim] = A_scaled
    U[:dim, dim:] = D1
    U[dim:, :dim] = D2
    U[dim:, dim:] = -A_scaled.conj().T
    
    # Re-unitarize via SVD polar factor to ensure exact machine-precision unitarity
    u_svd, _, vh_svd = la.svd(U)
    U_exact = u_svd @ vh_svd
    return U_exact


def verify_unitarity(U, tol=1e-10):
    """
    Verifies that U is strictly unitary: ||U^H U - I|| < tol.
    """
    dim = U.shape[0]
    eye = np.eye(dim, dtype=np.complex128)
    diff = la.norm(U.conj().T @ U - eye)
    return diff < tol, float(diff)


def apply_block_encoding(state_psi, U_dilation, alpha=1.0):
    """
    Applies the block-encoded unitary to state |0>_anc (x) |psi>,
    projects onto the |0> ancilla subspace, and decodes the result.
    
    Returns:
        output_state: A * psi (unnormalized physical state)
        p_success: Probability of measuring ancilla |0> = ||A_scaled psi||^2
        normalized_state: Normalized physical state on success
    """
    state_psi = np.asarray(state_psi, dtype=np.complex128).ravel()
    dim = state_psi.shape[0]
    
    # Lift to ancilla space: |0> (x) |psi> = [ psi; 0 ]
    lifted_in = np.zeros(2 * dim, dtype=np.complex128)
    lifted_in[:dim] = state_psi
    
    # Apply dilation
    lifted_out = U_dilation @ lifted_in
    
    # Project onto ancilla |0> (first dim components)
    success_branch = lifted_out[:dim]
    p_success = float(np.sum(np.abs(success_branch)**2))
    
    # Unscale by alpha to recover exact action A * psi
    output_state = success_branch * alpha
    
    norm_succ = np.linalg.norm(success_branch)
    normalized_state = (success_branch / norm_succ) if norm_succ > 1e-14 else np.zeros_like(success_branch)
    
    return {
        "output_state": output_state.real if np.all(np.isreal(state_psi)) else output_state,
        "p_success": p_success,
        "normalized_state": normalized_state,
        "alpha": alpha
    }
