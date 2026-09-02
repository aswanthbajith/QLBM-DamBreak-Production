# PHASE F13: COHERENT SPATIAL FORCE & CSF STENCILS
## Buoyancy, Interface Curvature, and Reversible Shift Stencils

**Document**: Coherent Spatial Force & Capillary Tension Formulation  
**Project**: Quantum Lattice Boltzmann Method (QLBM) for Two-Phase Flow  
**Repository**: `/home/aswa/Research/QLBM-DamBreak-Production`  
**Branch**: `feature/direct-encoding-two-phase-qlbm`  
**Date**: September 2026  

---

## 1. Reversible Shift Stencils

Phase-field gradients $\nabla \alpha$ and curvature $\kappa$ are evaluated using spatial coordinate shift unitaries:

$$\hat{S}_x^{\pm 1} |x, y\rangle = |(x \pm 1) \bmod N_x, y\rangle$$
$$\hat{S}_y^{\pm 1} |x, y\rangle = |x, (y \pm 1) \bmod N_y\rangle$$

$$\nabla_x \alpha = \frac{1}{2}(\hat{S}_x^{+1} - \hat{S}_x^{-1})\alpha, \quad \nabla_y \alpha = \frac{1}{2}(\hat{S}_y^{+1} - \hat{S}_y^{-1})\alpha$$
$$\mathbf{n} = \frac{\nabla \alpha}{|\nabla \alpha| + 10^{-12}}, \quad \kappa = -\nabla \cdot \mathbf{n}, \quad \mathbf{F}_{\text{CSF}} = \sigma \kappa \nabla \alpha$$

- **Buoyancy Force**: $\mathbf{F}_{\text{buoyancy}} = [0, (\rho - \rho_G)g_{\text{acc}}]^T$.
- **Total Force**: $\mathbf{F} = \mathbf{F}_{\text{buoyancy}} + \mathbf{F}_{\text{CSF}}$.
