#!/usr/bin/env python3
"""
Test Quantum Finite-Shot Measurement Statistics & SQL Scaling.

Validates that observable sampling noise scales strictly as O(1/sqrt(N_shots))
with R^2 > 0.99 across multiple random seeds.
"""

import sys, os
sys.path.append(os.path.join(os.path.dirname(__file__), "../classical"))
sys.path.append(os.path.join(os.path.dirname(__file__), "../quantum"))

import pytest
import numpy as np
import scipy.stats as stats
from dam_break_qlbm_sim import QLBMDamBreakSimulation

class TestShotNoiseStatistics:
    def test_01_sql_scaling_and_r_squared(self):
        """Tests empirical finite-shot noise regression against 1/sqrt(N_s)."""
        sim = QLBMDamBreakSimulation(nx=4, ny=2, dam_w=2, dam_h=2, total_steps=1, truncation_order=2)
        exact_obs = sim.extract_observables(sim.carleman.project_state(sim.Y_0), simulate_shots=False)
        exact_mass = exact_obs["mass"]

        shot_levels = [100, 1000, 10000, 100000]
        seeds = [42, 123, 456, 789]
        inv_sqrt_shots = [1.0 / np.sqrt(ns) for ns in shot_levels]
        mean_errors = []

        for ns in shot_levels:
            sim.n_shots = ns
            errors_ns = []
            for seed in seeds:
                np.random.seed(seed + ns)
                for _ in range(15):
                    sampled = sim.extract_observables(sim.carleman.project_state(sim.Y_0), simulate_shots=True)
                    rel_err = abs(sampled["mass"] - exact_mass) / exact_mass
                    errors_ns.append(rel_err)
            mean_errors.append(np.mean(errors_ns))

        # Log-log linear regression
        log_x = np.log10(inv_sqrt_shots)
        log_y = np.log10(mean_errors)
        slope, intercept, r_value, p_value, std_err = stats.linregress(log_x, log_y)
        r_squared = r_value**2

        assert r_squared > 0.99, f"Shot noise R^2 ({r_squared:.6f}) is below acceptance threshold 0.99"
        assert 0.85 <= slope <= 1.15, f"Scaling slope ({slope:.4f}) deviates from SQL theoretical 1.0"
