#!/usr/bin/env python3
"""
Level-5 Coupled Carleman Linearization vs. Classical Level-4 Two-Phase Validation.

Runs step-by-step comparative evolution between:
1. Validated Classical Level-4 Two-Phase Nonlinear Solver
2. Second-Order Coupled Carleman-Linearized Solver (A_eval)
3. Autonomous Closed Carleman Solver (C2)

Outputs:
- results/level5_carleman_validation.csv
- results/level5_carleman_validation.png
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
import scipy.linalg as la

from classical.level4_two_phase import Level4TwoPhaseLBM
from classical.streaming import stream
from classical.boundary import apply_noslip_box
from quantum.level5_two_phase_carleman import (
    compute_level5_carleman_matrices,
    lift_to_second_order,
    compute_closed_carleman_matrix_order2,
    analyze_carleman_operator_properties,
)


def run_carleman_step(f: np.ndarray, g: np.ndarray, A_eval: np.ndarray, ny: int, nx: int) -> Tuple[np.ndarray, np.ndarray]:
    """
    Executes one timestep of the local second-order Carleman solver.
    """
    f_coll = np.zeros_like(f)
    g_coll = np.zeros_like(g)

    # Local node-by-node evaluation
    for y in range(ny):
        for x in range(nx):
            z_node = np.concatenate((f[:, y, x], g[:, y, x]))  # (18,)
            Y_node = lift_to_second_order(z_node)              # (342,)
            z_post = A_eval @ Y_node                           # (18,)
            f_coll[:, y, x] = z_post[:9]
            g_coll[:, y, x] = z_post[9:]

    # Spatial streaming
    f_str = stream(f_coll)
    g_str = stream(g_coll)

    # Boundary exact bounce-back
    solid_mask = np.zeros((ny, nx), dtype=bool)
    solid_mask[0, :] = True
    solid_mask[-1, :] = True
    solid_mask[:, 0] = True
    solid_mask[:, -1] = True

    f_out = np.copy(f_str)
    g_out = np.copy(g_str)
    for i in range(9):
        opp = [0, 3, 4, 1, 2, 7, 8, 5, 6][i]
        f_out[opp, solid_mask] = f_str[i, solid_mask]
        g_out[opp, solid_mask] = g_str[i, solid_mask]

    return f_out, g_out


def run_validation():
    results_dir = os.path.join(os.path.dirname(__file__), "../results")
    os.makedirs(results_dir, exist_ok=True)

    nx, ny = 4, 4
    timesteps = 10
    g_acc = -0.0005

    print("=" * 80)
    print("LEVEL-5 COUPLED CARLEMAN LINEARIZATION VALIDATION (4x4 MESH)")
    print("=" * 80)

    # 1. Initialize Solvers
    classical_solver = Level4TwoPhaseLBM(nx=nx, ny=ny, g_acc=g_acc, sigma=0.0)
    M1, M2, A_eval = compute_level5_carleman_matrices(
        tau_f=1.0 / (3.0 * 0.05 + 0.5), tau_g=0.7, g_acc=g_acc
    )

    f_carleman = np.copy(classical_solver.f)
    g_carleman = np.copy(classical_solver.g)

    validation_records = []

    # Initial state t = 0
    rho_c = np.sum(classical_solver.f, axis=0)
    alpha_c = np.clip(np.sum(classical_solver.g, axis=0), 0.0, 1.0)
    rho_k = np.sum(f_carleman, axis=0)
    alpha_k = np.clip(np.sum(g_carleman, axis=0), 0.0, 1.0)

    record_0 = {
        "timestep": 0,
        "f_rel_l2": 0.0,
        "g_rel_l2": 0.0,
        "rho_rel_l2": 0.0,
        "alpha_rel_l2": 0.0,
        "rho_max_err": 0.0,
        "alpha_max_err": 0.0,
        "mass_c": float(np.sum(alpha_c)),
        "mass_k": float(np.sum(alpha_k)),
        "mass_diff": 0.0,
    }
    validation_records.append(record_0)

    print(f"{'Step':<5} | {'f Rel L2':<12} | {'g Rel L2':<12} | {'rho Rel L2':<12} | {'alpha Rel L2':<14} | {'Mass Diff'}")
    print("-" * 80)
    print(f"t= 0  | {0.0:8.4e}   | {0.0:8.4e}   | {0.0:8.4e}   | {0.0:8.4e}     | 0.00%")

    for t in range(1, timesteps + 1):
        # Step classical solver
        classical_solver.step()
        # Step Carleman solver
        f_carleman, g_carleman = run_carleman_step(f_carleman, g_carleman, A_eval, ny, nx)

        rho_c = np.sum(classical_solver.f, axis=0)
        alpha_c = np.clip(np.sum(classical_solver.g, axis=0), 0.0, 1.0)
        rho_k = np.sum(f_carleman, axis=0)
        alpha_k = np.clip(np.sum(g_carleman, axis=0), 0.0, 1.0)

        err_f = float(la.norm(f_carleman - classical_solver.f) / (la.norm(classical_solver.f) + 1e-15))
        err_g = float(la.norm(g_carleman - classical_solver.g) / (la.norm(classical_solver.g) + 1e-15))
        err_rho = float(la.norm(rho_k - rho_c) / (la.norm(rho_c) + 1e-15))
        err_alpha = float(la.norm(alpha_k - alpha_c) / (la.norm(alpha_c) + 1e-15))

        mass_c = float(np.sum(alpha_c))
        mass_k = float(np.sum(alpha_k))
        mass_diff = abs(mass_k - mass_c) / (mass_c + 1e-15)

        record = {
            "timestep": t,
            "f_rel_l2": err_f,
            "g_rel_l2": err_g,
            "rho_rel_l2": err_rho,
            "alpha_rel_l2": err_alpha,
            "rho_max_err": float(np.max(np.abs(rho_k - rho_c))),
            "alpha_max_err": float(np.max(np.abs(alpha_k - alpha_c))),
            "mass_c": mass_c,
            "mass_k": mass_k,
            "mass_diff": mass_diff,
        }
        validation_records.append(record)

        print(f"t={t:2d}  | {err_f:8.4e}   | {err_g:8.4e}   | {err_rho:8.4e}   | {err_alpha:8.4e}     | {mass_diff * 100:6.4f}%")

    # 2. Save Validation CSV
    csv_path = os.path.join(results_dir, "level5_carleman_validation.csv")
    with open(csv_path, "w", newline="") as f:
        writer = csv.DictWriter(f, fieldnames=list(validation_records[0].keys()))
        writer.writeheader()
        writer.writerows(validation_records)
    print(f"\n[+] Saved Carleman validation CSV to: {csv_path}")

    # 3. Generate Convergence Plot
    plot_path = os.path.join(results_dir, "level5_carleman_validation.png")
    fig, axes = plt.subplots(1, 2, figsize=(14, 5))

    steps = [r["timestep"] for r in validation_records]
    err_f_list = [r["f_rel_l2"] for r in validation_records]
    err_g_list = [r["g_rel_l2"] for r in validation_records]
    err_rho_list = [r["rho_rel_l2"] for r in validation_records]
    err_alpha_list = [r["alpha_rel_l2"] for r in validation_records]

    ax1 = axes[0]
    ax1.semilogy(steps, err_f_list, "o-", label=r"$f_i$ Population Rel $L_2$")
    ax1.semilogy(steps, err_g_list, "s-", label=r"$g_i$ Population Rel $L_2$")
    ax1.semilogy(steps, err_rho_list, "^--", label=r"$\rho$ Density Rel $L_2$")
    ax1.semilogy(steps, err_alpha_list, "d--", label=r"$\alpha$ Volume Fraction Rel $L_2$")
    ax1.set_xlabel("Timestep $t$", fontsize=11)
    ax1.set_ylabel("Relative $L_2$ Error", fontsize=11)
    ax1.set_title("Level-5 Carleman vs. Classical Two-Phase LBM", fontsize=12, fontweight="bold")
    ax1.grid(True, linestyle=":", alpha=0.6)
    ax1.legend(frameon=True)

    ax2 = axes[1]
    mass_diff_list = [r["mass_diff"] * 100 for r in validation_records]
    ax2.plot(steps, mass_diff_list, "ro-", linewidth=2, label="Liquid Mass Conservation Difference (%)")
    ax2.set_xlabel("Timestep $t$", fontsize=11)
    ax2.set_ylabel("Mass Difference (%)", fontsize=11)
    ax2.set_title("Conservation Metric Tracking", fontsize=12, fontweight="bold")
    ax2.grid(True, linestyle=":", alpha=0.6)
    ax2.legend(frameon=True)

    plt.tight_layout()
    plt.savefig(plot_path, dpi=300)
    plt.close()
    print(f"[+] Saved Carleman validation plot to: {plot_path}")
    print("=" * 80)


if __name__ == "__main__":
    run_validation()
