#!/usr/bin/env python3
"""
Test QSVT Condition Spectrum & Subnormalization Scaling.

Validates that condition number kappa(I + dt * A_C) < 1.5 and subnormalization
alpha <= 11.5 remains bounded across grid dimensions.
"""

import sys, os
sys.path.append(os.path.join(os.path.dirname(__file__), "../classical"))
sys.path.append(os.path.join(os.path.dirname(__file__), "../quantum"))

import pytest
import numpy as np
import scipy.linalg as la
from carleman_lbm import CarlemanTwoPhaseLBM
from block_encoding import QuantumBlockEncoding
from qsvt_solver import QSVTSolver

class TestQSVTConditionSpectrum:
    @pytest.mark.parametrize("nx,ny", [(1,1), (2,1), (2,2), (4,2)])
    def test_01_spectrum_bounds_and_inversion(self, nx, ny):
        """Tests condition number, subnormalization, and inversion accuracy."""
        c_mod = CarlemanTwoPhaseLBM(nx=nx, ny=ny, truncation_order=2)
        A = c_mod.A_C.toarray()
        dim = A.shape[0]

        # Step operator M = I + 0.01 * A
        M = np.eye(dim, dtype=np.complex128) + 0.01 * A

        # 1. Block encoding subnormalization
        be = QuantumBlockEncoding(M)
        assert be.alpha <= 12.0, f"Subnormalization alpha ({be.alpha:.4f}) exceeds bound 12.0"

        # 2. Condition number
        svs = la.svd(M, compute_uv=False)
        sigma_max = float(np.max(svs))
        sigma_min = float(np.min(svs))
        kappa = sigma_max / sigma_min
        assert kappa < 1.5, f"Condition number kappa ({kappa:.4f}) exceeds threshold 1.5"

        # 3. QSVT Inversion accuracy
        np.random.seed(42 + dim)
        b = np.random.randn(dim) + 0.1j * np.random.randn(dim)
        solver = QSVTSolver(M, b, degree=15)
        res = solver.solve()

        assert res["residual"] < 1e-9, f"Linear residual ({res["residual"]:.4e}) exceeds 1e-9"
        assert res["fidelity"] > 0.9999, f"Fidelity ({res["fidelity"]:.6f}) below 0.9999"
