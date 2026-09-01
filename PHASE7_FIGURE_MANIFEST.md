# PHASE 7 PUBLICATION FIGURE MANIFEST (STAGE 7.15)

**Status**: Verified High-Resolution (300 DPI) Publication Figures  
**Directory**: `publication_figures/phase7/`  
**Date**: 2026-08-19  

---

## Complete 12-Figure Publication Catalog

| Figure ID | Filename | Description | Source Dataset | Key Finding |
| :--- | :--- | :--- | :--- | :--- |
| **Figure 1** | `fig01_classical_runtime_vs_N.png` | Classical LBM wall-clock time per step vs. grid nodes | `PHASE7_CLASSICAL_FINAL_VALIDATION.csv` | Strict linear $\mathcal{O}(N)$ scaling from 8 to 30,000 nodes. |
| **Figure 2** | `fig02_classical_memory_vs_N.png` | Peak classical memory footprint vs. grid nodes | `PHASE7_CLASSICAL_FINAL_VALIDATION.csv` | Linear memory scaling ($14.65\text{ MB}$ at $300 \times 100$). |
| **Figure 3** | `fig03_carleman_error_vs_time.png` | Carleman $N_C=2$ relative $L_2$ and $L_\infty$ error over 200 steps | `PHASE7_CARLEMAN_ERROR.csv` | Stable error saturation at $\approx 1.05\%$ (non-divergent). |
| **Figure 4** | `fig04_manifold_defect_vs_time.png` | Quadratic invariant manifold defect vs. time | `PHASE7_CARLEMAN_ERROR.csv` | Manifold defect strictly bounded in $[0.074, 0.137]$. |
| **Figure 5** | `fig05_qsvt_residual_vs_degree.png` | Linear inversion residual vs. Chebyshev polynomial degree | `PHASE7_QSVT_FINAL_AUDIT.csv` | Exponential convergence reaching $5.03 \times 10^{-11}$ at $d=15$. |
| **Figure 6** | `fig06_condition_number_vs_dt.png` | System condition number $\kappa(I + \Delta t A_C)$ vs. time step $\Delta t$ | `PHASE6_CONDITION_NUMBER_SWEEP.csv` | Well-conditioned zone $\kappa < 1.5$ for $\Delta t \le 0.035$. |
| **Figure 7** | `fig07_qubit_count_vs_N.png` | Total logical qubit requirements vs. spatial mesh nodes | `PHASE7_RESOURCE_ESTIMATES.csv` | Strict logarithmic scaling $n = \lceil \log_2(342N) \rceil + 1$. |
| **Figure 8** | `fig08_carleman_dim_vs_N.png` | Lifted Carleman state space dimension $D_C = 342N$ | `PHASE7_RESOURCE_ESTIMATES.csv` | Linear scaling in $N$, avoiding global $(18N)^2$ explosion. |
| **Figure 9** | `fig09_circuit_depth_vs_degree.png` | Quantum circuit depth vs. QSVT polynomial degree | `PHASE6_CIRCUIT_RESOURCES.csv` | Strict linear depth $\text{Depth} = 2d$. |
| **Figure 10** | `fig10_error_budget.png` | Complete simulation error budget decomposition | `PHASE7_ERROR_BUDGET.csv` | Crossover between shot noise and Carleman truncation floor. |
| **Figure 11** | `fig11_noise_robustness.png` | State fidelity and mass error vs. depolarizing noise rate | `PHASE6_NOISE_ROBUSTNESS.csv` | Usable noise operating regime up to $\lambda \le 0.05$. |
| **Figure 12** | `fig12_observable_estimation_scaling.png`| Query complexity comparison (Classical Monte Carlo vs. QAE) | Theoretical QAE derivation | Quadratic query advantage $\mathcal{O}(1/\epsilon)$ for scalar integrals. |
