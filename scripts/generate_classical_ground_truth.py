#!/usr/bin/env python3
"""
Generates the immutable classical ground truth reference dataset:
validation/sim_data/classical_ground_truth.csv and checkpoint spatial fields.
"""

import os
import sys
sys.path.append(os.path.join(os.path.dirname(__file__), '../classical'))

import time
import numpy as np
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt

from two_phase_lbm import TwoPhaseLBM2D

def generate_ground_truth():
    out_dir = "/home/aswa/Research/QLBM-DamBreak/validation/sim_data"
    check_dir = f"{out_dir}/checkpoints"
    os.makedirs(out_dir, exist_ok=True)
    os.makedirs(check_dir, exist_ok=True)

    nx, ny = 300, 100
    dam_w, dam_h = 45, 45
    total_steps = 2200
    rho_L, rho_G = 1.0, 0.1
    nu_L, nu_G = 0.005, 0.01
    sigma = 0.001
    gy = -4.0e-4
    g_abs = abs(gy)
    p_hydrostatic = rho_L * g_abs * dam_h

    print("="*80)
    print("GENERATING IMMUTABLE CLASSICAL GROUND TRUTH DATASET")
    print(f"Domain: {nx}x{ny} | Dam: {dam_w}x{dam_h} | Steps: {total_steps}")
    print("="*80)

    sim = TwoPhaseLBM2D(
        nx=nx, ny=ny,
        rho_L=rho_L, rho_G=rho_G,
        nu_L=nu_L, nu_G=nu_G,
        sigma=sigma, gx=0.0, gy=gy,
        width=3.5, mobility=0.05,
        enable_surface_tension=True,
        free_slip_bottom=True
    )
    sim.initialize_dam(dam_w=dam_w, dam_h=dam_h)

    sensor_x = nx - 2
    sensor_y = 5

    initial_mass = float(np.sum(sim.phi))
    records = []

    t0 = time.time()

    for step in range(total_steps + 1):
        t_star = step * np.sqrt(g_abs / dam_h)
        x_front = sim.get_wavefront_x(threshold=0.5)
        h_col = sim.get_column_height(threshold=0.5)
        x_star = x_front / dam_h
        h_star = h_col / dam_h

        p_raw = sim.get_sensor_pressure(sensor_x, sensor_y)
        p_star = p_raw / (p_hydrostatic + 1e-12)

        cur_mass = float(np.sum(sim.phi))
        mass_err = abs(cur_mass - initial_mass) / initial_mass
        phase_vol = cur_mass

        u_mag = np.sqrt(sim.u**2 + sim.v**2)
        u_max = float(np.max(u_mag))

        rho_min = float(np.min(sim.rho))
        rho_max = float(np.max(sim.rho))
        rho_mean = float(np.mean(sim.rho))

        phi_mean = float(np.mean(sim.phi))
        interface_cells = int(np.sum((sim.phi > 0.05) & (sim.phi < 0.95)))

        rec = {
            'timestep': step,
            'physical_time': float(step),
            't_star': t_star,
            'mass': cur_mass,
            'mass_drift': mass_err,
            'phase_volume': phase_vol,
            'front_position_x': x_front,
            'front_position_x_star': x_star,
            'column_height_y': h_col,
            'column_height_h_star': h_star,
            'wall_pressure_raw': p_raw,
            'wall_pressure_star': p_star,
            'max_velocity': u_max,
            'rho_min': rho_min,
            'rho_max': rho_max,
            'rho_mean': rho_mean,
            'phi_mean': phi_mean,
            'interface_cells': interface_cells
        }
        records.append(rec)

        if step % 200 == 0 or step == total_steps:
            elapsed = time.time() - t0
            print(f"Step {step:5d}/{total_steps} | t* = {t_star:5.2f} | x* = {x_star:5.2f} | h* = {h_star:5.2f} | p* = {p_star:6.3f} | Mass Err = {mass_err:.2e} | U_max = {u_max:6.4f} | Time: {elapsed:.1f}s")
            # Save checkpoint
            np.savez_compressed(
                f"{check_dir}/checkpoint_step_{step:05d}.npz",
                step=step, t_star=t_star, phi=sim.phi, u=sim.u, v=sim.v, p=sim.p, rho=sim.rho
            )

        sim.step()

    # Write classical_ground_truth.csv
    csv_path = f"{out_dir}/classical_ground_truth.csv"
    headers = list(records[0].keys())
    with open(csv_path, "w") as f:
        f.write(",".join(headers) + "\n")
        for r in records:
            f.write(",".join([f"{r[k]:.8e}" if isinstance(r[k], float) else str(r[k]) for k in headers]) + "\n")

    print(f"\nGround truth saved to: {csv_path}")
    print(f"Checkpoints saved to: {check_dir}")

if __name__ == "__main__":
    generate_ground_truth()
