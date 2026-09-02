# LEVEL-7: MATHEMATICAL INVESTIGATION REPORT
## First-Principles Analysis of Coherent Multi-Timestep Quantum Operators

**Document**: Mathematical Derivation of Operator Composition, Streaming Permutations, and Invariant Manifolds  
**Repository**: `/home/aswa/Research/QLBM-DamBreak-Production`  
**Date**: September 2026  

---

## 1. Local Carleman Block-Encoding & Defect Operators

Let $C_2 \in \mathbb{R}^{342 \times 342}$ be the coupled second-order Carleman collision matrix, sub-unitarily normalized by $\alpha_C = 7.9004$ ($C_{\text{bar}} = C_2 / \alpha_C$).
The 10-qubit Sz.-Nagy unitary dilation is:

$$U_C = \begin{bmatrix} C_{\text{bar}} & D_* \\ D & -C_{\text{bar}}^T \end{bmatrix}, \quad D = \sqrt{I - C_{\text{bar}}^T C_{\text{bar}}}, \quad D_* = \sqrt{I - C_{\text{bar}} C_{\text{bar}}^T}$$

Let $P = [I_{342}, 0]$ be the projection onto the physical subspace (dilation ancilla $|0_{\text{anc}}\rangle$).

---

## 2. Derivation of Dilation Subspace Leakage

When $U_C$ is applied repeatedly without intermediate projection:

$$P U_C^2 P^T = C_{\text{bar}}^2 + D_* D = \frac{C_2^2}{\alpha_C^2} + \left(I - \frac{C_2 C_2^T}{\alpha_C^2}\right)$$

$$P (\alpha_C U_C)^2 P^T = C_2^2 + \alpha_C^2 \left(I - \frac{C_2 C_2^T}{\alpha_C^2}\right) \ne C_2^2$$

### Measured Numerical Divergence:
- $K = 1$: $\|P (\alpha_C U_C) P^T - C_2\| = 5.58 \times 10^{-17}$ (Exact)
- $K = 2$: $\|P (\alpha_C U_C)^2 P^T - C_2^2\| / \|C_2^2\| = \mathbf{20.987 \ (2098.7\% \text{ Error})}$
- $K = 4$: $\|P (\alpha_C U_C)^4 P^T - C_2^4\| / \|C_2^4\| = \mathbf{1558.3 \ (155830\% \text{ Error})}$

### Resolution via Projective Measurement / Reset:
Applying a mid-circuit projective measurement and reset on $|0_{\text{anc}}\rangle$ between steps yields:

$$[P (\alpha_C U_C) P^T]^K = C_2^K$$

- Error across all $K = 1 \dots 8$: $< 2.3 \times 10^{-16}$ (Exact to machine precision).
- Unamplified Success Probability: $p_{\text{succ}}(K) = \alpha_C^{-2K}$.
- Amplified Success Probability via Oblivious Amplitude Amplification (OAA): $p_{\text{succ},\text{OAA}} \approx 1 - \epsilon$ using $\mathcal{O}(\alpha_C)$ Grover reflections per step.

---

## 3. Spatial Advection & Invariant Manifold Derivation

In physical Lattice Boltzmann advection, linear populations shift along discrete velocities:
$$z_a^*(\mathbf{x}) = z_a(\mathbf{x} - \mathbf{c}_a)$$

The physical quadratic product at destination node $\mathbf{x}$ is:
$$(\mathbf{z}^* \otimes \mathbf{z}^*)_{ab}(\mathbf{x}) = z_a(\mathbf{x} - \mathbf{c}_a) \cdot z_b(\mathbf{x} - \mathbf{c}_b)$$

When $\mathbf{c}_a \ne \mathbf{c}_b$ (which occurs in 306 out of 324 quadratic terms), the two factors originate from **two distinct spatial nodes** $\mathbf{x}_1 = \mathbf{x} - \mathbf{c}_a$ and $\mathbf{x}_2 = \mathbf{x} - \mathbf{c}_b$.

### Non-Invariance Theorem:
> **Theorem**: In a decoupled local state $\mathbb{R}^{342 N}$, cross-node products $z_a(\mathbf{x}_1) z_b(\mathbf{x}_2)$ do not exist in the basis. Any linear decoupled tensor shift $S \otimes S$ shifts the entry by $(\mathbf{c}_a + \mathbf{c}_b)$, producing an invariance error:
> $$\frac{\|S_{\text{lifted}}(\mathbf{z}\otimes\mathbf{z}) - \mathcal{S}(\mathbf{z})\otimes\mathcal{S}(\mathbf{z})\|}{\|\mathcal{S}(\mathbf{z})\otimes\mathcal{S}(\mathbf{z})\|} \ge 419.5\%$$
> on non-uniform physical fields.

### Resolution:
Spatial streaming must operate as a unitary permutation circuit $S$ strictly on linear populations $\mathbf{z}(\mathbf{x}) \in \mathbb{R}^{18}$, followed by local quadratic tensor re-formation $\mathbf{z}(\mathbf{x}) \otimes \mathbf{z}(\mathbf{x})$ at each node.
