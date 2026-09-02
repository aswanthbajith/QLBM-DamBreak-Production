# PHASE F12: QUANTUM TWO-PHASE FORCE & CSF STENCILS
## Buoyancy Body Force, Continuum Surface Force, and Reversible Coordinate Shift Stencils

**Document**: Spatial Stencils & Capillary Force Formulation  
**Project**: Quantum Lattice Boltzmann Method (QLBM) for Two-Phase Flow  
**Repository**: `/home/aswa/Research/QLBM-DamBreak-Production`  
**Branch**: `feature/direct-encoding-two-phase-qlbm`  
**Date**: September 2026  

---

## 1. Spatial Coordinate Shift Stencil Operators

The phase gradient $\nabla \alpha$ and interface curvature $\kappa$ are evaluated using unitary spatial coordinate shift operators:

$$\hat{S}_x^{\pm 1} |x, y\rangle = |(x \pm 1) \bmod N_x, y\rangle$$
$$\hat{S}_y^{\pm 1} |x, y\rangle = |x, (y \pm 1) \bmod N_y\rangle$$

Central difference gradients:
$$\nabla_x \alpha(x, y) = \frac{1}{2} \left[ \hat{S}_x^{+1} \alpha(x, y) - \hat{S}_x^{-1} \alpha(x, y) \right]$$
$$\nabla_y \alpha(x, y) = \frac{1}{2} \left[ \hat{S}_y^{+1} \alpha(x, y) - \hat{S}_y^{-1} \alpha(x, y) \right]$$

---

## 2. Interface Curvature & CSF Tension

$$\mathbf{n}(x, y) = \frac{\nabla \alpha(x, y)}{|\nabla \alpha(x, y)| + 10^{-12}}, \quad \kappa(x, y) = -\nabla \cdot \mathbf{n}(x, y)$$
$$\mathbf{F}_{\text{CSF}}(x, y) = \sigma \kappa(x, y) \nabla \alpha(x, y)$$

- Total Body Force: $\mathbf{F}_{\text{total}} = [0, (\rho - \rho_G)g_{\text{acc}}]^T + \mathbf{F}_{\text{CSF}}$.
- Gate Overhead: $4(n_x + n_y)$ Toffoli gates per spatial stencil step.
