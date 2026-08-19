# Mathematical Formulation of the Carleman Linear Operator

**Author**: Lead Mathematical Modeler & Numerical Analyst  
**Date**: August 19, 2026  
**Repository**: `/home/aswa/Research/QLBM-DamBreak/`  

---

## 1. Carleman Linear System Definition

Given the discrete quadratic map:
$$ \mathbf{\Psi}(t+1) = \mathbf{S} \left[ \mathbf{M}_1 \mathbf{\Psi}(t) + \mathbf{M}_2 (\mathbf{\Psi}(t) \otimes_{local} \mathbf{\Psi}(t)) \right] $$

The second-order Carleman state vector $\mathbf{Y}_2(t) \in \mathbb{R}^{342 N}$ is defined as:
$$ \mathbf{Y}_2(t) = \begin{bmatrix} \mathbf{\Psi}(t) \\ \mathbf{\Psi}_{local}^{\otimes 2}(t) \end{bmatrix} \in \mathbb{R}^{18 N + 324 N} $$

The lifted discrete linear time-step system is:
$$ \mathbf{Y}_2(t+1) = \mathbf{A}_C \mathbf{Y}_2(t) + \mathbf{b}_C $$

where:
$$ \mathbf{A}_C = \mathbf{S}_C \cdot \mathbf{C}_2 \in \mathbb{R}^{342 N \times 342 N} $$

---

## 2. Block Collision Operator $\mathbf{C}_2 \in \mathbb{R}^{342 N \times 342 N}$
The collision operator is block upper-triangular:
$$ \mathbf{C}_2 = \begin{bmatrix} \mathbf{M}_1 & \mathbf{M}_2 \\ \mathbf{0} & \mathbf{M}_{1, kron2} \end{bmatrix} $$
where:
- $\mathbf{M}_1 = \mathbf{I}_N \otimes \mathbf{M}_{1, node} \in \mathbb{R}^{18N \times 18N}$: Linear relaxation.
- $\mathbf{M}_2 = \mathbf{I}_N \otimes \mathbf{M}_{2, node} \in \mathbb{R}^{18N \times 324N}$: Quadratic convective coupling.
- $\mathbf{M}_{1, kron2} = \mathbf{I}_N \otimes (\mathbf{M}_{1, node} \otimes \mathbf{M}_{1, node}) \in \mathbb{R}^{324N \times 324N}$: Kronecker square of linear relaxation.

---

## 3. Block Streaming Operator $\mathbf{S}_C \in \{0, 1\}^{342 N \times 342 N}$
The streaming operator is block-diagonal:
$$ \mathbf{S}_C = \begin{bmatrix} \mathbf{S} & \mathbf{0} \\ \mathbf{0} & \mathbf{S}_{kron2} \end{bmatrix} $$
where:
- $\mathbf{S} \in \{0, 1\}^{18N \times 18N}$: Unitary spatial streaming permutation for base populations.
- $\mathbf{S}_{kron2} \in \{0, 1\}^{324N \times 324N}$: Unitary spatial streaming permutation for product pairs $(q_1, q_2)$.

### Unitary Proof:
$$ \mathbf{S}_C^T \mathbf{S}_C = \begin{bmatrix} \mathbf{S}^T \mathbf{S} & \mathbf{0} \\ \mathbf{0} & \mathbf{S}_{kron2}^T \mathbf{S}_{kron2} \end{bmatrix} = \begin{bmatrix} \mathbf{I}_{18N} & \mathbf{0} \\ \mathbf{0} & \mathbf{I}_{324N} \end{bmatrix} = \mathbf{I}_{342N} $$
$\mathbf{S}_C$ is strictly orthogonal and unitary in $\mathbb{R}^{342N}$.

---

## 4. State Lifting and Projection
1. **Lifting Operator $\mathcal{L}: \mathbb{R}^{18N} \to \mathbb{R}^{342N}$**:
   $$ \mathcal{L}(\mathbf{\Psi}) = \begin{bmatrix} \mathbf{\Psi} \\ \mathbf{\psi}_1 \otimes \mathbf{\psi}_1 \\ \vdots \\ \mathbf{\psi}_N \otimes \mathbf{\psi}_N \end{bmatrix} $$
2. **Projection Operator $\mathcal{P}: \mathbb{R}^{342N} \to \mathbb{R}^{18N}$**:
   $$ \mathcal{P}(\mathbf{Y}_2) = \begin{bmatrix} \mathbf{I}_{18N} & \mathbf{0} \end{bmatrix} \mathbf{Y}_2 = \mathbf{\Psi} $$
