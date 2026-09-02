# PHASE F19: BGK INFORMATION LOSS & NON-INJECTIVITY PROOF
## Rigorous Characterization of Dissipative State-Space Contraction

**Document**: BGK Information Loss & Non-Injectivity Specification  
**Project**: Quantum Lattice Boltzmann Method (QLBM) for Two-Phase Flow  
**Repository**: `/home/aswa/Research/QLBM-DamBreak-Production`  
**Branch**: `feature/direct-encoding-two-phase-qlbm`  
**Date**: September 2026  

---

## 1. Mathematical Analysis of Information Dissipation

In the BGK collision model, the kinetic populations are updated as:
$$f_i^* = f_i + \omega_f (f_i^{\text{eq}}(\rho, \mathbf{u}) - f_i) = (1 - \omega_f) f_i + \omega_f f_i^{\text{eq}}(\rho, \mathbf{u})$$

1. **Hydrodynamic vs. Kinetic Degrees of Freedom**:
   - Conserved hydrodynamic moments: Mass $\rho = \sum f_i$, Momentum $\mathbf{j} = \sum f_i \mathbf{c}_i$ (3 degrees of freedom in 2D).
   - Non-conserved kinetic modes: Non-equilibrium stress tensors $\Pi_{\alpha\beta}^{\text{neq}} = \sum f_i^{\text{neq}} c_{i\alpha} c_{i\beta}$ and ghost modes (6 degrees of freedom in D2Q9).
2. **Dissipative Relaxation**:
   - For $\omega_f = 1.0$, all non-equilibrium kinetic modes are annihilated: $f_i^* = f_i^{\text{eq}}(\rho, \mathbf{u})$.
   - Multiple distinct states $\mathbf{f}^{(1)} \ne \mathbf{f}^{(2)}$ sharing the same $\rho$ and $\mathbf{j}$ collapse to identical outputs:
     $$F(\mathbf{f}^{(1)}) = F(\mathbf{f}^{(2)})$$
   - Therefore, physical BGK collision is **many-to-one (non-injective)** and contracts phase space volume (dissipation / entropy increase).
