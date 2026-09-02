# LEVEL-7: LITERATURE COMPARISON & SCIENTIFIC NOVELTY

**Document**: Comparative Literature Review and Identification of Novel Research Contributions  
**Repository**: `/home/aswa/Research/QLBM-DamBreak-Production`  
**Date**: September 2026  

---

## 1. Prior Art in Quantum Lattice Boltzmann & Carleman PDE Solvers

1. **Quantum Lattice Boltzmann for Single-Phase Flows** (e.g., Mezzacapo et al., 2015; Itani et al., 2024):
   Focuses predominantly on linearized single-phase single-relaxation-time (SRT) models without free surfaces or phase interfaces.
2. **Carleman Linearization for Fluid Dynamics** (e.g., Liu et al., 2021; Jin et al., 2022):
   Applies Carleman linearization to generic quadratic ODE systems or 1D/2D Burgers equations. Assumes global or continuous spatial differential operators.
3. **Quantum Singular Value Transformation (QSVT)** (Gilyén et al., 2019):
   Establishes optimal polynomial block-encoding transformations, but assumes static linear operators and does not address non-local dynamic interface curvature.

---

## 2. Novel Contributions of Level 7

1. **Identification of the Spatial Tensor Streaming Invariant Obstruction**:
   First rigorous mathematical proof that decoupled Kronecker tensor lifting $S \otimes S$ fails under spatial advection for discrete lattice velocity sets ($z_a(\mathbf{x}-\mathbf{c}_a) z_b(\mathbf{x}-\mathbf{c}_b)$ involves populations from distinct spatial nodes).
2. **First Coupled Two-Phase Carleman Block Encoding**:
   Formulation of the 18-variable coupled hydrodynamic-phase state vector $\mathbf{z} = [\mathbf{f}; \mathbf{g}]$, its 342-dimensional second-order Carleman expansion, and 10-qubit Sz.-Nagy unitary dilation $U_C \in \mathbb{U}(1024)$.
3. **Block-Encoded Multi-Step Composition with Projective Resets**:
   Rigorous derivation of dilation subspace leakage ($P U_C^K P \ne C_2^K$) and proof that projective resets or Oblivious Amplitude Amplification (OAA) restore machine-precision composition ($[P U_C P]^K = C_2^K$).
4. **Physical Dam-Break Validation**:
   First physical comparison of a Carleman-linearized QLBM against experimental multi-phase dam-break benchmark data (Martin & Moyce, 1952).
