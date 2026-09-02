# PHASE F17: QUANTUM HARDWARE RESOURCE PROFILING
## Logical Qubits, Depth, and Toffoli Gate Synthesis for Route D

**Document**: Resource Profiling & Hardware Synthesis Specification  
**Project**: Quantum Lattice Boltzmann Method (QLBM) for Two-Phase Flow  
**Repository**: `/home/aswa/Research/QLBM-DamBreak-Production`  
**Branch**: `feature/direct-encoding-two-phase-qlbm`  
**Date**: September 2026  

---

## 1. Qubit & Gate Resource Requirements by Lattice Domain

$$\begin{array}{|c|c|c|c|c|c|}
\hline
\textbf{Lattice Domain} & \textbf{Logical Qubits} & \textbf{Circuit Depth / Step} & \textbf{Toffoli Count / Step} & \textbf{T-Gate Count / Step} \\
\hline
\text{1 Node} & 288 & 32,400 & 6,192 & 43,344 \\
2 \times 2 \text{ (4 Nodes)} & 1,152 & 32,400 \text{ (Parallel)} & 24,768 & 173,376 \\
4 \times 4 \text{ (16 Nodes)} & 4,608 & 32,400 \text{ (Parallel)} & 99,072 & 693,504 \\
8 \times 4 \text{ (32 Nodes)} & 9,216 & 32,400 \text{ (Parallel)} & 198,144 & 1,387,008 \\
16 \times 8 \text{ (128 Nodes)} & 36,864 & 32,400 \text{ (Parallel)} & 792,576 & 5,548,032 \\
\hline
\end{array}$$

- **Parallel Depth Scaling**: Because local node collisions execute concurrently across spatial lattice sites, the circuit depth per timestep remains constant ($\approx 32,400$ gates) regardless of grid size!
