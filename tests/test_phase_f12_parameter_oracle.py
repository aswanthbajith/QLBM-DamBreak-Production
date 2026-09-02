"""
Phase F12: Test Suite for Coherent Parameter Oracle & Fixed-Point Arithmetic.
"""

import pytest
import numpy as np
import scipy.linalg as la

from quantum.coherent_parameter_oracle import FixedPointArithmetic, CoherentParameterOracle


def test_fixed_point_arithmetic_precision():
    """Verify precision scaling across Q4.8, Q4.12, Q6.12, Q8.16 formats."""
    formats = ["Q4.8", "Q4.12", "Q6.12", "Q8.16"]
    expected_tolerances = {"Q4.8": 2e-2, "Q4.12": 2e-3, "Q6.12": 2e-3, "Q8.16": 2e-4}

    a, b = 0.35, 0.25

    for fmt in formats:
        oracle = CoherentParameterOracle(precision_format=fmt)
        res_add, cost_add = oracle.fp.add(a, b)
        res_mul, cost_mul = oracle.fp.mul(a, b)
        res_div, cost_div = oracle.fp.div(a, b)

        tol = expected_tolerances[fmt]
        assert abs(res_add - (a + b)) < tol
        assert abs(res_mul - (a * b)) < tol
        assert abs(res_div - (a / b)) < tol
        assert cost_add["toffoli"] > 0
        assert cost_mul["toffoli"] > 0


def test_parameter_oracle_generation():
    """Verify local parameter and unitary dilation synthesis."""
    oracle = CoherentParameterOracle(precision_format="Q4.12")
    params = oracle.generate_local_parameters(
        rho=0.8,
        alpha=0.6,
        jx=0.04,
        jy=-0.02,
        Fx=0.001,
        Fy=-0.0005,
    )

    assert "U_C" in params
    assert params["U_C"].shape == (64, 64)
    U_C = params["U_C"]
    unitarity_err = float(la.norm(U_C.conj().T @ U_C - np.eye(64), 2))
    assert unitarity_err < 1e-12, f"Sz.-Nagy dilation non-unitary: {unitarity_err}"
