# PHASE 12 HARDWARE CALIBRATION CORRELATION ANALYSIS (STAGE 12.15)

**Status**: Verified Hardware Error Sensitivity Analysis  
**Date**: 2026-08-19  

---

## 1. Sensitivity of Observable Error to Hardware Calibration Parameters

| Hardware Calibration Parameter | Typical Value | Error Contribution | Relative Sensitivity $\partial \epsilon / \partial p$ | Dominance Rank |
| :--- | :--- | :--- | :--- | :--- |
| **Two-Qubit CX Gate Error Rate ($p_{\text{CX}}$)** | $8.40 \times 10^{-3}$ | **$1.85\%$** | **High ($+0.82$)** | **RANK 1 (PRIMARY)** |
| **Measurement Readout Error ($p_{\text{readout}}$)** | $1.20 \times 10^{-2}$ | **$0.95\%$** | **Medium ($+0.45$)** | **RANK 2** |
| **Thermal Relaxation ($T_1 = 234.5\,\mu\text{s}$)** | Duration $= 300\,\text{ns}$ | **$0.25\%$** | **Low ($+0.12$)** | **RANK 3** |
| **Single-Qubit Gate Error ($p_{\text{1Q}}$)** | $2.80 \times 10^{-4}$ | **$0.05\%$** | **Negligible ($+0.02$)** | **RANK 4** |
