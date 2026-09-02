"""
Phase F20: Entanglement and Complete Positivity Audit Engine.

Tests:
|Psi> = (1/sqrt(2)) (|x1>|a> + |x2>|b>)
under channel (E (x) I)(rho_SR).
"""

from typing import Dict, Any, Tuple
import numpy as np

from quantum.f20_channel import F20QuantumChannel


class F20EntanglementAudit:
    """
    Audits entanglement preservation and subsystem reduction under BGK channel.
    """

    def __init__(self, channel: F20QuantumChannel):
        self.channel = channel
        self.dim = channel.dim

    def test_entangled_pair(self, x1: int, x2: int) -> Dict[str, Any]:
        """
        Creates maximally entangled state on S (dim D) and R (dim 2).
        Applies E on S, leaves R untouched.
        """
        dim_S = self.dim
        dim_R = 2

        # State |Psi> = 1/sqrt(2) (|x1>|0> + |x2>|1>)
        psi = np.zeros(dim_S * dim_R, dtype=np.complex128)
        psi[x1 * dim_R + 0] = 1.0 / np.sqrt(2.0)
        psi[x2 * dim_R + 1] = 1.0 / np.sqrt(2.0)

        rho_SR = np.outer(psi, psi.conj())

        # Apply E on subsystem S
        rho_SR_out = np.zeros_like(rho_SR)
        kraus_ops = self.channel.kraus_rep.get_kraus_operators()

        for K in kraus_ops:
            K_joint = np.kron(K, np.eye(dim_R, dtype=np.complex128))
            rho_SR_out += K_joint @ rho_SR @ K_joint.conj().T

        # Reduced density matrix on S: Tr_R(rho_SR_out)
        rho_S_out = np.zeros((dim_S, dim_S), dtype=np.complex128)
        for r in range(dim_R):
            rho_S_out += rho_SR_out[r::dim_R, r::dim_R]

        # Reduced density matrix on R: Tr_S(rho_SR_out)
        rho_R_out = np.zeros((dim_R, dim_R), dtype=np.complex128)
        for s in range(dim_S):
            rho_R_out += rho_SR_out[s * dim_R : (s + 1) * dim_R, s * dim_R : (s + 1) * dim_R]

        trace_joint = float(np.real(np.trace(rho_SR_out)))
        evals_joint = np.linalg.eigvalsh(rho_SR_out)
        min_eval_joint = float(np.min(evals_joint))

        return {
            "trace_joint": trace_joint,
            "min_eigenvalue_joint": min_eval_joint,
            "is_valid_density_matrix": (min_eval_joint >= -1e-12 and abs(trace_joint - 1.0) < 1e-12),
        }
