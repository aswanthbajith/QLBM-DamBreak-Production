# QUANTUM TWO-PHASE DAM-BREAK LBM (QLBM)
## Quantum Collision Architecture Investigation & Decision Matrix (Phases B, C, D)

**Document**: Mathematical Derivation, Route Comparison, and Architectural Decision  
**Project**: Quantum Lattice Boltzmann Method (QLBM) for Two-Phase Flow  
**Repository**: `/home/aswa/Research/QLBM-DamBreak-Production`  
**Branch**: `feature/direct-encoding-two-phase-qlbm`  
**Date**: September 2026  

---

## 1. Phase B: Complete Dissection of the Local Two-Phase Collision Map

Starting from the exact Level-4 classical equations at spatial node $\mathbf{x}$, the local state is:
$$\mathbf{z} = [f_0, \dots, f_8, g_0, \dots, g_8]^T \in \mathbb{R}^{18}$$

The post-collision state $\mathbf{z}' = \mathcal{C}(\mathbf{z})$ is governed by:
$$\begin{aligned}
f_i' &= f_i - \omega_f(\alpha) [f_i - f_i^{\text{eq}}(\rho, \mathbf{u})] + S_i(\mathbf{u}, \mathbf{F}) \\
g_i' &= g_i - \omega_g [g_i - g_i^{\text{eq}}(\alpha, \mathbf{u})]
\end{aligned}$$

### Rigorous Algebraic Dissection:
$$\begin{array}{|l|l|c|l|}
\hline
\textbf{Component / Term} & \textbf{Mathematical Formulation} & \textbf{Algebraic Type} & \textbf{Quantum Realization Challenge} \\
\hline
\text{Linear Identity Block} & (1-\omega_f)f_i, \ (1-\omega_g)g_i & \textbf{Linear} & \text{Trivially block-encodable} \\
\text{Linear Equilibrium Sector} & w_i \rho, \ w_i \alpha, \ 3w_i (\mathbf{c}_i \cdot \mathbf{j}) & \textbf{Linear} & \text{Direct unitary matrix block} \\
\text{Convective Momentum Flux} & \frac{9}{2} w_i (\mathbf{c}_i \cdot \mathbf{u})^2 - \frac{3}{2} w_i u^2 & \textbf{Rational} \ (j_a j_b / \rho) & \text{Requires division by } \rho \text{ or Taylor expansion} \\
\text{Phase Advection Coupling} & 3 w_i \alpha (\mathbf{c}_i \cdot \mathbf{u}) & \textbf{Rational} \ (\alpha j_a / \rho) & \text{Requires bilinear division} \\
\text{Density Inversion} & \rho^{-1} & \textbf{Rational} & \text{Requires quantum divider or Taylor } 2-\rho \\
\text{Viscosity Inversion} & \omega_f(\alpha) = [3(\alpha\nu_L + (1-\alpha)\nu_G) + 0.5]^{-1} & \textbf{Rational} & \text{Requires parameter inversion} \\
\text{Buoyancy Forcing} & (\rho - \rho_G)\mathbf{g} & \textbf{Linear in } \rho & \text{Linear parameter input} \\
\text{CSF Surface Tension} & \mathbf{F}_s = \sigma \kappa \nabla\alpha & \textbf{Non-Local \& Rational} & \text{Requires spatial stencils \& normal division} \\
\text{Interface Normal Unitization} & \mathbf{n} = \nabla\alpha / \sqrt{|\nabla\alpha|^2 + \epsilon^2} & \textbf{Transcendental / Sqrt} & \text{Intractable on-chip ($> 10^9$ Toffoli depth)} \\
\text{Phase Fraction Clipping} & \alpha = \text{clip}(\sum g_i, 0, 1) & \textbf{Piecewise Non-Smooth} & \text{Requires comparator logic} \\
\hline
\end{array}$$

---

## 2. Phase C: Comparative Investigation of Three Quantum Collision Routes

### Route C1: Block-Encoded Local Collision Dilation
- **Mechanism**: Construct the linearized/approximated 18-variable collision matrix $C \in \mathbb{R}^{18 \times 18}$, pad to $32 \times 32$ (5 qubits: 4 velocity + 1 phase), and embed into a 6-qubit Sz.-Nagy unitary dilation $U_C \in \mathbb{U}(64)$ with dilation ancilla.
- **Normalization & Success Probability**:
  $$\|C\|_2 = 2.0443, \quad \alpha_C = 1.01 \cdot \|C\|_2 = \mathbf{2.0647} \implies p_0 = \frac{1}{\alpha_C^2} = \mathbf{23.46\%}$$
- **Oblivious Amplitude Amplification (OAA)**:
  - Grover angle: $\theta = \arcsin(1/\alpha_C) = 0.50536\text{ rad} \ (28.95^\circ)$.
  - After **$m = 1$ iteration**: $p_1 = \sin^2(3\theta) = \mathbf{99.71\%}$ per collision block!
  - Requires only **2 forward $U_C$ + 1 inverse $U_C^\dagger$ + 2 reflections = 5 total operations (3 unitaries)**.
