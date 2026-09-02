# LEVEL-7: NOVELTY MATRIX & SCIENTIFIC DIFFERENTIATION

**Document**: Formal Classification and Evidence for Research Novelty Claims  
**Repository**: `/home/aswa/Research/QLBM-DamBreak-Production`  
**Date**: September 2026  

---

## 1. Formal Novelty Classification Scale

- **Category A: Clearly Novel**: No precedent in published literature; first complete mathematical derivation and numerical demonstration.
- **Category B: Probably Novel**: Minor related concepts in disparate fields, but first application and derivation in quantum fluid dynamics.
- **Category C: Candidate Novelty**: Methodological contribution requiring further formal literature review; defensible as a thesis contribution.
- **Category D: Previously Known**: Known in prior literature; adopted and applied here.
- **Category E: Cannot Determine**: Insufficient literature data.

---

## 2. Evaluation of Project Novelty Claims

| Novelty Claim | Description & Theoretical Basis | Literature Precedent | Classification | Thesis Value |
| :--- | :--- | :--- | :---: | :---: |
| **Claim 1: Spatial Tensor Streaming Obstruction** | Mathematical proof that decoupled $S \otimes S$ shifts quadratic cross-terms erroneously by $\mathbf{c}_a + \mathbf{c}_b$ rather than assembling distinct physical node products $z_a(\mathbf{x}-\mathbf{c}_a) z_b(\mathbf{x}-\mathbf{c}_b)$. | Tensor non-invariance is known abstractly in algebraic lifting; specific derivation in discrete velocity kinetic lattices is unaddressed in QLBM literature. | **Category B (Probably Novel)** | **HIGH (Major diagnostic breakthrough)** |
| **Claim 2: Coupled 2-Phase Carleman Block Encoding** | Formulation of coupled 18-variable state $\mathbf{z} = [\mathbf{f}; \mathbf{g}]$, its 342-dim second-order Carleman expansion, and 10-qubit Sz.-Nagy unitary dilation $U_C \in \mathbb{U}(1024)$. | Prior Carleman QLBMs (Itani 2023, Lăcătuş 2026) are strictly single-phase. Budinski (2026) is variational VQE, not Carleman block-encoded. | **Category B (Probably Novel)** | **HIGH (First 2-phase Carleman block encoding)** |
| **Claim 3: Projected Multi-Step Block-Encoding Composition** | Derivation of dilation defect leakage $D_* D \ne 0$ and proof that projective resets restore exact powers $[P U_C P]^K = C_2^K$ to machine precision ($< 10^{-15}$). | Block-encoding dilation leakage is known in quantum linear algebra; systematic analysis and mitigation in multi-step kinetic LBM is specific to this work. | **Category C (Candidate Methodological Novelty)** | **MEDIUM-HIGH (Essential technical mechanism)** |
| **Claim 4: Dam-Break Hydrodynamic & CSF Pipeline** | Integration of second-order Carleman collision with linear permutation streaming, bounce-back boundary involution, and hybrid Brackbill CSF feedback validated against Martin & Moyce. | No prior quantum Lattice Boltzmann study has reproduced experimental dam-break surge-front collapse with surface tension. | **Category B (Probably Novel)** | **HIGH (First physical validation of its kind)** |
