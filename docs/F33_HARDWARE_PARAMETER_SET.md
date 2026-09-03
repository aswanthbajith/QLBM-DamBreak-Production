# PHASE F33: HARDWARE PARAMETER SET & SCALING
## Mapping Dam-Break CFD Parameters to Small-Lattice Quantum Demonstrator

**Document**: Parameter Set Comparison  
**Project**: Quantum Lattice Boltzmann Method (QLBM) for Two-Phase Flow  
**Repository**: `/home/aswa/Research/QLBM-DamBreak-Production`  
**Development Branch**: `feature/direct-encoding-two-phase-qlbm`  
**Audit Date**: September 2026  

---

## 1. Parameter Mapping Table

$$\begin{array}{|l|c|c|l|}
\hline
\textbf{Parameter} & \textbf{Level-4 Reference} & \textbf{F33 Hardware Demonstrator} & \textbf{Physical / Hardware Justification} \\
\hline
\text{Lattice Grid } (N_x \times N_y) & 128 \times 64 & 2 \times 2 & \text{Hardware width constraint for NISQ execution} \\
\text{Liquid Density } (\rho_L) & 1.0 & 1.0 & \text{Preserves hydrodynamic reference scale} \\
\text{Gas Density } (\rho_G) & 0.1 & 0.1 & \text{Preserves density ratio } r = 10 \\
\text{Liquid Phase Field } (\alpha_L) & 1.0 & 1.0 & \text{Clean fluid interface} \\
\text{Gas Phase Field } (\alpha_G) & 0.0 & 0.0 & \text{Clean gas interface} \\
\text{Relaxation } (\omega_f) & 1.0 & 1.0 & \text{Kinematic viscosity matching} \\
\text{Relaxation } (\omega_g) & 1.428 & 1.428 & \text{Phase field mobility matching} \\
\text{Surface Tension } (\sigma) & 0.001 & 0.001 & \text{CSF continuum surface force parameter} \\
\text{Gravity Acceleration } (g_y) & -0.0005 & -0.0005 & \text{Dam-break hydrostatic driving force} \\
\text{Fixed-Point Precision} & Q4.12\text{ / Float64} & Q4.6\text{ / }Q4.12 & \text{Hardware gate-depth vs precision Pareto tradeoff} \\
\hline
\end{array}$$
