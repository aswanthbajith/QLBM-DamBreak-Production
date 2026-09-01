# PHASE 6 CONDITION NUMBER & SPECTRUM STABILITY STUDY (STAGE 6.5)

**Status**: Verified Spectral Condition Analysis Across $\Delta t$  
**Date**: 2026-08-19  
**Operator**: $M(\Delta t) = I + \Delta t A_C$ with $A_C \in \mathbb{R}^{684 \times 684}$  

---

## 1. Condition Number Sweep Table

| Time Step $\Delta t$ | $\sigma_{\min}(M)$ | $\sigma_{\max}(M)$ | Condition Number $\kappa(M)$ | Spectral Norm $\|M\|_2$ | $\kappa < 1.5$ Bound | Inversion Residual ($d=15$) | Solution Fidelity | Req Degree for $10^{-10}$ | Classification |
| :--- | :--- | :--- | :--- | :--- | :--- | :--- | :--- | :--- | :--- |
| **$0.0010$** | 0.9940 | 1.0050 | **$1.0111$** | 1.0050 | **TRUE** | $2.49 \times 10^{-15}$ | 1.000000 | 11 | **MEASURED** |
| **$0.0050$** | 0.9704 | 1.0254 | **$1.0567$** | 1.0254 | **TRUE** | $2.16 \times 10^{-13}$ | 1.000000 | 11 | **MEASURED** |
| **$0.0100$** | 0.9415 | 1.0515 | **$1.1168$** | 1.0515 | **TRUE** | $5.03 \times 10^{-11}$ | 1.000000 | 15 | **MEASURED** |
| **$0.0200$** | 0.8861 | 1.1060 | **$1.2483$** | 1.1060 | **TRUE** | $1.32 \times 10^{-8}$ | 1.000000 | 17 | **MEASURED** |
| **$0.0500$** | 0.7373 | 1.2872 | **$1.7457$** | 1.2872 | **FALSE** | $2.90 \times 10^{-5}$ | 1.000000 | 21 | **MEASURED** |
| **$0.1000$** | 0.5444 | 1.6437 | **$3.0192$** | 1.6437 | **FALSE** | $2.55 \times 10^{-3}$ | 0.999991 | 31 | **MEASURED** |

---

## 2. Spectral Analysis & Stability Boundary
1. **Well-Conditioned Zone ($\kappa < 1.5$)**:
   For $\Delta t \le 0.020$, the condition number satisfies $\kappa(M) \le 1.2483$. In this regime, polynomial degree $d=15$ guarantees excellent inversion precision.
2. **Stability Boundary**:
   The stability boundary $\kappa = 1.5$ occurs at $\Delta t^* \approx 0.035$. For $\Delta t \ge 0.05$, condition number elevates to $\kappa = 1.75 - 3.02$, causing degree $d=15$ residual to degrade to $\sim 10^{-5}$, requiring degree $d \ge 21$ for high precision.
