# Carleman Linearization and State Space Lifting (Level 5)

## 1. Mathematical Formulation for Two-Phase LBM
The discrete two-phase evolution equation isolated in Level 4:
$$
\mathbf{\Psi}(t+1) = \mathbf{A}_1 \mathbf{\Psi}(t) + \mathbf{A}_2 (\mathbf{\Psi}(t) \otimes \mathbf{\Psi}(t)) + \mathbf{b}_{force}
$$
is lifted into the finite-dimensional Carleman state space:
$$
\mathbf{y}_2(t) = \begin{bmatrix} \mathbf{\Psi}(t) \\ \mathbf{\Psi}^{\otimes 2}_{local}(t) \end{bmatrix} \in \mathbb{R}^{D_2}
$$
where:
- Base physical state: $\mathbf{\Psi} = [\mathbf{g}; \mathbf{h}] \in \mathbb{R}^{18 N}$
- Local Kronecker square: $\mathbf{\Psi}^{\otimes 2}_{local}(\mathbf{x}_n) = \mathbf{\Psi}(\mathbf{x}_n) \otimes \mathbf{\Psi}(\mathbf{x}_n) \in \mathbb{R}^{324}$
- Total Carleman dimension: $D_2 = 18 N + 324 N = 342 N$.

---

## 2. Linear Carleman Operator
The lifted linear recurrence is:
$$
\mathbf{y}_2(t+1) = \mathcal{M}_2 \mathbf{y}_2(t) + \mathbf{b}_C
$$
where:
$$
\mathcal{M}_2 = \begin{bmatrix} \mathbf{S} & \mathbf{0} \\ \mathbf{0} & \mathbf{S} \otimes \mathbf{S} \end{bmatrix} \begin{bmatrix} \mathbf{M}_1 & \mathbf{M}_2 \\ \mathbf{0} & \mathbf{M}_1 \otimes \mathbf{M}_1 \end{bmatrix}
$$
- **Linear Collision $\mathbf{M}_1$**: Block-diagonal relaxation operator.
- **Quadratic Collision $\mathbf{M}_2$**: Local $18 \times 324$ quadratic tensor contraction kernel.
- **Carleman Streaming $\mathbf{S}_C$**: Unitary spatial permutation matrix ($\mathbf{S}_C^T \mathbf{S}_C = \mathbf{I}$).
