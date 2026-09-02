# PHASE F18: REVERSIBILITY & UNITARY EMBEDDING
## In-Place Replacement vs. Augmented Quantum State Embeddings

**Document**: Reversibility & Unitary Embedding Specification  
**Project**: Quantum Lattice Boltzmann Method (QLBM) for Two-Phase Flow  
**Repository**: `/home/aswa/Research/QLBM-DamBreak-Production`  
**Branch**: `feature/direct-encoding-two-phase-qlbm`  
**Date**: September 2026  

---

## 1. Unitary Embedding Classification

$$\begin{array}{|l|l|c|l|}
\hline
\textbf{Mapping Scheme} & \textbf{Quantum Transformation} & \textbf{Unitary?} & \textbf{Information Storage} \\
\hline
\text{1. In-Place Map} & |x\rangle \to |F(x)\rangle & \textbf{NO} & \text{Violates unitarity for non-injective } F \\
\text{2. Augmented Embedding} & |x\rangle |0\rangle \to |x\rangle |F(x)\rangle & \textbf{YES} & \text{Preserves input } x \text{ in memory register} \\
\text{3. Dissipative Ancilla Dilation} & |x\rangle |0\rangle_{\text{env}} \to |F(x)\rangle |e(x)\rangle_{\text{env}} & \textbf{YES} & \text{Dissipates non-equilibrium modes into env} \\
\hline
\end{array}$$

$$\mathbf{Conclusion:\ A\ valid\ quantum\ circuit\ must\ use\ Scheme\ 2\ or\ 3.}$$
In-place overwriting without an environmental reservoir is physically non-unitary.
