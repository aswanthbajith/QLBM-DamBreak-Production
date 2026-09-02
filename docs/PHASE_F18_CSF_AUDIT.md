# PHASE F18: CONTINUUM SURFACE FORCE (CSF) AUDIT
## Status of Surface Tension ($\sigma$) and Omitted Physics Taxonomy

**Document**: CSF Status & Physics Inclusion Taxonomy  
**Project**: Quantum Lattice Boltzmann Method (QLBM) for Two-Phase Flow  
**Repository**: `/home/aswa/Research/QLBM-DamBreak-Production`  
**Branch**: `feature/direct-encoding-two-phase-qlbm`  
**Date**: September 2026  

---

## 1. Physical Component Taxonomy

$$\begin{array}{|l|c|c|c|}
\hline
\textbf{Physical Component} & \textbf{Implemented?} & \textbf{Mechanism} & \textbf{Status} \\
\hline
\text{D2Q9 Hydrodynamic Populations } f_i & \textbf{YES} & \text{Reversible } Q4.12 & \textbf{INCLUDED} \\
\text{D2Q9 Phase-Field Populations } g_i & \textbf{YES} & \text{Reversible } Q4.12 & \textbf{INCLUDED} \\
\text{Moments } \rho, \alpha, \mathbf{j} & \textbf{YES} & \text{Reversible Adders} & \textbf{INCLUDED} \\
\text{Velocity } \mathbf{u} = \mathbf{j}/\rho & \textbf{YES} & \text{Reversible Divider} & \textbf{INCLUDED} \\
\text{Gravity Body Forcing } \mathbf{g} & \textbf{YES} & \text{Reversible Multiplier} & \textbf{INCLUDED} \\
\text{Spatial Streaming } S_{\text{arith}} & \textbf{YES} & \text{Unitary Permutation} & \textbf{INCLUDED} \\
\text{Solid Boundary } B_{\text{mask}} & \textbf{YES} & \text{Unitary Involution} & \textbf{INCLUDED} \\
\text{CSF Surface Tension } \mathbf{F}_s(\sigma) & \textbf{NO} & \text{Reduced to } \sigma = 0 & \textbf{OMITTED IN PROTOTYPE} \\
\text{State-Dependent Viscosity } \tau(\alpha) & \textbf{NO} & \text{Fixed reference } \tau & \textbf{OMITTED IN PROTOTYPE} \\
\hline
\end{array}$$

CSF surface tension is explicitly documented as omitted ($\sigma = 0$) in the prototype to isolate the collision bijectivity investigation.
