# PHASE F21: FIXED-POINT PRECISION & ERROR BUDGET
## Precision Scaling Across $Q4.8$, $Q4.12$, and $Q4.16$

**Document**: Fixed-Point Error Budget Specification  
**Project**: Quantum Lattice Boltzmann Method (QLBM) for Two-Phase Flow  
**Repository**: `/home/aswa/Research/QLBM-DamBreak-Production`  
**Branch**: `feature/direct-encoding-two-phase-qlbm`  
**Date**: September 2026  

---

## 1. Error Budget Comparison

$$\begin{array}{|l|c|c|c|c|}
\hline
\textbf{Precision Format} & \textbf{Total Bits} & \textbf{Fractional Bits} & \textbf{LSB Resolution} & \text{Sqrt Error } |\text{sqrt}(2) - \sqrt{2}| \\
\hline
Q4.8 & 12 & 8 & 3.906 \times 10^{-3} & 1.51 \times 10^{-4} \\
\mathbf{Q4.12 \text{ (Baseline)}} & \mathbf{16} & \mathbf{12} & \mathbf{2.441 \times 10^{-4}} & \mathbf{1.51 \times 10^{-4}} \\
Q4.16 & 20 & 16 & 1.526 \times 10^{-5} & 1.37 \times 10^{-5} \\
\hline
\end{array}$$
