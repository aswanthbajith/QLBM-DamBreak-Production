# PHASE 10 HARDWARE TRANSPILATION & CIRCUIT VALIDATION (STAGE 10.7 & 10.8)

**Status**: Verified Transpilation on IBM Eagle-127 Heavy-Hex Target  
**Date**: 2026-08-19  

---

## 1. Transpilation Metrics Table

| Circuit Name | Logical Qubits | Physical Qubits | Orig Depth | Transpiled Depth | Total Gates | CX Gates | 1Q Gates (`rz, sx, x`) | SWAPs | Equivalence Status |
| :--- | :--- | :--- | :--- | :--- | :--- | :--- | :--- | :--- | :--- |
| **`01_block_encoding_demo`** | 2 | 127 | 1 | 12 | 18 | 2 | 16 | 0 | **EXACT_VALIDATED** |
| **`02_qsvt_demo_deg3`** | 2 | 127 | 6 | 15 | 26 | 2 | 24 | 0 | **EXACT_VALIDATED** |
| **`03_measurement_demo`** | 2 | 127 | 5 | 7 | 7 | 2 | 3 | 0 | **EXACT_VALIDATED** |
| **`05_qae_scalar_demo`** | 3 | 127 | 7 | 12 | 18 | 4 | 13 | 0 | **EXACT_VALIDATED** |

---

## 2. Structural Routing Analysis
* **Zero Routing Overhead**: Because the demonstration circuits use 2 to 3 contiguous qubits, Qiskit maps them to adjacent physical qubits on the heavy-hex lattice, requiring **0 SWAP gates**.
* **Mathematical Equivalence**: Transpiled statevectors and probability distributions match ideal untranspiled circuits to within machine precision ($< 10^{-15}$).
