#!/usr/bin/env python3
"""
End-to-End Quantum Lattice Boltzmann Method (QLBM) Dam-Break Simulation Engine.

Couples:
1. Classical Two-Phase Reference Solver (TwoPhaseLBM2D)
2. Carleman Linearization Solver (CarlemanTwoPhaseLBM)
3. Quantum QSVT Circuit Solver (QSVTSolver in Qiskit)
4. Quantum Observable Extraction & Finite-Shot Measurement Estimators
"""

import os
import sys
sys.path.append(os.path.join(os.path.dirname(__file__), '../classical'))
sys.path.append(os.path.join(os.path.dirname(__file__), '../quantum'))

import time
import numpy as np
import scipy.linalg as la
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt

from two_phase_lbm import TwoPhaseLBM2D
from carleman_lbm import CarlemanTwoPhaseLBM
from qsvt_solver import QSVTSolver

class QLBMDamBreakSimulation:
    def __init__(self, nx=8, ny=4, dam_w=3, dam_h=3,
                 total_steps=12, rho_L=1.0, rho_G=0.1,
                 nu_L=0.01, nu_G=0.01, gy=-2.0e-4,
                 truncation_order=2, qsvt_degree=15,
                 n_shots=10000):
        
        self.nx = nx
        self.ny = ny
        self.N = nx * ny
        self.dam_w = dam_w
        self.dam_h = dam_h
        self.total_steps = total_steps
        self.rho_L = rho_L
        self.rho_G = rho_G
        self.nu_L = nu_L
        self.nu_G = nu_G
        self.gy = gy
        self.truncation_order = truncation_order
        self.qsvt_degree = qsvt_degree
        self.n_shots = n_shots

        # 1. Classical Reference Solver
        self.classical_sim = TwoPhaseLBM2D(
            nx=nx, ny=ny,
            rho_L=rho_L, rho_G=rho_G,
            nu_L=nu_L, nu_G=nu_G,
            sigma=0.0, gx=0.0, gy=gy,
            width=3.0, mobility=0.05,
            free_slip_bottom=True
        )
        self.classical_sim.initialize_dam(dam_w=dam_w, dam_h=dam_h)

        # 2. Carleman Model (Linearized State Space)
        self.carleman = CarlemanTwoPhaseLBM(
            nx=nx, ny=ny,
            rho0=rho_L, nu=nu_L,
            gy=gy, gx=0.0,
            truncation_order=truncation_order,
            free_slip_bottom=True
        )

        # Base and Carleman Dimensions
        self.dim_base = 18 * self.N
        self.dim_carleman = self.carleman.dim_carleman
        self.n_qubits = int(np.ceil(np.log2(self.dim_carleman))) + 1 # +1 ancilla

        # Initial State Preparation
        self.Psi_0 = self._prepare_initial_state()
        self.Y_0 = self.carleman.lift_state(self.Psi_0)
        self.norm_Y0 = float(la.norm(self.Y_0))
        self.state_prep_depth = int(2**np.ceil(np.log2(self.dim_carleman)))

    def _prepare_initial_state(self):
        """Initializes the physical dam-break state vector Psi(0) in R^(18 N)."""
        Psi = np.zeros(self.dim_base, dtype=np.float64)
        for q in range(9):
            Psi[q * self.N : (q + 1) * self.N] = self.classical_sim.g[q].flatten()
            Psi[(9 + q) * self.N : (9 + q + 1) * self.N] = self.classical_sim.phase_field.h[q].flatten()
        return Psi

    def extract_observables(self, Psi_vec, norm_scale=1.0, simulate_shots=False):
        """
        Extracts macroscopic fluid engineering observables from physical state vector.
        """
        Psi_scaled = Psi_vec * norm_scale
        g_mat = Psi_scaled[:9 * self.N].reshape((9, self.nx, self.ny))
        h_mat = Psi_scaled[9 * self.N : 18 * self.N].reshape((9, self.nx, self.ny))

        phi = np.sum(h_mat, axis=0)

        # Apply finite-shot sampling noise if requested
        if simulate_shots and self.n_shots > 0:
            shot_noise = np.random.normal(0.0, 1.0 / np.sqrt(self.n_shots), size=phi.shape)
            phi = phi + shot_noise

        phi_clamped = np.clip(phi, 0.0, 1.0)

        # 1. Surge Front Position x_star
        floor_phi = phi_clamped[:, min(1, self.ny - 1)]
        liq_idx = np.where(floor_phi > 0.5)[0]
        x_front = float(np.max(liq_idx)) if len(liq_idx) > 0 else float(self.dam_w)
        x_star = x_front / self.dam_h

        # 2. Residual Column Height h_star
        wall_phi = phi_clamped[min(1, self.nx - 1), :]
        col_idx = np.where(wall_phi > 0.5)[0]
        h_col = float(np.max(col_idx)) if len(col_idx) > 0 else float(self.dam_h)
        h_star = h_col / self.dam_h

        # 3. Total Fluid Mass
        total_mass = float(np.sum(phi_clamped))

        # 4. Downstream Wall Pressure (at sensor node x=nx-2, y=1)
        sensor_x = max(0, self.nx - 2)
        sensor_y = min(1, self.ny - 1)
        p_sensor = float(self.rho_L * (1.0 / 3.0) * np.sum(g_mat[:, sensor_x, sensor_y]))

        return {
            'phi': phi_clamped,
            'x_star': x_star,
            'h_star': h_star,
            'mass': total_mass,
            'p_sensor': p_sensor
        }

    def run_end_to_end(self):
        """Runs the complete Classical vs Carleman vs Quantum simulation."""
        print("="*85)
        print(f"STARTING END-TO-END QLBM DAM-BREAK SIMULATION")
        print(f"Domain: {self.nx}x{self.ny} ({self.N} nodes) | Dam: {self.dam_w}x{self.dam_h} | Steps: {self.total_steps}")
        print(f"Carleman Order: N_C={self.truncation_order} | Carleman Dim: {self.dim_carleman} | Qubits: {self.n_qubits}")
        print(f"QSVT Polynomial Degree: {self.qsvt_degree} | Finite Shots: {self.n_shots:,}")
        print("="*85)

        # State histories
        hist_t = []
        hist_class_x = []; hist_class_h = []; hist_class_p = []; hist_class_m = []
        hist_carle_x = []; hist_carle_h = []; hist_carle_p = []; hist_carle_m = []
        hist_quant_x = []; hist_quant_h = []; hist_quant_p = []; hist_quant_m = []
        hist_quant_shot_x = []; hist_quant_shot_h = []
        hist_fidelity = []
        hist_qsvt_res = []

        # Current state vectors
        Psi_c = self.Psi_0.copy()
        Y_carle = self.Y_0.copy()
        Y_quant = self.Y_0.copy()

        # Pre-instantiate QSVT Solver Operator M = I + 0.01 * A
        A_dense = self.carleman.A_C.toarray()
        M_step = np.eye(self.dim_carleman, dtype=np.complex128) + 0.01 * A_dense
        qsvt_solver = QSVTSolver(M_step, Y_quant, degree=self.qsvt_degree)

        # Record initial observables (t=0)
        obs_c = self.extract_observables(Psi_c)
        obs_carle = self.extract_observables(self.carleman.project_state(Y_carle))
        obs_q = self.extract_observables(self.carleman.project_state(Y_quant))
        obs_q_shot = self.extract_observables(self.carleman.project_state(Y_quant), simulate_shots=True)

        hist_t.append(0.0)
        hist_class_x.append(obs_c['x_star']); hist_class_h.append(obs_c['h_star']); hist_class_p.append(obs_c['p_sensor']); hist_class_m.append(obs_c['mass'])
        hist_carle_x.append(obs_carle['x_star']); hist_carle_h.append(obs_carle['h_star']); hist_carle_p.append(obs_carle['p_sensor']); hist_carle_m.append(obs_carle['mass'])
        hist_quant_x.append(obs_q['x_star']); hist_quant_h.append(obs_q['h_star']); hist_quant_p.append(obs_q['p_sensor']); hist_quant_m.append(obs_q['mass'])
        hist_quant_shot_x.append(obs_q_shot['x_star']); hist_quant_shot_h.append(obs_q_shot['h_star'])
        hist_fidelity.append(1.0)
        hist_qsvt_res.append(0.0)

        t_start = time.time()

        for step in range(1, self.total_steps + 1):
            t_star = step * np.sqrt(abs(self.gy) / self.dam_h)

            # 1. Classical Step
            self.classical_sim.step()
            Psi_c = np.zeros(self.dim_base, dtype=np.float64)
            for q in range(9):
                Psi_c[q * self.N : (q + 1) * self.N] = self.classical_sim.g[q].flatten()
                Psi_c[(9 + q) * self.N : (9 + q + 1) * self.N] = self.classical_sim.phase_field.h[q].flatten()

            # 2. Carleman Classical Step: Y(t+1) = A_C * Y(t)
            Y_carle = self.carleman.step(Y_carle)

            # 3. Quantum QSVT Solver Step
            rhs_step = Y_quant + 0.01 * (A_dense @ Y_quant)
            res_qsvt = qsvt_solver.solve_vector(rhs_step)
            Y_quant = np.real(res_qsvt['x_quantum'])

            # Fidelity between Quantum State and Carleman State
            fid = float(np.abs(np.vdot(Y_quant / la.norm(Y_quant), Y_carle / la.norm(Y_carle)))**2)

            # Extract Observables
            obs_c = self.extract_observables(Psi_c)
            obs_carle = self.extract_observables(self.carleman.project_state(Y_carle))
            obs_q = self.extract_observables(self.carleman.project_state(Y_quant))
            obs_q_shot = self.extract_observables(self.carleman.project_state(Y_quant), simulate_shots=True)

            hist_t.append(t_star)
            hist_class_x.append(obs_c['x_star']); hist_class_h.append(obs_c['h_star']); hist_class_p.append(obs_c['p_sensor']); hist_class_m.append(obs_c['mass'])
            hist_carle_x.append(obs_carle['x_star']); hist_carle_h.append(obs_carle['h_star']); hist_carle_p.append(obs_carle['p_sensor']); hist_carle_m.append(obs_carle['mass'])
            hist_quant_x.append(obs_q['x_star']); hist_quant_h.append(obs_q['h_star']); hist_quant_p.append(obs_q['p_sensor']); hist_quant_m.append(obs_q['mass'])
            hist_quant_shot_x.append(obs_q_shot['x_star']); hist_quant_shot_h.append(obs_q_shot['h_star'])
            hist_fidelity.append(fid)
            hist_qsvt_res.append(res_qsvt['residual'])


            print(f"Step {step:2d}/{self.total_steps} | t* = {t_star:4.2f} | Class x* = {obs_c['x_star']:4.2f} | Quant x* = {obs_q['x_star']:4.2f} | Fidelity = {fid:.6f} | QSVT Res = {res_qsvt['residual']:.2e}")

        total_runtime = time.time() - t_start

        return {
            'time': np.array(hist_t),
            'classical': {'x_star': np.array(hist_class_x), 'h_star': np.array(hist_class_h), 'p_sensor': np.array(hist_class_p), 'mass': np.array(hist_class_m)},
            'carleman': {'x_star': np.array(hist_carle_x), 'h_star': np.array(hist_carle_h), 'p_sensor': np.array(hist_carle_p), 'mass': np.array(hist_carle_m)},
            'quantum': {'x_star': np.array(hist_quant_x), 'h_star': np.array(hist_quant_h), 'p_sensor': np.array(hist_quant_p), 'mass': np.array(hist_quant_m)},
            'quantum_shots': {'x_star': np.array(hist_quant_shot_x), 'h_star': np.array(hist_quant_shot_h)},
            'fidelity': np.array(hist_fidelity),
            'qsvt_residual': np.array(hist_qsvt_res),
            'runtime': total_runtime,
            'final_phi_classical': obs_c['phi'],
            'final_phi_quantum': obs_q['phi']
        }
