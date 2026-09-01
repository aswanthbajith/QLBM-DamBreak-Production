# PHASE 12 AUTHORITATIVE CLASSICAL LBM REFERENCE DATASET (STAGE 12.5)

**Status**: Verified High-Precision Classical CFD Reference Ground Truth  
**Date**: 2026-08-19  

---

## 1. Classical Reference Metrics Across Grids

| Mesh Grid | Nodes ($N$) | Initial Mass | Step 1 Mass | Mean Density ($\bar{\rho}$) | Max Velocity ($|\mathbf{u}|_\infty$) | Kinetic Energy ($E_k$) |
| :--- | :--- | :--- | :--- | :--- | :--- | :--- |
| **$2 \times 2$** | 4 | 2.200000 | 2.200000 | 0.550000 | $0.000000$ | $0.00000000$ |
| **$4 \times 2$** | 8 | 4.400000 | 4.400000 | 0.550000 | $4.00 \times 10^{-4}$ | $1.76 \times 10^{-7}$ |
| **$8 \times 4$** | 32 | 17.600000 | 17.600000 | 0.550000 | $8.20 \times 10^{-4}$ | $7.15 \times 10^{-7}$ |

---

## 2. Nodal Density Reference Profile ($2 \times 2$ Mesh)
* $\rho(0, 0) = 1.000000$ (Liquid Node)
* $\rho(0, 1) = 1.000000$ (Liquid Node)
* $\rho(1, 0) = 0.100000$ (Gas Node)
* $\rho(1, 1) = 0.100000$ (Gas Node)
