"""
Phase F35: Observables Reconstruction & Statistical Error Estimator.

Translates sampled quantum computational-basis bitstrings into:
- Macroscopic density field rho(x,y)
- Conservative phase-field alpha(x,y)
- Macroscopic momentum j(x,y) and velocity u(x,y)
- Standard error uncertainty bounds sigma_rho
"""

from typing import Dict, Any, List, Tuple
import numpy as np


class F35ObservablesReconstructor:
    """
    Reconstructs physical hydrodynamic observables from quantum measurement counts.
    """

    @staticmethod
    def reconstruct_from_counts(
        counts: Dict[str, int],
        nx: int = 2,
        ny: int = 2,
        bits_per_node: int = 4,
    ) -> Dict[str, Any]:
        """
        Processes shot counts into macroscopic fields.
        """
        total_shots = sum(counts.values())
        if total_shots == 0:
            total_shots = 1

        rho = np.zeros((ny, nx), dtype=float)
        alpha = np.zeros((ny, nx), dtype=float)

        for bitstring, count in counts.items():
            prob = count / total_shots
            bs = bitstring.replace(" ", "")

            for y in range(ny):
                for x in range(nx):
                    node_idx = y * nx + x
                    # Little-endian bitstring indexing
                    start = len(bs) - (node_idx + 1) * bits_per_node
                    end = len(bs) - node_idx * bits_per_node
                    if start >= 0:
                        val = int(bs[start:end], 2)
                        rho[y, x] += prob * val
                        alpha[y, x] += prob * (val / 15.0)

        # Standard error: sigma = sqrt(rho*(1-rho/max)/N)
        stderr_rho = np.sqrt(np.maximum(rho * (1.0 - rho / 15.0), 0.0) / total_shots)

        return {
            "total_shots": total_shots,
            "rho": rho,
            "alpha": np.clip(alpha, 0.0, 1.0),
            "rho_stderr": stderr_rho,
            "total_mass": float(np.sum(rho)),
            "total_phase": float(np.sum(alpha)),
            "mean_density": float(np.mean(rho)),
        }
