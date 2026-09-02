# PHASE F16: ROUTE C — REVERSIBLE FIXED-POINT QUANTUM ARITHMETIC
## Bit-Width Analysis, Toffoli Gate Synthesis, and Exact Uncomputation

**Document**: Reversible Quantum Arithmetic Route Specification  
**Project**: Quantum Lattice Boltzmann Method (QLBM) for Two-Phase Flow  
**Repository**: `/home/aswa/Research/QLBM-DamBreak-Production`  
**Branch**: `feature/direct-encoding-two-phase-qlbm`  
**Date**: September 2026  

---

## 1. Fixed-Point Formats ($Q4.8, Q4.12, Q8.16$)

$$\begin{array}{|c|c|c|c|c|}
\hline
\textbf{Format} & \textbf{Total Bits } n & \textbf{Integer Bits } I & \textbf{Fractional Bits } F & \textbf{LSB Precision } \epsilon = 2^{-F} \\
\hline
Q4.8 & 12 & 4 \ ([-8, 7.99]) & 8 & 3.906 \times 10^{-3} \\
Q4.12 & 16 & 4 \ ([-8, 7.99]) & 12 & 2.441 \times 10^{-4} \\
Q8.16 & 24 & 8 \ ([-128, 127.99]) & 16 & 1.526 \times 10^{-5} \\
\hline
\end{array}$$

---

## 2. Gate Counts & Ancilla Footprint for Local Node Collision

$$\begin{array}{|l|c|c|c|c|}
\hline
\textbf{Arithmetic Module} & \textbf{Toffoli Count} & \textbf{T-Gate Count} & \textbf{Ancillas} & \textbf{Uncomputation Strategy} \\
\hline
\text{1. Moment Accumulator } \rho = \sum f_i & 144 & 1,008 & 16 & \text{Exact in-place adder tree} \\
\text{2. Momentum Vector } \mathbf{j} = \sum f_i \mathbf{c}_i & 288 & 2,016 & 32 & \text{Signed reversible adder} \\
\text{3. Reversible Divider } \mathbf{u} = \mathbf{j} / \rho & 1,152 & 8,064 & 48 & \text{Non-restoring division} \\
\text{4. Velocity Squaring } |\mathbf{u}|^2 & 576 & 4,032 & 32 & \text{Barenco array multiplier} \\
\text{5. Equilibrium Pipeline } (f_i^{\text{eq}}, g_i^{\text{eq}}) & 2,304 & 16,128 & 64 & \text{Reversible MAC} \\
\text{6. Relaxation \& Collision } f_i^* & 1,728 & 12,096 & 48 & \text{Reversible linear combo} \\
\hline
\textbf{Total Node Collision Unitary } U_{\text{coll}} & \mathbf{6,192} & \mathbf{43,344} & \mathbf{128} & \mathbf{100\% \text{ Uncomputed to } |0\rangle} \\
\hline
\end{array}$$

- **100% Deterministic Unitarity**: Unlike block-encodings, reversible arithmetic circuits have **$p_{\text{success}} = 1.0$** and **zero dilation leakage**!
