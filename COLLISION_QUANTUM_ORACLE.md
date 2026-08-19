# Mathematical Design of the Quantum Collision Operator Oracle

**Author**: Lead Quantum Algorithm Engineer & Quantum Linear Algebra Specialist  
**Date**: August 19, 2026  
**Repository**: `/home/aswa/Research/QLBM-DamBreak/`  

---

## 1. Local Kronecker Factorization of Collision

The global second-order Carleman collision matrix $\mathbf{C}_2 \in \mathbb{R}^{342N \times 342N}$ is strictly block-diagonal across spatial sites:
$$ \mathbf{C}_2 = \mathbf{I}_N \otimes \mathbf{C}_{2, node} $$

where $\mathbf{C}_{2, node} \in \mathbb{R}^{342 \times 342}$ is the local upper-triangular collision block:
$$ \mathbf{C}_{2, node} = \begin{bmatrix} \mathbf{M}_{1, node} & \mathbf{M}_{2, node} \\ \mathbf{0} & \mathbf{M}_{1, node} \otimes \mathbf{M}_{1, node} \end{bmatrix} $$

- $\mathbf{M}_{1, node} \in \mathbb{R}^{18 \times 18}$: Local linear relaxation operator.
- $\mathbf{M}_{2, node} \in \mathbb{R}^{18 \times 324}$: Local quadratic contraction tensor.
- $\mathbf{M}_{1, node} \otimes \mathbf{M}_{1, node} \in \mathbb{R}^{324 \times 324}$: Local Kronecker square of linear relaxation.

---

## 2. Scalable Quantum Block Encoding Strategy

Because $\mathbf{C}_2$ is a Kronecker product with the identity matrix $\mathbf{I}_N$:
1. Construct the canonical Halmos CS-dilation $\mathcal{U}_{C2, node} \in \mathbb{C}^{1024 \times 1024}$ of the local $342 \times 342$ matrix on exactly **10 qubits** ($1$ ancilla $+ 9$ node-state qubits).
2. The global block encoding is simply:
   $$ \mathcal{U}_{C2} = \mathbf{I}_N \otimes \mathcal{U}_{C2, node} $$
   which acts identically and independently on the internal distribution register of each spatial site $n$.

### Computational & Resource Scaling:
- **Global Normalization**: $\alpha = \|\mathbf{C}_2\|_2 = \|\mathbf{C}_{2, node}\|_2 = \mathbf{10.9275}$ (Strictly constant for all $N$).
- **Gate Synthesis Complexity**: Requires synthesizing only **one single 10-qubit local unitary $\mathcal{U}_{C2, node}$**, eliminating the need for dense $N$-qubit matrix decompositions.
