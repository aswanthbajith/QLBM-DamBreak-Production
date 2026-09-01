# PHASE 15 COMPLETE FORENSIC QUANTUM CIRCUIT INVENTORY

**Status**: Verified Complete Circuit Registry  
**Date**: 2026-08-19  

---

## 1. Forensic Quantum Circuit Registry

| Circuit ID | Function / Class | Role / Purpose | Logical Qubits | CX Count | Depth | Gate Count | Hardware Status |
| :--- | :--- | :--- | :--- | :--- | :--- | :--- | :--- |
| `QC_15_01_BE_DENSE` | `BlockEncodingCSDilation` | Dense CS Unitary Dilation | 8 | 2,150 | 1,840 | 4,820 | **NOT_EXECUTED** |
| `QC_15_02_COLL_2Q` | `build_structured_collision_oracle` | Level 1: 2Q Collision Oracle | 2 | 2 | 8 | 8 | **DRY_RUN_VALIDATED** |
| `QC_15_03_STREAM_6Q` | `build_d2q9_streaming_circuit` | Level 2: 6Q 2x2 Streaming Permutation | 6 | 4 | 3 | 4 | **DRY_RUN_VALIDATED** |
| `QC_15_04_QSVT_3Q_d3`| `build_structured_qsvt_circuit` | Level 3: 3Q QSVT Inversion (d=3) | 3 | 4 | 15 | 16 | **DRY_RUN_VALIDATED** |
| `QC_15_05_E2E_2X2_6Q`| `Primary_2x2_Structured_QLBM` | Level 4: 6Q Complete 2x2 QLBM Step | 6 | 4 | 9 | 14 | **DRY_RUN_VALIDATED** |
| `QC_15_06_LCU_4X2_13Q`| `build_13q_4x2_lcu_oracle` | Level 5: 13Q 4x2 Single Step | 13 | 34 | 42 | 146 | **COMPILED_ONLY** |
