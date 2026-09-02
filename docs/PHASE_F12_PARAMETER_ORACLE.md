# PHASE F12: COHERENT PARAMETER ORACLE ARCHITECTURE
## Fixed-Point Reversible Arithmetic, Velocity Limiter, and Collision Matrix Synthesis

**Document**: Reversible Arithmetic & Parameter Generation Specification  
**Project**: Quantum Lattice Boltzmann Method (QLBM) for Two-Phase Flow  
**Repository**: `/home/aswa/Research/QLBM-DamBreak-Production`  
**Branch**: `feature/direct-encoding-two-phase-qlbm`  
**Date**: September 2026  

---

## 1. Fixed-Point Arithmetic ($Qm.n$) Representation

To execute nonlinear kinematic parameter synthesis coherently without floating-point ALU coprocessors:
- **Format $Q4.12$**: 1 sign bit, 3 integer bits, 12 fractional bits ($16$ total qubits per arithmetic register).
- **Dynamic Range**: $[-8.0, +7.99975]$ with precision resolution $\Delta = 2^{-12} \approx 2.44 \times 10^{-4}$.

$$\begin{array}{|c|c|c|c|c|c|}
\hline
\textbf{Precision Format} & \textbf{Total Bits} & \textbf{Dynamic Range} & \textbf{Resolution } \Delta & \text{Division Error } (a/b) & \textbf{Toffoli Cost / Op} \\
\hline
Q4.8 & 12 & [-8.0, +7.996] & 3.91 \times 10^{-3} & 4.86 \times 10^{-2} & 144 \\
Q4.12 & 16 & [-8.0, +7.999] & 2.44 \times 10^{-4} & 2.40 \times 10^{-4} & 256 \\
Q6.12 & 18 & [-32.0, +31.999] & 2.44 \times 10^{-4} & 2.40 \times 10^{-4} & 324 \\
Q8.16 & 24 & [-128.0, +127.999] & 1.53 \times 10^{-5} & 1.50 \times 10^{-5} & 576 \\
\hline
\end{array}$$

---

## 2. Reversible Division via Goldschmidt Iteration

To compute shifted velocity $\mathbf{u} = (\mathbf{j} + \frac{1}{2}\mathbf{F})/\rho_{\text{safe}}$:
$$x_0 \approx \text{LUT}(d), \quad x_{k+1} = x_k (2 - d x_k)$$
3 iterations yield full 12-bit precision with $3$ reversible array multipliers ($768$ Toffoli gates).

---

## 3. Parameterized Collision Block Synthesis & Unitary Dilation

From $(u_x, u_y, \alpha, \rho, \mathbf{F})$, the oracle computes:
$$\nu_{\text{mix}}(\alpha) = \alpha \nu_L + (1 - \alpha)\nu_G, \quad \tau_f = 3\nu_{\text{mix}} + 0.5, \quad \omega_f = \frac{1}{\tau_f}$$
The resulting $18 \times 18$ linear matrix $C(\alpha, \mathbf{u}, \mathbf{F}/\rho)$ is embedded via 6-qubit Sz.-Nagy dilation $U_C \in \mathbb{U}(64)$ with success probability $p_0 \approx 0.82$.
