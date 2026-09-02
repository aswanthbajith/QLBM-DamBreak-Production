# PHASE F16: ROUTE E — ALTERNATIVE QUANTUM STATE ENCODINGS
## Amplitude vs. Register Value vs. Probability vs. Moment-Space Encodings

**Document**: Quantum State Encoding Comparative Analysis  
**Project**: Quantum Lattice Boltzmann Method (QLBM) for Two-Phase Flow  
**Repository**: `/home/aswa/Research/QLBM-DamBreak-Production`  
**Branch**: `feature/direct-encoding-two-phase-qlbm`  
**Date**: September 2026  

---

## 1. Comparative Analysis of State Encodings

$$\begin{array}{|l|l|l|l|c|}
\hline
\textbf{Encoding Scheme} & \textbf{Mathematical Definition} & \textbf{Streaming} & \textbf{Nonlinear Collision} & \textbf{Autonomy Verdict} \\
\hline
\text{1. Amplitude Encoding} & |\Psi\rangle = \sum f_i |i\rangle & \text{Exact } \mathcal{O}(1) \text{ permutation} & \text{Nonlinear rational obstruction} & \textbf{LEVEL C ONLY} \\
\text{2. Register Value Encoding} & |\mathbf{f}\rangle = |f_0\rangle \dots |f_8\rangle & \text{Wire / register swap} & \text{Exact reversible arithmetic} & \textbf{LEVEL A VIABLE} \\
\text{3. Square-Root Probability} & |\Psi\rangle = \sum \sqrt{f_i} |i\rangle & \text{Exact permutation} & \text{Nonlinear moments exacerbate} & \textbf{REJECTED} \\
\text{4. Moment-Space Encoding} & |\mathbf{m}\rangle = M_{\text{D2Q9}} |\mathbf{f}\rangle & \text{Nonlocal coupling} & \text{Equilibrium remains rational} & \textbf{LEVEL C ONLY} \\
\hline
\end{array}$$

$$\mathbf{Conclusion\ on\ Route\ E:\ Register\ value\ encoding\ is\ the\ only\ encoding\ permitting\ autonomous\ collision.}$$
