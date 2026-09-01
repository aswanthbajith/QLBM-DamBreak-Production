import pytest
import numpy as np
import scipy.linalg as la
from classical.reference_solver import run_two_phase_dambreak
from quantum.carleman_two_phase_step import quantum_carleman_two_phase_step


class TestMultistepCarleman:
    """
    Rigorously tests Level F: Multi-Step Convergence of the Carleman QLBM Solver.
    """

    def test_01_multistep_accuracy_4x4_t5(self):
        nx, ny = 4, 4
        timesteps = 5
        
        c_hist = run_two_phase_dambreak(nx=nx, ny=ny, timesteps=timesteps)
        q_hist = quantum_carleman_two_phase_step(nx=nx, ny=ny, timesteps=timesteps, order=2, use_block_encoding=True)
        
        for t in range(1, timesteps + 1):
            rho_c = c_hist[t]["rho"]
            rho_q = q_hist[t]["rho"]
            phi_c = c_hist[t]["phi"]
            phi_q = q_hist[t]["phi"]
            
            err_rho = float(la.norm(rho_q - rho_c) / la.norm(rho_c))
            err_phi = float(la.norm(phi_q - phi_c) / (la.norm(phi_c) + 1e-14))
            
            print(f"t={t:2d} | Density Error: {err_rho*100:6.3f}% | Phase Error: {err_phi*100:6.3f}% | P_succ: {q_hist[t]['p_success_mean']:.4f}")
            
            # Non-divergence check: error must remain bounded (< 10%) over multi-step evolution
            assert err_rho < 0.05, f"t={t}: Density error {err_rho*100:.2f}% >= 5%"
            assert err_phi < 0.10, f"t={t}: Phase error {err_phi*100:.2f}% >= 10%"
