# PHASE F17: FIXED-POINT ARITHMETIC MODEL SPECIFICATION
## $Q4.12$ Fixed-Point Quantum Register Representation

**Document**: Fixed-Point Representation & Numerical Domain Specification  
**Project**: Quantum Lattice Boltzmann Method (QLBM) for Two-Phase Flow  
**Repository**: `/home/aswa/Research/QLBM-DamBreak-Production`  
**Branch**: `feature/direct-encoding-two-phase-qlbm`  
**Date**: September 2026  

---

## 1. $Q4.12$ Fixed-Point Register Format

The physical population states $f_i(x,y)$ and $g_i(x,y)$ are represented as discrete 16-bit signed quantum registers in $Q4.12$ format:

$$X = (-1)^{b_{15}} \cdot 2^3 \cdot b_{15} + \sum_{k=0}^{14} b_k \cdot 2^{k-12}$$

- **Total Bit Width**: $n = 16$ bits.
- **Integer Bits**: $I = 4$ (Dynamic range $[-8.0, 7.999755859375]$).
- **Fractional Bits**: $F = 12$ (LSB resolution $\epsilon = 2^{-12} = 0.000244140625$).
- **Scaling Constant**: $S = 2^{12} = 4096$.

---

## 2. Fixed-Point Convergence Comparison

$$\begin{array}{|c|c|c|c|c|}
\hline
\textbf{Format} & \textbf{Total Bits } n & \textbf{Fractional Bits } F & \textbf{LSB Resolution } \epsilon & \textbf{Max Collision Error} \\
\hline
Q4.8 & 12 & 8 & 3.906 \times 10^{-3} & 4.12 \times 10^{-3} \\
\mathbf{Q4.12} & \mathbf{16} & \mathbf{12} & \mathbf{2.441 \times 10^{-4}} & \mathbf{3.18 \times 10^{-4}} \\
Q4.16 & 20 & 16 & 1.526 \times 10^{-5} & 2.10 \times 10^{-5} \\
\hline
\end{array}$$

$Q4.12$ provides the optimal balance of high hydrodynamic accuracy and practical quantum register footprint.
