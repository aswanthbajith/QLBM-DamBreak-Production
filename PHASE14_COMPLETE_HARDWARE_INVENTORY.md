# PHASE 14 COMPREHENSIVE FORENSIC HARDWARE CIRCUIT INVENTORY

**Status**: Verified Complete Circuit Registry  
**Date**: 2026-08-19  

---

## 1. Forensic Quantum Circuit Registry

| Source File | Function / Class | Role / Purpose | Qubits | CX Count | Depth | Transpilation Status | Hardware Execution Status |
| :--- | :--- | :--- | :--- | :--- | :--- | :--- | :--- |
| `quantum/block_encoding.py` | `BlockEncodingCSDilation` | Dense CS Unitary Dilation | 8 | 2,150 | 1,840 | Transpiled | **NOT_EXECUTED** |
| `PHASE11_STRUCTURED_QSVT.py` | `build_structured_collision_oracle` | Level 1: 2Q Collision Oracle | 2 | 2 | 8 | Transpiled (Depth 8) | **DRY_RUN_VALIDATED** |
| `PHASE11_STREAMING_ORACLE.py` | `build_d2q9_streaming_circuit` | Level 2: 6Q 2x2 Streaming Permutation | 6 | 4 | 3 | Transpiled (Depth 3) | **DRY_RUN_VALIDATED** |
| `PHASE11_STRUCTURED_QSVT.py` | `build_structured_qsvt_circuit` | Level 3: 3Q QSVT Inversion (d=3) | 3 | 4 | 15 | Transpiled (Depth 15) | **DRY_RUN_VALIDATED** |
| `scripts/run_phase12_batch2.py` | `Primary_2x2_Structured_QLBM` | Level 4: 6Q Complete 2x2 QLBM Step | 6 | 4 | 9 | Transpiled (Depth 9) | **DRY_RUN_VALIDATED** |
| `PHASE11_STRUCTURED_QSVT.py` | `build_13q_4x2_lcu_oracle` | Level 5: 13Q 4x2 Single Step | 13 | 34 | 42 | Transpiled (Depth 42) | **COMPILED_ONLY** |
