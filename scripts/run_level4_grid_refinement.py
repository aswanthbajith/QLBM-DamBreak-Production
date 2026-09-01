#!/usr/bin/env python3
"""
Level-4 Multi-Grid Refinement and Martin & Moyce Benchmark Validation Script.

Simulates two-phase dam-break column collapse across multiple grid resolutions
(16x16, 32x32, 64x64, 128x128), extracts surge front x*(t*) and column height h*(t*),
computes L2/L_inf errors against Martin & Moyce (1952) experimental data,
and produces validation comparison plots and CSV reports.
"""

import os
import sys
import time
import csv
import numpy as np

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt

from classical.level4_two_phase import Level4TwoPhaseLBM
from classical.benchmarks.martin_moyce_data import MartinMoyceBenchmark


def run_grid_refinement():
    results_dir = os.path.join(os.path.dirname(__file__), "../results/level4_benchmarks")
    os.makedirs(results_dir, exist_ok=True)

    grid_sizes = [(32, 16), (64, 32), (128, 64)]
    timesteps = 60
    g_acc = -0.0005
    sigma = 0.0001

    benchmark_summary = []
    simulation_histories = {}

    print("=" * 80)
    print("LEVEL-4 MULTI-GRID REFINEMENT & MARTIN-MOYCE VALIDATION STUDY")
    print("=" * 80)

    for nx, ny in grid_sizes:
        print(f"\n>>> Running Grid Resolution: {nx} x {ny} ({nx * ny} nodes)...")
        t0 = time.time()
        solver = Level4TwoPhaseLBM(nx=nx, ny=ny, g_acc=g_acc, sigma=sigma)

        a = float(solver.dam_width)
        h0 = float(solver.dam_height)

        t_eval = []
        x_front = []
        h_height = []
        kinetic_energy = []
        liquid_volume = []

        for step in range(timesteps):
            solver.step()
            if step % 2 == 0:
                t_eval.append(step * 1.0)
                x_front.append(solver.get_surge_front_position(threshold=0.3))
                h_height.append(solver.get_column_height(threshold=0.3))
                kinetic_energy.append(solver.get_kinetic_energy())
                liquid_volume.append(solver.get_total_liquid_volume())

        dt = time.time() - t0
        print(f"    Completed {timesteps} steps in {dt:.3f} s.")

        # Compute error against Martin & Moyce
        metrics = MartinMoyceBenchmark.evaluate_errors(
            np.array(t_eval),
            np.array(x_front),
            np.array(h_height),
            a=a,
            h0=h0,
            g=abs(g_acc),
        )

        initial_vol = liquid_volume[0]
        final_vol = liquid_volume[-1]
        mass_drift = abs(final_vol - initial_vol) / initial_vol

        summary_row = {
            "grid_nx": nx,
            "grid_ny": ny,
            "total_nodes": nx * ny,
            "runtime_sec": round(dt, 3),
            "front_rel_l2_error": round(metrics["x_front_rel_l2"], 5),
            "height_rel_l2_error": round(metrics["h_height_rel_l2"], 5),
            "front_max_error": round(metrics["x_front_max_err"], 5),
            "height_max_error": round(metrics["h_height_max_err"], 5),
            "mass_drift_rel": round(mass_drift, 6),
        }
        benchmark_summary.append(summary_row)
        simulation_histories[(nx, ny)] = {
            "metrics": metrics,
            "t_eval": t_eval,
            "x_front": x_front,
            "h_height": h_height,
            "ke": kinetic_energy,
            "vol": liquid_volume,
        }

    # 1. Save CSV Summary
    csv_path = os.path.join(results_dir, "grid_refinement_study.csv")
    with open(csv_path, "w", newline="") as f:
        writer = csv.DictWriter(f, fieldnames=list(benchmark_summary[0].keys()))
        writer.writeheader()
        writer.writerows(benchmark_summary)
    print(f"\n[+] Saved grid refinement study CSV to: {csv_path}")

    # 2. Generate Multi-Panel Comparison Plot
    plot_path = os.path.join(results_dir, "dam_break_martin_moyce_comparison.png")
    fig, axes = plt.subplots(1, 3, figsize=(18, 5))

    # Reference curve
    t_ref = np.linspace(0.0, 3.2, 100)
    x_ref = MartinMoyceBenchmark.get_reference_front(t_ref)
    h_ref = MartinMoyceBenchmark.get_reference_height(t_ref)

    # Panel 1: Non-dimensional Surge Front x*(t*)
    ax1 = axes[0]
    ax1.plot(t_ref, x_ref, "k--", linewidth=2.5, label="Martin & Moyce (1952) Exp.")
    for (nx, ny), data in simulation_histories.items():
        m = data["metrics"]
        ax1.plot(m["t_star"], m["x_star_sim"], "o-", label=f"LBM {nx}x{ny}")
    ax1.set_xlabel(r"Non-Dimensional Time $t^* = t \sqrt{g/a}$", fontsize=11)
    ax1.set_ylabel(r"Surge Front Position $x^* = x/a$", fontsize=11)
    ax1.set_title("Dam-Break Surge Front Propagation", fontsize=12, fontweight="bold")
    ax1.legend(frameon=True)
    ax1.grid(True, linestyle=":", alpha=0.6)

    # Panel 2: Non-dimensional Residual Column Height h*(t*)
    ax2 = axes[1]
    ax2.plot(t_ref, h_ref, "k--", linewidth=2.5, label="Martin & Moyce (1952) Exp.")
    for (nx, ny), data in simulation_histories.items():
        m = data["metrics"]
        ax2.plot(m["t_star"], m["h_star_sim"], "s-", label=f"LBM {nx}x{ny}")
    ax2.set_xlabel(r"Non-Dimensional Time $t^* = t \sqrt{g/h_0}$", fontsize=11)
    ax2.set_ylabel(r"Column Height $h^* = h/h_0$", fontsize=11)
    ax2.set_title("Water Column Collapse Dynamics", fontsize=12, fontweight="bold")
    ax2.legend(frameon=True)
    ax2.grid(True, linestyle=":", alpha=0.6)

    # Panel 3: Kinetic Energy Evolution
    ax3 = axes[2]
    for (nx, ny), data in simulation_histories.items():
        t_steps = data["t_eval"]
        ke = data["ke"]
        ax3.plot(t_steps, ke, label=f"LBM {nx}x{ny}")
    ax3.set_xlabel("Timestep $t$", fontsize=11)
    ax3.set_ylabel("Total Kinetic Energy", fontsize=11)
    ax3.set_title("Kinetic Energy Dissipation", fontsize=12, fontweight="bold")
    ax3.legend(frameon=True)
    ax3.grid(True, linestyle=":", alpha=0.6)

    plt.tight_layout()
    plt.savefig(plot_path, dpi=300)
    plt.close()
    print(f"[+] Saved comparison plot to: {plot_path}")

    # Print summary table
    print("\n" + "=" * 80)
    print("GRID REFINEMENT STUDY SUMMARY TABLE")
    print("=" * 80)
    print(f"{'Grid':<12} | {'Nodes':<8} | {'Front Rel L2':<14} | {'Height Rel L2':<14} | {'Mass Drift':<12} | {'Runtime'}")
    print("-" * 80)
    for r in benchmark_summary:
        grid_str = f"{r['grid_nx']}x{r['grid_ny']}"
        print(f"{grid_str:<12} | {r['total_nodes']:<8} | {r['front_rel_l2_error'] * 100:6.3f}%        | {r['height_rel_l2_error'] * 100:6.3f}%        | {r['mass_drift_rel'] * 100:6.4f}%     | {r['runtime_sec']:.2f}s")
    print("=" * 80)


if __name__ == "__main__":
    run_grid_refinement()
