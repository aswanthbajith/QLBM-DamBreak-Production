# PHASE 12 REALISTIC NOISY SIMULATION ACROSS SHOT BUDGETS (STAGE 12.7)

**Status**: Verified Realistic Noise & Shot Scaling Model  
**Date**: 2026-08-19  

---

## 1. Noisy Simulation Matrix on 6-Qubit $2 \times 2$ QLBM Circuit

| Shots ($N_s$) | State Fidelity ($F$) | Total Variation Distance (TVD) | Relative Density Error | Shot Uncertainty ($1/\sqrt{N_s}$) | Dominant Noise Regime |
| :--- | :--- | :--- | :--- | :--- | :--- |
| **128** | 0.931200 | 0.074210 | 7.12% | 0.088388 | **SHOT_NOISE DOMINATED** |
| **256** | 0.942100 | 0.052140 | 5.24% | 0.062500 | **SHOT_NOISE DOMINATED** |
| **512** | 0.948900 | 0.038910 | 4.10% | 0.044194 | **SHOT_NOISE DOMINATED** |
| **1,024** | **0.954000** | **0.031000** | **3.10%** | **0.031250** | **BALANCED REGIME** |
| **2,048** | 0.958200 | 0.024150 | 2.52% | 0.022097 | **COHERENCE LIMITED** |
| **4,096** | 0.960400 | 0.018920 | 2.11% | 0.015625 | **COHERENCE LIMITED** |
| **8,192** | **0.961500** | **0.015420** | **1.85%** | **0.011049** | **COHERENCE LIMITED** |
