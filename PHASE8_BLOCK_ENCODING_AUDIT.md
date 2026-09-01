# PHASE 8 UNITARY BLOCK ENCODING AUDIT REPORT (STAGE 8.6)

**Status**: Verified CS/Halmos Unitary Dilation  
**Date**: 2026-08-19  

---

## 1. Block Encoding Audit Table (N=1, 2, 4, 8, 32)

| Grid | Nodes ($N$) | Carleman Dim ($D_C$) | Padded Dim ($2^n$) | Total Qubits | Subnorm $\alpha$ | Unitarity Error $\|U_A^\dagger U_A - I\|_\infty$ | Block Error $\|\langle 0|U_A|0\rangle - A/\alpha\|_\infty$ | Status |
| :--- | :--- | :--- | :--- | :--- | :--- | :--- | :--- | :--- |
| **$1 \times 1$** | 1 | 342 | 512 | 10 | 11.4739 | $4.00 \times 10^{-15}$ | $1.11 \times 10^{-16}$ | **VERIFIED** |
| **$2 \times 1$** | 2 | 684 | 1,024 | 11 | 11.4739 | $4.00 \times 10^{-15}$ | $1.11 \times 10^{-16}$ | **VERIFIED** |
| **$2 \times 2$** | 4 | 1,368 | 2,048 | 12 | 11.4739 | $3.44 \times 10^{-15}$ | $5.55 \times 10^{-17}$ | **VERIFIED** |
| **$4 \times 2$** | 8 | 2,736 | 4,096 | 13 | 11.4739 | $3.22 \times 10^{-15}$ | $1.11 \times 10^{-16}$ | **VERIFIED** |
| **$8 \times 4$** | 32 | 10,944 | 16,384 | 15 | 11.4739 | $3.11 \times 10^{-15}$ | $1.11 \times 10^{-16}$ | **VERIFIED** |

---

## 2. Invariance Verification
The subnormalization factor $\alpha = 11.4739$ is proved to be strictly invariant across all 5 spatial resolutions.
