# Mathematical Derivation & Structure of Polynomial Coefficient Operators

**Author**: Lead Mathematical Modeler & Numerical Analyst  
**Date**: August 19, 2026  
**Repository**: `/home/aswa/Research/QLBM-DamBreak/`  

---

## 1. Streaming Permutation Matrix $\mathbf{S} \in \{0, 1\}^{18N \times 18N}$
The streaming matrix is a global block permutation:
$$ \mathbf{S} = \begin{bmatrix} \mathbf{S}_g & \mathbf{0} \\ \mathbf{0} & \mathbf{S}_h \end{bmatrix} $$
where each $\mathbf{S}_g, \mathbf{S}_h \in \{0, 1\}^{9N \times 9N}$ maps source node $(x, y)$ and velocity $q$ to destination $(x + c_x, y + c_y)$ with bounce-back reflection $\text{opp}[q]$ at solid boundaries.

### Exact Mathematical Properties:
- **Total Non-Zeros**: Exactly $18 N$ non-zeros ($1$ non-zero per row and column).
- **Sparsity**: $\frac{18 N}{(18N)^2} = \frac{1}{18 N}$.
- **Unitarity**: $\mathbf{S}^T \mathbf{S} = \mathbf{I}_{18N}$ (strictly orthogonal and unitary in $\mathbb{R}^{18N}$).

---

## 2. Linear Collision Matrix $\mathbf{M}_1 \in \mathbb{R}^{18N \times 18N}$
The linear relaxation matrix is block-diagonal with local $18 \times 18$ node blocks:
$$ \mathbf{M}_1 = \mathbf{I}_N \otimes \mathbf{M}_{1, node} $$
where:
$$ \mathbf{M}_{1, node} = \begin{bmatrix} \mathbf{M}_{1, g} & \mathbf{0} \\ \mathbf{0} & \mathbf{M}_{1, h} \end{bmatrix} \in \mathbb{R}^{18 \times 18} $$
- **Hydrodynamic Block**: $M_{1, g}[q^*, q] = \left(1 - \frac{1}{\tau_v}\right) \delta_{q^* q} + \frac{1}{\tau_v} w_{q^*}$
- **Phase-Field Block**: $M_{1, h}[q^*, q] = \left(1 - \frac{1}{\tau_\phi}\right) \delta_{q^* q} + \frac{1}{\tau_\phi} w_{q^*}$

### Exact Properties:
- **Non-Zeros**: $2 \times (9 \times 9) \times N = 162 N$ non-zeros.
- **Spectrum**: Real eigenvalues bounded in $(0, 1]$ when $\tau_v, \tau_\phi > 0.5$.

---

## 3. Quadratic Collision Tensor $\mathbf{M}_2 \in \mathbb{R}^{18N \times 324N}$
The quadratic collision tensor contracts the local Kronecker square $\mathbf{\psi}_n \otimes \mathbf{\psi}_n \in \mathbb{R}^{324}$ into $\mathbf{\psi}_n \in \mathbb{R}^{18}$:
$$ \mathbf{M}_2 = \mathbf{I}_N \otimes \mathbf{M}_{2, node} $$

### Exact Components of $\mathbf{M}_{2, node} \in \mathbb{R}^{18 \times 324}$:
1. **Hydrodynamic Convective Block** ($q^* \in 0..8$, pairs $(q_1, q_2) \in 0..8 \times 0..8$):
   $$ M_{2, node}[q^*, q_1 \cdot 18 + q_2] = \frac{w_{q^*}}{\tau_v \rho_0^2} \left[ \frac{(\mathbf{c}_{q1} \cdot \mathbf{c}_{q^*})(\mathbf{c}_{q2} \cdot \mathbf{c}_{q^*})}{2 c_s^4} - \frac{\mathbf{c}_{q1} \cdot \mathbf{c}_{q2}}{2 c_s^2} \right] $$
2. **Phase-Field Advection Block** ($9 + q^*$, pairs $(9 + q_1, q_2)$ where $q_1 \in \mathbf{h}, q_2 \in \mathbf{g}$):
   $$ M_{2, node}[9 + q^*, (9 + q_1) \cdot 18 + q_2] = \frac{w_{q^*}}{\tau_\phi \rho_0 c_s^2} (\mathbf{c}_{q^*} \cdot \mathbf{c}_{q2}) $$

---

## 4. Affine Forcing Vector $\mathbf{b}_{force} \in \mathbb{R}^{18N}$
Constant external body force components (e.g. baseline gravity):
$$ b_{force}[q^* \cdot N + n] = \left(1 - \frac{1}{2\tau_v}\right) w_{q^*} \frac{\mathbf{c}_{q^*} \cdot \mathbf{g}_{grav}}{c_s^2} $$
