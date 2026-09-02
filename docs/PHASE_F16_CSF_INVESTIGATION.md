# PHASE F16: CSF & NONLOCAL FORCE INVESTIGATION
## Reversible Spatial Stencil Shifts and Coherent Surface Tension Coupling

**Document**: Continuum Surface Force (CSF) Quantum Strategy  
**Project**: Quantum Lattice Boltzmann Method (QLBM) for Two-Phase Flow  
**Repository**: `/home/aswa/Research/QLBM-DamBreak-Production`  
**Branch**: `feature/direct-encoding-two-phase-qlbm`  
**Date**: September 2026  

---

## 1. Continuum Surface Force Formulation

$$\mathbf{F}_s = \sigma \kappa \nabla \alpha, \quad \kappa = -\nabla \cdot \left( \frac{\nabla \alpha}{|\nabla \alpha|} \right)$$

---

## 2. Reversible Coordinate Shift Stencils

Using spatial permutation operators $\hat{S}_x^{\pm 1}$ and $\hat{S}_y^{\pm 1}$, neighboring phase fractions $\alpha(x \pm 1, y \pm 1)$ are copied into local register stencils:

$$\frac{\partial \alpha}{\partial x} \approx \frac{\alpha(x+1, y) - \alpha(x-1, y)}{2 \Delta x}, \quad \frac{\partial \alpha}{\partial y} \approx \frac{\alpha(x, y+1) - \alpha(x, y-1)}{2 \Delta y}$$

In Route D, this is computed via reversible subtractor and shift registers, completely avoiding classical intermediate gradient evaluation!
