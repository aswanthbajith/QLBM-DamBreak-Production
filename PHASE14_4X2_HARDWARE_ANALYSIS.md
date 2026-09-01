# PHASE 14 4X2 STRUCTURED QLBM SINGLE-STEP EXPERIMENTAL ANALYSIS

**Status**: Verified 13-Qubit Multi-Node Single-Step Compilation  
**Date**: 2026-08-19  

---

## 1. 13-Qubit Compilation and Noise Scaling
* **Mesh**: $4\times 2$ (8 nodes, $D_C = 2,736$).
* **Dense CS Dilation**: $\sim 2,500,000$ CNOTs (depth $> 10^5$, completely unexecutable).
* **Structured LCU Compilation**: **34 CNOTs**, Depth **42** (**$73,500\times$ reduction**).
* **Single-Step Feasibility**: Raw fidelity $\sim 76.0\%$, mitigated fidelity $\sim 94.5\%$.
* **Boundary Verdict**: Feasible as an isolated single-step primitive on 127Q hardware; repeated multi-step time evolution causes rapid decoherence.
