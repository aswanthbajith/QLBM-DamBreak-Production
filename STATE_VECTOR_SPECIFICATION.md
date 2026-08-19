# Mathematical Specification of the Computational State Vector

**Author**: Lead Mathematical Modeler & Numerical Analyst  
**Date**: August 19, 2026  
**Repository**: `/home/aswa/Research/QLBM-DamBreak/`  

---

## 1. Base Physical State Vector $\mathbf{\Psi}(t) \in \mathbb{R}^{18 N}$

For a 2D spatial lattice grid containing $N = N_x \times N_y$ nodes, the complete physical state is uniquely and closedly specified by the 18 discrete particle distribution populations:

$$ \mathbf{\Psi}(t) = \begin{bmatrix} \mathbf{g}_0(t) \\ \mathbf{g}_1(t) \\ \vdots \\ \mathbf{g}_8(t) \\ \mathbf{h}_0(t) \\ \mathbf{h}_1(t) \\ \vdots \\ \mathbf{h}_8(t) \end{bmatrix} \in \mathbb{R}^{18 N} $$

where:
- $\mathbf{g}_q \in \mathbb{R}^N$ ($q = 0, \dots, 8$): Discrete velocity-based hydrodynamic distribution functions for lattice velocity direction $\mathbf{c}_q$.
- $\mathbf{h}_q \in \mathbb{R}^N$ ($q = 0, \dots, 8$): Discrete order-parameter phase-field distribution functions for lattice velocity direction $\mathbf{c}_q$.

### Exact Local Node Sub-Vector at site $n = x N_y + y$:
$$ \mathbf{\psi}_n(t) = \begin{bmatrix} g_0(n) \\ \vdots \\ g_8(n) \\ h_0(n) \\ \vdots \\ h_8(n) \end{bmatrix} \in \mathbb{R}^{18} $$

---

## 2. Elimination of Algebraic Redundancy
The following macroscopic quantities are **not** independent state variables; they are strictly linear or algebraic functions of $\mathbf{\Psi}$:
1. **Local Phase Fraction**: $\phi(n) = \sum_{q=0}^8 h_q(n) = \mathbf{1}_h^T \mathbf{\psi}_n$ (Strictly linear).
2. **Local Momentum**: $\mathbf{j}(n) = \sum_{q=0}^8 g_q(n) \mathbf{c}_q = \mathbf{C}_g \mathbf{\psi}_n$ (Strictly linear).
3. **Local Density**: $\rho(n) = \rho_G + \phi(n)(\rho_L - \rho_G) = \rho_G + (\rho_L - \rho_G) \mathbf{1}_h^T \mathbf{\psi}_n$ (Strictly affine).
4. **Local Dynamic Viscosity**: $\mu(n) = \mu_G + (\mu_L - \mu_G) \mathbf{1}_h^T \mathbf{\psi}_n$ (Strictly affine).

---

## 3. Auxiliary Variable Lifting for Variable Density ($\xi = 1/\rho$)
In the full variable-density regime where velocity and forcing require division by $\rho(\mathbf{x})$, the state vector is augmented with the auxiliary reciprocal density variable $\xi(n) = 1/\rho(n)$:

$$ \mathbf{\Psi}_{aug}(t) = \begin{bmatrix} \mathbf{g}(t) \\ \mathbf{h}(t) \\ \mathbf{\xi}(t) \end{bmatrix} \in \mathbb{R}^{19 N} $$

Under Kowalski reciprocal state evolution:
$$ \xi_{t+1}(n) = \xi_t(n) - \xi_t^2(n) \Delta \rho \Delta \phi(n) $$
which forms a closed polynomial system of degree 3 without rational division.

---

## 4. Lifted Carleman State Representation $\mathbf{Y}_2(t) \in \mathbb{R}^{342 N}$
For truncation order $N_C = 2$, local Kronecker powers are assembled per spatial node to preserve spatial locality:

$$ \mathbf{Y}_2(t) = \begin{bmatrix} \mathbf{\Psi}(t) \\ \mathbf{\Psi}_{local}^{\otimes 2}(t) \end{bmatrix} = \begin{bmatrix} \mathbf{\psi}_1 \\ \vdots \\ \mathbf{\psi}_N \\ \mathbf{\psi}_1 \otimes \mathbf{\psi}_1 \\ \vdots \\ \mathbf{\psi}_N \otimes \mathbf{\psi}_N \end{bmatrix} \in \mathbb{R}^{18 N + 324 N} = \mathbb{R}^{342 N} $$

- **Base Dimension**: $d_{base} = 18 N$
- **Quadratic Monomial Dimension**: $d_{quad} = 18^2 N = 324 N$
- **Total Carleman Dimension**: $D_C = \mathbf{342 N}$
