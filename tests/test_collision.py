import pytest
import numpy as np
from classical.equilibrium import compute_equilibrium, compute_macroscopic
from classical.collision import collide_bgk

class TestCollision:
    def test_01_mass_conservation_under_collision(self):
        rho = np.array([[1.0, 0.5], [0.8, 1.2]])
        u = np.array([[[0.05, -0.02], [0.01, 0.0]], [[0.0, 0.03], [-0.04, 0.02]]])
        f_eq = compute_equilibrium(rho, u)
        
        # Perturb populations
        f_in = f_eq * (1.0 + 0.01 * np.sin(np.arange(9)[:, None, None]))
        f_out = collide_bgk(f_in, omega=1.0)
        
        rho_in = np.sum(f_in, axis=0)
        rho_out = np.sum(f_out, axis=0)
        assert np.allclose(rho_in, rho_out, atol=1e-12)
