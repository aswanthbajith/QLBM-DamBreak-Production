# PHASE 8 COMPREHENSIVE SIMULATION ERROR BUDGET (STAGE 8.14)

**Status**: Verified Multi-Regime Error Budget Decomposition  
**Date**: 2026-08-19  

---

## 1. Final Multi-Regime Error Budget Matrix

| Shots ($N_s$) | $\epsilon_{\text{disc}}$ | $\epsilon_{\text{Carle}}$ | $\epsilon_{\text{QSVT}}$ | $\epsilon_{\text{meas}}$ | $\epsilon_{\text{noise}}$ | Total Additive Bound | Total RSS Empirical | Dominant Error | Regime |
| :--- | :--- | :--- | :--- | :--- | :--- | :--- | :--- | :--- | :--- |
| **$100$** | $2.00 \times 10^{-3}$ | $9.52 \times 10^{-3}$ | $5.03 \times 10^{-11}$ | $3.73 \times 10^{-2}$ | $7.80 \times 10^{-4}$ | $4.96 \times 10^{-2}$ | $3.86 \times 10^{-2}$ | **SHOT_NOISE** | LOW_SHOT |
| **$1,000$** | $2.00 \times 10^{-3}$ | $9.52 \times 10^{-3}$ | $5.03 \times 10^{-11}$ | $1.18 \times 10^{-2}$ | $7.80 \times 10^{-4}$ | $2.41 \times 10^{-2}$ | $1.53 \times 10^{-2}$ | **SHOT_NOISE** | MEDIUM_SHOT |
| **$10,000$** | $2.00 \times 10^{-3}$ | $9.52 \times 10^{-3}$ | $5.03 \times 10^{-11}$ | $3.73 \times 10^{-3}$ | $7.80 \times 10^{-4}$ | $1.60 \times 10^{-2}$ | $1.04 \times 10^{-2}$ | **CARLEMAN_TRUNCATION** | MEDIUM_SHOT |
| **$100,000$** | $2.00 \times 10^{-3}$ | $9.52 \times 10^{-3}$ | $5.03 \times 10^{-11}$ | $1.18 \times 10^{-3}$ | $7.80 \times 10^{-4}$ | $1.35 \times 10^{-2}$ | $9.81 \times 10^{-3}$ | **CARLEMAN_TRUNCATION** | HIGH_SHOT |
| **$1,000,000$** | $2.00 \times 10^{-3}$ | $9.52 \times 10^{-3}$ | $5.03 \times 10^{-11}$ | $3.73 \times 10^{-4}$ | $7.80 \times 10^{-4}$ | $1.27 \times 10^{-2}$ | $9.74 \times 10^{-3}$ | **CARLEMAN_TRUNCATION** | HIGH_SHOT |

---

## 2. Regime Analysis
* **Low-Shot / Noisy Condition ($N_s \le 1,000$)**: Statistical measurement shot noise ($\sim 1/\sqrt{N_s}$) dominates all deterministic modeling errors.
* **High-Shot / Ideal Condition ($N_s \ge 10,000$)**: Quadratic Carleman truncation ($\approx 0.95\%$) forms the asymptotic error floor.
* **QSVT Inversion Precision**: With degree $d=15$, inversion residual ($5.03 \times 10^{-11}$) remains completely negligible across all regimes.
