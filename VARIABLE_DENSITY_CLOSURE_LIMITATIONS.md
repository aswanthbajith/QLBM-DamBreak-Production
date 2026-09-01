# VARIABLE-DENSITY TWO-PHASE CLOSURE LIMITATIONS & MATHEMATICAL ANALYSIS

**Auditor Role**: Lead Computational Fluid Dynamics & Quantum Algorithm Engineer  
**Date**: 2026-08-19  

---

## 1. Why Full Variable-Density Two-Phase LBM Fails Exact Polynomial Closure

In multiphase Lattice Boltzmann hydrodynamics (e.g. Allen-Cahn or Cahn-Hilliard models), the governing equations contain mathematical terms that cannot be represented as finite-degree polynomials without severe truncation or infinite Taylor expansions.

### 1.1 Non-Polynomial Euclidean Interface Normal Vector
In the conservative Allen-Cahn equation, counter-gradient artificial compression flux prevents diffuse interface spreading:
$$\mathbf{f}_{\text{cg}} = 4 \phi (1 - \phi) \frac{\nabla \phi}{|\nabla \phi| + \epsilon}$$
The unit normal $\mathbf{n} = \frac{\nabla \phi}{|\nabla \phi|}$ requires evaluating:
$$|\nabla \phi| = \sqrt{(\partial_x \phi)^2 + (\partial_y \phi)^2}$$
The fractional exponent $(1/2)$ and reciprocal $1/|\nabla \phi|$ are **strictly non-polynomial functions**. 

### 1.2 Chemical Potential & Surface Tension Force
In the Continuum Surface Force (CSF) formulation, the surface tension force is:
$$\mathbf{F}_s = \mu_\phi \nabla \phi$$
where the chemical potential $\mu_\phi$ is:
$$\mu_\phi = 4 \beta \phi (1 - \phi)(\phi - 0.5) - \kappa_c \nabla^2 \phi$$
Multiplying $\mu_\phi$ (cubic in $\phi$) by $\nabla \phi$ (linear in $\phi$) yields a **quartic ($p=4$) non-local monomial** $\phi^3 \nabla \phi$. Expanding this into distribution function equilibria yields monomials of degree 5 and higher.

### 1.3 Reciprocal Density $\xi = 1/\rho$ Instability at High Density Ratios
The Kowalski / Jennings auxiliary variable method proposes lifting $\xi = 1/\rho$ via Newton-Raphson discrete updates:
$$\xi_{k+1} = \xi_k (2 - \rho \xi_k)$$
As proven in the Stage 7 adversarial audit:
* Convergence requires $|1 - \rho \xi_0| < 1 \implies 0 < \xi_0 < \frac{2}{\rho}$.
* For water-air ($\rho_L/\rho_G = 1000$), $\rho \in [0.1, 1.0]$ in lattice units corresponds to a wide density jump across the interface.
* With static initialization $\xi_0 = 1.0$:
  * At $\rho = 10$: $\xi_k$ error explodes to $4.30 \times 10^7$ within 3 iterations.
  * At $\rho = 1000$: $\xi_k$ error explodes to $9.92 \times 10^{23}$ within 3 iterations.
* Therefore, $\xi = 1/\rho$ does **not** dynamically close the variable-density system without complex multi-scale adaptive rescaling.

---

## 2. Scientific Conclusion for Phase 5
The quantum pipeline correctly implements a **constant-density quadratic surrogate ($p=2$)** with $\rho_0 = 1.0$. The complete variable-density physical dam break remains the validated classical ground truth.
