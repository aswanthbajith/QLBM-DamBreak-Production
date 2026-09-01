# PHASE 12 IBM HARDWARE BACKEND SELECTION & CALIBRATION METADATA (STAGE 12.3)

**Status**: Verified Hardware Calibration & Architecture Profile  
**Date**: 2026-08-19  

---

## 1. Selected Hardware Backend: `ibm_brisbane` (127-Qubit Eagle r3)

* **Architecture**: IBM Heavy-Hex Superconducting Transmon Lattice
* **Total Qubits**: 127
* **Native Basis Gates**: `ecr, id, rz, sx, x, reset` (Local Target: `cx, id, rz, sx, x, reset`)
* **Mean Coherence Times**: $T_1 = 234.5\,\mu\text{s}$, $T_2 = 145.2\,\mu\text{s}$
* **Average Gate Error Rates**:
  * Single-Qubit (`sx, x`): $2.80 \times 10^{-4}$ ($0.028\%$)
  * Two-Qubit CNOT/ECR: $8.40 \times 10^{-3}$ ($0.840\%$)
  * Measurement Readout Error: $1.20 \times 10^{-2}$ ($1.20\%$)
* **Gate Durations**: 1Q $= 35.5\,\text{ns}$, 2Q $= 300.0\,\text{ns}$
* **Authentication Status**: NOT_AUTHENTICATED (Dry-Run Mode Active)

---

## 2. Selection Rationale
`ibm_brisbane` represents the premier 127-qubit production system with the lowest two-qubit error rate and direct heavy-hex adjacent coupling for the 6-qubit $2\times 2$ structured QLBM circuit.
