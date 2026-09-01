# PHASE 8 QUANTUM AMPLITUDE ESTIMATION (QAE) OBSERVABLE READINESS ANALYSIS (STAGE 8.12)

**Status**: Verified Circuit Architecture & Readiness Classification  
**Date**: 2026-08-19  

---

## 1. Observable QAE Design & Readiness Matrix

| Observable | Mathematical Integral | Target Quantum Subspace | Oracle Operator $\mathcal{A}$ | QAE Queries ($1/\epsilon$) | Expected Qubits | Circuit Depth | Readiness Level |
| :--- | :--- | :--- | :--- | :--- | :--- | :--- | :--- |
| **Total Liquid Mass ($M$)** | $\int_\Omega \phi(\mathbf{x}) d\mathbf{x}$ | $\sum_{q=0}^8 |h_q(\mathbf{x})\rangle$ | Projector on phase distributions | $\mathcal{O}(1/\epsilon)$ | $n_{\text{tot}} + n_{\text{qae}} \approx 35$ | $\mathcal{O}(d / \epsilon)$ | **READY FOR CIRCUIT DESIGN** |
| **Kinetic Energy ($E_k$)** | $\frac{1}{2}\int \rho |\mathbf{u}|^2 d\mathbf{x}$ | Dual-register $|\Psi \otimes \Psi\rangle$ | Quadratic tensor contraction | $\mathcal{O}(1/\epsilon)$ | $2 n_{\text{tot}} + n_{\text{qae}} \approx 60$ | $\mathcal{O}(d / \epsilon)$ | **READY FOR CIRCUIT DESIGN** |
| **Wall Impact Force ($F_{\text{wall}}$)** | $\sum_{y} p(x_{\text{wall}}, y)$ | Boundary momentum modes | Projector on $x = x_{\text{wall}}$ | $\mathcal{O}(1/\epsilon)$ | $n_{\text{tot}} + n_{\text{qae}} \approx 35$ | $\mathcal{O}(d / \epsilon)$ | **READY FOR CIRCUIT DESIGN** |

---

## 2. Hardware Prerequisites for QAE Execution
* **Coherence Time**: QAE requires circuit depths scaling as $\mathcal{O}(d / \epsilon) \sim 10^4 - 10^6$ coherent gates, requiring active fault-tolerant quantum error correction (QEC).
* **Current Status**: Classified as **THEORETICAL / READY FOR CIRCUIT DESIGN**; no physical QAE execution has been performed.
