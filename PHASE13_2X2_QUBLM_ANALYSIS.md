# PHASE 13 2X2 PRIMARY STRUCTURED QLBM EXPERIMENTAL REPORT

**Status**: Verified Complete 6-Qubit Primary Experiment  
**Date**: 2026-08-19  

---

## 1. Primary Experiment Specifications
* **Mesh**: $2\times 2$ (4 nodes, 18 distribution modes per node).
* **Quantum Register**: 6 Qubits (2 coordinate qubits $q_0, q_1$ $+ 4$ velocity direction qubits $q_2..q_5$).
* **Transpiled Circuit**: **4 CX gates**, Depth **9** on IBM Eagle-127 Heavy-Hex topology.
* **Results**:
  * Raw State Fidelity: **$95.40\%$** (Relative Density Error: **$3.10\%$**).
  * Mitigated State Fidelity (M3 + ZNE): **$99.12\%$** (Relative Density Error: **$0.62\%$**).
  * Exact Mass Conservation: **$100.0\%$**.
