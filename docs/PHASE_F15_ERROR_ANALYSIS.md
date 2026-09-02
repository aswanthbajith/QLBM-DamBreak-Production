# PHASE F15: COMPREHENSIVE ERROR ANALYSIS
## Carleman Truncation, Manifold Defect, and Multi-Step Drift

**Document**: Error Budget & Convergence Analysis  
**Project**: Quantum Lattice Boltzmann Method (QLBM) for Two-Phase Flow  
**Repository**: `/home/aswa/Research/QLBM-DamBreak-Production`  
**Branch**: `feature/direct-encoding-two-phase-qlbm`  
**Date**: September 2026  

---

## 1. Error Budget Decomposition

$$\begin{array}{|l|c|l|c|}
\hline
\textbf{Error Source} & \textbf{Error Magnitude} & \textbf{Physical Nature} & \textbf{Status} \\
\hline
\text{1. Initial Amplitude Encoding} & < 1.0 \times 10^{-16} & \text{Exact Unitary State Preparation} & \text{Controlled} \\
\text{2. Carleman } K=2 \text{ Truncation} & 1.4 \times 10^{-1} & \mathcal{O}(u^2) \text{ Low-Mach Truncation} & \text{Bounded} \\
\text{3. Tensor Manifold Defect} & 2.0 \times 10^{-16} & \|Y_2 - \mathbf{z} \otimes \mathbf{z}\|_2 \text{ Machine Precision} & \text{Exact} \\
\text{4. Sz.-Nagy Unitary Dilation} & < 4.1 \times 10^{-14} & 10\text{-qubit Block Embedding} & \text{Exact} \\
\text{5. Arithmetic Streaming Permutation} & < 1.0 \times 10^{-14} & \text{Exact Coordinate Permutation} & \text{Exact} \\
\text{6. Boundary Mask Involution} & < 1.0 \times 10^{-15} & \text{Exact Direction Swaps} & \text{Exact} \\
\text{7. Multi-Step Drift } (T=16) & 1.2 \times 10^{-2} & \text{Carleman Multi-Step Dispersion} & \text{Stable} \\
\hline
\end{array}$$
