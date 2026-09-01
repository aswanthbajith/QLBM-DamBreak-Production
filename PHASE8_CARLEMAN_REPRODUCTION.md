# PHASE 8 CARLEMAN LINEARIZATION REPRODUCTION REPORT (STAGE 8.5)

**Status**: Verified Quadratic Carleman Stability  
**Date**: 2026-08-19  

---

## 1. Multi-Step Carleman Error Reproduction Table

| Step ($t$) | $L_1$ Error | $L_2$ Error | $L_\infty$ Error | Relative Mass Error | Manifold Defect | Stability Status |
| :--- | :--- | :--- | :--- | :--- | :--- | :--- |
| **1** | $6.97 \times 10^{-4}$ | $7.86 \times 10^{-4}$ | $2.32 \times 10^{-4}$ | $1.44 \times 10^{-5}$ | $0.1071$ | **STABLY_BOUNDED** |
| **5** | $4.59 \times 10^{-3}$ | $4.95 \times 10^{-3}$ | $2.85 \times 10^{-3}$ | $1.82 \times 10^{-3}$ | $0.0744$ | **STABLY_BOUNDED** |
| **10** | $5.36 \times 10^{-3}$ | $5.64 \times 10^{-3}$ | $2.84 \times 10^{-3}$ | $3.09 \times 10^{-3}$ | $0.0864$ | **STABLY_BOUNDED** |
| **20** | $9.38 \times 10^{-3}$ | $9.52 \times 10^{-3}$ | $4.13 \times 10^{-3}$ | $4.55 \times 10^{-3}$ | $0.1069$ | **STABLY_BOUNDED** |
| **50** | $3.55 \times 10^{-2}$ | $3.58 \times 10^{-2}$ | $1.31 \times 10^{-2}$ | $4.35 \times 10^{-3}$ | $0.1327$ | **STABLY_BOUNDED** |
| **100** | $1.41 \times 10^{-2}$ | $1.45 \times 10^{-2}$ | $6.30 \times 10^{-3}$ | $3.39 \times 10^{-3}$ | $0.1372$ | **STABLY_BOUNDED** |
| **200** | $1.04 \times 10^{-2}$ | $1.05 \times 10^{-2}$ | $3.44 \times 10^{-3}$ | $3.39 \times 10^{-3}$ | $0.1373$ | **STABLY_BOUNDED** |

---

## 2. Non-Divergence Confirmation
The quadratic Carleman truncation does not suffer from secular exponential growth, remaining stably bounded at $\approx 1.05\%$ over 200 time steps.
