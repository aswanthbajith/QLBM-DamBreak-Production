# PHASE F16: ROUTE D — FULLY REVERSIBLE NONLINEAR COLLISION CIRCUIT
## Unitary Embedding $|f, g\rangle |0\rangle \to |f^*, g^*\rangle |0\rangle$ with Deterministic Autonomy

**Document**: Reversible Collision Circuit Specification  
**Project**: Quantum Lattice Boltzmann Method (QLBM) for Two-Phase Flow  
**Repository**: `/home/aswa/Research/QLBM-DamBreak-Production`  
**Branch**: `feature/direct-encoding-two-phase-qlbm`  
**Date**: September 2026  

---

## 1. Unitary Node Transformation

$$U_{\text{coll}} \left( |\mathbf{f}\rangle \otimes |\mathbf{g}\rangle \otimes |0\rangle_{\text{work}} \right) = |\mathbf{f}^*\rangle \otimes |\mathbf{g}^*\rangle \otimes |0\rangle_{\text{work}}$$

- **Zero Garbage Qubits**: All intermediate work registers ($|\rho\rangle, |\alpha\rangle, |\mathbf{u}\rangle, |\mathbf{f}^{\text{eq}}\rangle$) are uncomputed back to $|0\rangle$ via mirror circuits.
- **Exact Unitary Multi-Step Evolution**: Because $U_{\text{coll}}$ is an exact discrete reversible bijection, $(U_{\text{step}})^T = (B_{\text{mask}} \cdot S_{\text{arith}} \cdot U_{\text{coll}})^T$ advances across arbitrary $T$ timesteps without any dilation leakage or amplitude decay.

$$\mathbf{Conclusion\ on\ Route\ D:\ RECOMMENDED\ as\ the\ single\ viable\ path\ to\ Level\ A.}$$
