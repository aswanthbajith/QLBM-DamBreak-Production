import pytest
import numpy as np
from classical.equilibrium import compute_equilibrium, compute_macroscopic
from classical.d2q9 import C_X, C_Y

class TestEquilibrium:
    def test_01_mass_and_momentum_conservation(self):
        rho = np.array([[1.0, 0.5], [0.8, 1.2]])
        u = np.array([[[0.05, -0.02], [0.01, 0.0]], [[0.0, 0.03], [-0.04, 0.02]]])
        
        f_eq = compute_equilibrium(rho, u)
        rho_rec, u_rec = compute_macroscopic(f_eq)
        
        assert np.allclose(rho_rec, rho, atol=1e-12)
        assert np.allclose(u_rec, u, atol=1e-12)

    def test_02_zero_velocity_rest_state(self):
        rho = np.ones((2, 2))
        u = np.zeros((2, 2, 2))
        f_eq = compute_equilibrium(rho, u)
        from classical.d2q9 import W
        for i in range(9):
            assert np.allclose(f_eq[i], W[i], atol=1e-12)