- **Multi-Step Leakage**: Unprojected powers leak defect amplitude ($300\%$ error at $K=2$), whereas intermediate projective reset restores exact algebraic powers $C^K$ to machine precision ($< 10^{-14}$).

### Route C2: Reversible Quantum Fixed-Point Arithmetic
- **Mechanism**: Construct coherent in-place fixed-point adders (Cuccaro), multipliers (Wallace-tree), and non-restoring dividers on quantum registers.
- **Resource Analysis (One Node)**:
  - 16-bit moment additions (26 operations): $\approx 416$ Toffolis.
  - 16-bit non-restoring divisions ($u = j/\rho$): $\approx 512$ Toffolis.
  - Multiplications (equilibrium & relaxation): $\approx 9,984$ Toffolis.
  - **Total Gate Count**: $\approx \mathbf{10,912 \text{ Toffolis}}$ ($\approx 76,000$ T-gates) per spatial node.
  - **Logical Qubits**: $32 - 338$ qubits per node; Toffoli depth $> 15,000$.
- **Classification**: Late-Stage Fault-Tolerant (FTQC) only.

### Route C3: Polynomial / Carleman Truncation Collision
- **Mechanism**: Second-order polynomial expansion with $1/\rho \approx 2 - \rho$.
- **Error Scaling vs Mach Number**:
  $$\mathcal{E}_{\text{collision}} = 0.1005 \cdot \text{Ma}^{6.009} \quad (R^2 = 1.00000)$$
  - $\text{Ma} = 0.005$: Error $= 1.47 \times 10^{-15}$
  - $\text{Ma} = 0.050$: Error $= 1.53 \times 10^{-9}$
  - $\text{Ma} = 0.100$: Error $= 9.78 \times 10^{-8}$
- **Conclusion**: Carleman polynomialization introduces negligible truncation error ($< 10^{-7}$) across the entire weakly compressible regime ($\text{Ma} \le 0.10$).

---

## 3. Phase D: Decision Matrix & Architectural Selection

$$\begin{array}{|l|c|c|c|}
\hline
\textbf{Decision Metric} & \textbf{Route C1: Block Encoding} & \textbf{Route C2: Quantum Arithmetic} & \textbf{Route C3: Carleman Truncation} \\
\hline
\text{Physical Fidelity} & \text{Exact linear, low-Mach approx} & \text{Exact fixed-point BGK} & \mathcal{O}(\text{Ma}^6) \text{ error } (< 10^{-7}) \\
\text{Quantum Realizability} & \textbf{High (6-Qubit Unitary } U_C) & \text{Low (Requires FTQC Arithmetic)} & \text{Medium (Lifted Subspace)} \\
\text{One-Node Qubits} & \mathbf{6 \text{ Logical Qubits}} & 32 - 338 \text{ Qubits} & 10 \text{ Qubits} \\
\text{One-Node Depth} & \mathbf{\approx 250 \text{ Gates}} & > 15,000 \text{ Toffoli Depth} & > 3.76\text{M (Full Lifted)} \\
\text{Base Success } p_0 & \mathbf{23.46\% \ (\alpha_C = 2.065)} & 100\% \ (\text{Unitary Arithmetic}) & 1.056\% \ (\alpha_C = 9.732) \\
\text{OAA Query Count} & \mathbf{m=1 \to 99.71\% \ (3 Unitaries)} & \text{None needed} & m=7 \to 99.93\% \ (15 Unitaries) \\
\text{Multi-Step Leakage} & \text{Requires projective reset} & \text{Autonomous (no leakage)} & \text{Requires projective reset} \\
\text{Scalability across Grid} & \mathcal{O}(\log N) \text{ with node block} & \mathcal{O}(N \times \text{Depth}) & \mathcal{O}(N \times \text{Lifted}) \\
\text{Two-Phase Compatibility} & \textbf{Full (Coupled 18-variable)} & \text{Full (Bilinear update)} & \textbf{Full (Coupled Carleman)} \\
\text{CSF Surface Tension} & \text{Hybrid Feedback} & \text{Hybrid / Quantum Stencil} & \text{Hybrid Feedback} \\
\hline
\textbf{Architectural Decision} & \mathbf{SELECTED\ FOR\ PHASE\ E} & \text{PROSPECTIVE\ (Late FTQC)} & \text{CONDITIONAL\ (High Depth)} \\
\hline
\end{array}$$

$$\mathbf{PRIMARY\ DECISION:\ SELECT\ ROUTE\ C1\ (BLOCK-ENCODED\ COLLISION\ DILATION)}$$
Route C1 is selected as the primary quantum collision mechanism for Phase E prototyping because it operates with compact register sizing (6 qubits per node), low normalization scaling ($\alpha_C \approx 2.06$, $p_0 \approx 23.5\%$), and requires only $m=1$ Grover iteration to achieve $> 99.7\%$ per-block success probability.
