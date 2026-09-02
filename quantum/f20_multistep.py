"""
Phase F20: Multi-Step Channel Evolution and Composition Engine.

Audits E^K vs F^K over K = 1, 2, 4, 8, 16 timesteps.
"""

from typing import Dict, Any, List
import numpy as np
import scipy.linalg as la

from quantum.f20_channel import F20QuantumChannel


class F20MultiStepChannelAudit:
    """
    Compares repeated quantum channel application E^K with repeated classical map F^K.
    """

    def __init__(self, channel: F20QuantumChannel):
        self.channel = channel
        self.dim = channel.dim

    def evolve_classical_state(self, x0: int, k_steps: int) -> int:
        """Applies classical map F^K(x0)."""
        curr = x0
        for _ in range(k_steps):
            curr = self.channel.mapping.get(curr, curr)
        return curr

    def evolve_quantum_density_matrix(self, rho0: np.ndarray, k_steps: int) -> np.ndarray:
        """Applies quantum channel E^K(rho0)."""
        curr_rho = np.copy(rho0)
        for _ in range(k_steps):
            curr_rho = self.channel.apply_channel(curr_rho)
        return curr_rho

    def verify_multistep_equivalence(self, x0: int, k_steps: int) -> Dict[str, Any]:
        """
        Tests whether E^K(|x0><x0|) == |F^K(x0)><F^K(x0)|.
        """
        rho0 = np.zeros((self.dim, self.dim), dtype=np.complex128)
        rho0[x0, x0] = 1.0

        x_k_classical = self.evolve_classical_state(x0, k_steps)
        rho_k_quantum = self.evolve_quantum_density_matrix(rho0, k_steps)

        rho_k_expected = np.zeros((self.dim, self.dim), dtype=np.complex128)
        rho_k_expected[x_k_classical, x_k_classical] = 1.0

        diff_fro = float(la.norm(rho_k_quantum - rho_k_expected, "fro"))
        is_exact = (diff_fro < 1e-12)

        return {
            "k_steps": k_steps,
            "x0": x0,
            "x_final": x_k_classical,
            "diff_frobenius": diff_fro,
            "is_exact_multistep": is_exact,
        }
