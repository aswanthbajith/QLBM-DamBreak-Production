# PHASE 6 PUBLICATION FIGURE MANIFEST (STAGE 6.13)

**Status**: Verified High-Resolution (300 DPI) Publication Figures  
**Directory**: `results/phase6/figures/`  
**Date**: 2026-08-19  

---

## Figure Catalog

| Figure ID | Filename | Description | Source CSV Data | Key Finding |
| :--- | :--- | :--- | :--- | :--- |
| **Figure 1** | `fig1_classical_benchmark.png` | Classical LBM scaling (step time & RAM) across grid resolutions | `PHASE6_CLASSICAL_BENCHMARK.csv` | Linear $\mathcal{O}(N)$ scaling from 8 to 30,000 nodes. |
| **Figure 2** | `fig2_carleman_error_vs_time.png` | Carleman $N_C=2$ truncation error & manifold defect vs. time ($t=1..200$) | `PHASE6_CARLEMAN_TIME_ERROR.csv` | Bounded error saturation at $\sim 1.05\%$ (non-divergent). |
| **Figure 3** | `fig3_qsvt_residual_vs_degree.png` | Linear inversion residual vs. Chebyshev polynomial degree ($d=3..31$) | `PHASE6_QSVT_DEGREE_SWEEP.csv` | Exponential convergence reaching $5.03 \times 10^{-11}$ at $d=15$. |
| **Figure 4** | `fig4_condition_number_vs_dt.png` | Condition number $\kappa(I + \Delta t A_C)$ vs. time step $\Delta t$ | `PHASE6_CONDITION_NUMBER_SWEEP.csv` | Well-conditioned zone $\kappa < 1.5$ for $\Delta t \le 0.035$. |
| **Figure 5** | `fig5_qubits_vs_nodes.png` | Total logical qubit requirements vs. spatial mesh nodes | `PHASE6_GRID_SCALING.csv` | Strict logarithmic scaling $n = \lceil \log_2(342N) \rceil + 1$. |
| **Figure 6** | `fig6_carleman_dim_vs_nodes.png` | Lifted Carleman state space dimension $D_C = 342N$ | `PHASE6_GRID_SCALING.csv` | Strict linear scaling avoiding global $(18N)^2$ explosion. |
| **Figure 7** | `fig7_circuit_depth_vs_degree.png` | Quantum circuit depth ($2d$) and CX gate counts vs. QSVT degree | `PHASE6_CIRCUIT_RESOURCES.csv` | Linear circuit depth scaling with zero exponential overhead. |
| **Figure 8** | `fig8_shot_noise_scaling.png` | Finite-shot measurement sampling error vs. shot budget $N_s$ | `PHASE6_ERROR_BUDGET.csv` | Exact Standard Quantum Limit scaling $\sigma \sim 1/\sqrt{N_s}$ ($R^2 > 0.999$). |
| **Figure 9** | `fig9_error_budget_decomposition.png` | Additive error budget: $\epsilon_{\text{total}} \approx \epsilon_{\text{Carle}} + \epsilon_{\text{QSVT}} + \epsilon_{\text{shot}}$ | `PHASE6_ERROR_BUDGET.csv` | Crossover between shot-noise and Carleman truncation floor. |
| **Figure 10** | `fig10_noise_robustness.png` | Quantum state fidelity & mass observable error vs. noise rate $\lambda$ | `PHASE6_NOISE_ROBUSTNESS.csv` | Algorithmic usability threshold at $\lambda \approx 0.05$ (fidelity $\approx 0.95$). |
