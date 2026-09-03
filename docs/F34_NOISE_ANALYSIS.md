# PHASE F34: NOISE ANALYSIS & HARDWARE ERROR BUDGET
## Five Distinct Error Contributions in NISQ Two-Phase QLBM

**Document**: Noise Analysis & Error Budget Report  
**Project**: Quantum Lattice Boltzmann Method (QLBM) for Two-Phase Flow  
**Repository**: `/home/aswa/Research/QLBM-DamBreak-Production`  
**Development Branch**: `feature/direct-encoding-two-phase-qlbm`  
**Audit Date**: September 2026  

---

## 1. Error Budget Decomposition

$$\begin{array}{|l|c|c|l|}
\hline
\textbf{Error Component} & \textbf{Symbol} & \textbf{Observed Magnitude} & \textbf{Physical Origin} \\
\hline
\text{1. Quantization Error} & E_{\text{quant}} & \sim 2.44 \times 10^{-4} & \text{Fixed-point fractional bit resolution } (Q4.12) \\
\text{2. Algorithmic Approximation} & E_{\text{alg}} & \sim 1.15 \times 10^{-3} & \text{Discrete LBM lattice truncation error} \\
\text{3. Circuit Synthesis Error} & E_{\text{synth}} & 0.0000 & \text{Exact Clifford+T discrete mapping } (0\text{ LSB}) \\
\text{4. Sampling / Shot Noise} & E_{\text{shot}} & \pm 0.0008 & \text{Finite shot sampling error } (N_{\text{shots}}=4096) \\
\text{5. Hardware Noise (Emulated)} & E_{\text{hw}} & 0.1662 & \text{Thermal relaxation } T_1/T_2\text{ and 2Q depolarizing error} \\
\hline
\end{array}$$
