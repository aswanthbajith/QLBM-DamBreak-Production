# PHASE F19: CONTINUUM SURFACE FORCE (CSF) AUDIT
## Surface Tension Implementation Status and Coherent Spatial Stencils

**Document**: CSF Status & Physics Inclusion Taxonomy  
**Project**: Quantum Lattice Boltzmann Method (QLBM) for Two-Phase Flow  
**Repository**: `/home/aswa/Research/QLBM-DamBreak-Production`  
**Branch**: `feature/direct-encoding-two-phase-qlbm`  
**Date**: September 2026  

---

## 1. Status of Surface Tension ($\sigma$)

In Phase F19, the surface tension coefficient remains set to $\sigma = 0$ in the baseline numerical runs to isolate the reversible BGK embedding analysis.

### Coherent Implementation Roadmap:
1. **Curvature Calculation**: $\kappa = -\nabla \cdot \mathbf{n} = -\nabla \cdot \left( \frac{\nabla \alpha}{|\nabla \alpha|} \right)$.
2. **Reversible Spatial Stencils**: Evaluated via coordinate wire shifts and reversible gradient adders.
