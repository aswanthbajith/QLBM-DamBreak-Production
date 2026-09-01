# PHASE 11 CLASSICAL LBM OPERATOR EXTRACTION & MATHEMATICAL MAPPING (STAGE 11.3)

**Auditor Role**: Senior Numerical Analyst & Quantum Algorithm Engineer  
**Date**: 2026-08-19  
**Source Code**: `classical/two_phase_lbm.py`, `classical/matrix_two_phase_lbm.py`, `quantum/carleman_lbm.py`  

---

## 1. Governing Evolution Operator Deconstruction

The actual classical LBM solver computes the time step via the operator composition:
$$\Psi(t+1) = S \cdot \Psi_{\text{post}}(\Psi(t))$$
where the state vector is partitioned into 18 discrete distribution modes per lattice node $n \in \{1..N\}$:
$$\Psi(t) = \begin{bmatrix} g_0(t) \\ \vdots \\ g_8(t) \\ h_0(t) \\ \vdots \\ h_8(t) \end{bmatrix} \in \mathbb{R}^{18N}$$

### A. Spatial Streaming & Reflection Operator $S \in \{0, 1\}^{18N \times 18N}$
* **Code Lineage**: `MatrixTwoPhaseLBM2D._build_streaming_matrix()` (Lines 74–116).
* **Mathematical Definition**: An exact spatial permutation operator:
  $$[S \Psi]_{field, q, \mathbf{x}} = \Psi_{field, q^*, \mathbf{x} - \mathbf{c}_q}$$
  where $q^* = q$ for interior streaming, $q^* = q_{\text{opp}}$ for no-slip walls, and $q^* = q_{\text{refl}}$ for free-slip boundaries.
* **Unitary Property**: $S^T S = I_{18N}$ (strictly orthogonal permutation matrix).

### B. Local Collision Operator $\mathcal{C}$
* **Code Lineage**: `MatrixTwoPhaseLBM2D.evaluate_collision()` (Lines 160–230) & `CarlemanTwoPhaseLBM` (Lines 100–180).
* **Quadratic Surrogate Representation**:
  $$\Psi_{\text{post}}(\mathbf{x}) = M_1 \Psi(\mathbf{x}) + M_2 (\Psi(\mathbf{x}) \otimes \Psi(\mathbf{x})) + \mathbf{b}_{\text{force}}(\mathbf{x})$$
  * $M_1 \in \mathbb{R}^{18 \times 18}$: Linear BGK relaxation operator $(I - \frac{1}{\tau}) + \frac{1}{\tau} \mathbf{w} \mathbf{1}^T$.
  * $M_2 \in \mathbb{R}^{18 \times 324}$: Local convective tensor coupling hydrodynamic momentum and phase advection.
  * $\mathbf{b}_{\text{force}} \in \mathbb{R}^{18}$: Constant gravitational and boundary force vector.

### C. Carleman Linearization Operator $A_C \in \mathbb{R}^{342N \times 342N}$
* **Code Lineage**: `CarlemanTwoPhaseLBM._build_carleman_matrix()` (Lines 125–220).
* **Block Upper-Triangular Form**:
  $$A_C = S_C \begin{bmatrix} M_1 & M_2 \\ 0 & M_1 \otimes I + I \otimes M_1 \end{bmatrix}$$
  where $S_C = S \oplus (S \otimes S)_{\text{local}}$ is the lifted spatial permutation matrix.
