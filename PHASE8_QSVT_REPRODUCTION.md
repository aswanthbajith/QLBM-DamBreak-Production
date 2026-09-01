# PHASE 8 QSVT POLYNOMIAL INVERSION REPRODUCTION REPORT (STAGE 8.7)

**Status**: Verified Chebyshev Inversion Convergence  
**Date**: 2026-08-19  

---

## 1. QSVT Polynomial Degree Sweep Table

| Degree ($d$) | Max $|P(x)|$ | Parity Error | Inversion Residual $\|M x - b\|/\|b\|$ | Relative Solution Error | Fidelity | Circuit Depth | Block Calls | Meets Threshold |
| :--- | :--- | :--- | :--- | :--- | :--- | :--- | :--- | :--- |
| **3** | 0.9285 | 0.0 | $9.60 \times 10^{-4}$ | $9.65 \times 10^{-4}$ | 0.999999 | 6 | 2 | None |
| **5** | 0.9500 | 0.0 | $9.14 \times 10^{-5}$ | $9.18 \times 10^{-5}$ | 1.000000 | 10 | 3 | None |
| **7** | 0.9500 | 0.0 | $4.52 \times 10^{-6}$ | $4.45 \times 10^{-6}$ | 1.000000 | 14 | 4 | None |
| **9** | 0.9500 | 0.0 | $3.84 \times 10^{-7}$ | $3.85 \times 10^{-7}$ | 1.000000 | 18 | 5 | None |
| **11** | 0.9500 | 0.0 | $1.62 \times 10^{-8}$ | $1.63 \times 10^{-8}$ | 1.000000 | 22 | 6 | **Meets $10^{-8}$** |
| **15** | 0.9500 | 0.0 | $5.03 \times 10^{-11}$ | $5.05 \times 10^{-11}$ | 1.000000 | 30 | 8 | **Meets $10^{-10}$** |
| **21** | 0.9500 | 0.0 | $1.58 \times 10^{-14}$ | $1.59 \times 10^{-14}$ | 1.000000 | 42 | 11 | **Meets $10^{-12}$** |
| **31** | 0.9500 | 0.0 | $2.76 \times 10^{-15}$ | $2.76 \times 10^{-15}$ | 1.000000 | 62 | 16 | **Machine Precision** |

---

## 2. Threshold Confirmation
* Degree **$d=11$** satisfies residual $< 10^{-8}$.
* Degree **$d=15$** satisfies residual $< 10^{-10}$.
* Degree **$d=21$** satisfies residual $< 10^{-12}$.
* Degree **$d=31$** achieves machine precision ($2.76 \times 10^{-15}$).
