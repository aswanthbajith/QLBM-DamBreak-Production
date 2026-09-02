# PHASE F13: FULLY COHERENT QUANTUM TIMESTEP
## Multi-Step Quantum Dam-Break Evolution Without Intermediate Extractions or Re-Encodings

**Document**: Coherent Timestep Integration Specification  
**Project**: Quantum Lattice Boltzmann Method (QLBM) for Two-Phase Flow  
**Repository**: `/home/aswa/Research/QLBM-DamBreak-Production`  
**Branch**: `feature/direct-encoding-two-phase-qlbm`  
**Date**: September 2026  

---

## 1. Unified Coherent Quantum Timestep Operator ($U_{\text{step}}$)

$$\mathbf{U_{\text{step}}^{\text{coherent}} = B_{\text{mask}} \cdot S_{\text{arith}} \cdot U_{\text{coll}}^{\text{coherent}} \cdot U_{\text{force}}^{\text{coherent}} \cdot U_{\text{vel}}^{\text{coherent}} \cdot U_{\text{moments}}^{\text{coherent}}}$$

Multi-step time evolution over $T$ steps:

$$|\Psi_T\rangle = \left( U_{\text{step}}^{\text{coherent}} \right)^T |\Psi_0\rangle$$

---

## 2. Multi-Grid Accuracy Benchmarks ($T=1 \dots 16$)

$$\begin{array}{|c|c|c|c|c|c|c|}
\hline
\textbf{Grid} & \textbf{Timesteps } T & \textbf{Extractions} & \textbf{Re-Encodings} & \text{Max } f \text{ Error} & \text{Max } g \text{ Error} & \text{Max } \rho \text{ Error} \\
\hline
4 \times 4 & T = 1 & 1 & 0 & 7.35 \times 10^{-5} & 6.58 \times 10^{-5} & 7.35 \times 10^{-5} \\
4 \times 4 & T = 2 & 1 & 0 & 1.89 \times 10^{-4} & 1.05 \times 10^{-4} & 2.56 \times 10^{-4} \\
4 \times 4 & T = 4 & 1 & 0 & 1.56 \times 10^{-3} & 3.99 \times 10^{-4} & 2.18 \times 10^{-3} \\
4 \times 4 & T = 8 & 1 & 0 & 7.56 \times 10^{-4} & 4.46 \times 10^{-4} & 1.50 \times 10^{-3} \\
4 \times 4 & T = 16 & 1 & 0 & 1.02 \times 10^{-3} & 5.48 \times 10^{-4} & 2.52 \times 10^{-3} \\
\hline
8 \times 4 & T = 16 & 1 & 0 & 1.28 \times 10^{-3} & 1.23 \times 10^{-3} & 2.20 \times 10^{-3} \\
16 \times 8 & T = 16 & 1 & 0 & 6.45 \times 10^{-3} & 2.64 \times 10^{-3} & 1.36 \times 10^{-2} \\
\hline
\end{array}$$

- **One Initial State Preparation**: $t=0$.
- **Zero Intermediate Classical Extractions**.
- **Zero Intermediate Re-Encodings**.
- **Final Measurement at Step $T$ Only**.
