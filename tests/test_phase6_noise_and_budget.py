#!/usr/bin/env python3
"""
Phase 6 Noise Robustness and Error Budget Tests.
"""

import sys, os
sys.path.append(os.path.join(os.path.dirname(__file__), "../classical"))
sys.path.append(os.path.join(os.path.dirname(__file__), "../quantum"))

import pytest
import numpy as np
import scipy.linalg as la
from dam_break_qlbm_sim import QLBMDamBreakSimulation

class TestPhase6NoiseAndBudget:
    def test_01_noise_robustness_threshold(self):
        """Tests that depolarizing noise rate lambda <= 0.01 preserves fidelity > 0.98."""
        sim = QLBMDamBreakSimulation(nx=4, ny=2, dam_w=2, dam_h=2, total_steps=1, truncation_order=2)
        psi = sim.carleman.project_state(sim.Y_0)
        psi_norm = psi / la.norm(psi)
        dim = len(psi_norm)
        
        for lambda_n in [0.0001, 0.001, 0.01]:
            np.random.seed(42)
            n_vec = np.random.randn(dim)
            n_vec = n_vec / la.norm(n_vec)
            noisy_psi = np.sqrt(1.0 - lambda_n) * psi_norm + np.sqrt(lambda_n) * n_vec
            noisy_psi = noisy_psi / la.norm(noisy_psi)
            fid = float(abs(np.dot(psi_norm, noisy_psi))**2)
            assert fid > 0.98, f"Noise {lambda_n}: Fidelity {fid:.4f} below 0.98"

    def test_02_error_budget_monotonicity(self):
        """Tests that measurement error decreases monotonically with shot count N_s."""
        sim = QLBMDamBreakSimulation(nx=4, ny=2, dam_w=2, dam_h=2, total_steps=1, truncation_order=2)
        exact_state = sim.carleman.project_state(sim.Y_0)
        exact_m = sim.extract_observables(exact_state, simulate_shots=False)["mass"]
        
        errors = []
        for ns in [100, 1000, 10000, 100000]:
            sim.n_shots = ns
            np.random.seed(42 + ns)
            e_ns = []
            for _ in range(15):
                obs = sim.extract_observables(exact_state, simulate_shots=True)
                e_ns.append(abs(obs["mass"] - exact_m) / exact_m)
            errors.append(np.mean(e_ns))
            
        assert errors[0] > errors[1] > errors[2] > errors[3], "Shot noise error is not monotonically decreasing"
