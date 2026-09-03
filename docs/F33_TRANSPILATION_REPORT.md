# PHASE F33: QUANTUM HARDWARE TRANSPILATION REPORT
## Physical Gate Synthesis and Topology Mapping on 127-Qubit IBM Hardware

**Document**: Hardware Transpilation Report  
**Project**: Quantum Lattice Boltzmann Method (QLBM) for Two-Phase Flow  
**Repository**: `/home/aswa/Research/QLBM-DamBreak-Production`  
**Development Branch**: `feature/direct-encoding-two-phase-qlbm`  
**Audit Date**: September 2026  

---

## 1. Transpilation Metrics (Target: IBM Sherbrooke 127-Qubit Processor)

$$\begin{array}{|l|c|c|l|}
\hline
\textbf{Metric} & \textbf{Pre-Transpilation} & \textbf{Post-Transpilation} & \textbf{Physical Interpretation} \\
\hline
\text{Qubit Width} & 16\text{ logical qubits} & 127\text{ physical qubits} & \text{Mapped to heavy-hex active coupling graph} \\
\text{Circuit Depth} & 10\text{ logical layers} & 19\text{ physical layers} & \text{Shallow execution well within } T_2 \text{ coherence} \\
\text{Two-Qubit Gates} & 8\text{ CX/SWAP} & 16\text{ native ECR gates} & \text{Decomposed into hardware-native 2Q basis} \\
\text{Single-Qubit Gates} & 18\text{ gates} & 139\text{ gates } (R_z, SX, X) & \text{Euler angle decomposition} \\
\text{Measurement Gates} & 16 & 16 & \text{Parallel final computational-basis readout} \\
\textbf{Total Physical Gates} & \mathbf{34} & \mathbf{155} & \mathbf{Fully\ synthesizable\ on\ NISQ\ QPUs} \\
\hline
\end{array}$$
