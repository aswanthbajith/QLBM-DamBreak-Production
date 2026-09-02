# PHASE F19: HARDWARE RESOURCE AUDIT
## Logical Qubits, Gate Counts, and Multi-Node Domain Profiling

**Document**: Circuit Resource & Gate Synthesis Audit  
**Project**: Quantum Lattice Boltzmann Method (QLBM) for Two-Phase Flow  
**Repository**: `/home/aswa/Research/QLBM-DamBreak-Production`  
**Branch**: `feature/direct-encoding-two-phase-qlbm`  
**Date**: September 2026  

---

## 1. Hardware Requirements by Domain

$$\begin{array}{|c|c|c|c|c|}
\hline
\textbf{Lattice Domain} & \textbf{Logical Qubits (Mode Retention)} & \textbf{Circuit Depth / Step} & \textbf{Toffoli Count / Step} & \textbf{T-Gate Count / Step} \\
\hline
\text{1 Node} & 576 & 32,400 & 6,192 & 43,344 \\
2 \times 2 & 2,304 & 32,400 \text{ (Parallel)} & 24,768 & 173,376 \\
4 \times 4 & 9,216 & 32,400 \text{ (Parallel)} & 99,072 & 693,504 \\
8 \times 4 & 18,432 & 32,400 \text{ (Parallel)} & 198,144 & 1,387,008 \\
\hline
\end{array}$$
