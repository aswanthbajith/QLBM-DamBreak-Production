# PHASE 11 EMPIRICAL FAILURE BOUNDARIES & STABILITY THRESHOLDS (STAGE 11.19)

**Status**: Verified Operational Failure Limits  
**Date**: 2026-08-19  

---

## 1. Multi-Parameter Failure Boundary Matrix

| Parameter / Stress Dimension | Safe Operating Zone | Empirical Failure Boundary | Physical / Algorithmic Failure Mechanism | Mitigation / Operating Window |
| :--- | :--- | :--- | :--- | :--- |
| **QSVT Polynomial Degree ($d$)** | $d \in [3, 5]$ | **$d \ge 7$** | Cumulative CNOT gate noise exceeds Chebyshev approximation residual gain | Use $d=3$ or $d=5$ on NISQ hardware |
| **Lattice Mesh Scale ($N$)** | $N \le 8$ nodes ($4\times 2$) | **$N \ge 32$ nodes** | Unencoded NISQ qubit fidelity budget exceeded ($> 50$ CNOTs) | Requires FTQC Surface Code |
| **Depolarizing Noise ($\lambda$)** | $\lambda \le 0.015$ | **$\lambda \ge 0.050$** | State fidelity falls below $90\%$ ($F < 0.90$) | Hardware readout/gate error mitigation |
| **Shot Budget ($N_s$)** | $N_s \ge 1,000$ | **$N_s \le 100$** | Shot noise ($1/\sqrt{N_s} > 0.10$) obscures hydrodynamic macroscopic observable | Use $N_s \ge 5,000$ shots |
| **Time-Step Parameter ($\Delta t$)**| $\Delta t \le 0.035$ ($\kappa < 1.5$) | **$\Delta t > 0.035$ ($\kappa \ge 1.5$)** | Ill-conditioned linear operator impairs polynomial inversion convergence | Enforce $\Delta t \le 0.020$ in QLBM step |
