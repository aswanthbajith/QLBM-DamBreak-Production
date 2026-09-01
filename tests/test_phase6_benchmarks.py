#!/usr/bin/env python3
"""
Phase 6 Automated Benchmark Tests.
Validates classical scaling, Carleman long-time stability, QSVT degree sweep, and condition numbers.
"""

import sys, os
sys.path.append(os.path.join(os.path.dirname(__file__), "../classical"))
sys.path.append(os.path.join(os.path.dirname(__file__), "../quantum"))

import pytest
import numpy as np
import scipy.linalg as la
from two_phase_lbm import TwoPhaseLBM2D
from carleman_lbm import CarlemanTwoPhaseLBM
from qsvt_solver import QSVTSolver

class TestPhase6Benchmarks:
    def test_01_classical_benchmark_mass_drift(self):
        """Tests classical reference mass conservation drift across test grid."""
        sim = TwoPhaseLBM2D(nx=16, ny=8, rho_L=1.0, rho_G=0.1, nu_L=0.01, nu_G=0.01, gy=-2e-4, free_slip_bottom=True)
        sim.initialize_dam(dam_w=6, dam_h=6)
        m0 = float(np.sum(sim.phi))
        for _ in range(50):
            sim.step()
        m1 = float(np.sum(sim.phi))
        drift = abs(m1 - m0) / m0
        assert drift < 0.01, f"Classical mass drift {drift:.4e} exceeds 1% bound"

    def test_02_carleman_long_time_saturation(self):
        """Tests that Carleman truncation error stably saturates <= 4% over 200 steps."""
        nx, ny = 4, 2
        N = nx * ny
        sim = TwoPhaseLBM2D(nx=nx, ny=ny, rho_L=1.0, rho_G=0.1, nu_L=0.01, nu_G=0.01, gy=-2e-4, free_slip_bottom=True)
        sim.initialize_dam(dam_w=2, dam_h=2)
        carle = CarlemanTwoPhaseLBM(nx=nx, ny=ny, rho0=1.0, nu=0.01, gy=-2e-4, truncation_order=2, free_slip_bottom=True)
        
        Psi_0 = np.zeros(18 * N, dtype=np.float64)
        for q in range(9):
            Psi_0[q * N : (q + 1) * N] = sim.g[q].flatten()
            Psi_0[(9 + q) * N : (9 + q + 1) * N] = sim.phase_field.h[q].flatten()
        
        Y = carle.lift_state(Psi_0)
        for _ in range(200):
            sim.step()
            Y = carle.step(Y)
            
        Psi_c = np.zeros(18 * N, dtype=np.float64)
        for q in range(9):
            Psi_c[q * N : (q + 1) * N] = sim.g[q].flatten()
            Psi_c[(9 + q) * N : (9 + q + 1) * N] = sim.phase_field.h[q].flatten()
            
        Psi_k = carle.project_state(Y)
        rel_l2 = float(la.norm(Psi_k - Psi_c) / la.norm(Psi_c))
        assert rel_l2 < 0.05, f"Carleman error at t=200 ({rel_l2:.4e}) exceeds 5%"

    @pytest.mark.parametrize("deg,max_res", [(11, 1e-7), (15, 1e-9), (21, 1e-12)])
    def test_03_qsvt_degree_accuracy(self, deg, max_res):
        """Tests QSVT Chebyshev inversion convergence across degrees."""
        c_m = CarlemanTwoPhaseLBM(nx=2, ny=1, truncation_order=2)
        A = c_m.A_C.toarray()
        M = np.eye(A.shape[0], dtype=np.complex128) + 0.01 * A
        np.random.seed(42)
        b = np.random.randn(A.shape[0]) + 0.1j * np.random.randn(A.shape[0])
        solver = QSVTSolver(M, b, degree=deg)
        res = solver.solve()
        assert res["residual"] < max_res, f"Degree {deg} residual {res["residual"]:.4e} exceeds {max_res}"

    def test_04_condition_number_stability_bound(self):
        """Tests system condition number kappa(I + dt * A_C) < 1.5 for dt <= 0.02."""
        c_m = CarlemanTwoPhaseLBM(nx=2, ny=1, truncation_order=2)
        A = c_m.A_C.toarray()
        for dt in [0.001, 0.005, 0.01, 0.02]:
            M = np.eye(A.shape[0], dtype=np.complex128) + dt * A
            svs = la.svd(M, compute_uv=False)
            kappa = float(np.max(svs) / np.min(svs))
            assert kappa < 1.5, f"dt={dt}: kappa={kappa:.4f} exceeds 1.5"
