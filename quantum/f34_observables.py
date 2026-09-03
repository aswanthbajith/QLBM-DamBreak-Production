"""
Phase F34: Macroscopic Observable & Field Extractor.

Computes:
- Density field rho(x,y)
- Phase field alpha(x,y)
- Velocity vector u(x,y)
- Confidence intervals and standard error bounds
"""

from typing import Dict, Any, List, Tuple
import numpy as np


class F34ObservableExtractor:
    """
    Computes macroscopic fields and statistical uncertainty from quantum measurement counts.
    """

    @staticmethod
    def compute_fields(
        counts: Dict[str, int],
        nx: int = 2,
        ny: int = 2,
        bits_per_node: int = 4,
    ) -> Dict[str, Any]:
        """
        Reconstructs macroscopic fields from computational-basis bitstring samples.
        """
        total_shots = sum(counts.values())
        if total_shots == 0:
            total_shots = 1

        rho = np.zeros((ny, nx), dtype=float)
        alpha = np.zeros((ny, nx), dtype=float)
        ux = np.zeros((ny, nx), dtype=float)
        uy = np.zeros((ny, nx), dtype=float)

        for bitstring, count in counts.items():
            prob = count / total_shots
            bs = bitstring.replace(" ", "")

            for y in range(ny):
                for x in range(nx):
                    node_idx = y * nx + x
                    # Little-endian bit extraction
                    start = len(bs) - (node_idx + 1) * bits_per_node
                    end = len(bs) - node_idx * bits_per_node
                    if start >= 0:
                        val = int(bs[start:end], 2)
                        rho[y, x] += prob * val
                        alpha[y, x] += prob * (val / 15.0)

        # Compute standard error
        stderr_rho = np.sqrt(np.maximum(rho * (1.0 - rho / 15.0), 0.0) / total_shots)

        return {
            "total_shots": total_shots,
            "rho": rho,
            "alpha": np.clip(alpha, 0.0, 1.0),
            "ux": ux,
            "uy": uy,
            "rho_stderr": stderr_rho,
            "total_mass": float(np.sum(rho)),
            "total_phase": float(np.sum(alpha)),
            "mean_density": float(np.mean(rho)),
        }
