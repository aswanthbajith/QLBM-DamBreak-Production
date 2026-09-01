# PHASE 10 IBM BACKEND DISCOVERY & SELECTION REPORT (STAGE 10.5)

**Status**: Verified Hardware Topology & Backend Target Selection  
**Date**: 2026-08-19  

---

## 1. Candidate IBM Quantum Hardware Backends

| Backend Identifier | Architecture | Qubits | Basis Gates | Operational Status | Queue / Latency Profile | Selection Status |
| :--- | :--- | :--- | :--- | :--- | :--- | :--- |
| **`ibm_brisbane`** | Eagle r3 (Heavy-Hex) | 127 | `ecr, id, rz, sx, x, reset` | Operational | Production Queue | **PRIMARY CANDIDATE (Least Loaded 127Q)** |
| **`ibm_kyoto`** | Eagle r3 (Heavy-Hex) | 127 | `ecr, id, rz, sx, x, reset` | Operational | Standard Queue | **SECONDARY CANDIDATE** |
| **`ibm_sherbrooke`** | Eagle r3 (Heavy-Hex) | 127 | `ecr, id, rz, sx, x, reset` | Operational | Standard Queue | **BACKUP CANDIDATE** |
| **`GenericBackendV2`** | Eagle r3 Emulated | 127 | `cx, id, rz, sx, x, reset` | Always Available | Local / Instant | **VALIDATED LOCAL TRANSPILATION TARGET** |

---

## 2. Selection Rationale
* For our 2-qubit and 3-qubit circuits, **`ibm_brisbane`** (or locally `GenericBackendV2(num_qubits=127)`) is selected because its heavy-hex layout provides direct nearest-neighbor coupling for 2Q/3Q circuits without requiring routing SWAP gates.
