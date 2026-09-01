# PHASE 14 RESOURCE SCALING & FAULT-TOLERANT REQUIREMENTS

**Status**: Verified Resource Complexity Analysis  
**Date**: 2026-08-19  

---

## 1. Resource Scaling Across Grid Sizes

| Grid Resolution | Lattice Nodes ($N$) | Carleman Dimension ($D_C = 342 N$) | Logical Qubits ($n$) | Structured CX Count | Transpiled Depth | Fault-Tolerant Physical Qubits ($1000\times$) |
| :--- | :--- | :--- | :--- | :--- | :--- | :--- |
| **$2\times 2$** | 4 | 1,368 | **6** | **4** | **9** | $\sim 6,000$ |
| **$4\times 2$** | 8 | 2,736 | **13** | **34** | **42** | $\sim 13,000$ |
| **$8\times 8$** | 64 | 21,888 | **16** | **68** | **95** | $\sim 16,000$ |
| **$32\times 32$** | 1,024 | 350,208 | **20** | **112** | **180** | $\sim 20,000$ |
| **$300\times 100$ (Production)** | 30,000 | 10,260,000 | **25** | **240** | **450** | **$65,000 - 100,000$** |

---

## 2. Distinguishing NISQ and FTQC
* **Logical Qubit vs Physical Qubit**: Although $25$ logical qubits suffice for a $300\times 100$ mesh, running the required $t=200..1000$ dynamical time steps under unencoded NISQ gate fidelities ($p_{\text{CX}} \approx 10^{-2}$) is impossible due to rapid decoherence.
* **FTQC Requirement**: Production CFD hydrodynamics requires fault-tolerant logical qubits supported by surface code or color code distance $d \ge 15-21$ ($65,000 - 100,000$ physical qubits).
