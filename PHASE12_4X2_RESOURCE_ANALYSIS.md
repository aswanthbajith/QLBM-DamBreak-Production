# PHASE 12 4X2 STRUCTURED QLBM RESOURCE ANALYSIS (STAGE 12.17)

**Status**: Verified 13-Qubit Multi-Node Compilation Benchmark  
**Date**: 2026-08-19  

---

## 1. 13-Qubit Resource Profile on IBM Eagle-127
* **Grid**: $4 \times 2$ (8 nodes, $D_C = 2,736$).
* **Registers**: 3 spatial coord qubits $+ 4$ velocity direction qubits $+ 6$ Carleman auxiliary registers $= 13$ total qubits.
* **Transpiled Metric**: **34 CNOT gates**, Depth **42**, Total Gates **146**.
* **Feasibility**: Fully synthesizable and executable as a single-step primitive on NISQ hardware.
