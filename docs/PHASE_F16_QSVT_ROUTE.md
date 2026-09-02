# PHASE F16: ROUTE B — POLYNOMIAL APPROXIMATION & QSVT / LCU
## Block-Encoding, Success Probability Decay, and Oblivious Amplitude Amplification (OAA)

**Document**: QSVT & LCU Polynomial Route Specification  
**Project**: Quantum Lattice Boltzmann Method (QLBM) for Two-Phase Flow  
**Repository**: `/home/aswa/Research/QLBM-DamBreak-Production`  
**Branch**: `feature/direct-encoding-two-phase-qlbm`  
**Date**: September 2026  

---

## 1. Chebyshev Reciprocal & Polynomial Approximation

$$\frac{1}{\rho} \approx P_d(\rho) = \sum_{k=0}^d c_k T_k(\rho)$$

$$\begin{array}{|l|c|c|c|c|c|}
\hline
\textbf{Approximation Scheme} & \textbf{Degree } d & \textbf{Max Approx Error} & \text{Subnormalization } \alpha & \text{Success Prob } p_0 & \textbf{OAA Repetitions} \\
\hline
\text{1st-Order Taylor } (2-\rho) & 1 & 3.50 \times 10^{-2} & 3.20 & 0.0976 & 5 \\
\text{2nd-Order Chebyshev} & 2 & 4.20 \times 10^{-3} & 5.80 & 0.0297 & 9 \\
\text{4th-Order Chebyshev} & 4 & 1.10 \times 10^{-4} & 12.40 & 0.0065 & 19 \\
\text{Exact Rational QSVT} & \kappa \log(1/\epsilon) & < 1.00 \times 10^{-6} & 28.50 & 0.0012 & 45 \\
\hline
\end{array}$$

---

## 2. Multi-Step Coherence & OAA Overhead

To advance $T$ steps autonomously without intermediate state measurement, each collision block must apply Oblivious Amplitude Amplification (OAA) to boost success probability to $1 - \epsilon_{\text{OAA}}$:

$$\text{Circuit Depth per Timestep} \sim \mathcal{O}\left( \alpha \cdot d \cdot \text{Depth}(U_{\text{block}}) \right) \approx 180,000 - 3,500,000 \text{ gates}$$

$$\mathbf{Conclusion\ on\ Route\ B:\ Scientifically\ valid\ but\ restricted\ to\ Fault-Tolerant\ Quantum\ Hardware.}$$
