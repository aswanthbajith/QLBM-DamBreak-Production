# Mathematical Vector & Matrix Formulation (Level 3)

## 1. Global State Vector
Let $N = N_x \times N_y$ be the total spatial lattice nodes and $Q=9$ the D2Q9 velocity set.
The coupled two-phase state vector is:
$$
\mathbf{\Psi}(t) = \begin{bmatrix} \mathbf{g}(t) \\ \mathbf{h}(t) \end{bmatrix} \in \mathbb{R}^{2 Q N} = \mathbb{R}^{18 N}
$$
where:
- $\mathbf{g}(t) = [g_0(\mathbf{x}_1), \dots, g_0(\mathbf{x}_N), g_1(\mathbf{x}_1), \dots, g_{Q-1}(\mathbf{x}_N)]^T \in \mathbb{R}^{QN}$
- $\mathbf{h}(t) = [h_0(\mathbf{x}_1), \dots, h_0(\mathbf{x}_N), h_1(\mathbf{x}_1), \dots, h_{Q-1}(\mathbf{x}_N)]^T \in \mathbb{R}^{QN}$

---

## 2. Global Linear Streaming Operator $\mathbf{S}$
The spatial advection and boundary reflections are mapped into a single global sparse permutation matrix $\mathbf{S} \in \mathbb{R}^{18 N \times 18 N}$:
$$
\mathbf{S} = \begin{bmatrix} \mathbf{S}_g & \mathbf{0} \\ \mathbf{0} & \mathbf{S}_h \end{bmatrix}
$$
- **Sparsity**: Exactly $1$ non-zero element ($+1$) per row and column.
- **Unitary Property**:
  $$ \mathbf{S}^T \mathbf{S} = \mathbf{I}_{18 N} $$
- **Boundary Handling**:
  - Interior shift: $(\mathbf{x}_n + \mathbf{c}_q \Delta t, q)$
  - Lateral & top walls: $(\mathbf{x}_n, \bar{q})$ (half-way bounce-back reflection $\mathbf{c}_{\bar{q}} = -\mathbf{c}_q$)
  - Bottom floor: $(\mathbf{x}_n, q_{mirror})$ (free-slip specular reflection $\mathbf{c}_{mirror} = [c_{qx}, -c_{qy}]$)

---

## 3. Linear Relaxation Matrix $\mathbf{M}_1$
The linear portion of the local BGK collision operator is represented by the block-diagonal matrix $\mathbf{M}_1 \in \mathbb{R}^{18 N \times 18 N}$:
$$
\mathbf{M}_1 = \begin{bmatrix} \mathbf{M}_1^{(g)} & \mathbf{0} \\ \mathbf{0} & \mathbf{M}_1^{(h)} \end{bmatrix}
$$
where for node $n$:
- **Hydrodynamic block**:
  $$ (\mathbf{M}_1^{(g)})_{(q^* n)(q n)} = \left(1 - \frac{1}{\tau_v}\right) \delta_{q^* q} + \frac{1}{\tau_v} w_{q^*} \left( 1 + \frac{\mathbf{c}_{q^*} \cdot \mathbf{c}_q}{c_s^2} \right) $$
- **Phase-field block**:
  $$ (\mathbf{M}_1^{(h)})_{(q^* n)(q n)} = \left(1 - \frac{1}{\tau_\phi}\right) \delta_{q^* q} + \frac{1}{\tau_\phi} w_{q^*} $$
- **Sparsity**: Exactly $9$ non-zeros per row ($0.05\%$ dense).
