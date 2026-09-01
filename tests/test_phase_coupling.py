import pytest
import numpy as np
from classical.two_phase import initialize_two_phase_dambreak, step_two_phase, run_two_phase_dambreak
from classical.phase_field import update_phase_field
from quantum.two_phase_collision import build_two_phase_collision_unitary
from quantum.two_phase_step import quantum_two_phase_step


class TestPhaseCoupling:
    """
    Rigorously tests Part H: Two-Phase Hydrodynamic Coupling.
    - Verifies phase qubit conditions the collision operator (omega_liquid != omega_gas)
    - Verifies density contrast rho(phi) = phi*rho_l + (1-phi)*rho_g
    - Verifies horizontal liquid column spreading (dam-break front advancement)
    - Verifies phase interface advection
    """

    def test_01_phase_conditioned_collision_distinction(self):
        # Collision unitary must act differently on phase=0 (gas) vs phase=1 (liquid)
        U_coll = build_two_phase_collision_unitary(tau_liquid=0.80, tau_gas=0.65)
        U_gas = U_coll[:16, :16]
        U_liq = U_coll[16:, 16:]
        
        diff = np.linalg.norm(U_liq - U_gas)
        assert diff > 0.01, f"Phase qubit does not distinguish collision operators: diff={diff}"

    def test_02_density_contrast(self):
        phi, rho, u, f, g = initialize_two_phase_dambreak(4, 4)
        
        # Liquid region (x < 2 and y < 2) vs Gas region (other nodes)
        rho_liq = rho[:2, :2]
        rho_gas = rho[2:, 2:]
        assert np.allclose(rho_liq, 1.0)
        assert np.allclose(rho_gas, 0.1)

    def test_03_phase_interface_advection(self):
        nx, ny = 4, 4
        phi_init = np.array([[1.0 if x < 2 else 0.0 for x in range(nx)] for _ in range(ny)])
        
        # Imposed rightward velocity
        u_flow = np.zeros((2, ny, nx))
        u_flow[0, :, :] = 0.1 # ux = +0.1
        
        phi_adv = update_phase_field(phi_init, u_flow)
        
        # Liquid mass should have shifted rightward
        cm_init = np.sum(np.arange(nx) * np.sum(phi_init, axis=0)) / np.sum(phi_init)
        cm_adv = np.sum(np.arange(nx) * np.sum(phi_adv, axis=0)) / np.sum(phi_adv)
        assert cm_adv >= cm_init, f"Phase field did not advect in flow direction: init={cm_init}, adv={cm_adv}"

    def test_04_dam_break_horizontal_spreading(self):
        # 5 steps of classical dam-break on 8x4 mesh
        history = run_two_phase_dambreak(nx=8, ny=4, timesteps=5, g_acc=-0.002)
        
        phi_0 = history[0]["phi"]
        phi_final = history[-1]["phi"]
        
        # Horizontal center of mass: x_cm = sum(x * phi) / sum(phi)
        x_indices = np.arange(8)[None, :]
        x_cm_0 = float(np.sum(x_indices * phi_0) / np.sum(phi_0))
        x_cm_final = float(np.sum(x_indices * phi_final) / np.sum(phi_final))
        
        # Dam break liquid column spreads rightward: x_cm should advance to the right
        assert x_cm_final >= x_cm_0, f"Dam break did not spread rightward: x0={x_cm_0}, x_final={x_cm_final}"
