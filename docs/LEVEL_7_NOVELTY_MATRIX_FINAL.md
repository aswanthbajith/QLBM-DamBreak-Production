# LEVEL-7: NOVELTY MATRIX & SCIENTIFIC PRIOR-ART DIFFERENTIATION (FINAL)
## Rigorous Qualification of Novelty Claims Against Published Literature (2015–2026)

**Document**: Final Hardened Novelty and Differentiation Matrix  
**Repository**: `/home/aswa/Research/QLBM-DamBreak-Production`  
**Date**: September 2026  

---

## 1. Five-Level Novelty Classification Rubric

- **Category A (Clearly Novel)**: No prior precedent in published literature; first complete mathematical derivation and numerical demonstration.
- **Category B (Probably Novel / Candidate Contribution)**: Related abstract principles exist in disparate mathematical physics domains, but first specific application, derivation, and validation in quantum fluid dynamics / QLBM.
- **Category C (Methodological Extension)**: Extension of existing quantum linear algebra methods to the specific problem domain.
- **Category D (Established Prior Art)**: Standard techniques adopted from existing literature.
- **Category E (Indeterminate)**: Literature priority cannot be definitively established.

---

## 2. Hardened Evaluation of Research Contributions

| Research Contribution | Prior Art Literature Precedent | Scientific Differentiation | Final Hardened Classification |
| :--- | :--- | :--- | :---: |
| **1. Spatial Tensor Streaming Obstruction** | Tensor non-invariance is known abstractly in nonlinear algebra. Unaddressed in QLBM literature. | First rigorous proof that decoupled spatial streaming $S \otimes S$ shifts quadratic cross-terms erroneously by $\mathbf{c}_a + \mathbf{c}_b$ rather than assembling distinct physical node products $z_a(\mathbf{x}-\mathbf{c}_a) z_b(\mathbf{x}-\mathbf{c}_b)$ ($419.5\%$ error). | **Category B (Candidate Novelty / Major Diagnostic Result)** |
| **2. Coupled 2-Phase Carleman Block Encoding** | Existing Carleman QLBMs (Itani 2023, Lăcătuş 2026) are strictly single-phase. Budinski (2026) is variational VQE. | First coupled 18-variable hydrodynamic-phase state vector $\mathbf{z} = [\mathbf{f}; \mathbf{g}]$ with 342-dim second-order Carleman expansion and 10-qubit Sz.-Nagy unitary dilation. | **Category B (Candidate Novelty / First Formulation)** |
| **3. Projected Block-Encoding Composition via Reset** | Subspace dilation leakage is known in quantum linear algebra; unaddressed in kinetic LBM multi-step loops. | Systematic derivation of defect operator leakage $D_* D \ne 0$ and demonstration that mid-circuit projective resets restore exact algebraic powers $[P U_C P]^K = C_2^K$ ($< 1.71 \times 10^{-15}$ at $K=32$). | **Category C (Methodological Extension)** |
| **4. Two-Phase Dam-Break Physical Validation** | No prior quantum fluid study has reproduced free-surface dam-break column collapse. | First physical benchmark comparison of a Carleman QLBM with Brackbill CSF surface tension against Martin & Moyce (1952) experimental data ($< 7\%$ error). | **Category B (Candidate Novelty / Physical Validation)** |
