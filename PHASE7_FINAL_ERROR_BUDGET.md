# PHASE 7 COMPREHENSIVE SIMULATION ERROR BUDGET (STAGE 7.11)

**Status**: Verified Multi-Scale Error Budget Decomposition  
**Date**: 2026-08-19  

---

## 1. Error Budget Decomposition Table

| Shots ($N_s$) | $\epsilon_{\text{{disc}}}$ (LBM) | $\epsilon_{\text{{Carle}}}$ (Order 2) | $\epsilon_{\text{{QSVT}}}$ ($d=15$) | $\epsilon_{\text{{meas}}}$ ($1/\sqrt{{N_s}}$) | $\epsilon_{\text{{noise}}}$ ($\lambda=10^{{-4}}$) | Total Bound $\sum \epsilon_i$ | Total RSS $\sqrt{{\sum \epsilon_i^2}}$ | Dominant Error |
| :--- | :--- | :--- | :--- | :--- | :--- | :--- | :--- | :--- |
| **$100$** | $2.00 \times 10^{-3}$ | $9.52 \times 10^{-3}$ | $5.03 \times 10^{-11}$ | $3.73 \times 10^{-2}$ | $7.80 \times 10^{-4}$ | $4.96 \times 10^{-2}$ | $3.86 \times 10^{-2}$ | **SHOT_NOISE** |
| **$1,000$** | $2.00 \times 10^{-3}$ | $9.52 \times 10^{-3}$ | $5.03 \times 10^{-11}$ | $1.18 \times 10^{-2}$ | $7.80 \times 10^{-4}$ | $2.41 \times 10^{-2}$ | $1.53 \times 10^{-2}$ | **SHOT_NOISE** |
| **$10,000$** | $2.00 \times 10^{-3}$ | $9.52 \times 10^{-3}$ | $5.03 \times 10^{-11}$ | $3.73 \times 10^{-3}$ | $7.80 \times 10^{-4}$ | $1.60 \times 10^{-2}$ | $1.04 \times 10^{-2}$ | **CARLEMAN_TRUNCATION** |
| **$100,000$** | $2.00 \times 10^{-3}$ | $9.52 \times 10^{-3}$ | $5.03 \times 10^{-11}$ | $1.18 \times 10^{-3}$ | $7.80 \times 10^{-4}$ | $1.35 \times 10^{-2}$ | $9.81 \times 10^{-3}$ | **CARLEMAN_TRUNCATION** |
| **$1,000,000$** | $2.00 \times 10^{-3}$ | $9.52 \times 10^{-3}$ | $5.03 \times 10^{-11}$ | $3.73 \times 10^{-4}$ | $7.80 \times 10^{-4}$ | $1.27 \times 10^{-2}$ | $9.74 \times 10^{-3}$ | **CARLEMAN_TRUNCATION** |

---

## 2. Error Propagation & Hierarchy
1. **Shot Noise Regime ($N_s < 5,000$)**: Measurement error $\epsilon_{{\text{{meas}}}} \sim 1/\sqrt{{N_s}}$ dominates all deterministic terms.
2. **Carleman Floor Regime ($N_s \ge 10,000$)**: Truncation error of quadratic Carleman lifting ($\approx 0.95\%$) forms the asymptotic error floor.
3. **QSVT Inversion Precision**: With degree $d=15$, inversion error ($\approx 5 \times 10^{-11}$) is 8 orders of magnitude below the physical and truncation errors.
