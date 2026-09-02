"""
Phase F22: Superposition, Entanglement, and Purity Characterization Module.

Analyzes:
1. Coherent superpositions |psi> = a|x1> + b|x2> under dephasing CPTP BGK channel.
2. Bipartite entangled states (|00> + |11>)/sqrt(2) under CPTP channel acting on subsystem A.
3. Quantifies Negativity, Purity, and von Neumann Entropy.
"""

from typing import Dict, Any, Tuple
import numpy as np
import scipy.linalg as la


class F22EntanglementSuperpositionAudit:
    """
    Rigorously characterizes channel action on non-diagonal coherences and entangled states.
    """

    @staticmethod
    def evaluate_superposition_state(
        dim: int,
        mapping: Dict[int, int],
        a: float = 1.0 / np.sqrt(2),
        b: float = 1.0 / np.sqrt(2),
        phase_theta: float = 0.0,
        idx1: int = 0,
        idx2: int = 1,
    ) -> Dict[str, Any]:
        """
        Applies CPTP channel to pure superposition |psi> = a|idx1> + b e^(i theta)|idx2>.
        """
        psi = np.zeros(dim, dtype=np.complex128)
        psi[idx1] = a
        psi[idx2] = b * np.exp(1j * phase_theta)

        rho_in = np.outer(psi, psi.conj())

        # Channel action: E(rho) = sum_x rho_xx |F(x)><F(x)|
        rho_out = np.zeros((dim, dim), dtype=np.complex128)
        for x in range(dim):
            fx = mapping[x]
            rho_out[fx, fx] += rho_in[x, x]

        purity_in = float(np.real(np.trace(rho_in @ rho_in)))
        purity_out = float(np.real(np.trace(rho_out @ rho_out)))

        # Von Neumann Entropy
        eigvals = la.eigvalsh(rho_out)
        eigvals = eigvals[eigvals > 1e-15]
        vn_entropy = float(-np.sum(eigvals * np.log2(eigvals)))

        return {
            "purity_in": purity_in,
            "purity_out": purity_out,
            "von_neumann_entropy": vn_entropy,
            "coherence_off_diagonal_preserved": False,
            "is_thermalized_mixture": (purity_out < 1.0) if mapping[idx1] != mapping[idx2] else True,
        }

    @staticmethod
    def evaluate_entangled_bell_state(
        mapping_2x2: Dict[int, int],
    ) -> Dict[str, Any]:
        """
        Evaluates maximally entangled Bell state (|00> + |11>)/sqrt(2) under (E (x) I).
        """
        # Bell state |Phi+> = 1/sqrt(2) (|00> + |11>)
        psi = np.zeros(4, dtype=np.complex128)
        psi[0] = 1.0 / np.sqrt(2)  # |00>
        psi[3] = 1.0 / np.sqrt(2)  # |11>
        rho_in = np.outer(psi, psi.conj())

        # Apply channel to subsystem A (dim=2)
        # E(rho_AB) = sum_x <x_A|rho_AB|x_A> |F(x)_A><F(x)_A| (x) rho_B(x)
        rho_out = np.zeros((4, 4), dtype=np.complex128)
        # Subsystem A basis states: x=0 (|00>, |01>) -> f(0), x=1 (|10>, |11>) -> f(1)
        # rho_in: |00><00| = 0.5, |11><11| = 0.5, |00><11| = 0.5, |11><00| = 0.5
        f0 = mapping_2x2[0]
        f1 = mapping_2x2[1]

        # Diagonals survive into output:
        # |00><00| -> |f(0), 0><f(0), 0|
        idx_f0_0 = f0 * 2 + 0
        rho_out[idx_f0_0, idx_f0_0] += 0.5

        # |11><11| -> |f(1), 1><f(1), 1|
        idx_f1_1 = f1 * 2 + 1
        rho_out[idx_f1_1, idx_f1_1] += 0.5

        # Off-diagonals dephase to 0 because environment traces out orthogonality
        # Compute partial transpose over A for Peres-Horodecki criterion
        rho_pt = np.zeros((4, 4), dtype=np.complex128)
        for i_a in range(2):
            for j_a in range(2):
                for i_b in range(2):
                    for j_b in range(2):
                        row = i_a * 2 + i_b
                        col = j_a * 2 + j_b
                        pt_row = j_a * 2 + i_b
                        pt_col = i_a * 2 + j_b
                        rho_pt[pt_row, pt_col] = rho_out[row, col]

        pt_eigvals = la.eigvalsh(rho_pt)
        negativity = float(max(0.0, np.sum(np.abs(pt_eigvals[pt_eigvals < 0]))))

        return {
            "initial_entanglement_negativity": 0.5,
            "final_entanglement_negativity": negativity,
            "entanglement_survives": (negativity > 1e-12),
            "positivity_preserved": (np.min(la.eigvalsh(rho_out)) >= -1e-15),
        }
