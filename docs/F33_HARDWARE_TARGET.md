# PHASE F33: HARDWARE TARGET SELECTION & BACKEND ANALYSIS
## Quantum Processor Selection and Transpilation Topology

**Document**: Hardware Target Selection Report  
**Project**: Quantum Lattice Boltzmann Method (QLBM) for Two-Phase Flow  
**Repository**: `/home/aswa/Research/QLBM-DamBreak-Production`  
**Development Branch**: `feature/direct-encoding-two-phase-qlbm`  
**Audit Date**: September 2026  

---

## 1. Candidate Backend Evaluation

$$\begin{array}{|l|c|c|c|c|l|}
\hline
\textbf{Backend} & \textbf{Qubits} & \textbf{Native Gate Set} & \textbf{Avg CNOT Error} & \textbf{Avg Readout Error} & \textbf{Selection Decision} \\
\hline
\text{IBM Manila (FakeManilaV2)} & 5 & \{CZ, R_z, SX, X\} & 7.2 \times 10^{-3} & 2.1 \times 10^{-2} & \textbf{Selected for 1-Node Collision} \\
\text{IBM Sherbrooke (FakeSherbrooke)} & 127 & \{ECR, R_z, SX, X\} & 8.5 \times 10^{-3} & 1.8 \times 10^{-2} & \textbf{Selected for 2x2 Full Lattice} \\
\text{IBM Brisbane (FakeBrisbane)} & 127 & \{ECR, R_z, SX, X\} & 9.1 \times 10^{-3} & 2.4 \times 10^{-2} & \text{Secondary Verification Target} \\
\text{Real IBM QPU} & 127+ & \text{Cloud Queue} & \text{Variable} & \text{Variable} & \text{Guarded by Safety Flag} \\
\hline
\end{array}$$

---

## 2. Selection Rationale

- **Primary Goal**: Maximize physical signal-to-noise ratio by matching circuit width to tightest high-coherence sub-topologies.
- **Transpilation Optimization**: Optimization Level 3 with dynamical decoupling and readout error mitigation.
