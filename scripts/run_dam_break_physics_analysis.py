#!/usr/bin/env python3
"""
Physical Dam-Break Hydrodynamic Analysis & Interface Tracking Script (Part Q).

Extracts:
1. Liquid Front Position x_front(t)
2. Liquid Center of Mass (x_cm(t), y_cm(t))
3. Maximum Velocity |u_max|(t)
4. Mass & Volume Conservation Time-Series

Generates:
- results/validation/interface_front_vs_time.png
- results/validation/center_of_mass_vs_time.png
- results/validation/dam_break_physical_metrics.json
"""
import os
import sys
import json
import numpy as np
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt

# Add root directory
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from classical.two_phase import run_two_phase_dambreak


def main():
    print("============================================================")
    print("PART Q: PHYSICAL DAM-BREAK HYDRODYNAMICS & FRONT TRACKING")
    print("============================================================")
    
    nx, ny = 16, 8
    timesteps = 15
    
    history = run_two_phase_dambreak(nx=nx, ny=ny, timesteps=timesteps, g_acc=-0.002)
    
    times = []
    x_fronts = []
    x_cms = []
    y_cms = []
    u_maxs = []
    masses = []
    liquid_masses = []
    
    x_coords = np.arange(nx)[None, :]
    y_coords = np.arange(ny)[:, None]
    
    for step_data in history:
        t = step_data["step"]
        phi = step_data["phi"]
        rho = step_data["rho"]
        u = step_data["u"]
        
        # 1. Front position: furthest x where phi >= 0.5
        liquid_mask = (phi >= 0.5)
        if np.any(liquid_mask):
            cols_with_liq = np.where(np.any(liquid_mask, axis=0))[0]
            x_f = float(cols_with_liq[-1])
        else:
            x_f = 0.0
            
        # 2. Center of mass
        total_phi = np.sum(phi)
        if total_phi > 0:
            x_cm = float(np.sum(x_coords * phi) / total_phi)
            y_cm = float(np.sum(y_coords * phi) / total_phi)
        else:
            x_cm, y_cm = 0.0, 0.0
            
        # 3. Max velocity
        vel_mag = np.sqrt(u[0]**2 + u[1]**2)
        u_max = float(np.max(vel_mag))
        
        times.append(t)
        x_fronts.append(x_f)
        x_cms.append(x_cm)
        y_cms.append(y_cm)
        u_maxs.append(u_max)
        masses.append(step_data["total_mass"])
        liquid_masses.append(step_data["total_liquid_mass"])
        
        print(f"t={t:2d} | x_front = {x_f:4.1f} | Center of Mass = ({x_cm:.2f}, {y_cm:.2f}) | |u_max| = {u_max:.4f}")
        
    metrics = {
        "mesh": f"{nx}x{ny}",
        "timesteps": timesteps,
        "times": times,
        "x_front": x_fronts,
        "x_center_of_mass": x_cms,
        "y_center_of_mass": y_cms,
        "max_velocity": u_maxs,
        "total_mass": masses,
        "liquid_mass": liquid_masses
    }
    
    out_dir = os.path.join(os.path.dirname(__file__), "..", "results/validation")
    os.makedirs(out_dir, exist_ok=True)
    
    with open(os.path.join(out_dir, "dam_break_physical_metrics.json"), "w") as f:
        json.dump(metrics, f, indent=2)
        
    # Plot 1: Interface Front vs Time
    fig, ax = plt.subplots(figsize=(8, 5))
    ax.plot(times, x_fronts, "o-", color="darkblue", lw=2, label="Surge Front $x_{\\mathrm{front}}(t)$")
    ax.set_title("Dam-Break Surge Front Advancement vs Time")
    ax.set_xlabel("Lattice Timestep $t$")
    ax.set_ylabel("Front Coordinate $x / \\Delta x$")
    ax.grid(True, alpha=0.3)
    ax.legend()
    plt.tight_layout()
    plt.savefig(os.path.join(out_dir, "interface_front_vs_time.png"), dpi=300)
    plt.close()
    
    # Plot 2: Center of Mass vs Time
    fig, ax = plt.subplots(figsize=(8, 5))
    ax.plot(times, x_cms, "s-", color="crimson", lw=2, label="Horizontal $x_{\\mathrm{cm}}(t)$ (Rightward Surge)")
    ax.plot(times, y_cms, "d-", color="forestgreen", lw=2, label="Vertical $y_{\\mathrm{cm}}(t)$ (Gravitational Slump)")
    ax.set_title("Liquid Column Center of Mass Trajectory")
    ax.set_xlabel("Lattice Timestep $t$")
    ax.set_ylabel("Coordinate Center of Mass")
    ax.grid(True, alpha=0.3)
    ax.legend()
    plt.tight_layout()
    plt.savefig(os.path.join(out_dir, "center_of_mass_vs_time.png"), dpi=300)
    plt.close()
    
    print("============================================================")
    print("Dam-break physics validation saved in results/validation/")
    print("============================================================")


if __name__ == "__main__":
    main()
