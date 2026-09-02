# LEVEL-7: FINAL SCIENTIFIC HARDENING AUDIT
## Comprehensive Source Verification, Categorization, and Academic Proof Matrix

**Document**: Master Evidence and Hardening Audit  
**Repository**: `/home/aswa/Research/QLBM-DamBreak-Production`  
**Date**: September 2026  

---

## 1. Categorized Evidence Matrix

| Fact / Statement | Categorization | Exact Evidence & Traceability |
| :--- | :---: | :--- |
| **Classical Level-4 Dam-Break Accuracy** | **DIRECTLY VERIFIED BY CODE** | Replicated Martin & Moyce experimental surge front $x^*(t^*)$ within $< 7\%$ error (`classical/level4_two_phase.py`). |
| **10-Qubit Sz.-Nagy Unitary Dilation** | **MATHEMATICALLY DERIVED & VERIFIED** | $\|U_C^\dagger U_C - I\| = 4.44 \times 10^{-16}$, $\|P (\alpha_C U_C) P^T - C_2\| = 2.28 \times 10^{-13}$ in double precision. |
| **Dilation Normalization Scaling** | **MATHEMATICALLY DERIVED** | $\alpha_C = 7.9004$ for $\tau_f = 0.80$; $\alpha_C = 9.7321$ for $\tau_f = 0.65$ ($\alpha_C \propto \omega_f = 1/\tau_f$). |
| **Spatial Tensor Streaming Failure** | **MATHEMATICALLY DERIVED & REPRODUCED** | Naive $S \otimes S$ shifts quadratic cross-terms by $\mathbf{c}_a + \mathbf{c}_b$, yielding $419.5\%$ error on non-uniform fields. |
| **Linear Permutation Streaming Repair** | **DIRECTLY VERIFIED BY CODE** | Linear streaming permutation $S$ on $\mathbb{R}^{18}$ + local re-lifting achieves $0.000000 \times 10^0$ error on $Y_2 = \mathbf{z} \otimes \mathbf{z}$. |
| **Dilation Leakage vs Projected Reset** | **MATHEMATICALLY DERIVED & VERIFIED** | Unprojected chain leaks $2098.7\%$ at $K=2$; projective reset achieves $[P (\alpha_C U_C) P^T]^K = C_2^K$ ($< 1.71 \times 10^{-15}$ at $K=32$). |
| **OAA First-Principles Derivation** | **MATHEMATICALLY DERIVED** | For $\alpha_C = 9.7321$, $m=7$ iterations achieves $p_7 = 99.928\%$ requiring 8 $U_C$ + 7 $U_C^\dagger$ + 14 reflections = 29 operations. |
| **Cumulative Multi-Block Success** | **MATHEMATICALLY DERIVED** | Cumulative OAA success probability for $K=32$ blocks is $(0.999283)^{32} = 97.73\%$. |
| **Logical Qubit Allocation** | **MATHEMATICALLY DERIVED** | 19 data logical qubits ($7_x + 6_y + 5_{\text{vel}} + 1_{\text{anc}}$); 21 complete algorithmic logical qubits (including OAA and Carry ancillas). |
| **Hardware Viability (NISQ vs FTQC)** | **RESOURCE ESTIMATED** | Transpiled depth $> 3.76\text{M}$ with $> 831\text{k}$ ECR gates is NOT NISQ-viable; classified strictly as Fault-Tolerant (FTQC). |
| **Mach-Number Truncation Scaling** | **EMPIRICAL OBSERVATION** | Single-site error follows $\mathcal{E} = 0.0370 \cdot \text{Ma}^{2.003}$ ($R^2 = 1.00000$) over $\text{Ma} \in [0.005, 0.100]$. |
| **Grid Refinement Trend** | **EMPIRICAL OBSERVATION** | Monotonic error drop from $31.72\%$ ($16\times 8$) to $5.97\%$ ($256\times 128$) at $T=10$ with observed order $p \approx 0.54$. |
| **Bounded Mass Drift** | **EMPIRICAL OBSERVATION** | Liquid mass drift strictly bounded at $\le 1.528\%$ across 50 timesteps, matching Level-4 classical discretization. |
| **Interfacial CSF Surface Tension** | **HYBRID CLASSIFIED** | Brackbill CSF curvature $\kappa = -\nabla\cdot\mathbf{n}$ is evaluated on classical CPU and coupled as hybrid feedback every $K$ steps. |
| **Research Novelty Claims** | **LITERATURE-SUPPORTED** | Spatial tensor streaming obstruction and coupled 2-phase Carleman block encoding classified as Candidate Novelty (Category B). |
| **Fully Autonomous Quantum Solver** | **UNRESOLVED ISSUE / OPEN PROBLEM** | Requires on-chip quantum arithmetic for curvature stencils; left as future fault-tolerant research. |
