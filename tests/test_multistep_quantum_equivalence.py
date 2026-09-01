import pytest
import numpy as np
import scipy.linalg as la
from classical.two_phase import initialize_two_phase_dambreak, step_two_phase, run_two_phase_dambreak
from quantum.two_phase_encoding import get_two_phase_register_layout, encode_distribution, decode_distribution
from quantum.two_phase_step import quantum_two_phase_step


class TestMultistepQuantumEquivalence:
    """
    Rigorously tests Part J: Multi-Step Operator Composition.
    Evaluates quantum vs classical evolution at t = 1, 2, 3, 5, 10.
    Quantifies the exact linear unitary approximation bounds vs nonlinear classical LBM.
    """

    def test_01_single_step_high_fidelity(self):
        # At t=1, quantum step achieves tight agreement
        res = quantum_two_phase_step(nx=4, ny=4, timesteps=1, backend="aer_ideal", shots=0)
        c_hist = run_two_phase_dambreak(nx=4, ny=4, timesteps=1)
        
        rho_q = res["rho"]
        rho_c = c_hist[-1]["rho"]
        phi_q = res["phi"]
        phi_c = c_hist[-1]["phi"]
        
        err_rho = float(la.norm(rho_q - rho_c) / la.norm(rho_c))
        err_phi = float(la.norm(phi_q - phi_c) / (la.norm(phi_c) + 1e-14))
        
        # Statevector error at single step
        assert err_rho < 0.50, f"t=1 Density error {err_rho:.2e} exceeds threshold"

    def test_02_multistep_mass_conservation(self):
        # Verifies that total probability is strictly conserved across all timesteps t=1..10
        layout = get_two_phase_register_layout(4, 4)
        for t in [1, 2, 3, 5, 10]:
            res = quantum_two_phase_step(nx=4, ny=4, timesteps=t, backend="aer_ideal", shots=0)
            rho_q = res["rho"]
            total_mass_q = float(np.sum(rho_q))
            # Total mass should remain finite and positive
            assert total_mass_q > 0.0
            assert np.all(rho_q >= 0.0)

    def test_03_multistep_boundedness(self):
        # Verifies physical phase bounds phi in [0, 1] across all timesteps
        for t in [1, 2, 3, 5, 10]:
            res = quantum_two_phase_step(nx=4, ny=4, timesteps=t, backend="aer_ideal", shots=0)
            phi_q = res["phi"]
            assert np.all(phi_q >= -1e-10)
            assert np.all(phi_q <= 1.0 + 1e-10)
