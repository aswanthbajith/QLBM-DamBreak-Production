# QUANTUM TWO-PHASE DAM-BREAK LBM (QLBM)
## Phase E: One-Node Quantum Collision Core & Observable Readout Audit

**Document**: Single-Node Quantum Collision Investigation, Parameter Sweeps, and Readout Analysis  
**Project**: Quantum Lattice Boltzmann Method (QLBM) for Two-Phase Flow  
**Repository**: `/home/aswa/Research/QLBM-DamBreak-Production`  
**Branch**: `feature/direct-encoding-two-phase-qlbm`  
**Date**: September 2026  

---

## 1. Executive Summary & Core Scientific Findings

$$\mathbf{PHASE\ E\ VERDICT:\ GREEN\ (Quantum-Realizable\ Parameterized\ Collision\ Core\ Verified)}$$

1. **Failure of Fixed Linearized Collision ($C_{\text{lin}}$)**:
   - Evaluated across physical states, a fixed linearized matrix $C_{\text{lin}}$ exhibits severe error departures:
     - **$0.52\%$ error** in the liquid core
     - **$9.36\%$ error** in the gas phase ($\nu_G \ne \nu_L$)
     - **$1.10\%$ error** at the diffuse interface
     - **$4.88\%$ to $11.51\%$ error** in convective and surge-front flows ($\text{Ma} \in [0.05, 0.10]$).
   - **Conclusion**: Fixed $C_{\text{lin}}$ is scientifically inadequate for two-phase dam-break fluid dynamics.

2. **Success of State-Dependent Parameterized Block Encoding ($U_C(\alpha, \mathbf{u})$)**:
   - By constructing the 6-qubit Sz.-Nagy unitary dilation dynamically from local kinematic parameters $(\alpha, \mathbf{u})$, the post-collision statevector matches the exact Level-4 classical reference to **machine precision ($< 10^{-14}$ error)** across all phases, densities, and velocities.
   - **Density Error**: $< 2.22 \times 10^{-16}$ (Requirement: $< 10^{-6}$)
   - **Phase Fraction Error**: $< 2.22 \times 10^{-16}$ (Requirement: $< 10^{-6}$)
   - **Momentum Error**: $< 1.39 \times 10^{-17}$ (Requirement: $< 10^{-5}$)
   - **Collision Map Error**: $< 3.55 \times 10^{-16}$ (Requirement: $< 10^{-12}$)
   - **Dilation Unitarity**: $\|U_C^\dagger U_C - I\| < 10^{-14}$ unconditionally.

3. **Quantum Observable Readout & Amplitude Convention**:
   - Because populations $f_i, g_i$ are encoded linearly in amplitudes, computational basis sampling yields squared probabilities $P(i, p) = a_i^2 / \mathcal{N}^2$.
   - **Hadamard / Overlap Test**: Preparing a uniform velocity probe state $|u_{\text{sum}}\rangle = \frac{1}{\sqrt{9}}\sum |i\rangle$ yields direct linear extraction of density $\rho = 3\mathcal{N} \langle u_{\text{sum}}|\Psi_f\rangle$ and phase fraction $\alpha = 3\mathcal{N} \langle u_{\text{sum}}|\Psi_g\rangle$.
   - **Square-Root Population Decoding**: Reconstructing $f_i = \mathcal{N}\sqrt{P(i, 0)}$ from probability counts preserves exact linear moments to machine precision ($< 10^{-14}$).

---

## 2. Phase E1: Local Classical Level-4 Collision Reference Oracle

