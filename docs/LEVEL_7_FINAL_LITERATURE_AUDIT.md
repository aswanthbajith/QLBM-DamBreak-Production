# LEVEL-7: COMPREHENSIVE LITERATURE & PRIOR-ART AUDIT
## Contextualizing Two-Phase Carleman QLBM in the Modern Quantum Fluid Dynamics Literature (2015–2026)

**Document**: Independent Literature Review and Prior-Art Differentiation  
**Repository**: `/home/aswa/Research/QLBM-DamBreak-Production`  
**Date**: September 2026  

---

## 1. Overview of the Quantum Fluid Dynamics Landscape

Quantum algorithms for fluid dynamics have evolved along two primary branches:
1. **Direct Non-Linear Carleman ODE/PDE Solvers**: Focus on polynomial embedding of Navier-Stokes/Burgers equations (e.g., Liu et al., PNAS 2021; Jin et al., 2022) into global spacetime linear systems ($L \mathbf{y} = \mathbf{b}$) solved via Quantum Linear System Algorithms (QLSA / HHL) or Quantum Singular Value Transformation (QSVT).
2. **Quantum Lattice Boltzmann Methods (QLBM)**: Discretize kinetic phase space onto discrete velocity lattices (D1Q2, D1Q3, D2Q9) and evolve hydrodynamic distributions through alternating collision and streaming operators (e.g., Mezzacapo et al., PRL 2015; Itani et al., PRA 2023; Lăcătuş & Möller, IJNME 2026; Budinski, CPC 2026).

---

## 2. Detailed Comparison with Landmark Publications

### A. Mezzacapo et al. (Phys. Rev. Lett. 115, 160501, 2015)
- **Model**: Linearized single-phase collision without Carleman linearization.
- **Velocity Lattice**: 1D/2D toy models (D1Q2, D2Q4).
- **Distinction**: Uses direct unitary gate synthesis on discrete velocity states; does not incorporate nonlinear advection, Carleman quadratic lifting, multi-phase phase fields, or surface tension.

### B. Liu et al. (PNAS 118 (35), e2026805118, 2021)
- **Model**: Global Carleman linearization for general dissipative quadratic ODEs and continuous Burgers equations.
- **Algorithm**: Global space-time QLSA / Carleman truncation with logarithmic state preparation.
- **Distinction**: Focuses on continuous differential operators in macro-space; does not address kinetic lattice streaming, discrete velocity involutions, or free-surface boundary conditions.

### C. Itani et al. (Phys. Rev. A 108, 022409, 2023)
- **Model**: Single-phase D1Q3 and D2Q9 hydrodynamic Lattice Boltzmann with Carleman collision block encoding.
- **Architecture**: Hybrid single-step ($K=1$) execution.
- **Distinction**: Demonstrates single-phase hydrodynamic Carleman collision. Does not feature coupled two-phase phase-field equations ($g_i$), Brackbill Continuum Surface Force (CSF), or multi-phase dam-break benchmarking.

### D. Lăcătuş & Möller (Int. J. Numer. Meth. Eng. 127(4), e70286, 2026)
- **Model**: Second-order Carleman-linearized D2Q9 solver formulated as a global space-time linear system solved via Linear Combination of Unitaries (LCU) and QSVT.
- **Benchmark**: Single-phase 2D Poiseuille and lid-driven cavity flows.
- **Distinction**: Operates as a global spacetime linear system assuming static linear collision operators. Cannot evaluate state-dependent dynamic surface tension $\mathbf{F}_s = \sigma \kappa(\alpha) \nabla\alpha$ without an intractable quantum arithmetic oracle.

### E. Budinski (Comput. Phys. Commun. 321, 110040, 2026)
- **Model**: Color-gradient two-phase multiphase Lattice Boltzmann method.
- **Algorithm**: Variational Quantum Eigensolver (VQE) optimization on classical NISQ emulator.
- **Distinction**: Uses a variational parametric ansatz rather than unitary block encoding, Carleman linearization, or Sz.-Nagy dilation.

---

## 3. Position of This Research Project

This research project uniquely bridges the gap between **Carleman block-encoded kinetic lattices** and **complex two-phase free-surface hydrodynamic flow**:
1. It formulates the **18-variable coupled hydrodynamic-phase state vector** $\mathbf{z}(\mathbf{x}) = [\mathbf{f}(\mathbf{x}); \mathbf{g}(\mathbf{x})]$ and its 342-dimensional second-order Carleman expansion.
2. It discovers and mathematically proves the **spatial tensor streaming obstruction** in lifted Carleman lattices.
3. It resolves dilation subspace leakage via **mid-circuit projective resets** ($[P U_C P]^K = C_2^K$).
4. It provides the first comparison of a Carleman QLBM against the classical experimental dam-break benchmark (Martin & Moyce, 1952).
