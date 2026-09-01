# LEVEL-5: COUPLED NONLINEAR POLYNOMIAL FORMULATION & CARLEMAN COMPATIBILITY

This document derives the exact polynomial decomposition and Carleman linearization tensors for the coupled Two-Phase D2Q9 Lattice Boltzmann equations.

---

## 1. Polynomial Decomposition of Kinetic Collision Operators

Let $\mathbf{z}(\mathbf{x}) = [f_0..f_8, g_0..g_8]^T \in \mathbb{R}^{18}$ denote the local nodal population vector.

### A. Hydrodynamic Equilibrium Operator ($f_i^{\text{eq}}$)
The continuous convective equilibrium in terms of density $\rho = \sum_k f_k$ and momentum flux $\mathbf{j} = \sum_k \mathbf{c}_k f_k$ expands as:

$$f_i^{\text{eq}}(\mathbf{f}) = \sum_{k=0}^8 E_{1, ik}^{(f)} f_k + \sum_{j,k=0}^8 E_{2, ijk}^{(f)} f_j f_k + \mathcal{O}(\text{Ma}^2 \delta\rho)$$

where:
* **Linear Hydrodynamic Coefficient**:
  $$E_{1, ik}^{(f)} = w_i \left[ 1 + 3 (\mathbf{c}_i \cdot \mathbf{c}_k) \right]$$
* **Quadratic Convective Tensor**:
  $$E_{2, ijk}^{(f)} = \frac{w_i}{\rho_0} \left[ \frac{9}{2} (\mathbf{c}_i \cdot \mathbf{c}_j)(\mathbf{c}_i \cdot \mathbf{c}_k) - \frac{3}{2} (\mathbf{c}_j \cdot \mathbf{c}_k) \right]$$

### B. Phase-Field Interface Equilibrium Operator ($g_i^{\text{eq}}$)
The phase advection equilibrium in terms of volume fraction $\alpha = \sum_k g_k$ and momentum $\mathbf{j} = \sum_k \mathbf{c}_k f_k$ expands as:

$$g_i^{\text{eq}}(\mathbf{g}, \mathbf{f}) = \sum_{k=0}^8 E_{1, ik}^{(g)} g_k + \sum_{j,k=0}^8 E_{2, ijk}^{(g)} g_j f_k$$

where:
* **Linear Phase Coefficient**:
  $$E_{1, ik}^{(g)} = w_i$$
* **Quadratic Phase-Momentum Coupling Tensor**:
  $$E_{2, ijk}^{(g)} = \frac{3 w_i}{\rho_0} (\mathbf{c}_i \cdot \mathbf{c}_k)$$

---

## 2. Mathematical Classification of Equation Components

| Component | Mathematical Term | Algebraic Nature | Carleman Representation | Truncation Impact |
| :--- | :--- | :---: | :---: | :---: |
| **Mass Diffusion** | $w_i \sum f_k$ | Linear | Exact in $M_1$ ($18\times 18$) | None ($E = 0$) |
| **Linear Advection** | $3 w_i (\mathbf{c}_i \cdot \mathbf{j})$ | Linear | Exact in $M_1$ ($18\times 18$) | None ($E = 0$) |
| **Hydrodynamic Convection** | $\frac{9}{2} w_i \frac{(\mathbf{c}_i \cdot \mathbf{j})^2}{\rho_0}$ | Quadratic | Exact in $M_2$ ($18\times 324$) | Second-order exact |
| **Phase Advection** | $3 w_i \frac{\alpha (\mathbf{c}_i \cdot \mathbf{j})}{\rho_0}$ | Bilinear | Exact in $M_2$ ($18\times 324$) | Second-order exact |
| **Gravitational Buoyancy** | $(\rho - \rho_G) \mathbf{g}$ | Linear | Exact in $M_1$ ($18\times 18$) | None ($E = 0$) |
| **Guo Convective Source** | $9 (\mathbf{c}_i \cdot \mathbf{u})(\mathbf{c}_i \cdot \mathbf{F})$ | Quadratic | Exact in $M_2$ ($18\times 324$) | Second-order exact |
| **Surface Tension ($\mathbf{F}_s$)** | $\sigma \kappa \nabla \alpha$ | Spatial Nonlocal | Hybrid Classical / Spatial Oracle | Handled via spatial stencil |

---

## 3. Second-Order Carleman Linearized Equation

Let $\mathbf{Y}_t = \begin{bmatrix} \mathbf{z}_t \\ \mathbf{z}_t \otimes \mathbf{z}_t \end{bmatrix} \in \mathbb{R}^{342}$. The local update equation is:

$$\mathbf{z}_{t+1}^* = M_1 \mathbf{z}_t + M_2 (\mathbf{z}_t \otimes \mathbf{z}_t) = A_{\text{eval}} \mathbf{Y}_t$$

where:
$$A_{\text{eval}} = \begin{bmatrix} M_1 & M_2 \end{bmatrix} \in \mathbb{R}^{18 \times 342}$$
$$M_1 = (1 - \omega) I_{18} + \omega E_1 \in \mathbb{R}^{18 \times 18}$$
$$M_2 = \omega E_2 \in \mathbb{R}^{18 \times 324}$$
