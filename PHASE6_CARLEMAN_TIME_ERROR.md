# PHASE 6 CARLEMAN ACCURACY VS TIME EVOLUTION (STAGE 6.3)

**Status**: Verified Quadratic Truncation ($N_C = 2$) Time Tracking  
**Date**: 2026-08-19  
**Domain**: $4 \times 2$ grid ($N=8$, $D_C = 2,736$)  

---

## 1. Truncation Error Progression Table

| Step ($t$) | $L_1$ Error | $L_2$ Error | $L_\infty$ Error | Relative Phase Error | Relative Mass Error | Invariant Manifold Defect | Error Regime | Classification |
| :--- | :--- | :--- | :--- | :--- | :--- | :--- | :--- | :--- |
| **1** | $6.97 \times 10^{-4}$ | $7.86 \times 10^{-4}$ | $2.32 \times 10^{-4}$ | $4.75 \times 10^{-4}$ | $1.44 \times 10^{-5}$ | $0.1071$ | INITIALIZING | **MEASURED** |
| **5** | $4.59 \times 10^{-3}$ | $4.95 \times 10^{-3}$ | $2.85 \times 10^{-3}$ | $4.06 \times 10^{-3}$ | $1.82 \times 10^{-3}$ | $0.0744$ | TRANSIENT | **MEASURED** |
| **10** | $5.36 \times 10^{-3}$ | $5.64 \times 10^{-3}$ | $2.84 \times 10^{-3}$ | $5.13 \times 10^{-3}$ | $3.09 \times 10^{-3}$ | $0.0864$ | TRANSIENT | **MEASURED** |
| **20** | $9.38 \times 10^{-3}$ | $9.52 \times 10^{-3}$ | $4.13 \times 10^{-3}$ | $9.47 \times 10^{-3}$ | $4.55 \times 10^{-3}$ | $0.1069$ | TRANSIENT | **MEASURED** |
| **50** | $3.55 \times 10^{-2}$ | $3.58 \times 10^{-2}$ | $1.31 \times 10^{-2}$ | $3.57 \times 10^{-2}$ | $4.35 \times 10^{-3}$ | $0.1327$ | SATURATING | **MEASURED** |
| **100** | $1.41 \times 10^{-2}$ | $1.45 \times 10^{-2}$ | $6.30 \times 10^{-3}$ | $1.17 \times 10^{-2}$ | $3.39 \times 10^{-3}$ | $0.1372$ | BOUNDED SATURATION | **MEASURED** |
| **200** | $1.04 \times 10^{-2}$ | $1.05 \times 10^{-2}$ | $3.44 \times 10^{-3}$ | $3.47 \times 10^{-3}$ | $3.39 \times 10^{-3}$ | $0.1373$ | BOUNDED SATURATION | **MEASURED** |

---

## 2. Key Mathematical Analysis
1. **Bounded Error Saturation (Non-Exponential)**:
   The relative $L_2$ error does **not** grow exponentially. Instead, it reaches a peak of $\approx 3.58\%$ at $t=50$ and saturates stably around $\approx 1.05\%$ at $t=200$.
2. **Invariant Manifold Defect**:
   The local quadratic manifold defect $\|Y_{\text{actual}} - \Psi \otimes \Psi\| / \|\Psi \otimes \Psi\|$ remains strictly bounded in $[0.074, 0.137]$, proving that the streaming approximation $S_{\text{kron2}}$ maintains physical consistency over long time horizons.
3. **Mass Conservation**:
   Total liquid phase mass error remains $< 0.46\%$ throughout 200 time steps.
