# Complete Mathematical Audit of Polynomial Degree & Non-Polynomial Terms in Two-Phase LBM

**Author**: Lead Numerical Fluid-Dynamics Researcher  
**Target Operator**: $\mathbf{\Psi}(t+1) = \mathcal{F}(\mathbf{\Psi}(t))$  
**Base State Vector**: $\mathbf{\Psi} \in \mathbb{R}^{18 N}$  

---

## 1. Master Summary of Polynomial Degrees Across All Physical Sub-Operators

| Sub-Operator / Term | Mathematical Formula | Implemented Form | Exact Degree in State $\mathbf{\Psi}$ | Classification |
| :--- | :--- | :--- | :---: | :---: |
| **Phase Moment $\phi$** | $\sum_{i=0}^8 h_i$ | Linear summation | **Degree 1** | Polynomial (Linear) |
| **Pressure Moment $p^*$** | $\sum_{i=0}^8 g_i$ | Linear summation | **Degree 1** | Polynomial (Linear) |
| **Linear Phase Collision** | $h_i - \frac{1}{\tau_\phi}(h_i - w_i \phi)$ | Linear relaxation | **Degree 1** | Polynomial (Linear) |
| **Linear Hydro Collision** | $g_i - \frac{1}{\tau_v}(g_i - w_i \sum g_k)$ | Linear relaxation | **Degree 1** | Polynomial (Linear) |
| **Phase Advection Flux** | $w_i \phi \frac{\mathbf{c}_i \cdot \mathbf{u}}{c_s^2}$ | Bilinear product $\phi \mathbf{u}$ | **Degree 2** | Polynomial (Quadratic) |
| **Hydro Convective Flux** | $w_i \left[ \frac{(\mathbf{c}_i \cdot \mathbf{u})^2}{2 c_s^4} - \frac{|\mathbf{u}|^2}{2 c_s^2} \right]$ | Quadratic velocity tensor $\mathbf{u} \otimes \mathbf{u}$ | **Degree 2** | Polynomial (Quadratic) |
| **Interface Counter-Flux** | $1 - 4(\phi - 0.5)^2 = 4\phi(1-\phi)$ | Quadratic polynomial | **Degree 2** | Polynomial (Quadratic) |
| **Guo Force Velocity Coupling** | $\mathbf{u} \cdot \mathbf{F}$ and $(\mathbf{c}_i \cdot \mathbf{u})(\mathbf{c}_i \cdot \mathbf{F})$ | Cross-product $\mathbf{u} \otimes \mathbf{F}$ | **Degree 2** | Polynomial (Quadratic) |
| **Density Model $\rho(\phi)$** | $\rho_G + \phi (\rho_L - \rho_G)$ | Linear interpolation | **Degree 1** | Polynomial (Linear) |
| **Kinematic Viscosity $\nu(\phi)$** | $\frac{\mu_G + \phi \Delta \mu}{\rho_G + \phi \Delta \rho}$ | Rational function | **Rational** | Non-Polynomial (Rational) |
| **Force Scaling $1/\rho(\phi)$** | $\frac{1}{\rho_G + \phi \Delta \rho}$ | Rational quotient | **Rational** | Non-Polynomial (Rational) |
| **Interface Normal Normalization** | $\mathbf{n} = \frac{\nabla \phi}{|\nabla \phi| + \epsilon}$ | Radical quotient | **Non-Polynomial** | Non-Polynomial (Radical) |
| **Global Streaming $\mathbf{S}$** | Spatial shift + wall reflection | Unitary permutation matrix | **Degree 1** | Linear Unitary Operator |

---

## 2. Deep Dive: Rational & Non-Polynomial Terms

### A. The Density Quotient $\frac{1}{\rho(\phi)}$
In the macroscopic velocity update:
$$ \mathbf{u} = \sum g_i \mathbf{c}_i + \frac{\Delta t}{2 \rho(\phi)} \mathbf{F} $$
1. **Case 1: Constant Density / Boussinesq Regime ($\rho_L = \rho_G = \rho_0$)**:
   $$ \frac{1}{\rho(\phi)} = \frac{1}{\rho_0} = \text{const} $$
   $\implies \mathbf{u}$ is strictly **Degree 1 (Linear)** in $\mathbf{\Psi}$.
   The entire system $\mathbf{\Psi}(t+1) = \mathcal{F}(\mathbf{\Psi}(t))$ is **STRICTLY DEGREE 2 (QUADRATIC POLYNOMIAL)**.

