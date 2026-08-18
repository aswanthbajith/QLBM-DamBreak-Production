#!/usr/bin/env python3
"""
Benchmark Validation Suite for Classical Two-Phase LBM Dam-Break.
Compares simulation results against Martin & Moyce (1952) experimental benchmark.
"""

import os
import sys
import numpy as np
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
from dam_break_sim import run_dam_break_simulation

def run_validation():
    val_dir = "/home/aswa/Research/QLBM-DamBreak/validation"
    ref_file = f"{val_dir}/reference_data/martin_moyce_1952.csv"
    os.makedirs(val_dir, exist_ok=True)

    print("\n" + "="*80)
    print("EXECUTING TWO-PHASE LBM BENCHMARK VALIDATION")
    print("="*80 + "\n")

    # Run production dam break simulation
    history = run_dam_break_simulation(
        nx=300, ny=100,
        dam_w=45, dam_h=45,
        total_steps=2200,
        save_interval=200,
        rho_L=1.0, rho_G=0.1,
        nu_L=0.005, nu_G=0.01,
        sigma=0.001, gy=-4.0e-4,
        output_dir=f"{val_dir}/sim_data"
    )

    t_sim = np.array(history['t_star'])
    x_sim = np.array(history['x_star'])
    h_sim = np.array(history['h_star'])
    p_sim = np.array(history['p_impact_star'])
    mass_err = np.array(history['mass_error'])

    # Read reference data safely
    ref_data = np.genfromtxt(ref_file, delimiter=',', comments='#')
    ref_data = ref_data[~np.isnan(ref_data).any(axis=1)]
    mm_t = ref_data[:, 0]
    mm_x = ref_data[:, 1]
    mm_h = ref_data[:, 2]

    # Convert dimensionless time T = t * sqrt(2 * g / a) = t* * sqrt(2)
    t_scale = np.sqrt(2.0)
    t_scaled_sim = t_sim * t_scale

    # Interpolate simulation results onto experimental time points
    x_interp = np.interp(mm_t, t_scaled_sim, x_sim)
    h_interp = np.interp(mm_t, t_scaled_sim, h_sim)

    # Compute comprehensive error norms
    # 1. Surge Front
    err_x = x_interp - mm_x
    l1_x = np.mean(np.abs(err_x))
    l2_x = np.sqrt(np.mean(err_x**2))
    linf_x = np.max(np.abs(err_x))
    rel_l2_x = l2_x / np.mean(mm_x)

    # 2. Column Height
    err_h = h_interp - mm_h
    l1_h = np.mean(np.abs(err_h))
    l2_h = np.sqrt(np.mean(err_h**2))
    linf_h = np.max(np.abs(err_h))
    rel_l2_h = l2_h / np.mean(mm_h)

    # 3. Mass Conservation
    max_mass_err = np.max(mass_err)

    print("\n" + "="*80)
    print("QUANTITATIVE BENCHMARK ERROR ANALYSIS")
    print("="*80)
    print(f"Surge Front L1 Error       : {l1_x:.4f} (Relative: {l1_x/np.mean(mm_x)*100:.2f}%)")
    print(f"Surge Front L2 Error       : {l2_x:.4f} (Relative: {rel_l2_x*100:.2f}%)")
    print(f"Surge Front Linf Error     : {linf_x:.4f}")
    print(f"Column Height L1 Error     : {l1_h:.4f} (Relative: {l1_h/np.mean(mm_h)*100:.2f}%)")
    print(f"Column Height L2 Error     : {l2_h:.4f} (Relative: {rel_l2_h*100:.2f}%)")
    print(f"Column Height Linf Error   : {linf_h:.4f}")
    print(f"Max Mass Conservation Error: {max_mass_err:.4e} ({max_mass_err*100:.3f}%)")
    print("="*80 + "\n")

    # Plot 1: Surge Wavefront Comparison
    fig, ax = plt.subplots(figsize=(7.5, 5.2))
    ax.plot(t_scaled_sim[t_scaled_sim <= 4.5], x_sim[t_scaled_sim <= 4.5], 'b-', linewidth=2.5, label='Two-Phase LBM (Present)')
    ax.scatter(mm_t, mm_x, color='crimson', marker='o', s=65, zorder=5, label='Martin & Moyce (1952) Exp.')
    ax.plot(mm_t, 1.0 + 1.2 * mm_t, 'k--', alpha=0.6, label=r'Analytical Surge Line ($x^* = 1 + 1.2 T$)')
    ax.set_title("Two-Phase Dam-Break Surge Wavefront Propagation $x^*(T)$", fontsize=12, fontweight='bold')
    ax.set_xlabel(r"Dimensionless Time $T = t \sqrt{2g / a}$", fontsize=11)
    ax.set_ylabel(r"Dimensionless Surge Position $x^* = x / a$", fontsize=11)
    ax.grid(True, linestyle=':', alpha=0.6)
    ax.legend(loc='upper left', frameon=True)
    ax.set_xlim([0, 4.2])
    plt.tight_layout()
    plt.savefig(f"{val_dir}/two_phase_dam_break_wavefront.png", dpi=300)
    plt.close()

    # Plot 2: Column Height Decay Comparison
    fig, ax = plt.subplots(figsize=(7.5, 5.2))
    ax.plot(t_scaled_sim[t_scaled_sim <= 4.5], h_sim[t_scaled_sim <= 4.5], 'b-', linewidth=2.5, label='Two-Phase LBM (Present)')
    ax.scatter(mm_t, mm_h, color='crimson', marker='s', s=65, zorder=5, label='Martin & Moyce (1952) Exp.')
    ax.set_title("Two-Phase Dam-Break Column Height Decay $h^*(T)$", fontsize=12, fontweight='bold')
    ax.set_xlabel(r"Dimensionless Time $T = t \sqrt{2g / a}$", fontsize=11)
    ax.set_ylabel(r"Dimensionless Column Height $h^* = h / a$", fontsize=11)
    ax.grid(True, linestyle=':', alpha=0.6)
    ax.legend(loc='upper right', frameon=True)
    ax.set_xlim([0, 4.2])
    ax.set_ylim([0, 1.1])
    plt.tight_layout()
    plt.savefig(f"{val_dir}/two_phase_dam_break_height.png", dpi=300)
    plt.close()

    # Plot 3: Downstream Impact Pressure History
    fig, ax = plt.subplots(figsize=(7.5, 5.2))
    ax.plot(t_sim, p_sim, color='teal', linewidth=2.2, label='Sensor P1 (Right Impact Wall)')
    ax.set_title("Downstream Wall Impact Pressure History $p^*(t^*)$", fontsize=12, fontweight='bold')
    ax.set_xlabel(r"Dimensionless Time $t^* = t \sqrt{g / b}$", fontsize=11)
    ax.set_ylabel(r"Dimensionless Pressure $p^* = p / (\rho_L g b)$", fontsize=11)
    ax.grid(True, linestyle=':', alpha=0.6)
    ax.legend(loc='upper right', frameon=True)
    plt.tight_layout()
    plt.savefig(f"{val_dir}/two_phase_dam_break_pressure.png", dpi=300)
    plt.close()

    # Write comprehensive validation report
    report = f"""# Classical Two-Phase LBM Dam-Break Validation Report

## 1. Physical & Numerical Setup
- **Hydrodynamics**: Incompressible velocity-based D2Q9 LBM with variable density and viscosity.
- **Interface Tracking**: Conservative Allen-Cahn phase-field with counter-gradient sharpening.
- **Lattice Resolution**: $300 \\times 100$ nodes.
- **Dam Geometry**: $45 \\times 45$ nodes (Aspect ratio $a/b = 1.0$).
- **Liquid Phase**: $\\rho_L = 1.0$, $\\nu_L = 0.005$.
- **Gas Phase**: $\\rho_G = 0.1$, $\\nu_G = 0.01$ (Density ratio $\\rho_L/\\rho_G = 10.0$).
- **Surface Tension**: $\\sigma = 0.001$, interface thickness $W = 3.5$, mobility $M = 0.05$.
- **Gravity Acceleration**: $g_y = -4.0 \\times 10^{{-4}}$ lattice units.
- **Boundary Conditions**: Solid wall half-way bounce-back on lateral/top walls, free-slip floor.

---

## 2. Quantitative Error Analysis (vs. Martin & Moyce 1952)

| Metric | $L_1$ Error | $L_2$ Error | $L_\\infty$ Error | Relative $L_2$ Error |
| :--- | :---: | :---: | :---: | :---: |
| **Surge Front $x^*(T)$** | **{l1_x:.4f}** | **{l2_x:.4f}** | **{linf_x:.4f}** | **{rel_l2_x*100:.2f}%** |
| **Column Height $h^*(T)$** | **{l1_h:.4f}** | **{l2_h:.4f}** | **{linf_h:.4f}** | **{rel_l2_h*100:.2f}%** |
| **Mass Conservation $\\Delta M / M_0$** | - | - | - | **<{max_mass_err*100:.3f}%** |

---

## 3. Generated Figures
1. [`two_phase_dam_break_wavefront.png`](file:///home/aswa/Research/QLBM-DamBreak/validation/two_phase_dam_break_wavefront.png): Surge wavefront position $x^*(T)$ compared against Martin & Moyce (1952) experiment.
2. [`two_phase_dam_break_height.png`](file:///home/aswa/Research/QLBM-DamBreak/validation/two_phase_dam_break_height.png): Water column collapse rate $h^*(T)$ vs. experimental points.
3. [`two_phase_dam_break_pressure.png`](file:///home/aswa/Research/QLBM-DamBreak/validation/two_phase_dam_break_pressure.png): Downstream wall sensor pressure history $p^*(t^*)$.
"""

    with open(f"{val_dir}/classical_two_phase_validation.md", "w") as f:
        f.write(report)

    print(f"Validation complete! Report saved to: {val_dir}/classical_two_phase_validation.md")

if __name__ == "__main__":
    run_validation()
