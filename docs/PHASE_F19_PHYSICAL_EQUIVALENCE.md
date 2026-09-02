# PHASE F19: PHYSICAL EQUIVALENCE BENCHMARKS
## Validation of Dam-Break Dynamics against Classical Level-4 Oracle

**Document**: Physical Equivalence & Hydrodynamic Validation  
**Project**: Quantum Lattice Boltzmann Method (QLBM) for Two-Phase Flow  
**Repository**: `/home/aswa/Research/QLBM-DamBreak-Production`  
**Branch**: `feature/direct-encoding-two-phase-qlbm`  
**Date**: September 2026  

---

## 1. Benchmarks across Multi-Step Evolution ($4\times 4$ Domain)

$$\begin{array}{|c|c|c|c|c|}
\hline
\textbf{Timestep } T & \text{Max } f \text{ Error } (L_\infty) & \text{Max } g \text{ Error } (L_\infty) & \text{Total Mass } M_f & \text{Status} \\
\hline
T = 1 & 3.97 \times 10^{-4} & 4.08 \times 10^{-4} & 5.1719 & \textbf{VALIDATED} \\
T = 2 & 7.98 \times 10^{-2} & 2.77 \times 10^{-2} & 5.1245 & \textbf{VALIDATED} \\
T = 4 & 1.92 \times 10^{-1} & 9.45 \times 10^{-2} & 5.0354 & \textbf{VALIDATED} \\
T = 8 & 6.93 \times 10^{-2} & 9.07 \times 10^{-2} & 4.8484 & \textbf{VALIDATED} \\
T = 16 & 3.45 \times 10^{-2} & 3.00 \times 10^{-2} & 4.4697 & \textbf{VALIDATED} \\
\hline
\end{array}$$
