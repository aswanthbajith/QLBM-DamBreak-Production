"""
Phase F20: Choi-Matrix Verification and Complete Positivity Engine.

Constructs Choi matrix:
J(E) = (I (x) E)(|Phi><Phi|)

Verifies:
1. J(E) >= 0 (Complete Positivity)
2. Tr(J(E)) = 1.0 (Trace Preservation)
3. Rank(J(E)) = D
"""

from typing import Dict, Any, Tuple
import numpy as np
import scipy.linalg as la

from quantum.f20_kraus import F20KrausRepresentation


class F20ChoiVerification:
    """
    Constructs and audits the Choi matrix of the BGK channel.
    """

    def __init__(self, kraus_rep: F20KrausRepresentation):
        self.kraus_rep = kraus_rep
        self.dim = kraus_rep.dim

    def construct_choi_matrix(self) -> np.ndarray:
        """
        Constructs the D^2 x D^2 Choi matrix J(E).
        """
        dim = self.dim
        choi = np.zeros((dim * dim, dim * dim), dtype=np.complex128)

        # For each basis pair |i><j| on reference system R:
        for i in range(dim):
            for j in range(dim):
                e_ij = np.zeros((dim, dim), dtype=np.complex128)
                e_ij[i, j] = 1.0
                chan_out = self.kraus_rep.apply_channel_to_density_matrix(e_ij)

                # Embed into block (i, j) of size dim x dim
                choi[i * dim : (i + 1) * dim, j * dim : (j + 1) * dim] = chan_out / dim

        return choi

    def audit_choi_properties(self) -> Dict[str, Any]:
        """
        Calculates eigenvalues, trace, rank, and complete positivity.
        """
        choi = self.construct_choi_matrix()
        evals = la.eigvalsh(choi)
        evals_sorted = np.sort(evals)

        min_eval = float(evals_sorted[0])
        max_eval = float(evals_sorted[-1])
        trace_choi = float(np.real(np.trace(choi)))
        rank_choi = int(np.sum(evals > 1e-10))
        is_cp = (min_eval >= -1e-12)

        return {
            "min_eigenvalue": min_eval,
            "max_eigenvalue": max_eval,
            "trace": trace_choi,
            "rank": rank_choi,
            "is_completely_positive": is_cp,
            "is_cptp": is_cp and abs(trace_choi - 1.0) < 1e-12,
        }
