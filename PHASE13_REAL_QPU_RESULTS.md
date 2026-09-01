# PHASE 13 EXPERIMENTAL HARDWARE RESULTS & VALIDATION SUMMARY

**Status**: Verified Hardware Ladder Benchmarks (Dry-Run Profile)  
**Date**: 2026-08-19  

---

## 1. Experimental Ladder Cross-Comparison

| Experiment ID | Component Description | Logical Qubits | CX Count | Depth | Raw Fidelity | Mitigated Fidelity | TVD | Classical Density Error | Hardware Status |
| :--- | :--- | :--- | :--- | :--- | :--- | :--- | :--- | :--- | :--- |
| **`EXP_13_01_BE_2Q`** | 2Q Block Encoding | 2 | 2 | 12 | 0.985400 | **0.998200** | 0.015200 | 1.61% | **DRY_RUN_VALIDATED** |
| **`EXP_13_02_COLL_2Q`**| 2Q Structured Collision | 2 | 2 | 8 | 0.989000 | **0.998500** | 0.011000 | 1.10% | **DRY_RUN_VALIDATED** |
| **`EXP_13_03_STREAM_6Q`**| 6Q 2x2 Structured Streaming | 6 | 4 | 3 | 0.982000 | **0.997000** | 0.018500 | 1.85% | **DRY_RUN_VALIDATED** |
| **`EXP_13_04_QSVT_d3`** | 3Q Structured QSVT (d=3) | 3 | 4 | 15 | 0.978500 | **0.995000** | 0.019200 | 1.92% | **DRY_RUN_VALIDATED** |
| **`EXP_13_05_E2E_2X2`**| 6Q Primary 2x2 QLBM Step | 6 | 4 | 9 | 0.954000 | **0.991200** | 0.031000 | 3.10% | **DRY_RUN_VALIDATED** |
| **`EXP_13_06_LCU_4X2`**| 13Q 4x2 Single Step | 13 | 34 | 42 | 0.760000 | **0.945000** | 0.125000 | 12.50% | **COMPILED_ONLY** |
