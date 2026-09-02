# PHASE F10: GENERALIZED BOUNDARY AUDIT & BENCHMARK REPORT
## Multi-Grid Unitarity, Isolated Wall Accuracy, and Two-Phase Sector Isolation

**Document**: Independent Multi-Node Boundary Audit & Forensic Verification  
**Project**: Quantum Lattice Boltzmann Method (QLBM) for Two-Phase Flow  
**Repository**: `/home/aswa/Research/QLBM-DamBreak-Production`  
**Branch**: `feature/direct-encoding-two-phase-qlbm`  
**Date**: September 2026  

---

## 1. Multi-Grid Unitarity & Involution Benchmark

Evaluated across domain sizes from $2 \times 2$ to $32 \times 16$:

$$\begin{array}{|c|c|c|c|c|c|}
\hline
\textbf{Grid Size } N_x \times N_y & \textbf{Qubits } (n_x + n_y + 5) & \textbf{Hilbert Dim} & \text{Unitarity Err } \|B^\dagger B - I\| & \text{Involution Err } \|B^2 - I\| & \textbf{Audit Verdict} \\
\hline
2 \times 2 & 7 & 128 & \mathbf{0.00 \times 10^0} & \mathbf{0.00 \times 10^0} & \text{PASSED (Exact)} \\
4 \times 4 & 9 & 512 & \mathbf{0.00 \times 10^0} & \mathbf{0.00 \times 10^0} & \text{PASSED (Exact)} \\
8 \times 4 & 10 & 1,024 & \mathbf{0.00 \times 10^0} & \mathbf{0.00 \times 10^0} & \text{PASSED (Exact)} \\
16 \times 8 & 12 & 4,096 & \mathbf{0.00 \times 10^0} & \mathbf{0.00 \times 10^0} & \text{PASSED (Exact)} \\
32 \times 16 & 14 & 16,384 & \mathbf{0.00 \times 10^0} & \mathbf{0.00 \times 10^0} & \text{PASSED (Exact)} \\
\hline
\end{array}$$

---

## 2. Isolated Wall Reflection & Cross-Talk Accuracy

$$\begin{array}{|l|c|c|c|c|}
\hline
\textbf{Boundary Wall} & \text{Reflection Error } |a_{\text{opp}} - 1.0| & \text{Residual Incident Error } |a_{\text{inc}}| & \text{Phase Cross-Talk } (f \leftrightarrow g) & \textbf{Verdict} \\
\hline
\text{Left Wall } (i=3 \to 1) & \mathbf{0.00 \times 10^0} & \mathbf{0.00 \times 10^0} & \mathbf{0.00 \times 10^0} & \text{PASSED} \\
\text{Right Wall } (i=1 \to 3) & \mathbf{0.00 \times 10^0} & \mathbf{0.00 \times 10^0} & \mathbf{0.00 \times 10^0} & \text{PASSED} \\
\text{Bottom Wall } (i=4 \to 2) & \mathbf{0.00 \times 10^0} & \mathbf{0.00 \times 10^0} & \mathbf{0.00 \times 10^0} & \text{PASSED} \\
\text{Top Wall } (i=2 \to 4) & \mathbf{0.00 \times 10^0} & \mathbf{0.00 \times 10^0} & \mathbf{0.00 \times 10^0} & \text{PASSED} \\
\hline
\end{array}$$

---

## 3. Wrap-Around Prevention & Kill-Switch Differential Analysis

1. **Periodic Wrap-Around Prevention**:
   - Outgoing particle incident on right wall rebounds cleanly into fluid interior with **$< 6.94 \times 10^{-31}$ leakage** to opposite boundary ($x=0$).
2. **Differential Kill Switch**:
   - Replacing $B_{\text{mask}}$ with $I$ leaves incoming boundary populations unreflected ($\Delta \Psi = 1.000$), immediately departing from the physical Level-4 benchmark.
