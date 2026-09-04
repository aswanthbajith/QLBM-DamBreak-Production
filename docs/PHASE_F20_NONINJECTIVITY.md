# PHASE F20: NON-INJECTIVITY THEOREM & DEGENERATE PREIMAGE PROOF

## 1. The Non-Injectivity Theorem
Let $F_{\text{BGK}}: \mathbb{R}^9 \to \mathbb{R}^9$ denote the local D2Q9 BGK collision operator.
The map $F_{\text{BGK}}$ is non-injective: there exist distinct population states $\mathbf{f}_1 \neq \mathbf{f}_2$ such that:
$$F_{\text{BGK}}(\mathbf{f}_1) = F_{\text{BGK}}(\mathbf{f}_2)$$

### Proof:
In moment space with $\omega_f = 1.0$:
$$\mathbf{m}^* = [\rho, m_1^{\text{eq}}(\rho, \mathbf{j}), m_2^{\text{eq}}(\rho, \mathbf{j}), j_x, -j_x, j_y, -j_y, m_7^{\text{eq}}(\rho, \mathbf{j}), m_8^{\text{eq}}(\rho, \mathbf{j})]^T$$
Notice that $\mathbf{m}^*$ depends solely on the conserved moments $(\rho, j_x, j_y)$.
For any fixed triplet $(\rho, j_x, j_y)$, let $\mathcal{A}(\rho, \mathbf{j})$ be the 6-dimensional affine subspace of population vectors $\mathbf{f}$ satisfying:
$$\sum_{i=0}^8 f_i = \rho, \qquad \sum_{i=0}^8 c_{ix} f_i = j_x, \qquad \sum_{i=0}^8 c_{iy} f_i = j_y$$
Every state $\mathbf{f} \in \mathcal{A}(\rho, \mathbf{j})$ maps to the exact same equilibrium distribution $\mathbf{f}^{\text{eq}}(\rho, \mathbf{j})$.
Because the dimension of $\mathcal{A}(\rho, \mathbf{j})$ is $9 - 3 = 6$, the preimage $F_{\text{BGK}}^{-1}(\mathbf{f}^*)$ is an entire 6-dimensional affine subspace. $\blacksquare$

---

## 2. Numerical Demonstration Across 7 Physical Regimes
As recorded in [`results/phase_f20/noninjectivity.csv`](file:///home/aswa/Research/QLBM-DamBreak-Production/results/phase_f20/noninjectivity.csv), non-injectivity was tested across 7 regimes using the $Q4.12$ fixed-point engine:
1. **Ideal BGK**: $\|\mathbf{f}_1 - \mathbf{f}_2\|_1 = 40 \implies \|F(\mathbf{f}_1) - F(\mathbf{f}_2)\|_1 = 0$.
2. **Finite-Precision BGK**: In $Q4.12$, integer truncation produces complete degeneracy in shear modes.
3. **Two-Phase BGK**: Non-injectivity holds simultaneously in both hydrodynamic $f$ and phase $g$ distributions.
4. **Forcing Enabled**: External buoyancy shifts the conserved momentum $\mathbf{j} \to \mathbf{j} + \frac{1}{2}\mathbf{F}$, but preserves the 6D degenerate kernel in non-equilibrium modes.
5. **Forcing Disabled**: Exact non-injectivity confirmed.
6. **CSF Surface Tension Disabled**: Exact non-injectivity confirmed.
7. **CSF Surface Tension Enabled**: For local collision with external CSF input, the non-equilibrium degeneracy remains 6-dimensional.

---

## 3. The Isometric Embedding Theorem
For any isometric embedding of a discrete map $F: \mathcal{H}_S \to \mathcal{H}_S$ into an open quantum system:
$$V |x\rangle = |F(x)\rangle_S \otimes |e_x\rangle_E$$
Unitarity of $V$ requires $V^\dagger V = I$, which implies that for any two basis states $|x\rangle, |y\rangle$:
$$\langle V x | V y \rangle = \langle F(x) | F(y) \rangle_S \cdot \langle e_x | e_y \rangle_E = \langle x | y \rangle$$
For orthogonal computational basis states $x \neq y$, $\langle x | y \rangle = 0$.
Therefore, if $F(x) = F(y)$ (i.e. $x$ and $y$ are degenerate preimages mapping to the same output):
$$\langle F(x) | F(y) \rangle_S = 1 \implies \langle e_x | e_y \rangle_E = 0$$

### Physical Consequence:
Whenever two distinct states relax to the same equilibrium, their corresponding environment states **must be strictly orthogonal**.
When the environment is traced out:
$$\rho_S = \text{Tr}_E(V |\psi\rangle\langle\psi| V^\dagger)$$
For $|\psi\rangle = a|x\rangle + b|y\rangle$:
$$\rho_S = (|a|^2 + |b|^2) |F(x)\rangle\langle F(x)|$$
The relative phase between $x$ and $y$ is entirely transferred into the environment register.
This proves mathematically why microscopic non-equilibrium fluctuations must decohere under physical BGK relaxation.
