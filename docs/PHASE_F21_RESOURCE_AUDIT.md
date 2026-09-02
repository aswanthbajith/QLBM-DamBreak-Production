# PHASE F21: HARDWARE RESOURCE AUDIT
## Qubit Footprint and Circuit Gate Scaling for Reversible CSF

**Document**: Circuit Resource & Gate Synthesis Audit  
**Project**: Quantum Lattice Boltzmann Method (QLBM) for Two-Phase Flow  
**Repository**: `/home/aswa/Research/QLBM-DamBreak-Production`  
**Branch**: `feature/direct-encoding-two-phase-qlbm`  
**Date**: September 2026  

---

## 1. Hardware Resource Scaling by Domain

$$\begin{array}{|c|c|c|c|c|}
\hline
\textbf{Lattice Domain} & \textbf{Total Nodes} & \textbf{Active CSF Qubits} & \textbf{Total Lattice Qubits (QLBM + CSF)} & \textbf{Qubits / Node} \\
\hline
2 \times 2 & 4 & 192 & 2,496 & 624 \\
4 \times 4 & 16 & 768 & 9,984 & 624 \\
8 \times 4 & 32 & 1,536 & 19,968 & 624 \\
16 \times 8 & 128 & 6,144 & 79,872 & 624 \\
\hline
\end{array}$$
