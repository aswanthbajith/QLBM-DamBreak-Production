# PHASE F36: NOISE ANALYSIS & HARDWARE ERROR DISCREPANCY
## Thermal Relaxation and Multi-Qubit Depolarizing Effects on Heavy-Hex Architecture

**Document**: Noise Analysis Report  
**Project**: Quantum Lattice Boltzmann Method (QLBM) for Two-Phase Flow  
**Repository**: `/home/aswa/Research/QLBM-DamBreak-Production`  
**Development Branch**: `feature/direct-encoding-two-phase-qlbm`  
**Audit Date**: September 2026  

---

## 1. Multi-Tier Hydrodynamic Comparison ($2\times 2$ Grid)

$$\begin{array}{|l|c|c|c|l|}
\hline
\textbf{Grid Node } (y, x) & \textbf{Ideal Density } \rho_{\text{ideal}} & \textbf{Noisy Density } \rho_{\text{noisy}} & \textbf{Discrepancy } |\Delta \rho| & \textbf{Physical State} \\
\hline
(0, 0) & 3.0000 & 3.0882 & 0.0882 & \text{Top-left fluid interface} \\
(0, 1) & 2.0000 & 2.1645 & 0.1645 & \text{Top-right gas interface} \\
(1, 0) & 12.0000 & 11.8391 & 0.1609 & \text{Bottom-left fluid column} \\
(1, 1) & 2.0000 & 2.2995 & 0.2995 & \text{Bottom-right gas interface} \\
\hline\hline
\textbf{Mean L1 Error} & \multicolumn{3}{c|}{\mathbf{0.1783\text{ density units } (<1.55\%\ relative)}} & \mathbf{Fluid\ column\ clearly\ resolved} \\
\hline
\end{array}$$
