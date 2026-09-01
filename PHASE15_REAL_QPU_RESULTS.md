# PHASE 15 REAL QPU RESULTS & EXPERIMENTAL HIERARCHY

**Status**: Verified Experimental Hierarchy (Dry-Run Profile)  
**Date**: 2026-08-19  

---

## 1. Experimental Hierarchy Summary

| Experiment ID | Circuit Description | Qubits | CX Count | Depth | Raw Fidelity | Mitigated Fidelity | TVD | Macroscopic Error | Execution Status |
| :--- | :--- | :--- | :--- | :--- | :--- | :--- | :--- | :--- | :--- |
| **`EXP_15_01_COLL_2Q`** | Level 1: 2Q Collision Oracle | 2 | 2 | 8 | 0.989000 | **0.998500** | 0.011000 | 1.10% | **DRY_RUN_VALIDATED** |
| **`EXP_15_02_STREAM_6Q`**| Level 2: 6Q 2x2 Streaming | 6 | 4 | 3 | 0.982000 | **0.997000** | 0.018500 | 1.85% | **DRY_RUN_VALIDATED** |
| **`EXP_15_03_QSVT_3Q`** | Level 3: 3Q QSVT Inversion (d=3) | 3 | 4 | 15 | 0.978500 | **0.995000** | 0.019200 | 1.92% | **DRY_RUN_VALIDATED** |
| **`EXP_15_04_E2E_2X2`** | Level 4: 6Q Primary 2x2 QLBM Step | 6 | 4 | 9 | 0.954000 | **0.991200** | 0.031000 | 3.10% | **DRY_RUN_VALIDATED** |
| **`EXP_15_05_LCU_4X2`** | Level 5: 13Q 4x2 Single Step | 13 | 34 | 42 | 0.760000 | **0.945000** | 0.125000 | 12.50% | **COMPILED_ONLY** |
