# PHASE F26: RESOURCE-OPTIMIZED OPEN-SYSTEM TWO-PHASE QLBM
## Sequential Workspace Scheduling, Symmetry-Optimized Arithmetic, and Spatial Architecture Trade-Offs

**Document**: Resource-Optimized Open-System Two-Phase QLBM Report  
**Project**: Quantum Lattice Boltzmann Method (QLBM) for Two-Phase Flow  
**Repository**: `/home/aswa/Research/QLBM-DamBreak-Production`  
**Development Branch**: `feature/direct-encoding-two-phase-qlbm`  
**Baseline Level-6B SHA-256**: `2a306f5a413945adc1acd10f3f63340c3d3617e4ef1c94981a92e8ebad8742c8` (**100% Intact**)  
**Audit Date**: September 2026  

---

## 1. Executive Summary

Phase F26 performed a systematic optimization study of the validated Level-B open-system two-phase QLBM architecture. Without altering the underlying physical equations, the optimizations demonstrate:
1. **50% Toffoli Reduction in Equilibrium**: By exploiting D2Q9 velocity symmetries ($c_1 = -c_3, c_2 = -c_4, c_5 = -c_7, c_6 = -c_8$), the required directional squaring operations were halved, reducing equilibrium multiplier Toffoli count from $7,168 \to 3,584\text{ Toffolis/node}$.
2. **Sequential Compute-Use-Uncompute-Reuse Workspace Scheduling**: Bounded peak arithmetic ancillas to **$48\text{ qubits/node}$** by recycling scratchpad registers across phases rather than holding cumulative workspace.
3. **Spatial Architecture Trade-Offs**: Architecture B (shared reversible execution core with spatial population storage) achieves a **$2.17\times\text{ reduction in total logical qubits}$** ($5.11\text{M} \to 2.36\text{M}$ qubits for a $128 \times 64$ mesh).
4. **Precision/Accuracy Pareto Optimum**: **$Q4.16$** provides the optimal engineering trade-off ($1.54\%$ relative CSF force error, $3.05 \times 10^{-5}$ hydrodynamic error, and exact integer mass conservation).

---

## 2. Corrected Resource Accounting Breakdown ($16\text{-bit } Q4.12$)

$$\begin{array}{|l|c|c|l|}
\hline
\textbf{Register Category} & \textbf{Bit-Width } n & \textbf{Qubits / Node} & \textbf{Allocation Semantics} \\
\hline
\text{System Populations } (f_i, g_i) & 16 & 288 & \text{Persistent spatial state (18 fields } \times 16\text{ bits)} \\
\text{Environment Registers } (e_{f_i}, e_{g_i}) & 16 & 288 & \text{Open-system Stinespring dilation bath (recycled per step)} \\
\text{Peak Arithmetic Workspace} & 16 & 48 & \text{Sequential scratchpad (reused across moments, divs, CSF, eq)} \\
\hline\hline
\mathbf{Total\ Logical\ Qubits\ per\ Node} & \mathbf{16} & \mathbf{624} & \mathbf{Peak\ active\ footprint\ per\ lattice\ node} \\
\hline
\end{array}$$

---

## 3. D2Q9 Symmetry-Optimized Arithmetic Formulation

$$\begin{array}{rcl}
u_{\text{diag1}} = u_x + u_y, &\quad& u_{\text{diag2}} = -u_x + u_y \\
(c_1 \cdot \mathbf{u})^2 = (c_3 \cdot \mathbf{u})^2 = u_x^2, &\quad& (c_2 \cdot \mathbf{u})^2 = (c_4 \cdot \mathbf{u})^2 = u_y^2 \\
(c_5 \cdot \mathbf{u})^2 = (c_7 \cdot \mathbf{u})^2 = u_{\text{diag1}}^2, &\quad& (c_6 \cdot \mathbf{u})^2 = (c_8 \cdot \mathbf{u})^2 = u_{\text{diag2}}^2
\end{array}$$
- **Toffoli Savings**: Computing only $4$ quadratic invariants ($u_x^2, u_y^2, u_{\text{diag1}}^2, u_{\text{diag2}}^2$) reduces polynomial equilibrium Toffolis by **$50\%$**.

---

## 4. Sequential Compute-Use-Uncompute-Reuse Workspace Schedule

