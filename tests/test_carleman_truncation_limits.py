#!/usr/bin/env python3
"""
Test Carleman Multi-Step Truncation Limits & Stability.

Evaluates Carleman Order 2 truncation error across time horizons t in [1, 200]
against the nonlinear reference surrogate.
"""

import sys, os
sys.path.append(os.path.join(os.path.dirname(__file__), "../classical"))
sys.path.append(os.path.join(os.path.dirname(__file__), "../quantum"))

import pytest
import numpy as np
import scipy.linalg as la
from two_phase_lbm import TwoPhaseLBM2D
from carleman_lbm import CarlemanTwoPhaseLBM

class TestCarlemanTruncationLimits:
    @classmethod
    def setup_class(cls):
        cls.nx = 4
        cls.ny = 2
        cls.N = cls.nx * cls.ny
        cls.dam_w = 2
        cls.dam_h = 2
        cls.horizons = [1, 5, 10, 20, 50, 100, 200]
        
        # Initialize classical reference
        cls.sim_c = TwoPhaseLBM2D(
            nx=cls.nx, ny=cls.ny,
            rho_L=1.0, rho_G=0.1,
            nu_L=0.01, nu_G=0.01,
            gy=-2e-4, free_slip_bottom=True
        )
        cls.sim_c.initialize_dam(dam_w=cls.dam_w, dam_h=cls.dam_h)

        # Initialize Carleman model
        cls.carle = CarlemanTwoPhaseLBM(
            nx=cls.nx, ny=cls.ny,
            rho0=1.0, nu=0.01,
            gy=-2e-4, truncation_order=2,
            free_slip_bottom=True
        )

        cls.Psi_0 = np.zeros(18 * cls.N, dtype=np.float64)
        for q in range(9):
            cls.Psi_0[q * cls.N : (q + 1) * cls.N] = cls.sim_c.g[q].flatten()
            cls.Psi_0[(9 + q) * cls.N : (9 + q + 1) * cls.N] = cls.sim_c.phase_field.h[q].flatten()

        cls.Y_0 = cls.carle.lift_state(cls.Psi_0)

    def test_01_multistep_stability_and_bounds(self):
        """Tests that Carleman truncation error remains stably bounded over 200 steps."""
        sim = TwoPhaseLBM2D(
            nx=self.nx, ny=self.ny,
            rho_L=1.0, rho_G=0.1,
            nu_L=0.01, nu_G=0.01,
            gy=-2e-4, free_slip_bottom=True
        )
        sim.initialize_dam(dam_w=self.dam_w, dam_h=self.dam_h)

        Y = self.Y_0.copy()

        for step in range(1, 201):
            sim.step()
            Y = self.carle.step(Y)

            if step in self.horizons:
                # Reconstruct classical state
                Psi_c = np.zeros(18 * self.N, dtype=np.float64)
                for q in range(9):
                    Psi_c[q * self.N : (q + 1) * self.N] = sim.g[q].flatten()
                    Psi_c[(9 + q) * self.N : (9 + q + 1) * self.N] = sim.phase_field.h[q].flatten()

                Psi_k = self.carle.project_state(Y)

                # 1. Relative L2 Error
                rel_l2 = float(la.norm(Psi_k - Psi_c) / (la.norm(Psi_c) + 1e-15))
                assert rel_l2 < 0.05, f"Step {step}: L2 relative error {rel_l2:.4e} exceeds 5% bound"

                # 2. Invariant manifold defect
                psi_mat = Psi_k.reshape((18, self.N))
                ideal_quad = np.einsum("in,jn->ijn", psi_mat, psi_mat).reshape((324 * self.N,))
                actual_quad = Y[18 * self.N:]
                defect = float(la.norm(actual_quad - ideal_quad) / (la.norm(ideal_quad) + 1e-15))
                assert defect < 0.20, f"Step {step}: Manifold defect {defect:.4e} exceeds 20% bound"

                # 3. Mass Conservation Error
                h_k = Psi_k[9 * self.N : 18 * self.N].reshape((9, self.nx, self.ny))
                phi_k = np.sum(h_k, axis=0)
                mass_k = np.sum(np.clip(phi_k, 0, 1))

                h_c = Psi_c[9 * self.N : 18 * self.N].reshape((9, self.nx, self.ny))
                phi_c = np.sum(h_c, axis=0)
                mass_c = np.sum(np.clip(phi_c, 0, 1))

                rel_mass_err = float(abs(mass_k - mass_c) / (mass_c + 1e-15))
                assert rel_mass_err < 0.01, f"Step {step}: Relative mass error {rel_mass_err:.4e} exceeds 1% bound"
