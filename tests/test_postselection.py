import pytest
import numpy as np
from quantum.carleman_collision import build_local_carleman_operator, lift_state
from quantum.unitary_dilation import (
    normalize_operator,
    build_unitary_dilation,
    apply_block_encoding
)


class TestPostselection:
    """
    Rigorously tests Step 6: Postselection & Success Probability Tracking.
    """

    def test_01_success_probability_positivity_and_bound(self):
        C2 = build_local_carleman_operator(omega=1.25, order=2)
        C2_scaled, alpha = normalize_operator(C2)
        U2 = build_unitary_dilation(C2_scaled)
        
        # Test across physical states
        for rho in [0.5, 1.0, 1.5]:
            f0 = np.full(9, rho / 9.0)
            Y0 = lift_state(f0, order=2)
            Y0_normed = Y0 / np.linalg.norm(Y0)
            
            res = apply_block_encoding(Y0_normed, U2, alpha=alpha)
            p_succ = res["p_success"]
            
            assert 0.0 < p_succ <= 1.0, f"Invalid success probability: {p_succ}"
            assert np.isclose(p_succ, np.linalg.norm(C2_scaled @ Y0_normed)**2)
