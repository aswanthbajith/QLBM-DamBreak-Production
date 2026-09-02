# PHASE F21: REVERSIBLE CURVATURE STENCIL SPECIFICATION
## Discrete Curvature $\kappa = -\nabla \cdot \mathbf{n}$ on Fixed-Point Registers

**Document**: Reversible Curvature Stencil Specification  
**Project**: Quantum Lattice Boltzmann Method (QLBM) for Two-Phase Flow  
**Repository**: `/home/aswa/Research/QLBM-DamBreak-Production`  
**Branch**: `feature/direct-encoding-two-phase-qlbm`  
**Date**: September 2026  

---

## 1. Unit Normal & Curvature Formulation

1. **Unit Normal Vector**:
   $$\mathbf{n}(y, x) = \begin{cases} \frac{\nabla \alpha}{\|\nabla \alpha\|} & \text{if } \|\nabla \alpha\| > 10^{-3} \\ \mathbf{0} & \text{otherwise} \end{cases}$$
2. **Curvature**:
   $$\kappa(y, x) = \text{clip}\left( -\left( \frac{n_x(y, x+1) - n_x(y, x-1)}{2 \Delta x} + \frac{n_y(y+1, x) - n_y(y-1, x)}{2 \Delta y} \right), -2.0, 2.0 \right)$$
3. **Reversible Implementation**:
   $$U_\kappa: |\mathbf{n}\rangle |0\rangle \mapsto |\mathbf{n}\rangle |\kappa\rangle$$
