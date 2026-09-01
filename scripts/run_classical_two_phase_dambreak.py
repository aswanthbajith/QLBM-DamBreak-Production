#!/usr/bin/env python3
"""
Classical Reference Benchmark Runner for Reduced Two-Phase Dam-Break Hydrodynamics.

Executes classical dam-break simulation, tracks physical observables,
calculates conservation metrics, and outputs artifacts in results/classical_two_phase/.
"""
import argparse
import os
import sys
import json
import numpy as np
import scipy.linalg as la
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt

# Add root directory
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from classical.two_phase import (
    initialize_two_phase_dambreak,
    step_two_phase,
    run_two_phase_dambreak,
    compute_density,
    compute_velocity,
    compute_phase_field
)


def parse_args():
    parser = argparse.ArgumentParser(description="Run Classical Two-Phase Dam-Break Benchmark")
    parser.add_argument("--nx", type=int, default=4, help="Grid nodes in X (default: 4)")
    parser.add_argument("--ny", type=int, default=4, help="Grid nodes in Y (default: 4)")
    parser.add_argument("--timesteps", type=int, default=10, help="Number of timesteps (default: 10)")
    parser.add_argument("--tau_f", type=float, default=0.8, help="Fluid relaxation time (default: 0.8)")
    parser.add_argument("--tau_g", type=float, default=0.7, help="Phase relaxation time (default: 0.7)")
    parser.add_argument("--g_acc", type=float, default=-0.001, help="Downward gravity acceleration (default: -0.001)")
    return parser.parse_args()


def compute_center_of_mass(phi):
    """Calculates spatial center of mass for the liquid phase (phi)."""
    ny, nx = phi.shape
    total_liq = np.sum(phi)
    if total_liq <= 1e-14:
        return 0.0, 0.0
    x_indices, y_indices = np.meshgrid(np.arange(nx), np.arange(ny))
    x_com = float(np.sum(x_indices * phi) / total_liq)
    y_com = float(np.sum(y_indices * phi) / total_liq)
    return x_com, y_com


def main():
    args = parse_args()
    print("============================================================")
    print("STARTING CLASSICAL TWO-PHASE DAM-BREAK BENCHMARK")
    print(f"Mesh: {args.nx} x {args.ny}")
    print(f"Timesteps: {args.timesteps}")
    print(f"tau_f: {args.tau_f}, tau_g: {args.tau_g}, g_acc: {args.g_acc}")
    print("============================================================")

    # 1. Run simulation
    history = run_two_phase_dambreak(
        nx=args.nx, ny=args.ny, timesteps=args.timesteps,
        tau_f=args.tau_f, tau_g=args.tau_g, g_acc=args.g_acc
    )

    initial_mass = history[0]["total_mass"]
    initial_liq = history[0]["total_liquid_mass"]

    time_series = []
    for step_data in history:
        t = step_data["step"]
        phi = step_data["phi"]
        rho = step_data["rho"]
        u = step_data["u"]

        x_com, y_com = compute_center_of_mass(phi)
        max_u = float(np.max(np.sqrt(u[0]**2 + u[1]**2)))
        mass_drift = float(abs(step_data["total_mass"] - initial_mass) / (initial_mass + 1e-14))
        liq_drift = float(abs(step_data["total_liquid_mass"] - initial_liq) / (initial_liq + 1e-14))

        metrics = {
            "step": t,
            "total_mass": step_data["total_mass"],
            "total_liquid_mass": step_data["total_liquid_mass"],
            "mass_drift": mass_drift,
            "liquid_drift": liq_drift,
            "min_phi": float(np.min(phi)),
            "max_phi": float(np.max(phi)),
            "min_rho": float(np.min(rho)),
            "max_rho": float(np.max(rho)),
            "max_velocity": max_u,
            "center_of_mass_x": x_com,
            "center_of_mass_y": y_com
        }
        time_series.append(metrics)

    final_metrics = time_series[-1]
    print(f"Final Step {args.timesteps}:")
    print(f"  Total Mass:        {final_metrics['total_mass']:.6f} (drift: {final_metrics['mass_drift']*100:.4f}%)")
    print(f"  Liquid Volume:     {final_metrics['total_liquid_mass']:.6f} (drift: {final_metrics['liquid_drift']*100:.4f}%)")
    print(f"  Phase Bounds:      [{final_metrics['min_phi']:.4f}, {final_metrics['max_phi']:.4f}]")
    print(f"  Density Bounds:    [{final_metrics['min_rho']:.4f}, {final_metrics['max_rho']:.4f}]")
    print(f"  Max Velocity:      {final_metrics['max_velocity']:.6f}")
    print(f"  Center of Mass:    ({final_metrics['center_of_mass_x']:.4f}, {final_metrics['center_of_mass_y']:.4f})")

    # 2. Save results
    out_dir = os.path.join(os.path.dirname(__file__), "..", "results/classical_two_phase")
    os.makedirs(out_dir, exist_ok=True)

    # Save arrays
    final_step = history[-1]
    np.savez(
        os.path.join(out_dir, "classical_fields.npz"),
        rho_initial=history[0]["rho"],
        phi_initial=history[0]["phi"],
        u_initial=history[0]["u"],
        rho_final=final_step["rho"],
        phi_final=final_step["phi"],
        u_final=final_step["u"]
    )

    # Save config and metrics JSON
    config = {
        "nx": args.nx,
        "ny": args.ny,
        "timesteps": args.timesteps,
        "tau_f": args.tau_f,
        "tau_g": args.tau_g,
        "g_acc": args.g_acc,
        "rho_liquid": 1.0,
        "rho_gas": 0.1
    }
    with open(os.path.join(out_dir, "configuration.json"), "w") as f:
        json.dump(config, f, indent=2)

    with open(os.path.join(out_dir, "metrics.json"), "w") as f:
        json.dump({"time_series": time_series, "summary": final_metrics}, f, indent=2)

    # 3. Generate verification plot
    fig, axes = plt.subplots(2, 2, figsize=(10, 8))

    # Initial Phase
    im0 = axes[0, 0].imshow(history[0]["phi"], origin="lower", cmap="Blues", vmin=0, vmax=1)
    axes[0, 0].set_title("Initial Phase phi(0)")
    plt.colorbar(im0, ax=axes[0, 0])

    # Final Phase
    im1 = axes[0, 1].imshow(final_step["phi"], origin="lower", cmap="Blues", vmin=0, vmax=1)
    axes[0, 1].set_title(f"Final Phase phi(t={args.timesteps})")
    plt.colorbar(im1, ax=axes[0, 1])

    # Final Density
    im2 = axes[1, 0].imshow(final_step["rho"], origin="lower", cmap="viridis")
    axes[1, 0].set_title(f"Final Density rho(t={args.timesteps})")
    plt.colorbar(im2, ax=axes[1, 0])

    # Velocity Quiver / Magnitude
    u_mag = np.sqrt(final_step["u"][0]**2 + final_step["u"][1]**2)
    im3 = axes[1, 1].imshow(u_mag, origin="lower", cmap="plasma")
    axes[1, 1].set_title(f"Velocity Magnitude |u|(t={args.timesteps})")
    plt.colorbar(im3, ax=axes[1, 1])

    plt.tight_layout()
    plt.savefig(os.path.join(out_dir, "classical_dambreak_evolution.png"), dpi=300)
    plt.close()

    print(f"Classical benchmark completed. Artifacts saved in {out_dir}")
    print("============================================================")


if __name__ == "__main__":
    main()
