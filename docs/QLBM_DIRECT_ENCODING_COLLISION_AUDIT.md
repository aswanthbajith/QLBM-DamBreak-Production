# QUANTUM TWO-PHASE DAM-BREAK LBM (QLBM)
## Collision Strategy Audit & Quantum Collision Mechanisms

**Document**: Analysis of Quantum Collision Realizability & Mechanism Proposals  
**Repository**: `/home/aswa/Research/QLBM-DamBreak-Production`  
**Branch**: `feature/direct-encoding-two-phase-qlbm`  
**Date**: September 2026  

---

## 1. Current Scientific Status of Collision

In the Phase 1 direct-encoding prototype, the collision step is executed as a **classical numerical update** in a hybrid quantum-classical loop:
$$\mathbf{f}^*(\mathbf{x}) = \mathbf{f}(\mathbf{x}) - \omega_f (\mathbf{f}(\mathbf{x}) - \mathbf{f}^{\text{eq}}(\mathbf{x})) + \mathbf{S}_{\text{Guo}}(\mathbf{x})$$
and the updated populations are re-encoded into the statevector $|\Psi\rangle$.

$$\mathbf{STATUS:\ Quantum\ collision\ is\ NOT\ yet\ executed\ on-chip\ in\ this\ prototype.}$$

---

## 2. Three Proposed Quantum Collision Mechanisms

$$\begin{array}{|l|c|c|c|}
\hline
\textbf{Mechanism Feature} & \textbf{Mechanism A: Block-Encoded Dilation} & \textbf{Mechanism B: Reversible Arithmetic} & \textbf{Mechanism C: Unitary Low-Mach Taylor} \\
\hline
\text{Mathematical Mapping} & \text{Embed local } M_{\text{coll}} \in \mathbb{R}^{18\times 18} \text{ in unitary dilation } U_{\text{coll}} & \text{Evaluate } \rho, \mathbf{u}, f^{\text{eq}} \text{ via coherent adder/divider} & \text{Unitary polynomial approximation } e^{-i H_{\text{BGK}} \Delta t} \\
\text{Qubit Ancillas} & 1 \text{ dilation ancilla per node} & > 50 \text{ arithmetic work qubits} & 0 \text{ ancillas (unitary)} \\
\text{Reversibility} & \text{Dilated unitary; requires projection} & \text{Fully reversible (uncomputing)} & \text{Strictly unitary} \\
\text{Dilation Scaling } (\alpha_{\text{coll}}) & \alpha_{\text{coll}} \approx 1.5 \implies p_0 \approx 44\% & \text{None (exact arithmetic)} & \text{None (unitary generator)} \\
\text{Circuit Depth} & \mathcal{O}(10^3) \text{ per node} & > 10^7 \text{ Toffoli depth} & \mathcal{O}(10^2) \text{ per node} \\
\text{Approximation Error} & \text{Exact for linear sector; low-Mach} & \text{Exact to register precision} & \mathcal{O}(\text{Ma}^2) \text{ truncation error} \\
\text{Multi-Step Stability} & \text{Requires projective reset} & \text{Autonomous} & \text{Energy-conserving} \\
\text{Feasibility} & \textbf{Early-to-Mid FTQC} & \text{Late-Stage FTQC} & \textbf{Early FTQC / NISQ Study} \\
\hline
\end{array}$$

---

## 3. Recommended Path for Quantum Collision
- **Short-Term (Phase 2/3)**: Maintain hybrid classical collision and hybrid CSF feedback while scaling gate-level quantum streaming and boundary circuits.
- **Medium-Term (Phase 4)**: Implement **Mechanism A (Node-Conditioned Block-Encoded Collision Dilation)** across the 5-qubit velocity/phase register.
