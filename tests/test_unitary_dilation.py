import pytest
import numpy as np
import scipy.linalg as la
from quantum.carleman_collision import build_local_carleman_operator
from quantum.unitary_dilation import (
    normalize_operator,
    build_unitary_dilation,
    verify_unitarity,
    apply_block_encoding
)


class TestUnitaryDilation:
    """
    Rigorously tests Step 5: Unitary Dilation & Block Encoding for Non-Unitary Operators.
    """

    def test_01_dilation_unitarity_order1(self):
        C1 = build_local_carleman_operator(omega=1.25, order=1)
        C1_scaled, alpha = normalize_operator(C1)
        
        assert alpha >= 1.0
        assert la.norm(C1_scaled, 2) <= 1.0
        
        U1 = build_unitary_dilation(C1_scaled)
        is_unitary, err = verify_unitarity(U1)
        assert is_unitary, f"U1 non-unitary: {err:.2e}"
        assert err < 1e-12

    def test_02_dilation_unitarity_order2(self):
        C2 = build_local_carleman_operator(omega=1.25, order=2) # 90x90
        C2_scaled, alpha = normalize_operator(C2)
        
        assert alpha >= 1.0
        assert la.norm(C2_scaled, 2) <= 1.0
        
        U2 = build_unitary_dilation(C2_scaled) # 180x180
        is_unitary, err = verify_unitarity(U2)
        assert is_unitary, f"U2 non-unitary: {err:.2e}"
        assert err < 1e-12

    def test_03_block_encoding_exact_action(self):
        C2 = build_local_carleman_operator(omega=1.25, order=2)
        C2_scaled, alpha = normalize_operator(C2)
        U2 = build_unitary_dilation(C2_scaled)
        
        np.random.seed(42)
        psi = np.random.uniform(-1, 1, 90)
        psi /= np.linalg.norm(psi)
        
        # Expected linear action: C2 * psi
        expected = C2 @ psi
        
        res = apply_block_encoding(psi, U2, alpha=alpha)
        actual = res["output_state"]
        
        err = la.norm(actual - expected) / la.norm(expected)
        assert err < 1e-12, f"Block encoding recovery error {err:.2e} >= 1e-12"
        assert 0.0 < res["p_success"] <= 1.0
