# PHASE 8 PUBLICATION FIGURE FORENSIC AUDIT (STAGE 8.15)

**Status**: Verified High-Resolution (300 DPI) Publication Figures (12 Figures)  
**Directory**: `publication_figures/phase7/`  
**Date**: 2026-08-19  

---

## 1. Figure Forensic Audit Matrix

| Figure File | Source CSV Dataset | Plotted Variables | Axes Scale | Verification Status | Visual Artifact Check |
| :--- | :--- | :--- | :--- | :--- | :--- |
| `fig01_classical_runtime_vs_N.png` | `PHASE8_CLASSICAL_REPRODUCTION.csv` | Step time (ms) vs. Nodes ($N$) | Semi-log (X log) | **VERIFIED** | Clean linear scaling, no artifacts |
| `fig02_classical_memory_vs_N.png` | `PHASE8_CLASSICAL_REPRODUCTION.csv` | Peak RAM (MB) vs. Nodes ($N$) | Log-log | **VERIFIED** | Clean linear memory scaling |
| `fig03_carleman_error_vs_time.png` | `PHASE8_CARLEMAN_REPRODUCTION.csv` | Relative $L_2, L_\infty$ vs. Steps ($t$) | Linear | **VERIFIED** | Non-divergent error saturation |
| `fig04_manifold_defect_vs_time.png`| `PHASE8_CARLEMAN_REPRODUCTION.csv` | Manifold defect vs. Steps ($t$) | Linear | **VERIFIED** | Defect bounded in $[0.074, 0.137]$ |
| `fig05_qsvt_residual_vs_degree.png`| `PHASE8_QSVT_REPRODUCTION.csv` | Linear residual vs. Degree ($d$) | Semi-log (Y log) | **VERIFIED** | Exponential convergence to $10^{-15}$ |
| `fig06_condition_number_vs_dt.png` | `PHASE8_CONDITIONING_BOUNDARY.csv` | $\kappa(I + \Delta t A_C)$ vs. $\Delta t$ | Linear | **VERIFIED** | Threshold $\kappa=1.5$ at $\Delta t^* \approx 0.035$ |
| `fig07_qubit_count_vs_N.png` | `PHASE8_RESOURCE_AUDIT.csv` | Logical qubits vs. Nodes ($N$) | Semi-log (X log) | **VERIFIED** | Strict logarithmic qubit scaling |
| `fig08_carleman_dim_vs_N.png` | `PHASE8_RESOURCE_AUDIT.csv` | Dimension $D_C$ vs. Nodes ($N$) | Log-log | **VERIFIED** | Exact $D_C = 342N$ scaling |
| `fig09_circuit_depth_vs_degree.png`| `PHASE6_CIRCUIT_RESOURCES.csv` | Circuit depth vs. Degree ($d$) | Linear | **VERIFIED** | Exact linear depth $\text{Depth} = 2d$ |
| `fig10_error_budget.png` | `PHASE8_FINAL_ERROR_BUDGET.csv` | Total error & components vs. $N_s$ | Log-log | **VERIFIED** | Crossover at $N_s \approx 5,000$ |
| `fig11_noise_robustness.png` | `PHASE6_NOISE_ROBUSTNESS.csv` | Fidelity & Mass error vs. $\lambda$| Linear | **VERIFIED** | Threshold boundary at $\lambda \approx 0.05$ |
| `fig12_observable_estimation_scaling.png` | Theoretical derivation | Query count vs. Precision $\epsilon$ | Log-log | **VERIFIED** | QAE $\mathcal{O}(1/\epsilon)$ vs. Classical $\mathcal{O}(1/\epsilon^2)$ |

---

## 2. Forensic Conformance
Every figure is programmatically regenerated from clean-room CSV datasets with exact axis units, legends, high contrast, and 300 DPI resolution.
