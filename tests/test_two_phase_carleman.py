import pytest
import numpy as np
import scipy.linalg as la
from classical.d2q9 import C_X, C_Y, W
from classical.reference_solver import initialize_two_phase_dambreak, collision_two_phase
from quantum.two_phase_carleman import (
    build_two_phase_carleman_basis,
    build_two_phase_carleman_operator,
    apply_two_phase_carleman
)


class TestTwoPhaseCarleman:
    """
    Rigorously tests Step 8: Two-Phase Coupled Carleman Linearization.
    """

    def test_01_basis_dimensions(self):
        b1 = build_two_phase_carleman_basis(order=1)
        assert b1["total_dim"] == 18
        
        b2 = build_two_phase_carleman_basis(order=2)
        assert b2["total_dim"] == 342
        assert b2["layer_dims"] == [18, 324]

    def test_02_two_phase_dam_break_node_collision(self):
        phi, rho, u, f, g = initialize_two_phase_dambreak(4, 4)
        
        # Test on liquid node (0, 0) and gas node (3, 3)
        for y, x in [(0, 0), (3, 3)]:
            f_node = f[:, y, x]
            g_node = g[:, y, x]
            phi_node = phi[y:y+1, x:x+1]
            rho_node = rho[y:y+1, x:x+1]
            u_node = u[:, y:y+1, x:x+1]
            
            # Classical reference collision (zero forcing)
            f_c, g_c = collision_two_phase(f[:, y:y+1, x:x+1], g[:, y:y+1, x:x+1],
                                           phi_node, rho_node, u_node, g_acc=0.0)
            f_c = f_c.ravel()
            g_c = g_c.ravel()
            
            # Carleman Order 2
            C2 = build_two_phase_carleman_operator(tau_f=0.8, tau_g=0.7, rho0=float(rho[y, x]), order=2)
            f_q, g_q = apply_two_phase_carleman(f_node, g_node, C2, order=2)
            
            err_f = la.norm(f_q - f_c) / la.norm(f_c)
            err_g = la.norm(g_q - g_c) / (la.norm(g_c) + 1e-14)
            
            assert err_f < 1e-3, f"Node ({y},{x}): Hydrodynamic error {err_f:.2e} >= 1e-3"
            assert err_g < 1e-3, f"Node ({y},{x}): Phase error {err_g:.2e} >= 1e-3"