2. **Case 2: Moderate Density Ratio ($\rho_L / \rho_G \le 10$)**:
   Let $\bar{\rho} = \frac{\rho_L + \rho_G}{2}$ be the mean reference density and $\epsilon_\rho = \frac{\rho_L - \rho_G}{2 \bar{\rho}} < 1$.
   The density quotient expands into a convergent Neumann polynomial series:
   $$ \frac{1}{\rho(\phi)} = \frac{1}{\bar{\rho}} \left[ 1 - \epsilon_\rho (2\phi - 1) + \epsilon_\rho^2 (2\phi - 1)^2 - \epsilon_\rho^3 (2\phi - 1)^3 + \dots \right] $$
   - Truncating at order $d_\rho = 1$ yields a **Degree 2** approximation.
   - Truncating at order $d_\rho = 2$ yields a **Degree 3** polynomial system with truncation error $< \epsilon_\rho^3$.

3. **Case 3: Exact Polynomialization via Auxiliary Variable State Lifting (Kowalski 1991)**:
   Define the auxiliary state variable:
   $$ \xi(\mathbf{x}, t) = \frac{1}{\rho(\phi(\mathbf{x}, t))} $$
   Since $\rho(\phi) = \rho_G + \phi \Delta \rho$, the discrete update for $\xi$ is:
   $$ \xi(t+1) = \xi(t) - \xi^2(t) \Delta \rho (\phi(t+1) - \phi(t)) $$
   This transforms the rational system into an **exact degree-3 (cubic) polynomial system** with zero rational terms!

---

## 3. Carleman State Space Dimension Analysis

Let $N = N_x \times N_y$ be the total spatial grid nodes, and $d = 18 N$ the base state dimension.

### A. Local Kronecker Basis (Independent Local Node Carleman State)
Because the collision operator $\mathbf{\Omega}(\mathbf{\Psi})$ is strictly local at each spatial node $\mathbf{x}_n$, we construct the local Kronecker power at each node:
$$ \mathbf{\Psi}_{local}(\mathbf{x}_n) \in \mathbb{R}^{18} $$
1. **Order $N_C = 1$ (Linearized State)**:
   $$ \mathbf{Y}_1 \in \mathbb{R}^{18 N} $$
2. **Order $N_C = 2$ (Quadratic Lifted State)**:
   - Base linear variables: $18 N$
   - Local quadratic monomials $\mathbf{\Psi}_{local} \otimes \mathbf{\Psi}_{local}$: $18 \times 18 = 324$ per node $\implies 324 N$.
   - **Total Carleman Dimension $D_2$**:
     $$ D_2 = 18 N + 324 N = 342 N $$
3. **Order $N_C = 3$ (Cubic Lifted State)**:
   - Local cubic monomials $\mathbf{\Psi}_{local}^{\otimes 3}$: $18^3 = 5,832$ per node $\implies 5,832 N$.
   - **Total Carleman Dimension $D_3$**:
     $$ D_3 = 18 N + 324 N + 5,832 N = 6,174 N $$

### B. Analytical Sparsity of Carleman Matrix $\mathbf{A}_C$
For the quadratic model ($N_C = 2$, dimension $342 N \times 342 N$):
- **Streaming block $\mathbf{S}_C$**:
  $$ \mathbf{S}_C = \begin{bmatrix} \mathbf{S} & \mathbf{0} \\ \mathbf{0} & \mathbf{S}_{kron2} \end{bmatrix} $$
  where $\mathbf{S}_{kron2} \in \{0, 1\}^{324N \times 324N}$ is the exact shift permutation for quadratic variable pairs.
  - **Sparsity**: Exactly $1.0$ non-zero entry per row (strictly unitary permutation).
- **Collision block $\mathbf{C}_2$**:
  $$ \mathbf{C}_2 = \begin{bmatrix} \mathbf{M}_1 & \mathbf{M}_2 \\ \mathbf{0} & \mathbf{M}_1 \otimes \mathbf{M}_1 \end{bmatrix} $$
  - **Sparsity**: Block-diagonal across spatial nodes with $18 + 324 = 342$ non-zeros per local node block.
