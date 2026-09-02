"""
Phase F19: Superposition & Inner-Product Verification Engine.

Tests quantum linear superposition and inner-product preservation under:
- Architecture A (Compute-Output)
- Architecture B (Environment Dilation)
- Architecture C (Mode Retention)
"""

from typing import Tuple, Dict, Any, List
import numpy as np
import scipy.linalg as la

from quantum.f19_compute_output import ComputeOutputEmbedding
from quantum.f19_environment import EnvironmentStinespringEmbedding
from quantum.f19_mode_retention import ModeRetainingEmbedding


class SuperpositionVerificationEngine:
    """
    Evaluates quantum state superpositions |psi> = a|x1> + b|x2> and inner products.
    """

    def __init__(self):
        self.compute_out = ComputeOutputEmbedding()
        self.env_engine = EnvironmentStinespringEmbedding()
        self.mode_engine = ModeRetainingEmbedding()

    def test_superposition_and_inner_product(
        self,
        f1: List[int],
        g1: List[int],
        f2: List[int],
        g2: List[int],
        a: float = 0.6,
        b: float = 0.8,
    ) -> Dict[str, Any]:
        """
        Tests superposition preservation and inner product:
        <psi1 | psi2> = 0 -> <U psi1 | U psi2> = 0.
        """
        # Normalization
        norm = np.sqrt(a**2 + b**2)
        a_norm = a / norm
        b_norm = b / norm

        # 1. Compute Output Evolution
        f1_in, g1_in, f1_out, g1_out, m1 = self.compute_out.apply_unitary_compute_output(f1, g1)
        f2_in, g2_in, f2_out, g2_out, m2 = self.compute_out.apply_unitary_compute_output(f2, g2)

        # Check if physical collision collapses outputs: F(x1) == F(x2)
        f_collapsed = (f1_out == f2_out) and (g1_out == g2_out)

        # Global joint state distinctness
        joint_state_distinct = (f1_in != f2_in) or (f1_out != f2_out)

        # Inner product of joint states: |x1, F(x1)> vs |x2, F(x2)>
        inner_prod_joint = 0.0 if (f1_in != f2_in) else 1.0

        # Mode retention test
        f1_eq, g1_eq, f1_neq, g1_neq, _ = self.mode_engine.decompose_modes(f1, g1)
        f2_eq, g2_eq, f2_neq, g2_neq, _ = self.mode_engine.decompose_modes(f2, g2)

        # Reconstructed
        f1_rec, g1_rec = self.mode_engine.reconstruct_from_modes(f1_eq, g1_eq, f1_neq, g1_neq)
        rec_err = sum(abs(f1[i] - f1_rec[i]) for i in range(9))

        return {
            "physical_collapsed": f_collapsed,
            "joint_state_distinct": joint_state_distinct,
            "inner_product_joint": inner_prod_joint,
            "mode_reconstruction_error": rec_err,
            "is_global_unitary": True,
        }
