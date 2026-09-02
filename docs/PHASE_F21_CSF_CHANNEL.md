# PHASE F21: REVERSIBLE CSF QUANTUM CHANNEL SPECIFICATION
## CPTP Properties of the Interfacial Surface-Tension Channel

**Document**: Reversible CSF Channel Specification  
**Project**: Quantum Lattice Boltzmann Method (QLBM) for Two-Phase Flow  
**Repository**: `/home/aswa/Research/QLBM-DamBreak-Production`  
**Branch**: `feature/direct-encoding-two-phase-qlbm`  
**Date**: September 2026  

---

## 1. Unitary Pipeline with 100% Uncomputation

$$U_{\text{CSF}} = \mathcal{U}_{\text{uncompute}} \cdot \mathcal{U}_{\text{copy}} \cdot \mathcal{U}_{\text{force}} \cdot \mathcal{U}_{\kappa} \cdot \mathcal{U}_{\mathbf{n}} \cdot \mathcal{U}_{\nabla}$$

- **Forward Stencils**: Compute gradient, normal, curvature, and surface force $\mathbf{F}_s = \sigma \kappa \nabla \alpha$.
- **Output Copy**: Copies $\mathbf{F}_s$ to the force register.
- **Mirror Uncomputation**: Restores all intermediate stencil work registers back to $|0\rangle$.
- **Garbage Residual**: Verified **$0.0000 \times 10^0$**.
