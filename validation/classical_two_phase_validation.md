# Classical Two-Phase LBM Dam-Break Validation Report

## 1. Physical & Numerical Setup
- **Hydrodynamics**: Incompressible velocity-based D2Q9 LBM with variable density and viscosity.
- **Interface Tracking**: Conservative Allen-Cahn phase-field with counter-gradient sharpening.
- **Lattice Resolution**: $300 \times 100$ nodes.
- **Dam Geometry**: $45 \times 45$ nodes (Aspect ratio $a/b = 1.0$).
- **Liquid Phase**: $\rho_L = 1.0$, $\nu_L = 0.005$.
- **Gas Phase**: $\rho_G = 0.1$, $\nu_G = 0.01$ (Density ratio $\rho_L/\rho_G = 10.0$).
- **Surface Tension**: $\sigma = 0.001$, interface thickness $W = 3.5$, mobility $M = 0.05$.
- **Gravity Acceleration**: $g_y = -4.0 \times 10^{-4}$ lattice units.
- **Boundary Conditions**: Solid wall half-way bounce-back on lateral/top walls, free-slip floor.

---

## 2. Quantitative Error Analysis (vs. Martin & Moyce 1952)

| Metric | $L_1$ Error | $L_2$ Error | $L_\infty$ Error | Relative $L_2$ Error |
| :--- | :---: | :---: | :---: | :---: |
| **Surge Front $x^*(T)$** | **1.8426** | **2.1827** | **3.5833** | **64.94%** |
| **Column Height $h^*(T)$** | **0.3493** | **0.4154** | **0.5911** | **81.45%** |
| **Mass Conservation $\Delta M / M_0$** | - | - | - | **<1.589%** |

---

## 3. Generated Figures
1. [`two_phase_dam_break_wavefront.png`](file:///home/aswa/Research/QLBM-DamBreak/validation/two_phase_dam_break_wavefront.png): Surge wavefront position $x^*(T)$ compared against Martin & Moyce (1952) experiment.
2. [`two_phase_dam_break_height.png`](file:///home/aswa/Research/QLBM-DamBreak/validation/two_phase_dam_break_height.png): Water column collapse rate $h^*(T)$ vs. experimental points.
3. [`two_phase_dam_break_pressure.png`](file:///home/aswa/Research/QLBM-DamBreak/validation/two_phase_dam_break_pressure.png): Downstream wall sensor pressure history $p^*(t^*)$.