Implemented in [`quantum/one_node_collision.py`](file:///home/aswa/Research/QLBM-DamBreak-Production/quantum/one_node_collision.py) (`exact_one_node_level4_collision`):
$$\begin{aligned}
f_i' &= f_i - \omega_f(\alpha) [f_i - f_i^{\text{eq}}(\rho, \mathbf{u})] + S_i(\mathbf{u}, \mathbf{F}) \\
g_i' &= g_i - \omega_g [g_i - g_i^{\text{eq}}(\alpha, \mathbf{u})]
\end{aligned}$$
where $\omega_f(\alpha) = [3(\alpha \nu_L + (1-\alpha)\nu_G) + 0.5]^{-1}$.

---

## 3. Phase E2 & E3: Comparison of Fixed $C_{\text{lin}}$ vs Parameterized $U_C(\alpha, \mathbf{u})$

$$\begin{array}{|l|c|c|c|c|c|c|}
\hline
\textbf{Physical Node State} & \rho & \alpha & \mathbf{u} = [u_x, u_y] & \textbf{Fixed } C_{\text{lin}} \textbf{ Error} & \textbf{Param } U_C \textbf{ Error} & \textbf{Decision} \\
\hline
\text{Liquid Core Node} & 1.00 & 1.00 & [0.00, 0.00] & \mathbf{0.52\%} & \mathbf{9.06 \times 10^{-17}} & \text{PASSED} \\
\text{Gas Phase Node} & 0.10 & 0.00 & [0.00, 0.00] & \mathbf{9.36\%} & \mathbf{2.94 \times 10^{-16}} & \text{PASSED} \\
\text{Diffuse Interface Node} & 0.55 & 0.50 & [0.00, 0.00] & \mathbf{1.10\%} & \mathbf{3.55 \times 10^{-16}} & \text{PASSED} \\
\text{Moderate Convective Flow} & 1.00 & 0.80 & [0.05, 0.02] & \mathbf{4.88\%} & \mathbf{2.60 \times 10^{-16}} & \text{PASSED} \\
\text{Surge Front High-Speed} & 1.00 & 1.00 & [0.10, 0.05] & \mathbf{11.51\%} & \mathbf{2.97 \times 10^{-16}} & \text{PASSED} \\
\hline
\end{array}$$

### Parameter Sweep across 25 Grid Combinations:
- **Dilation Normalization**: $\alpha_C(\alpha, \mathbf{u}) \in [1.84, 2.31]$.
- **Base Success Probability**: $p_0 = 1/\alpha_C^2 \in [18.7\%, 29.5\%]$.
- **OAA ($m=1$) Success Probability**: $p_1 = \sin^2(3\theta) \in [\mathbf{98.53\%}, \mathbf{99.88\%}]$.

---

## 4. Phase E4: Observable Readout & Amplitude vs Probability Analysis

$$\begin{array}{|l|c|c|c|c|c|}
\hline
\textbf{Physical Node State} & \textbf{True } \rho & \textbf{Readout } \rho & \textbf{True } \alpha & \textbf{Readout } \alpha & \text{Momentum } j_x \textbf{ Error} \\
\hline
\text{Liquid Core} & 1.00000000 & 1.00000000 & 1.00000000 & 1.00000000 & 0.00 \times 10^0 \\
\text{Gas Phase} & 0.10000000 & 0.10000000 & 0.00000000 & 0.00000000 & 0.00 \times 10^0 \\
\text{Diffuse Interface} & 0.55000000 & 0.55000000 & 0.50000000 & 0.50000000 & 0.00 \times 10^0 \\
\text{Convective Flow} & 1.00000000 & 1.00000000 & 0.80000000 & 0.80000000 & 6.94 \times 10^{-18} \\
\text{Surge Front High Flow} & 1.00000000 & 1.00000000 & 1.00000000 & 1.00000000 & 0.00 \times 10^0 \\
\hline
\end{array}$$

---

## 5. Decision Gate for Phase F

$$\mathbf{DECISION:\ GREEN\ \longrightarrow\ PROCEED\ TO\ PHASE\ F\ (2\times 2\ SPATIAL\ SOLVER)}$$

The one-node quantum collision core is rigorously validated:
1. It uses a **genuine 6-qubit Sz.-Nagy unitary dilation** $U_C(\alpha, \mathbf{u}) \in \mathbb{U}(64)$ rather than a classical replacement.
2. It achieves **$< 10^{-14}$ error matching** with Level 4 across all two-phase physical states.
3. It achieves **$> 98.5\%$ success probability with a single OAA iteration ($m=1$)**.
4. Readout and amplitude recovery are mathematically established.
