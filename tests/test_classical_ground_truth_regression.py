#!/usr/bin/env python3
"""
Deterministic Regression Test comparing against the locked classical ground truth.
"""

import sys
import os
sys.path.append(os.path.join(os.path.dirname(__file__), '../classical'))

import unittest
import numpy as np
from two_phase_lbm import TwoPhaseLBM2D

class TestClassicalGroundTruthRegression(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.csv_path = "/home/aswa/Research/QLBM-DamBreak/validation/sim_data/classical_ground_truth.csv"
        cls.check_dir = "/home/aswa/Research/QLBM-DamBreak/validation/sim_data/checkpoints"
        cls.has_ground_truth = os.path.exists(cls.csv_path)

    def test_01_ground_truth_file_exists_and_valid(self):
        """Verify ground truth dataset exists and has all 2201 timesteps."""
        self.assertTrue(self.has_ground_truth, "Ground truth CSV missing")
        data = np.genfromtxt(self.csv_path, delimiter=',', names=True)
        self.assertEqual(len(data), 2201)
        self.assertAlmostEqual(data['timestep'][0], 0.0)
        self.assertAlmostEqual(data['timestep'][-1], 2200.0)

    def test_02_deterministic_regression_50_steps(self):
        """Verify deterministic bitwise-compatible execution over first 50 steps."""
        sim = TwoPhaseLBM2D(
            nx=300, ny=100,
            rho_L=1.0, rho_G=0.1,
            nu_L=0.005, nu_G=0.01,
            sigma=0.001, gy=-4.0e-4,
            width=3.5, mobility=0.05,
            enable_surface_tension=True,
            free_slip_bottom=True
        )
        sim.initialize_dam(dam_w=45, dam_h=45)
        for _ in range(50):
            sim.step()

        # Load reference at step 50
        data = np.genfromtxt(self.csv_path, delimiter=',', names=True)
        ref_mass = data['mass'][50]
        ref_x = data['front_position_x_star'][50]
        ref_h = data['column_height_h_star'][50]

        cur_mass = np.sum(sim.phi)
        cur_x = sim.get_wavefront_x(0.5) / 45.0
        cur_h = sim.get_column_height(0.5) / 45.0

        np.testing.assert_allclose(cur_mass, ref_mass, rtol=1e-5, err_msg="Mass drifted from ground truth")
        np.testing.assert_allclose(cur_x, ref_x, rtol=1e-4, err_msg="Front position shifted from ground truth")
        np.testing.assert_allclose(cur_h, ref_h, rtol=1e-4, err_msg="Column height shifted from ground truth")

    def test_03_checkpoint_fields_reproducibility(self):
        """Verify checkpoint spatial fields at step 0 match analytical initialization."""
        cp0_path = f"{self.check_dir}/checkpoint_step_00000.npz"
        self.assertTrue(os.path.exists(cp0_path))
        cp0 = np.load(cp0_path)
        self.assertEqual(cp0['phi'].shape, (300, 100))
        self.assertAlmostEqual(float(np.min(cp0['phi'])), 0.0, places=3)
        self.assertAlmostEqual(float(np.max(cp0['phi'])), 1.0, places=3)

if __name__ == "__main__":
    unittest.main()
