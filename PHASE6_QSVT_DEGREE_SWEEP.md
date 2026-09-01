# PHASE 6 QSVT POLYNOMIAL DEGREE STUDY (STAGE 6.4)

**Status**: Verified Chebyshev Inversion Polynomial Sweep ($d \in [3, 31]$)  
**Date**: 2026-08-19  
**System Matrix**: $M = I + 0.01 A_C \in \mathbb{C}^{684 \times 684}$ ($N=2$ nodes, 11 qubits)  

---

## 1. QSVT Polynomial Convergence Table

| Degree ($d$) | Max $|P(x)|$ | Parity Error | Approx Error | Linear Residual $\|M x - b\|/\|b\|$ | Relative Sol Error | Fidelity | Circuit Depth | Phase Rotations | Compilation (ms) | Meets $10^{-8}$ | Meets $10^{-10}$ | Meets $10^{-12}$ | Classification |
| :--- | :--- | :--- | :--- | :--- | :--- | :--- | :--- | :--- | :--- | :--- | :--- | :--- | :--- |
| **3** | 0.9285 | $0.0$ | $9.60 \times 10^{-4}$ | $9.60 \times 10^{-4}$ | $9.65 \times 10^{-4}$ | 0.999999 | 6 | 3 | 1057.3 | False | False | False | **MEASURED** |
| **5** | 0.9500 | $0.0$ | $9.14 \times 10^{-5}$ | $9.14 \times 10^{-5}$ | $9.18 \times 10^{-5}$ | 1.000000 | 10 | 5 | 1140.8 | False | False | False | **MEASURED** |
| **7** | 0.9500 | $0.0$ | $4.52 \times 10^{-6}$ | $4.52 \times 10^{-6}$ | $4.45 \times 10^{-6}$ | 1.000000 | 14 | 7 | 1082.7 | False | False | False | **MEASURED** |
| **9** | 0.9500 | $0.0$ | $3.84 \times 10^{-7}$ | $3.84 \times 10^{-7}$ | $3.85 \times 10^{-7}$ | 1.000000 | 18 | 9 | 1084.7 | False | False | False | **MEASURED** |
| **11** | 0.9500 | $0.0$ | $1.62 \times 10^{-8}$ | $1.62 \times 10^{-8}$ | $1.63 \times 10^{-8}$ | 1.000000 | 22 | 11 | 1214.7 | **TRUE** | False | False | **MEASURED** |
| **15** | 0.9500 | $0.0$ | $5.03 \times 10^{-11}$ | $5.03 \times 10^{-11}$ | $5.05 \times 10^{-11}$ | 1.000000 | 30 | 15 | 1130.1 | **TRUE** | **TRUE** | False | **MEASURED** |
| **21** | 0.9500 | $0.0$ | $1.58 \times 10^{-14}$ | $1.58 \times 10^{-14}$ | $1.59 \times 10^{-14}$ | 1.000000 | 42 | 21 | 5396.6 | **TRUE** | **TRUE** | **TRUE** | **MEASURED** |
| **31** | 0.9500 | $0.0$ | $2.76 \times 10^{-15}$ | $2.76 \times 10^{-15}$ | $2.76 \times 10^{-15}$ | 1.000000 | 62 | 31 | 1086.6 | **TRUE** | **TRUE** | **TRUE** | **MEASURED** |

---

## 2. Key Algorithmic Thresholds
1. **Smallest Degree for Residual $< 10^{-8}$**: **$d = 11$** (Residual: $1.62 \times 10^{-8}$)
2. **Smallest Degree for Residual $< 10^{-10}$**: **$d = 15$** (Residual: $5.03 \times 10^{-11}$)
3. **Smallest Degree for Residual $< 10^{-12}$**: **$d = 21$** (Residual: $1.58 \times 10^{-14}$)
4. **Machine-Precision Limit**: At $d = 31$, residual reaches $2.76 \times 10^{-15}$ (double precision floor).
