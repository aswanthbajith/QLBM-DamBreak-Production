"""
Phase F20: Kraus Operator Derivation and Completeness Verification.

For Stinespring dilation U |x>_S |0>_E = |F(x)>_S |x>_E,
the Kraus operators are:
K_mu = <mu|_E U |0>_E = |F(mu)> <mu|

Satisfying exact trace preservation:
sum_mu K_mu^dag K_mu = sum_mu |mu><mu| = I_S
"""

from typing import List, Dict, Any, Tuple
import numpy as np
import scipy.linalg as la


class F20KrausRepresentation:
    """
    Derives and verifies Kraus operators for the finite-register BGK channel.
    """

    def __init__(self, dim: int, mapping_dict: Dict[int, int]):
        """
        dim: Dimension D of the Hilbert space.
        mapping_dict: Map from state index x to output index F(x).
        """
        self.dim = dim
        self.mapping = mapping_dict

    def get_kraus_operators(self) -> List[np.ndarray]:
        """
        Returns list of D Kraus matrices K_mu = |F(mu)><mu|.
        Each K_mu is a D x D matrix with a single 1 at row F(mu) and col mu.
        """
        kraus_ops = []
        for mu in range(self.dim):
            K_mu = np.zeros((self.dim, self.dim), dtype=np.complex128)
            f_mu = self.mapping.get(mu, mu)
            K_mu[f_mu, mu] = 1.0
            kraus_ops.append(K_mu)
        return kraus_ops

    def verify_trace_preservation(self) -> Tuple[float, bool]:
        """
        Computes || sum_mu K_mu^dag K_mu - I ||_2.
        """
        kraus_ops = self.get_kraus_operators()
        accum = np.zeros((self.dim, self.dim), dtype=np.complex128)
        for K in kraus_ops:
            accum += K.conj().T @ K

        identity = np.eye(self.dim, dtype=np.complex128)
        residual = float(la.norm(accum - identity, 2))
        is_trace_preserving = (residual < 1e-12)
        return residual, is_trace_preserving

    def apply_channel_to_density_matrix(self, rho: np.ndarray) -> np.ndarray:
        """
        Evaluates E(rho) = sum_mu K_mu rho K_mu^dag.
        """
        kraus_ops = self.get_kraus_operators()
        rho_out = np.zeros((self.dim, self.dim), dtype=np.complex128)
        for K in kraus_ops:
            rho_out += K @ rho @ K.conj().T
        return rho_out