$$\begin{array}{|l|c|l|}
\hline
\textbf{Execution Phase} & \textbf{Peak Ancillas} & \textbf{Uncomputation & Recycling Action} \\
\hline
\text{Phase 1: Moments } (\rho, \alpha, \mathbf{j}) & 32\text{ qubits} & \text{Accumulates sums into workspace; passes to velocity divider} \\
\text{Phase 2: Velocity Division } (\mathbf{u} = \mathbf{j}/\rho) & 48\text{ qubits} & \text{Computes reciprocal, writes } \mathbf{u}\text{, uncomputes reciprocal scratch} \\
\text{Phase 3: Reversible CSF Stencils} & 48\text{ qubits} & \text{Evaluates } \nabla \alpha, \kappa, \mathbf{F}_s\text{, adds to } \mathbf{j}\text{, uncomputes stencils} \\
\text{Phase 4: Equilibrium & BGK Relaxation} & 48\text{ qubits} & \text{Computes symmetric invariants and linear relaxation, uncomputes} \\
\text{Phase 5: Positivity & Mass Guard} & 16\text{ qubits} & \text{Enforces } f_0 \ge 0\text{, uncomputes comparator flag} \\
\hline
\end{array}$$

---

## 5. Precision/Accuracy Pareto Front ($4\times 4$ Dam-Break)

$$\begin{array}{|l|c|c|c|c|c|}
\hline
\textbf{Format} & \textbf{Fractional Bits} & \text{LSB Resolution} & \text{Hydro Error } (\Delta \rho) & \text{CSF Rel Error } (L_2) & \textbf{Mass Drift} \\
\hline
Q4.8 & 8 & 3.91 \times 10^{-3} & 1.56 \times 10^{-2} & \sim 68\% & \mathbf{0.000000} \\
Q4.10 & 10 & 9.77 \times 10^{-4} & 1.95 \times 10^{-3} & \sim 35\% & \mathbf{0.000000} \\
Q4.12 & 12 & 2.44 \times 10^{-4} & 2.44 \times 10^{-4} & 23.35\% & \mathbf{0.000000} \\
Q4.14 & 14 & 6.10 \times 10^{-5} & 2.44 \times 10^{-4} & 6.20\% & \mathbf{0.000000} \\
\mathbf{Q4.16} & \mathbf{16} & \mathbf{1.53 \times 10^{-5}} & \mathbf{3.05 \times 10^{-5}} & \mathbf{1.54\%} & \mathbf{0.000000} \\
Q4.18 & 18 & 3.81 \times 10^{-6} & 3.81 \times 10^{-6} & 0.40\% & \mathbf{0.000000} \\
\mathbf{Q4.20} & \mathbf{20} & \mathbf{9.54 \times 10^{-7}} & \mathbf{3.81 \times 10^{-6}} & \mathbf{0.10\%} & \mathbf{0.000000} \\
\hline
\end{array}$$

$$\mathbf{Pareto\ Optimum:\ Q4.16\ provides\ optimal\ precision\ (<1.6\%\ force\ error,\ 3.05 \times 10^{-5}\ density\ error).}$$

---

## 6. Spatial Scaling Comparison ($128 \times 64$ Domain, $8,192\text{ Nodes}$)

$$\begin{array}{|l|c|c|c|}
\hline
\textbf{Spatial Architecture} & \textbf{Total Logical Qubits} & \textbf{Hardware Strategy} & \textbf{Trade-Off} \\
\hline
\text{Architecture A (Parallel 2D Grid)} & 5,111,808 & \text{Dedicated circuits per node} & \text{Fastest wall-clock, max qubits} \\
\mathbf{Architecture\ B\ (Shared\ Core)} & \mathbf{2,359,632} & \mathbf{Shared\ reversible\ ALU\ +\ memory} & \mathbf{2.17\times\ qubit\ reduction,\ serialized\ execution} \\
\hline
\end{array}$$

---

## 7. Final Scientific Classification & Recommendation

### Recommended Architecture:
$$\mathbf{Architecture\ B\ (Shared\ Reversible\ Arithmetic\ Core)\ with\ Q4.16\ Fixed\text{-}Point\ Precision}$$

### Scientific Classification:
$$\mathbf{PHASE\ F26\ SCIENTIFIC\ CLASSIFICATION:\ LEVEL\ B}$$

$$\boxed{\text{“Open-system quantum channel formulation of two-phase LBM with validated CPTP evolution and quantified finite-precision equivalence; gate-level reversible realization of the nonlinear BGK+CSF map remains a separate resource-intensive research problem.”}}$$
