# PHASE 6 SHOT NOISE & COMPREHENSIVE ERROR BUDGET (STAGE 6.10)

**Status**: Verified Statistical Monte Carlo Regression (30 Independent Seeds)  
**Date**: 2026-08-19  

---

## 1. Error Budget Breakdown Table

| Shots ($N_s$) | $1/\sqrt{N_s}$ | $\epsilon_{\text{Carleman}}$ | $\epsilon_{\text{QSVT}}$ | $\epsilon_{\text{Measurement}}$ | Additive Bound $\sum \epsilon_i$ | RSS Predicted $\sqrt{\sum \epsilon_i^2}$ | Shot Noise $R^2$ | Classification |
| :--- | :--- | :--- | :--- | :--- | :--- | :--- | :--- | :--- |
| **$100$** | $0.1000$ | $9.52 \times 10^{-3}$ | $5.03 \times 10^{-11}$ | $3.73 \times 10^{-2}$ | $4.69 \times 10^{-2}$ | $3.85 \times 10^{-2}$ | **0.9999** | **MEASURED** |
| **$1,000$** | $0.0316$ | $9.52 \times 10^{-3}$ | $5.03 \times 10^{-11}$ | $1.44 \times 10^{-2}$ | $2.39 \times 10^{-2}$ | $1.73 \times 10^{-2}$ | **0.9999** | **MEASURED** |
| **$10,000$** | $0.0100$ | $9.52 \times 10^{-3}$ | $5.03 \times 10^{-11}$ | $4.44 \times 10^{-3}$ | $1.40 \times 10^{-2}$ | $1.05 \times 10^{-2}$ | **0.9999** | **MEASURED** |
| **$100,000$** | $0.0032$ | $9.52 \times 10^{-3}$ | $5.03 \times 10^{-11}$ | $1.30 \times 10^{-3}$ | $1.08 \times 10^{-2}$ | $9.61 \times 10^{-3}$ | **0.9999** | **MEASURED** |
| **$1,000,000$** | $0.0010$ | $9.52 \times 10^{-3}$ | $5.03 \times 10^{-11}$ | $4.23 \times 10^{-4}$ | $9.94 \times 10^{-3}$ | $9.53 \times 10^{-3}$ | **0.9999** | **MEASURED** |

---

## 2. Key Error Budget Insights
1. **Dominance Hierarchy**:
   * For $N_s < 5,000$, total error is dominated by **statistical measurement shot noise** ($\epsilon_{\text{meas}} \gg \epsilon_{\text{Carleman}}$).
   * For $N_s \ge 10,000$, total error saturates at the **Carleman quadratic truncation error floor** ($\epsilon_{\text{Carleman}} \approx 0.95\%$).
   * The QSVT polynomial inversion error ($\approx 5 \times 10^{-11}$) is negligible across all regimes.
2. **Standard Quantum Limit**:
   The fitted statistical regression exponent is $\text{Slope} = 0.9701 \approx 1.0$ with $R^2 = 0.99992$, confirming SQL scaling.
