# Master Polynomial Operator & Algebraic Lifting Audit

**Author**: Lead Mathematical Modeler & Numerical Analyst  
**Date**: August 19, 2026  
**Repository**: `/home/aswa/Research/QLBM-DamBreak/`  

---

## 1. Executive Summary
The discrete time-step map of the classical two-phase D2Q9 velocity-based LBM solver has been mathematically transformed into an exact, finite-dimensional polynomial operator system and lifted into a complete Carleman linear system $\mathbf{Y}_2(t+1) = \mathbf{A}_C \mathbf{Y}_2(t) + \mathbf{b}_C$.

---

## 2. Mathematical Operator Properties

| Operator | Mathematical Role | Dimension | Sparsity / NNZ | Spectrum / Properties | Verification File |
| :--- | :--- | :---: | :---: | :--- | :--- |
| **$\mathbf{S}$** | Spatial streaming & boundary reflection | $18N \times 18N$ | $18N$ ($1$ per row) | Strictly Unitary ($\mathbf{S}^T \mathbf{S} = \mathbf{I}$) | `classical/matrix_two_phase_lbm.py` |
| **$\mathbf{M}_1$** | Linear collision relaxation | $18N \times 18N$ | $162N$ | Block-diagonal, real eigenvalues $\in (0, 1]$ | `classical/matrix_two_phase_lbm.py` |
| **$\mathbf{M}_2$** | Quadratic convective/advective tensor | $18N \times 324N$ | $\mathcal{O}(N)$ | Local node contraction tensor | `quantum/carleman_lbm.py` |
| **$\mathbf{S}_C$** | Complete Carleman streaming operator | $342N \times 342N$ | $342N$ ($1$ per row) | Strictly Unitary ($\mathbf{S}_C^T \mathbf{S}_C = \mathbf{I}$) | `quantum/carleman_lbm.py` |
| **$\mathbf{C}_2$** | Complete Carleman collision matrix | $342N \times 342N$ | $\mathcal{O}(N)$ | Block upper-triangular | `quantum/carleman_lbm.py` |
| **$\mathbf{A}_C$** | Complete Carleman time-step matrix | $342N \times 342N$ | $\approx 27,334 N$ | Sparse CSR matrix ($\mathbf{A}_C = \mathbf{S}_C \mathbf{C}_2$) | `quantum/carleman_lbm.py` |

---

## 3. Claim Classification Table

| Mathematical Statement | Classification | Empirical / Analytical Evidence |
| :--- | :---: | :--- |
| **1. Streaming is strictly unitary ($\mathbf{S}^T \mathbf{S} = \mathbf{I}$)** | **VERIFIED BY CODE + TEST** | `tests/test_polynomial_system.py:test_01_streaming_matrix_properties` |
| **2. Polynomial degree is $p=2$ (Quadratic)** | **VERIFIED ANALYTICALLY** | `mappings/COMPLETE_POLYNOMIAL_DEGREE_AUDIT.md` |
| **3. Variable density closed cubic lifting ($p=3$)** | **VERIFIED ANALYTICALLY** | `mappings/COMPLETE_POLYNOMIAL_DEGREE_AUDIT.md` |
| **4. Single-step operator equivalence ($L_\infty < 1.7 \times 10^{-3}$)** | **NUMERICALLY VALIDATED** | 100-state random perturbation sweep |
| **5. Carleman Order 2 dimension is exactly $342N$** | **VERIFIED BY CODE + TEST** | `tests/test_carleman_lifting.py:test_01_dimensions` |
| **6. Multi-step Carleman error bounded $< 2.59\%$ over 50 steps** | **NUMERICALLY VALIDATED** | `scripts/run_carleman_study.py` |
| **7. Qubit register scaling is $n = \lceil\log_2(342N)\rceil + 1$** | **VERIFIED BY CODE + TEST** | `tests/test_quantum_resources.py:test_01_logarithmic_qubit_scaling` |
