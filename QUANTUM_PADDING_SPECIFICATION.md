# Mathematical Specification of Non-Power-of-Two Subspace Padding

**Author**: Lead Quantum Algorithm Engineer & Quantum Linear Algebra Specialist  
**Date**: August 19, 2026  
**Repository**: `/home/aswa/Research/QLBM-DamBreak/`  

---

## 1. Subspace Embedding Transformation

Because the Carleman state dimension $D_C = 342 N$ is not an exact power of two, the operator is embedded into the nearest containing $n_{sys}$-qubit Hilbert space $\mathcal{H}_{sys} \cong \mathbb{C}^{D_{pad}}$ where $D_{pad} = 2^{n_{sys}}$:

$$ \mathbf{A}_{pad} = \begin{bmatrix} \mathbf{A}_C & \mathbf{0} \\ \mathbf{0} & \mathbf{I}_{pad} \end{bmatrix} \in \mathbb{C}^{D_{pad} \times D_{pad}} $$

where $\mathbf{I}_{pad} = \mathbf{I}_{D_{pad} - D_C}$ is the identity operator on the unphysical subspace.

---

## 2. Invariance & Non-Contamination Theorems

### Theorem 1 (Physical Subspace Restriction):
For any physical state vector $|Y\rangle \in \mathbb{C}^{D_C}$ embedded as $|Y_{pad}\rangle = \begin{bmatrix} |Y\rangle \\ \mathbf{0} \end{bmatrix} \in \mathbb{C}^{D_{pad}}$:
$$ \mathbf{A}_{pad} |Y_{pad}\rangle = \begin{bmatrix} \mathbf{A}_C & \mathbf{0} \\ \mathbf{0} & \mathbf{I}_{pad} \end{bmatrix} \begin{bmatrix} |Y\rangle \\ \mathbf{0} \end{bmatrix} = \begin{bmatrix} \mathbf{A}_C |Y\rangle \\ \mathbf{0} \end{bmatrix} $$
The action of $\mathbf{A}_{pad}$ on the physical subspace is **strictly identical** to $\mathbf{A}_C$.

### Theorem 2 (Zero Contamination):
Because the off-diagonal coupling blocks are strictly zero:
$$ \mathbf{A}_{pad}[:D_C, D_C:] = \mathbf{0}, \quad \mathbf{A}_{pad}[D_C:, :D_C] = \mathbf{0} $$
no amplitude from the unphysical padding subspace can leak into the physical fluid state, and no physical amplitude can scatter into the padding subspace.

### Theorem 3 (Spectral Norm Invariance):
Because $\|\mathbf{I}_{pad}\|_2 = 1.0$ and $\|\mathbf{A}_C\|_2 = 10.9275 \ge 1.0$:
$$ \|\mathbf{A}_{pad}\|_2 = \max\left( \|\mathbf{A}_C\|_2, \|\mathbf{I}_{pad}\|_2 \right) = \|\mathbf{A}_C\|_2 = 10.9275 $$
Padding does **not** inflate the subnormalization factor $\alpha$.
