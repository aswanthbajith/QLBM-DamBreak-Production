#!/usr/bin/env python3
"""
Unit Tests for Observable Extraction & Measurement Estimators.
"""

import sys
import os
sys.path.append(os.path.join(os.path.dirname(__file__), '../quantum'))
sys.path.append(os.path.join(os.path.dirname(__file__), '../classical'))

import unittest
import numpy as np
from dam_break_qlbm_sim import QLBMDamBreakSimulation

class TestDamBreakObservables(unittest.TestCase):
    def setUp(self):
        self.sim = QLBMDamBreakSimulation(nx=8, ny=4, dam_w=3, dam_h=3, total_steps=2, n_shots=10000)

    def test_01_observable_extraction_bounds(self):
        """Verify that extracted physical observables are bounded physically."""
        obs = self.sim.extract_observables(self.sim.Psi_0)
        self.assertGreaterEqual(obs['x_star'], 0.5)
        self.assertLessEqual(obs['x_star'], 3.0)
        self.assertGreaterEqual(obs['h_star'], 0.5)
        self.assertLessEqual(obs['h_star'], 1.5)
        self.assertGreater(obs['mass'], 0.0)

    def test_02_finite_shot_sampling(self):
        """Verify that finite-shot estimator produces bounded statistical perturbation."""
        obs_exact = self.sim.extract_observables(self.sim.Psi_0, simulate_shots=False)
        obs_shot = self.sim.extract_observables(self.sim.Psi_0, simulate_shots=True)
        # Mass difference should be within 3-sigma shot noise bound
        rel_diff = abs(obs_shot['mass'] - obs_exact['mass']) / obs_exact['mass']
        self.assertLess(rel_diff, 0.10)

if __name__ == "__main__":
    unittest.main()
