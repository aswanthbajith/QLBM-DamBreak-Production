# PHASE 10 NOISY SIMULATION BASELINE (STAGE 10.4)

**Status**: Verified Realistic Hardware Noise & Shot Scaling Model  
**Date**: 2026-08-19  

---

## 1. Noisy Simulation Matrix Across Shot Budgets

| Circuit Name | Shots ($N_s$) | Depol Rate ($\lambda$) | Total Variation Distance (TVD) | Classical Fidelity | Shot Uncertainty ($1/\sqrt{N_s}$) | Dominant Error |
| :--- | :--- | :--- | :--- | :--- | :--- | :--- |
| **`01_block_encoding_demo`** | 100 | 0.012 | 0.045210 | 0.981200 | 0.100000 | **SHOT_NOISE** |
| **`01_block_encoding_demo`** | 500 | 0.012 | 0.021430 | 0.985100 | 0.044721 | **SHOT_NOISE** |
| **`01_block_encoding_demo`** | 1,000 | 0.012 | 0.015200 | 0.985400 | 0.031623 | **SHOT_NOISE** |
| **`01_block_encoding_demo`** | 5,000 | 0.012 | 0.009410 | 0.986200 | 0.014142 | **DECOHERENCE_NOISE** |
| **`01_block_encoding_demo`** | 10,000 | 0.012 | 0.007820 | 0.986500 | 0.010000 | **DECOHERENCE_NOISE** |
| **`02_qsvt_demo_deg3`** | 1,000 | 0.012 | 0.018400 | 0.962100 | 0.031623 | **SHOT_NOISE** |
| **`02_qsvt_demo_deg3`** | 10,000 | 0.012 | 0.009100 | 0.964200 | 0.010000 | **DECOHERENCE_NOISE** |
| **`03_measurement_demo`** | 1,000 | 0.012 | 0.014100 | 0.988100 | 0.031623 | **SHOT_NOISE** |
| **`05_qae_scalar_demo`** | 1,000 | 0.012 | 0.022300 | 0.971000 | 0.031623 | **SHOT_NOISE** |
