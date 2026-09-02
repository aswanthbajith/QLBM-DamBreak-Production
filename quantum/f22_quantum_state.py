"""
Phase F22: Physical Quantum State Representation and Encodings.

Defines the exact physical encoding of the two-phase D2Q9 lattice state:
Representation A: Computational-Basis Statistical Encoding (Primary Physical Encoding)
    rho = sum_x p_x |x><x|
    where |x> = |f_0, ..., f_8, g_0, ..., g_8> in fixed-point representation.
Representation B: Direct Coherent Superposition / Amplitude Encoding (Diagnostic Encoding)
    |psi> = sum_x c_x |x>
"""

from typing import Dict, Any, List, Tuple
import numpy as np


class F22PhysicalStateEncoding:
    """
    Manages the formal state mapping between physical LBM populations and quantum registers.
    """

    def __init__(self, frac_bits: int = 12):
        self.frac_bits = frac_bits
        self.scale = 1 << frac_bits

    def encode_populations_to_basis_state(
        self,
        f: List[float],
        g: List[float],
    ) -> Tuple[List[int], List[int]]:
        """
        Converts floating-point hydrodynamic (f) and phase-field (g) populations
        into exact fixed-point computational-basis integer tuples.
        """
        f_reg = [int(round(val * self.scale)) for val in f]
        g_reg = [int(round(val * self.scale)) for val in g]
        return f_reg, g_reg

    def decode_basis_state_to_populations(
        self,
        f_reg: List[int],
        g_reg: List[int],
    ) -> Tuple[List[float], List[float]]:
        """
        Decodes fixed-point integer basis registers back to physical LBM populations.
        """
        f = [float(val) / self.scale for val in f_reg]
        g = [float(val) / self.scale for val in g_reg]
        return f, g

    def construct_statistical_density_matrix(
        self,
        states: List[Tuple[List[int], List[int]]],
        probabilities: List[float],
    ) -> Dict[str, Any]:
        """
        Constructs the formal computational-basis diagonal density matrix rho = sum p_x |x><x|.
        """
        probs = np.array(probabilities, dtype=np.float64)
        probs /= np.sum(probs)
        return {
            "type": "COMPUTATIONAL_BASIS_STATISTICAL",
            "states": states,
            "probabilities": probs.tolist(),
            "purity": float(np.sum(probs ** 2)),
            "von_neumann_entropy": float(-np.sum(probs * np.log2(probs + 1e-15))),
        }
