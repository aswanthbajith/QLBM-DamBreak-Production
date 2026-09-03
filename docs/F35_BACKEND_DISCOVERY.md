# PHASE F35: BACKEND DISCOVERY & TOPOLOGY CATALOG
## Analysis of Candidate Physical QPUs and Coupling Graphs

**Document**: Backend Discovery Report  
**Project**: Quantum Lattice Boltzmann Method (QLBM) for Two-Phase Flow  
**Repository**: `/home/aswa/Research/QLBM-DamBreak-Production`  
**Development Branch**: `feature/direct-encoding-two-phase-qlbm`  
**Audit Date**: September 2026  

---

## 1. Discovered Quantum Processor Topologies

$$\begin{array}{|l|c|c|c|l|}
\hline
\textbf{Hardware Target} & \textbf{Qubits} & \textbf{Native Gate Basis} & \textbf{Coupling Mesh} & \textbf{Operational State} \\
\hline
\text{IBM Sherbrooke (Eagle r3)} & 127 & \{\text{ECR}, R_z, \sqrt{X}, X\} & \text{Heavy-Hex} & \text{Primary 127-Qubit Target} \\
\text{IBM Brisbane (Eagle r3)} & 127 & \{\text{ECR}, R_z, \sqrt{X}, X\} & \text{Heavy-Hex} & \text{Alternative 127-Qubit Target} \\
\text{IBM Manila (Falcon r5)} & 5 & \{\text{CX}, R_z, \sqrt{X}, X\} & \text{T-Topology} & \text{Single-Node Kernel Target} \\
\hline
\end{array}$$
