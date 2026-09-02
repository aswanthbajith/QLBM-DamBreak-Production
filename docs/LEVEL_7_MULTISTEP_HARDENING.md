# LEVEL-7: MULTI-STEP HARDENING & CUMULATIVE SUCCESS ANALYSIS
## Extended Verification of Projected Block-Encoding Composition up to $K=32$

**Document**: Multi-Step Numerical Precision and Cumulative Probability Compounding  
**Repository**: `/home/aswa/Research/QLBM-DamBreak-Production`  
**Date**: September 2026  

---

## 1. Unprojected Dilation Leakage vs Projected Reset Accuracy

Let $C_2 \in \mathbb{R}^{342 \times 342}$ be embedded in the 10-qubit Sz.-Nagy unitary dilation $U_C$ with $\alpha_C = 9.7321$.
Evaluating operator powers up to $K = 32$:

$$\begin{array}{|c|c|c|c|c|c|}
\hline
\textbf{Steps } (K) & \textbf{Unprojected Error} & \textbf{Projected Reset Error} & \textbf{Raw Cumulative } p_{\text{succ}} & \textbf{OAA Cumulative } p_{\text{succ}} & \textbf{Status} \\
\hline
K = 1 & 6.578 \times 10^{-17} & 6.578 \times 10^{-17} & 1.056 \times 10^{-2} & 99.93\% & \text{Exact} \\
K = 2 & 2.099 \times 10^{1} \ (2098.7\%) & 1.446 \times 10^{-16} & 1.115 \times 10^{-4} & 99.86\% & \text{Exact} \\
K = 4 & 1.558 \times 10^{3} \ (155830\%) & 2.065 \times 10^{-16} & 1.243 \times 10^{-8} & 99.71\% & \text{Exact} \\
K = 8 & 1.292 \times 10^{7} & 4.512 \times 10^{-16} & 1.544 \times 10^{-16} & 99.43\% & \text{Exact} \\
K = 16 & 1.033 \times 10^{15} & 8.773 \times 10^{-16} & 2.385 \times 10^{-32} & 98.86\% & \text{Exact} \\
K = 32 & 6.686 \times 10^{30} & 1.710 \times 10^{-15} & 5.687 \times 10^{-64} & 97.73\% & \text{Exact} \\
\hline
\end{array}$$

---

## 2. Key Scientific Insights

1. **Defect Operator Growth**: Without mid-circuit projection/reset, unprojected unitary dilation multiplication diverges exponentially with relative error exceeding $10^{30}$ at $K=32$.
2. **Machine-Precision Composition**: Mid-circuit projective ancilla reset projects the state back onto the physical subspace, maintaining numerical agreement with the finite-dimensional operator power $C_2^K$ within $< 1.71 \times 10^{-15}$ across all 32 timesteps.
3. **Cumulative Probability Compounding**:
   - Without amplitude amplification, raw postselection probability collapses to $5.69 \times 10^{-64}$ at $K=32$.
   - With $m=7$ OAA iterations ($p_{\text{step}} = 99.9283\%$), the cumulative success probability across $K=32$ consecutive blocks remains **$97.73\%$**.
