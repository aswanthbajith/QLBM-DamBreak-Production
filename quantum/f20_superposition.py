"""
Phase F20: Superposition and Coherence Analysis Module.

Evaluates:
|psi> = a|x1> + b e^{i theta} |x2>
under the CPTP channel E(rho).
"""

from typing import Dict, Any, Tuple
import numpy as np

from quantum.f20_channel import F20QuantumChannel


class F20SuperpositionAudit:
    """
    Audits coherence loss and state evolution under BGK channel.
    """

    def __init__(self, channel: F20QuantumChannel):
        self.channel = channel
        self.dim = channel.dim

    def test_superposition(
        self,
        x1: int,
        x2: int,
        a: float = 0.6,
        b: float = 0.8,
        theta: float = 0.0,
    ) -> Dict[str, Any]:
        """
        Constructs |psi> = a|x1> + b e^{i theta}|x2> and applies E(rho).
        """
        norm = np.sqrt(a**2 + b**2)
        c1 = a / norm
        c2 = (b / norm) * np.exp(1j * theta)

        psi = np.zeros(self.dim, dtype=np.complex128)
        psi[x1] = c1
        psi[x2] = c2

        rho_in = np.outer(psi, psi.conj())
        rho_out = self.channel.apply_channel(rho_in)

        f_x1 = self.channel.mapping.get(x1, x1)
        f_x2 = self.channel.mapping.get(x2, x2)
        outputs_equal = (f_x1 == f_x2)

        # Off-diagonal coherence remaining
        off_diag_remaining = float(np.sum(np.abs(rho_out - np.diag(np.diag(rho_out)))))
        trace_out = float(np.real(np.trace(rho_out)))

        return {
            "x1": x1,
            "x2": x2,
            "f_x1": f_x1,
            "f_x2": f_x2,
            "outputs_equal": outputs_equal,
            "theta": theta,
            "trace_out": trace_out,
            "off_diag_remaining": off_diag_remaining,
            "is_pure_output": (outputs_equal and off_diag_remaining < 1e-12),
        }
