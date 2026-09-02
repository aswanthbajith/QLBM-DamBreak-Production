# PHASE F15: QUANTUM RESOURCE PROFILING
## Logical Qubits, Carleman Lifted State Overhead, and Transpilation Metrics

**Document**: Hardware Resource Profiling & Complexity Analysis  
**Project**: Quantum Lattice Boltzmann Method (QLBM) for Two-Phase Flow  
**Repository**: `/home/aswa/Research/QLBM-DamBreak-Production`  
**Branch**: `feature/direct-encoding-two-phase-qlbm`  
**Date**: September 2026  

---

## 1. Qubit Footprint by Domain Grid

$$\begin{array}{|c|c|c|c|c|c|}
\hline
\textbf{Grid Size} & \textbf{Data Qubits} & \textbf{Lifted Carleman Qubits / Node} & \textbf{Total Logical Qubits} & \textbf{Hilbert Dimension} \\
\hline
2 \times 2 & 7 & 10 \text{ qubits (dim 1024)} & 10 & 1,024 \\
4 \times 4 & 9 & 10 \text{ qubits (dim 1024)} & 12 & 4,096 \\
8 \times 4 & 10 & 10 \text{ qubits (dim 1024)} & 13 & 8,192 \\
16 \times 8 & 12 & 10 \text{ qubits (dim 1024)} & 15 & 32,768 \\
32 \times 16 & 14 & 10 \text{ qubits (dim 1024)} & 17 & 131,072 \\
\hline
\end{array}$$

---

## 2. IBM FakeSherbrooke (127Q) Transpilation Profile

$$\begin{array}{|c|c|c|c|c|c|}
\hline
\textbf{Grid Size} & \textbf{Logical Qubits} & \textbf{Transpiled Depth} & \textbf{2Q Gates (ECR/CX)} & \textbf{Total Gates} \\
\hline
2 \times 2 & 7 & 16,101 & 4,016 & 27,233 \\
4 \times 4 & 9 & 792,197 & 201,744 & 1,328,615 \\
8 \times 4 & 10 & \approx 1,584,000 & \approx 403,000 & \approx 2,650,000 \\
16 \times 8 & 12 & \approx 6,336,000 & \approx 1,612,000 & \approx 10,600,000 \\
\hline
\end{array}$$

- **Safety Interlock**: Verified active (`QLBM_ENABLE_REAL_QPU=0`, `QLBM_CONFIRM_REAL_QPU=NO`).
