# Mathematical Audit: Local vs. Global Kronecker Structure in Carleman LBM

**Author**: Lead Mathematical Scientist & Senior Numerical Analyst  
**Date**: August 19, 2026  
**Repository**: `/home/aswa/Research/QLBM-DamBreak/`  

---

## 1. Global vs. Local Kronecker Dimension Scaling

In standard naive Carleman linearization for a global state vector $\mathbf{\Psi} \in \mathbb{R}^{d_{global}}$ ($d_{global} = 18 N$), the full second Kronecker power is:
$$ \mathbf{\Psi} \otimes \mathbf{\Psi} \in \mathbb{R}^{(18 N)^2} = \mathbb{R}^{324 N^2} $$
For a grid with $N = 30,000$ nodes, this global representation would require $324 \times 9 \times 10^8 \approx 2.91 \times 10^{11}$ variables ($\approx 2.3 \text{ TB}$ of state memory), which is computationally intractable.

However, the Lattice Boltzmann Method possesses an exact mathematical property: **Strict Locality of the Collision Operator**.

---

## 2. Mathematical Decoupling Theorem

### Theorem (Local Collision / Linear Streaming Decoupling):
Let the discrete LBM time-step operator be partitioned into collision $\mathcal{C}$ and streaming $\mathcal{S}$:
$$ \mathbf{\Psi}(t+1) = \mathcal{S}(\mathcal{C}(\mathbf{\Psi}(t))) $$
1. **Collision is Strictly Local**: For every lattice site $n \in \{1, \dots, N\}$, the post-collision state $\mathbf{\psi}_n^{post} \in \mathbb{R}^{18}$ depends *only* on the local node state $\mathbf{\psi}_n(t) \in \mathbb{R}^{18}$:
   $$ \mathbf{\psi}_n^{post} = \mathbf{M}_{1, node} \mathbf{\psi}_n(t) + \mathbf{M}_{2, node} (\mathbf{\psi}_n(t) \otimes \mathbf{\psi}_n(t)) $$
   Therefore, no cross-node quadratic products $\mathbf{\psi}_i(t) \otimes \mathbf{\psi}_j(t)$ for $i \neq j$ are generated during collision.
2. **Streaming is Strictly Linear**: The spatial propagation operator $\mathcal{S}$ is a linear spatial permutation matrix $\mathbf{S} \in \{0, 1\}^{18N \times 18N}$. Spatial interaction across neighboring nodes occurs *exclusively* through $\mathbf{S}$.
3. **Exact Linear Streaming for Quadratic Monomials**: For the quadratic sector $\mathbf{Y}_{2, quad}(t) = \bigoplus_{n=1}^N (\mathbf{\psi}_n(t) \otimes \mathbf{\psi}_n(t)) \in \mathbb{R}^{324 N}$, spatial advection of product pairs $(q_1, q_2)$ is performed by the block permutation $\mathbf{S}_{kron2} \in \{0, 1\}^{324 N \times 324 N}$.

### Conclusion:
Local Kronecker assembly $\mathbf{\Psi}_{local}^{\otimes 2} \in \mathbb{R}^{324 N}$ is **mathematically exact** for the collision step, reducing the quadratic dimension from $\mathcal{O}(N^2)$ to $\mathcal{O}(N)$ without omitting any local nonlinear interaction.
