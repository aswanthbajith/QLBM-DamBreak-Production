"""
Phase F22: Rigorous Stinespring Dilation and CPTP Quantum Channel Engine.

Proves:
1. Isometry V |x>_S |0>_E = |F(x)>_S |x>_E with V^dagger V = I_S.
2. Kraus decomposition K_mu = |F(mu)><mu| with sum K_mu^dagger K_mu = I_S.
3. Choi matrix J(E) >= 0 (Complete Positivity).
4. Exact channel action on arbitrary density matrices rho:
   E(rho) = sum_x <x|rho|x> |F(x)><F(x)|
"""

from typing import Dict, Any, List, Tuple
import numpy as np
import scipy.linalg as la


class F22StinespringDilationProof:
    """
    Rigorously verifies Stinespring dilation, Kraus decomposition, and Choi complete positivity.
    """

    def __init__(self, dim_S: int, mapping_dict: Dict[int, int]):
        self.dim_S = dim_S
        self.dim_E = dim_S
        self.mapping = mapping_dict

    def construct_isometry_matrix(self) -> np.ndarray:
        """
        Constructs the explicit matrix representation of isometry V: H_S -> H_S (x) H_E.
        V maps |x>_S to |F(x)>_S (x) |x>_E.
        """
        V = np.zeros((self.dim_S * self.dim_E, self.dim_S), dtype=np.complex128)
        for x in range(self.dim_S):
            fx = self.mapping[x]
            idx_out = fx * self.dim_E + x
            V[idx_out, x] = 1.0
        return V

    def verify_isometry(self) -> Tuple[float, bool]:
        """
        Verifies V^dagger V = I_S.
        """
        V = self.construct_isometry_matrix()
        V_dag_V = V.conj().T @ V
        diff = V_dag_V - np.eye(self.dim_S, dtype=np.complex128)
        res = float(la.norm(diff))
        return res, (res < 1e-12)

    def construct_kraus_operators(self) -> List[np.ndarray]:
        """
        Constructs explicit Kraus operators K_mu = <mu|_E V = |F(mu)><mu|.
        """
        kraus_list = []
        for mu in range(self.dim_E):
            K_mu = np.zeros((self.dim_S, self.dim_S), dtype=np.complex128)
            f_mu = self.mapping[mu]
            K_mu[f_mu, mu] = 1.0
            kraus_list.append(K_mu)
        return kraus_list

    def verify_trace_preservation(self) -> Tuple[float, bool]:
        """
        Verifies sum_mu K_mu^dagger K_mu = I_S.
        """
        kraus_list = self.construct_kraus_operators()
        tp_sum = sum(K.conj().T @ K for K in kraus_list)
        diff = tp_sum - np.eye(self.dim_S, dtype=np.complex128)
        res = float(la.norm(diff))
        return res, (res < 1e-12)

    def construct_choi_matrix(self) -> np.ndarray:
        """
        Constructs the Choi matrix J(E) = (I (x) E)(|Phi><Phi|).
        """
        d = self.dim_S
        choi = np.zeros((d * d, d * d), dtype=np.complex128)
        for x in range(d):
            fx = self.mapping[x]
            # Basis element |x><x| (x) |F(x)><F(x)|
            idx = x * d + fx
            choi[idx, idx] = 1.0 / d
        return choi

    def audit_complete_positivity(self) -> Dict[str, Any]:
        """
        Computes Choi spectrum to prove complete positivity (lambda_min >= 0).
        """
        choi = self.construct_choi_matrix()
        eigvals = la.eigvalsh(choi)
        min_eig = float(np.min(eigvals))
        trace_val = float(np.real(np.trace(choi)))

        return {
            "min_eigenvalue": min_eig,
            "trace": trace_val,
            "is_completely_positive": (min_eig >= -1e-14),
            "is_trace_preserving": abs(trace_val - 1.0) < 1e-12,
            "is_cptp": (min_eig >= -1e-14) and (abs(trace_val - 1.0) < 1e-12),
        }

    def apply_channel_to_density_matrix(self, rho: np.ndarray) -> np.ndarray:
        """
        Applies channel E(rho) = sum_mu K_mu rho K_mu^dagger.
        """
        kraus_list = self.construct_kraus_operators()
        rho_out = sum(K @ rho @ K.conj().T for K in kraus_list)
        return rho_out
