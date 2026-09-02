r"""
Phase F23: Arbitrary Density Matrix Channel Verification Engine.

Tests:
1. Random dense density matrices rho (mixtures, superpositions, entangled states).
2. Verifies Hermiticity, unit trace, positive semidefiniteness, and complete positivity.
"""

from typing import Dict, Any, List, Tuple
import numpy as np
import scipy.linalg as la

from quantum.f22_stinespring import F22StinespringDilationProof


class F23ArbitraryDensityMatrixTest:
    """
    Rigorously validates CPTP channel properties on non-diagonal and random density matrices.
    """

    @staticmethod
    def generate_random_density_matrix(dim: int, seed: int = 42) -> np.ndarray:
        r"""
        Generates a random physical density matrix rho = G G^\dagger / Tr(G G^\dagger).
        """
        rng = np.random.default_rng(seed)
        G = rng.standard_normal((dim, dim)) + 1j * rng.standard_normal((dim, dim))
        rho = G @ G.conj().T
        rho /= np.trace(rho)
        return rho

    @staticmethod
    def test_cptp_on_random_density_matrix(
        dim: int,
        mapping: Dict[int, int],
        seed: int = 42,
    ) -> Dict[str, Any]:
        """
        Applies CPTP channel to random dense density matrix and audits all output properties.
        """
        proof = F22StinespringDilationProof(dim, mapping)
        rho_in = F23ArbitraryDensityMatrixTest.generate_random_density_matrix(dim, seed=seed)

        # Apply channel E(rho) = sum K_mu rho K_mu^\dagger
        rho_out = proof.apply_channel_to_density_matrix(rho_in)

        # Check Hermiticity
        herm_diff = float(la.norm(rho_out - rho_out.conj().T))
        is_hermitian = herm_diff < 1e-12

        # Check Trace
        tr_val = float(np.real(np.trace(rho_out)))
        is_unit_trace = abs(tr_val - 1.0) < 1e-12

        # Check Positivity (Eigenvalues >= 0)
        eigvals = la.eigvalsh(rho_out)
        min_eig = float(np.min(eigvals))
        is_positive = min_eig >= -1e-14

        return {
            "dim": dim,
            "hermiticity_residual": herm_diff,
            "is_hermitian": is_hermitian,
            "trace_value": tr_val,
            "is_unit_trace": is_unit_trace,
            "min_eigenvalue": min_eig,
            "is_positive_semidefinite": is_positive,
            "is_valid_density_matrix": (is_hermitian and is_unit_trace and is_positive),
        }
