# Exact Matrix-Operator Equivalence Verification Report

## 1. Executive Summary
- **Operator Structure**:
  $$\mathbf{\Psi}(t+1) = \mathbf{S} \cdot \mathbf{\Psi}^{post}(\mathbf{\Psi}(t))$$
  where $\mathbf{S} \in \{0, 1\}^{18N \times 18N}$ is the unitary spatial permutation and boundary reflection matrix.
- **Maximum Point-wise Discrepancy**: $L_\infty = 6.0454e-04$ across 50 time steps.
- **Maximum Relative $L_2$ Discrepancy**: $L_2 = 1.1487e-03$.

---

## 2. Step-by-Step Numerical Verification Table

| Step | Max Point-Wise Error $L_\infty$ | Relative Error $L_2$ | Equivalence Status |
| :---: | :---: | :---: | :---: |
| **0** | $0.0000e+00$ | $0.0000e+00$ | **EXACT (ZERO)** |
| **10** | $5.4791e-05$ | $8.7047e-05$ | **DISCREPANCY** |
| **20** | $1.3559e-04$ | $3.1942e-04$ | **DISCREPANCY** |
| **30** | $2.7174e-04$ | $6.2150e-04$ | **DISCREPANCY** |
| **40** | $4.2656e-04$ | $9.0197e-04$ | **DISCREPANCY** |
| **50** | $6.0454e-04$ | $1.1487e-03$ | **DISCREPANCY** |

---

## 3. Structural Properties of Discrete Operators
1. **Global Streaming Matrix $\mathbf{S}$**:
   - Dimension: $18N \times 18N = 14400 \times 14400$
   - Sparsity: Exactly $1.0$ non-zero entry ($+1.0$) per row and column.
   - Unitary Property: $\mathbf{S}^T \mathbf{S} = \mathbf{I}_{18N}$ (strictly exact).
2. **Boundary Treatment**:
   - Solid walls: Half-way bounce back ($\mathbf{c}_{\bar{q}} = -\mathbf{c}_q$).
   - Floor: Specular reflection ($c_y \to -c_y$).
