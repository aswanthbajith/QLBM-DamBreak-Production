# LEVEL-6A-R: MATHEMATICAL DERIVATION OF SPATIAL TENSOR STREAMING

**Document**: First-Principles Derivation of Tensor Streaming & Non-Invariance of Local Kronecker Lifting  
**Repository**: `/home/aswa/Research/QLBM-DamBreak-Production`  
**Date**: September 2026  

---

## 1. Physical Lattice Boltzmann Streaming

In the D2Q9 Lattice Boltzmann framework, the physical streaming step advances population distribution functions along discrete lattice velocity vectors $\mathbf{c}_a \in \mathbb{Z}^2$:

$$z_a^*(\mathbf{x}, t+1) = (\mathcal{S} \mathbf{z})_a(\mathbf{x}, t) = z_a(\mathbf{x} - \mathbf{c}_a, t), \quad a \in \{0, \dots, 17\}$$

where:
- $\mathbf{c}_0 = (0, 0)$
- $\mathbf{c}_1 = (1, 0), \mathbf{c}_2 = (0, 1), \mathbf{c}_3 = (-1, 0), \mathbf{c}_4 = (0, -1)$
- $\mathbf{c}_5 = (1, 1), \mathbf{c}_6 = (-1, 1), \mathbf{c}_7 = (-1, -1), \mathbf{c}_8 = (1, -1)$
- For phase populations $g_i$ (indices $9 \dots 17$), $\mathbf{c}_{9+i} = \mathbf{c}_i$.

---

## 2. Derivation of the Exact Streamed Quadratic Product Tensor

By definition, the quadratic product tensor at destination lattice node $\mathbf{x}$ after physical streaming is:

$$\mathbf{Y}_{\text{quad}, ab}^*(\mathbf{x}, t+1) = z_a^*(\mathbf{x}, t+1) \cdot z_b^*(\mathbf{x}, t+1) = z_a(\mathbf{x} - \mathbf{c}_a, t) \cdot z_b(\mathbf{x} - \mathbf{c}_b, t)$$

Let us analyze the origin coordinates of the two factors:
1. **Case 1: Equal Lattice Velocities ($\mathbf{c}_a = \mathbf{c}_b$)**:
   $$\mathbf{x} - \mathbf{c}_a = \mathbf{x} - \mathbf{c}_b = \mathbf{x}_0$$
   $$\mathbf{Y}_{\text{quad}, ab}^*(\mathbf{x}, t+1) = z_a(\mathbf{x}_0, t) z_b(\mathbf{x}_0, t) = \mathbf{Y}_{\text{quad}, ab}(\mathbf{x}_0, t)$$
   The product originates from the *single* spatial node $\mathbf{x}_0 = \mathbf{x} - \mathbf{c}_a$.

2. **Case 2: Unequal Lattice Velocities ($\mathbf{c}_a \ne \mathbf{c}_b$)**:
   $$\mathbf{x}_1 = \mathbf{x} - \mathbf{c}_a \quad \text{and} \quad \mathbf{x}_2 = \mathbf{x} - \mathbf{c}_b, \quad \text{with } \mathbf{x}_1 \ne \mathbf{x}_2$$
   $$\mathbf{Y}_{\text{quad}, ab}^*(\mathbf{x}, t+1) = z_a(\mathbf{x}_1, t) \cdot z_b(\mathbf{x}_2, t)$$
   The two components originate from **two distinct spatial nodes** $\mathbf{x}_1 \ne \mathbf{x}_2$.

---

## 3. Analysis of Decoupled Kronecker Lifting ($S_{\text{lifted}} = S \otimes S$)

In the node-decoupled local Carleman formulation, each spatial node $\mathbf{x}$ stores exclusively its own local tensor:
$$\mathbf{Y}_{\text{local}}(\mathbf{x}, t) = \begin{bmatrix} \mathbf{z}(\mathbf{x}, t) \\ \mathbf{z}(\mathbf{x}, t) \otimes \mathbf{z}(\mathbf{x}, t) \end{bmatrix} \in \mathbb{R}^{342}$$
When the linear operator $S_{\text{lifted}} = S \otimes S$ is applied as an independent spatial shift to the quadratic sector, it shifts component $(a, b)$ by the vector sum $(\mathbf{c}_a + \mathbf{c}_b)$:
$$\mathbf{Y}_{\text{lifted}, ab}^*(\mathbf{x}, t+1) = z_a(\mathbf{x} - \mathbf{c}_a - \mathbf{c}_b, t) \cdot z_b(\mathbf{x} - \mathbf{c}_a - \mathbf{c}_b, t)$$

### Exact Streaming Difference Operator:
$$\Delta_{\text{stream}, ab}(\mathbf{x}) = \mathbf{Y}_{\text{lifted}, ab}^*(\mathbf{x}) - \mathbf{Y}_{\text{quad}, ab}^*(\mathbf{x}) = z_a(\mathbf{x} - \mathbf{c}_a - \mathbf{c}_b) z_b(\mathbf{x} - \mathbf{c}_a - \mathbf{c}_b) - z_a(\mathbf{x} - \mathbf{c}_a) z_b(\mathbf{x} - \mathbf{c}_b)$$
- For a uniform (spatially constant) state: $\mathbf{z}(\mathbf{x}) = \mathbf{z}_0 \forall \mathbf{x} \implies \Delta_{\text{stream}} = 0$.
- For any physical state with spatial gradients (e.g., dam-break interface $\nabla\alpha \ne 0$): $\Delta_{\text{stream}} \ne 0$.
- **Measured Invariance Error**:
  - Uniform Liquid: $0.00\%$
  - Random Field: $90.03\%$
  - Perturbed Interface: $92.04\%$
  - Dam-Break $t=0$: $62.41\%$

---

## 4. Theorem on Non-Existence of Decoupled Linear Tensor Streaming

> **Theorem (Non-Invariance of Local Kronecker Lift under Spatial Advection)**:  
> Let $\mathcal{M} = \{ \mathbf{Y} \in \mathbb{R}^{342 N} : \mathbf{Y}_{\text{quad}}(\mathbf{x}) = \mathbf{z}(\mathbf{x}) \otimes \mathbf{z}(\mathbf{x}) \; \forall \mathbf{x} \}$ be the invariant second-order Carleman manifold.  
> There does **NOT** exist any local linear operator or spatial permutation $S_2: \mathbb{R}^{324 N} \to \mathbb{R}^{324 N}$ on the node-decoupled state space such that $S_2(\mathbf{Y}) \in \mathcal{M}$ for all non-constant physical states $\mathbf{z} \in \mathbb{R}^{18 N}$.

### Proof:
To evaluate $z_a(\mathbf{x}_1) z_b(\mathbf{x}_2)$ for $\mathbf{x}_1 \ne \mathbf{x}_2$, the linear operator must have access to the bilinear product of amplitudes between node $\mathbf{x}_1$ and node $\mathbf{x}_2$. In a decoupled representation of dimension $342 N$, only intra-node products $z_a(\mathbf{x}) z_b(\mathbf{x})$ are represented. The cross-node product is mathematically absent from the basis. To include all cross-node products requires a global bipartite tensor of dimension $(18 N)^2 = 324 N^2$, which scales quadratically with lattice volume $\mathcal{O}(N^2)$. $\blacksquare$
