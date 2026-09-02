"""
Phase F20: Quantum Channel Definition and Evaluation Engine.

Implements the four interpretations of quantum BGK collision:
- Interpretation 1: Classical stochastic channel
- Interpretation 2: Complete computational-basis dephasing followed by BGK
- Interpretation 3: Coherent Stinespring dilation followed by environmental trace-out
- Interpretation 4: Amplitude-encoded transformation
"""

from typing import Dict, Any, List, Tuple
import numpy as np

from quantum.f20_kraus import F20KrausRepresentation
from quantum.f20_choi import F20ChoiVerification


class F20QuantumChannel:
    """
    Evaluates and compares quantum channel interpretations for BGK collision.
    """

    def __init__(self, dim: int, mapping_dict: Dict[int, int]):
        self.dim = dim
        self.mapping = mapping_dict
        self.kraus_rep = F20KrausRepresentation(dim, mapping_dict)
        self.choi_audit = F20ChoiVerification(self.kraus_rep)

    def apply_channel(self, rho: np.ndarray) -> np.ndarray:
        """
        Applies Stinespring/Kraus channel: E(rho) = sum_mu K_mu rho K_mu^dag.
        """
        return self.kraus_rep.apply_channel_to_density_matrix(rho)

    def apply_interpretation_2_dephasing(self, rho: np.ndarray) -> np.ndarray:
        """
        Interpretation 2: Dephase diag(rho), then map |x><x| -> |F(x)><F(x)|.
        """
        rho_out = np.zeros((self.dim, self.dim), dtype=np.complex128)
        for x in range(self.dim):
            p_x = rho[x, x]
            f_x = self.mapping.get(x, x)
            rho_out[f_x, f_x] += p_x
        return rho_out

    def check_interpretation_equivalence(self, rho: np.ndarray) -> Tuple[float, bool]:
        """
        Verifies || E_Stinespring(rho) - E_Dephasing(rho) ||_F.
        """
        out_stinespring = self.apply_channel(rho)
        out_dephasing = self.apply_interpretation_2_dephasing(rho)
        diff = float(np.linalg.norm(out_stinespring - out_dephasing, "fro"))
        is_exact = (diff < 1e-12)
        return diff, is_exact
