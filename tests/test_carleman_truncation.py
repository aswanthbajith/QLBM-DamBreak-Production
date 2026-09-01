import pytest
import numpy as np
import scipy.linalg as la
from classical.d2q9 import C_X, C_Y, W
from quantum.carleman_collision import (
    build_local_carleman_operator,
    apply_carleman_operator
)


def classical_bgk(f, omega=1.25):
    rho = float(np.sum(f))
    ux = float(np.sum(f * C_X) / rho)
    uy = float(np.sum(f * C_Y) / rho)
    f_eq = np.zeros(9)
    for i in range(9):
        c_dot_u = C_X[i] * ux + C_Y[i] * uy
        u_sq = ux**2 + uy**2
        f_eq[i] = W[i] * rho * (1.0 + 3.0 * c_dot_u + 4.5 * c_dot_u**2 - 1.5 * u_sq)
    return (1.0 - omega) * f + omega * f_eq


class TestCarlemanTruncation:
    """
    Rigorously tests Carleman Truncation Error and Order Refinement.
    """

    def test_01_truncation_monotonicity(self):
        np.random.seed(123)
        omega = 1.25
        rho0 = 1.0
        
        C1 = build_local_carleman_operator(omega=omega, rho0=rho0, order=1)
        C2 = build_local_carleman_operator(omega=omega, rho0=rho0, order=2)
        
        # High-velocity non-equilibrium perturbation
        rho = 1.0
        u = np.array([0.08, -0.06])
        f0 = np.zeros(9)
        for i in range(9):
            c_dot_u = C_X[i] * u[0] + C_Y[i] * u[1]
            u_sq = u[0]**2 + u[1]**2
            f0[i] = W[i] * rho * (1.0 + 3.0 * c_dot_u + 4.5 * c_dot_u**2 - 1.5 * u_sq)
        f0 += np.random.uniform(-0.005, 0.005, 9)
        f0 = np.maximum(f0, 1e-4)
        f0 = f0 * (rho / np.sum(f0))
        
        f_c = classical_bgk(f0, omega=omega)
        f_o1 = apply_carleman_operator(f0, C1, order=1)
        f_o2 = apply_carleman_operator(f0, C2, order=2)
        
        err1 = la.norm(f_o1 - f_c) / la.norm(f_c)
        err2 = la.norm(f_o2 - f_c) / la.norm(f_c)
        
        # Order 2 must improve upon Order 1
        assert err2 < err1
        assert err2 < 0.01, f"Order 2 error {err2:.2e} >= 0.01"
