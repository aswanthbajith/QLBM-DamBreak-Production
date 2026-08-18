#!/usr/bin/env python3
"""
Level 8: End-to-End Quantum Lattice Boltzmann Method (QLBM) Dam-Break Simulation.

Simulates two-phase dam-break fluid collapse using:
1. Carleman state space lifting (Level 5)
2. Block-encoded grand linear system with final-state idling (Level 6)
3. QSVT polynomial inversion solving all time steps simultaneously (Level 7)
4. Quantum observable extraction for wavefront, height, and impact pressure
"""

import numpy as np
import scipy.sparse as sp
import scipy.sparse.linalg as spla
import time

from carleman_lbm import CarlemanTwoPhaseLBM
from block_encoding import QuantumBlockEncoding
from qsvt_solver import QSVTSolver

class DamBreakQLBM:
    def __init__(self, nx=32, ny=16,
                 dam_w=8, dam_h=8,
                 T_sim=16, T_idle=6,
                 rho0=1.0, nu=0.015,
                 gy=-3.0e-4, gx=0.0,
                 tau_phi=0.6,
                 poly_degree=50):
        
        self.nx = nx
        self.ny = ny
        self.N = nx * ny
        self.dam_w = dam_w
        self.dam_h = dam_h
        self.T_sim = T_sim
        self.T_idle = T_idle
        self.T_total = T_sim + T_idle
        self.rho0 = rho0
        self.nu = nu
        self.gx = gx
        self.gy = gy
        self.g_abs = abs(gy)
        self.tau_phi = tau_phi
        self.poly_degree = poly_degree

        print("="*75)
        print(f"Initializing Dam-Break QLBM Simulator: {nx}x{ny} Grid (N={self.N})")
        print(f"Dam Geometry: {dam_w}x{dam_h} Column | Horizon: T_sim={T_sim}, T_idle={T_idle} (Total {self.T_total})")
        print("="*75)

        # 1. Carleman Model (Order N_C = 1)
        self.carleman = CarlemanTwoPhaseLBM(
            nx=nx, ny=ny,
            rho0=rho0, nu=nu,
            gy=gy, gx=gx,
            tau_phi=tau_phi,
            truncation_order=1,
            free_slip_bottom=True
        )

        # 2. Prepare initial dam-break state Psi(0)
        self.phi_init = np.zeros((nx, ny), dtype=np.float64)
        self.phi_init[:dam_w, :dam_h] = 1.0

        self.Psi_0 = np.zeros(self.carleman.dim_base, dtype=np.float64)
        for q in range(9):
            # h field initialized with phase-field distribution
            self.Psi_0[(9 + q) * self.N : (9 + q + 1) * self.N] = self.carleman.w[q] * self.phi_init.flatten()

        self.A_step = self.carleman.build_carleman_one_step_matrix()

        # 3. Forcing vector b_force
        self.b_force = np.zeros(self.carleman.dim_base, dtype=np.float64)
        for q in range(9):
            wi = self.carleman.w[q]
            cy = self.carleman.c[q, 1]
            Fi = (1.0 - 0.5 / self.carleman.tau_v) * wi * (cy * self.phi_init.flatten() * gy / self.carleman.cs2)
            self.b_force[q * self.N : (q + 1) * self.N] = Fi

        # 4. Block Encoding of Grand System
        self.block_enc = QuantumBlockEncoding(
            A_step=self.A_step,
            y_init=self.Psi_0,
            b_force=self.b_force,
            T_sim=self.T_sim,
            T_idle=self.T_idle
        )

        # 5. QSVT Solver
        self.qsvt = QSVTSolver(self.block_enc, poly_degree=poly_degree)

    def run_simulation(self):
        """
        Executes the QLBM simulation via QSVT polynomial matrix inversion.
        Extracts time-trajectory states and observable histories.
        """
        print("\nExecuting Quantum Singular Value Transformation (QSVT) Solver...")
        t0 = time.time()
        Y_qsvt = self.qsvt.solve_qsvt_polynomial()
        elapsed_qsvt = time.time() - t0
        print(f"QSVT Trajectory Inversion Completed in {elapsed_qsvt:.3f} s.")

        # Extract step-by-step physical fields from the quantum trajectory vector
        D_base = self.carleman.dim_base # 18 N
        
        history = {
            'step': [],
            't_star': [],
            'x_star_qlbm': [],
            'h_star_qlbm': [],
            'p_sensor_qlbm': [],
            'phi_fields': []
        }

        sensor_x = self.nx - 2
        sensor_y = 2
        p_hydro = self.rho0 * self.g_abs * self.dam_h

        for t in range(self.T_sim + 1):
            t_star = t * np.sqrt(self.g_abs / self.dam_h)
            state_t = Y_qsvt[t * D_base : (t + 1) * D_base]

            g_arr = state_t[:self.carleman.dim_single].reshape((9, self.N))
            h_arr = state_t[self.carleman.dim_single:].reshape((9, self.N))

            phi_t = np.sum(h_arr, axis=0).reshape((self.nx, self.ny))
            p_t = self.carleman.cs2 * np.sum(g_arr, axis=0).reshape((self.nx, self.ny))

            # Observable 1: Surge Wavefront x*(t*)
            floor_phi = phi_t[:, 1]
            liq_x = np.where(floor_phi > 0.5)[0]
            x_front = float(np.max(liq_x)) if len(liq_x) > 0 else float(self.dam_w)
            x_star = x_front / self.dam_h

            # Observable 2: Column Height Decay h*(t*)
            wall_phi = phi_t[1, :]
            liq_y = np.where(wall_phi > 0.5)[0]
            h_col = float(np.max(liq_y)) if len(liq_y) > 0 else float(self.dam_h)
            h_star = h_col / self.dam_h

            # Observable 3: Wall Sensor Pressure p*(t*)
            p_raw = p_t[sensor_x, sensor_y]
            p_star = p_raw / (p_hydro + 1e-12)

            history['step'].append(t)
            history['t_star'].append(t_star)
            history['x_star_qlbm'].append(x_star)
            history['h_star_qlbm'].append(h_star)
            history['p_sensor_qlbm'].append(p_star)
            history['phi_fields'].append(phi_t)

            print(f"Time Step {t:2d}/{self.T_sim} | t* = {t_star:5.2f} | Wavefront x* = {x_star:5.2f} | Height h* = {h_star:5.2f} | Sensor p* = {p_star:6.3f}")

        return history
