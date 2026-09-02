# PHASE F21: CSF FORCE ACCURACY & STENCIL AUDIT
## Comparison of Quantum vs Classical Level-4 Continuum Surface Force

**Document**: CSF Force Accuracy & Stencil Audit  
**Project**: Quantum Lattice Boltzmann Method (QLBM) for Two-Phase Flow  
**Repository**: `/home/aswa/Research/QLBM-DamBreak-Production`  
**Branch**: `feature/direct-encoding-two-phase-qlbm`  
**Date**: September 2026  

---

## 1. Stencil Equivalence Metrics

$$\begin{array}{|l|c|c|}
\hline
\textbf{Test Configuration} & \textbf{Force Difference } \|\mathbf{F}_{\text{quantum}} - \mathbf{F}_{\text{classical}}\|_{L_\infty} & \textbf{Status} \\
\hline
\text{Planar Dam Interface } (\sigma = 0.001) & < 2.44 \times 10^{-4} \text{ (1 LSB)} & \textbf{EXACT WITHIN Q4.12} \\
\text{Circular Droplet Interface } (\sigma = 0.005) & < 2.44 \times 10^{-4} \text{ (1 LSB)} & \textbf{EXACT WITHIN Q4.12} \\
\text{Zero Surface Tension } (\sigma = 0.0) & 0.0000 \times 10^0 & \textbf{EXACT ZERO} \\
\hline
\end{array}$$
