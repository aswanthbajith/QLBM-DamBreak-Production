# PHASE 12 COMPREHENSIVE QUANTUM CIRCUIT INVENTORY (STAGE 12.2)

**Status**: Verified Complete Registry of Classical, Simulated, Transpiled & Hardware Quantum Circuits  
**Date**: 2026-08-19  

---

## 1. Master Circuit Classification Registry

| Circuit Identifier | File Lineage | Qubits | Clbits | Transpiled CX | Depth | Classification | Hardware Readiness | Real-QPU Execution Status |
| :--- | :--- | :--- | :--- | :--- | :--- | :--- | :--- | :--- |
| **`QC_01_DENSE_U_A`** | `quantum/block_encoding.py` | $1+\lceil\log_2 D_C\rceil$ | 0 | 2 to $2.5\times 10^6$ | 12 to $1.5\times 10^6$ | **CLASSICAL_DENSE_DILATION** | 2Q NISQ / 13Q FTQC | **DRY_RUN_VALIDATED** |
| **`QC_02_DENSE_QSVT`** | `quantum/qsvt_solver.py` | $1+\lceil\log_2 D_C\rceil$ | 0 | 6 to $10\times 10^6$ | 15 to $5\times 10^6$ | **CPU_EMULATION_ACCELERATOR** | 2Q NISQ / 13Q FTQC | **DRY_RUN_VALIDATED** |
| **`QC_03_STRUCT_STREAM`** | `PHASE11_STREAMING_ORACLE.py` | 6 | 0 | **4** | **3** | **STRUCTURED_ORACLE** | **HARDWARE_READY** | **DRY_RUN_VALIDATED** |
| **`QC_04_STRUCT_COLL`** | `PHASE11_STRUCTURED_QSVT.py` | 2 | 0 | **2** | **8** | **STRUCTURED_ORACLE** | **HARDWARE_READY** | **DRY_RUN_VALIDATED** |
| **`QC_05_STRUCT_QSVT`** | `PHASE11_STRUCTURED_QSVT.py` | 3 | 0 | **4** | **15** | **STRUCTURED_ORACLE** | **HARDWARE_READY** | **DRY_RUN_VALIDATED** |
| **`QC_06_STRUCT_E2E_2X2`**| `scripts/run_phase11_batch3.py`| 6 | 6 | **4** | **9** | **STRUCTURED_ORACLE** | **PRIMARY_TARGET** | **DRY_RUN_VALIDATED** |
| **`QC_07_STRUCT_LCU_4X2`**| `PHASE11_SCALING_ANALYSIS.md` | 13 | 0 | **34** | **42** | **STRUCTURED_ORACLE** | **NISQ_ACCESSIBLE** | **COMPILED_ONLY** |

See [`PHASE12_COMPLETE_CIRCUIT_INVENTORY.csv`](PHASE12_COMPLETE_CIRCUIT_INVENTORY.csv) for full attribute columns.
