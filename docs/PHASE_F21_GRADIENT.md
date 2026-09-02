# PHASE F21: REVERSIBLE DISCRETE GRADIENT STENCILS
## Central-Difference Phase Gradients on Quantum Fixed-Point Registers

**Document**: Reversible Discrete Gradient Stencil Specification  
**Project**: Quantum Lattice Boltzmann Method (QLBM) for Two-Phase Flow  
**Repository**: `/home/aswa/Research/QLBM-DamBreak-Production`  
**Branch**: `feature/direct-encoding-two-phase-qlbm`  
**Date**: September 2026  

---

## 1. Discrete Gradient Formulation

Matching the Level-4 classical solver, discrete central-difference gradients of the phase fraction $\alpha(y, x)$ are:
$$\nabla_x \alpha(y, x) = \frac{\alpha(y, x+1) - \alpha(y, x-1)}{2 \Delta x}, \quad \nabla_y \alpha(y, x) = \frac{\alpha(y+1, x) - \alpha(y-1, x)}{2 \Delta y}$$
with zero-gradient at solid wall boundaries ($x=0, x=N_x-1, y=0, y=N_y-1$).

### Reversible Quantum Transformation:
$$U_{\nabla}: |\alpha\rangle |0\rangle_{\text{grad}} \mapsto |\alpha\rangle |\nabla_x \alpha, \nabla_y \alpha\rangle$$
Implemented via coordinate wire shifts and reversible in-place subtraction / shift-right logic.
