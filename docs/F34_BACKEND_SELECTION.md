# PHASE F34: BACKEND SELECTION & HARDWARE DISCOVERY
## Architectural Mapping on Superconducting Quantum Processors

**Document**: Backend Selection Report  
**Project**: Quantum Lattice Boltzmann Method (QLBM) for Two-Phase Flow  
**Repository**: `/home/aswa/Research/QLBM-DamBreak-Production`  
**Development Branch**: `feature/direct-encoding-two-phase-qlbm`  
**Audit Date**: September 2026  

---

## 1. Target Hardware Architectures

$$\begin{array}{|l|c|c|c|l|}
\hline
\textbf{Hardware Target} & \textbf{Qubits} & \textbf{Native Gate Basis} & \textbf{Coupling Graph} & \textbf{Selection Role} \\
\hline
\text{IBM Sherbrooke} & 127 & \{\text{ECR}, R_z, \sqrt{X}, X\} & \text{Heavy-Hex} & \textbf{Primary Target Architecture} \\
\text{IBM Brisbane} & 127 & \{\text{ECR}, R_z, \sqrt{X}, X\} & \text{Heavy-Hex} & \text{Secondary Validation Target} \\
\text{IBM Kyoto} & 127 & \{\text{ECR}, R_z, \sqrt{X}, X\} & \text{Heavy-Hex} & \text{Cross-Device Verification} \\
\hline
\end{array}$$
