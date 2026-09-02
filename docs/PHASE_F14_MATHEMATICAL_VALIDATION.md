# PHASE F14: MATHEMATICAL VALIDATION & OBSTRUCTION ANALYSIS
## Non-Unitarity, Nonlinearity, and the Fundamental Limits of Direct Population Amplitude Encoding

**Document**: Mathematical Validation & Fundamental Obstruction Analysis  
**Project**: Quantum Lattice Boltzmann Method (QLBM) for Two-Phase Flow  
**Repository**: `/home/aswa/Research/QLBM-DamBreak-Production`  
**Branch**: `feature/direct-encoding-two-phase-qlbm`  
**Date**: September 2026  

---

## 1. Mathematical Nature of the LBM Collision Map

The two-phase BGK collision operator is defined as:

$$f_i^* = (1 - \omega_f) f_i + \omega_f f_i^{\text{eq}}(\rho, \mathbf{u}) + S_i(\mathbf{F}, \mathbf{u})$$
$$g_i^* = (1 - \omega_g) g_i + \omega_g g_i^{\text{eq}}(\alpha, \mathbf{u})$$

where:
$$\rho = \sum_{i=0}^8 f_i, \quad \alpha = \sum_{i=0}^8 g_i, \quad \mathbf{u} = \frac{\sum f_i \mathbf{c}_i + \frac{1}{2}\mathbf{F}}{\rho}$$
$$f_i^{\text{eq}}(\rho, \mathbf{u}) = w_i \rho \left[ 1 + 3\mathbf{c}_i \cdot \mathbf{u} + \frac{9}{2}(\mathbf{c}_i \cdot \mathbf{u})^2 - \frac{3}{2}|\mathbf{u}|^2 \right]$$

### The Nonlinearity & Non-Unitarity Proof:
1. **Non-Unitarity**:
   $$\|C^\dagger C - I\|_2 > 0$$
   In general, BGK relaxation is strictly dissipative (entropy-increasing / $H$-theorem compliant). It contracts non-equilibrium fluctuations toward equilibrium, so all eigenvalues satisfy $|\lambda| \le 1$, meaning $C$ is a strict contraction and non-unitary.
2. **Nonlinearity on Statevector Amplitudes**:
   Under direct population encoding $|\Psi\rangle = \frac{1}{\mathcal{N}} \sum f_i |i, 0\rangle + g_i |i, 1\rangle$, the equilibrium distribution $f_i^{\text{eq}}$ involves rational polynomial functions of amplitudes:
   $$f_i^{\text{eq}} \propto \frac{(\sum f_j c_{jx})^2}{\sum f_k}$$
   Linear quantum mechanics forbids any single unitary operator $U$ from evaluating $U|\Psi\rangle = |\Psi^2 / \Psi\rangle$ on the computational basis amplitudes without auxiliary tensor copies ($|\Psi\rangle^{\otimes k}$) or intermediate observable conditioning.

---

## 2. Proven Pathways for Future Quantum Fluid Research

$$\begin{array}{|l|l|l|}
\hline
\textbf{Pathway} & \textbf{Mechanism} & \textbf{Resource / Complexity Trade-off} \\
\hline
\text{1. Hybrid Observable Feedback (Current)} & \text{Probe moments } \to \text{ Parameterize } U_C & \text{Practical, NISQ-compatible, } O(n_x+n_y) \text{ qubits} \\
\text{2. Carleman Linearization} & |\Psi\rangle \otimes |\Psi\rangle \dots \text{ tensor products} & \text{Exponential Hilbert space expansion} \\
\text{3. QSVT / LCU Polynomial Block-Encoding} & \text{Polynomial approximations of } f^{\text{eq}} & \text{Fault-tolerant, deep T-gate circuit depth} \\
\hline
\end{array}$$

---

## 3. Final Milestone Classification

$$\mathbf{PHASE\ F14\ SCIENTIFIC\ DECISION:\ LEVEL\ B}$$

$$\boxed{\text{“COHERENT QUANTUM EVOLUTION WITH A FORMALLY IDENTIFIED RESIDUAL HYBRID INTERFACE”}}$$
