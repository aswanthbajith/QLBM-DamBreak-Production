#!/usr/bin/env python3
"""
Production Two-Phase Dam-Break 2D Simulation Driver with Diagnostics.
"""

import os
import time
import numpy as np
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
from two_phase_lbm import TwoPhaseLBM2D

def run_dam_break_simulation(nx=300, ny=100,
                             dam_w=45, dam_h=45,
                             total_steps=2200,
                             save_interval=200,
                             rho_L=1.0, rho_G=0.1,
                             nu_L=0.005, nu_G=0.01,
                             sigma=0.001, gy=-4.0e-4,
                             output_dir="validation/sim_data"):
    
    os.makedirs(output_dir, exist_ok=True)
    os.makedirs(f"{output_dir}/frames", exist_ok=True)

    print("="*75)
    print(f"Two-Phase Gas-Liquid LBM Dam-Break Simulation: {nx}x{ny} Grid")
    print(f"Dam Geometry: {dam_w}x{dam_h} Column (Aspect Ratio: {dam_w/dam_h:.2f})")
    print(f"Density Ratio: rho_L/rho_G = {rho_L/rho_G:.1f} | Viscosity: nu_L = {nu_L}")
    print("="*75)

    g_abs = abs(gy)

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

    # Downstream sensor location on right wall
    sensor_x = nx - 2
    sensor_y = 5

    history = {
        'step': [],
        't_star': [],
        'x_star': [],
        'h_star': [],
        'p_impact_star': [],
        'mass_error': []
    }

    initial_mass = np.sum(sim.phi)
    p_hydrostatic = rho_L * g_abs * dam_h

    t0 = time.time()

    for step in range(total_steps + 1):
        t_star = step * np.sqrt(g_abs / dam_h)
        x_front = sim.get_wavefront_x(threshold=0.5)
        h_col = sim.get_column_height(threshold=0.5)

        x_star = x_front / dam_h
        h_star = h_col / dam_h

        p_raw = sim.get_sensor_pressure(sensor_x, sensor_y)
        p_star = p_raw / (p_hydrostatic + 1e-12)

        current_mass = np.sum(sim.phi)
        mass_err = abs(current_mass - initial_mass) / initial_mass

        history['step'].append(step)
        history['t_star'].append(t_star)
        history['x_star'].append(x_star)
        history['h_star'].append(h_star)
        history['p_impact_star'].append(p_star)
        history['mass_error'].append(mass_err)

        if step % 200 == 0 or step == total_steps:
            elapsed = time.time() - t0
            print(f"Step {step:5d}/{total_steps} | t* = {t_star:5.2f} | x* = {x_star:5.2f} | h* = {h_star:5.2f} | p* = {p_star:6.3f} | Mass Err = {mass_err:.2e} | Elapsed: {elapsed:.1f}s")

        if step % save_interval == 0 or step == total_steps:
            fig, ax = plt.subplots(figsize=(9, 3.8))
            im = ax.imshow(sim.phi.T, origin='lower', cmap='Blues', vmin=0.0, vmax=1.0, extent=[0, nx, 0, ny])
            ax.contour(sim.phi.T, levels=[0.5], colors='crimson', linewidths=1.8, extent=[0, nx, 0, ny])
            ax.scatter([sensor_x], [sensor_y], color='darkred', marker='x', s=80, label='Sensor P1 (Impact)')
            ax.set_title(rf"Two-Phase Dam-Break: $t^* = {t_star:.2f}$ (Step {step})", fontsize=11, fontweight='bold')
            ax.set_xlabel("Lattice X")
            ax.set_ylabel("Lattice Y")
            ax.legend(loc='upper right')
            cbar = plt.colorbar(im, ax=ax)
            cbar.set_label(r"Liquid Phase Fraction $\phi$", fontsize=10)
            plt.tight_layout()
            plt.savefig(f"{output_dir}/frames/dam_break_step_{step:05d}.png", dpi=120)
            plt.close()

        sim.step()

    # Save output diagnostics
    np.savez(f"{output_dir}/dam_break_diagnostics.npz", **history)
    with open(f"{output_dir}/dam_break_diagnostics.csv", "w") as f:
        f.write("step,t_star,x_star,h_star,p_impact_star,mass_error\n")
        for i in range(len(history['step'])):
            f.write(f"{history['step'][i]},{history['t_star'][i]:.6f},{history['x_star'][i]:.6f},{history['h_star'][i]:.6f},{history['p_impact_star'][i]:.6f},{history['mass_error'][i]:.6e}\n")

    print(f"\nSimulation successfully finished. Output saved in '{output_dir}'.")
    return history

if __name__ == "__main__":
    run_dam_break_simulation()
