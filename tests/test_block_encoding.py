import pytest
import numpy as np
import scipy.linalg as la
from quantum.carleman_collision import build_local_carleman_operator
from quantum.unitary_dilation import (
    normalize_operator,
    build_unitary_dilation,
    apply_block_encoding
)


class TestBlockEncoding:
    """
    Rigorously tests Level D: Block Encoding Operator Recovery.
    """

    def test_01_matrix_block_reconstruction(self):
        for order in [1, 2]:
            C = build_local_carleman_operator(omega=1.25, order=order)
            dim = C.shape[0]
            C_scaled, alpha = normalize_operator(C)
            U = build_unitary_dilation(C_scaled)
            
            # Extract top-left dim x dim block of U
            top_left_block = U[:dim, :dim]
            reconstructed_C = top_left_block * alpha
            
            err = float(la.norm(reconstructed_C - C) / la.norm(C))
            assert err < 1e-12, f"Order {order}: Block extraction relative error {err:.2e} >= 1e-12"
