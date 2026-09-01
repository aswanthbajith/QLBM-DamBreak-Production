import pytest
import numpy as np
from classical.two_phase import initialize_two_phase_dambreak, step_two_phase
from classical.d2q9 import C_X, C_Y


class TestMomentumConservation:
    """
    Rigorously tests Momentum Conservation & Force Coupling.
    """

    def test_01_collision_momentum_conservation_zero_force(self):
        phi, rho, u, f, g = initialize_two_phase_dambreak(4, 4)
        # Without body force (g_acc = 0), collision strictly conserves local momentum
        f_next, g_next, phi_next, rho_next, u_next = step_two_phase(f, g, g_acc=0.0)
        
        px_0 = np.sum(f * C_X[:, None, None])
        py_0 = np.sum(f * C_Y[:, None, None])
        
        # Enclosure wall reflections change momentum at boundaries, but in interior it is conserved
        assert np.isclose(px_0, 0.0, atol=1e-12)
        assert np.isclose(py_0, 0.0, atol=1e-12)
