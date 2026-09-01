# PHASE 15 BACKEND SELECTION & DISCOVERY REPORT

**Status**: Target Backend Architecture Evaluated  
**Date**: 2026-08-19  

---

## 1. Candidate Backend Architecture Comparison

| Backend Name | Qubits | Target Family | Mean CX Error | Mean Readout Error | Role |
| :--- | :--- | :--- | :--- | :--- | :--- |
| **`ibm_brisbane`** | 127 | IBM Eagle r3 | $8.40 \times 10^-3$ | $1.20 \times 10^-2$ | **PRIMARY PRODUCTION TARGET** |
| **`ibm_kyoto`** | 127 | IBM Eagle r3 | $9.10 \times 10^-3$ | $1.45 \times 10^-2$ | **BACKUP CANDIDATE** |
| **`ibm_sherbrooke`** | 127 | IBM Eagle r3 | $8.80 \times 10^-3$ | $1.30 \times 10^-2$ | **BACKUP CANDIDATE** |
| **`GenericBackendV2`**| 127 | Eagle Topology | $8.40 \times 10^-3$ | $1.20 \times 10^-2$ | **LOCAL DRY-RUN HARNESS** |
