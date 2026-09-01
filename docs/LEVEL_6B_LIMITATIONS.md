# LEVEL-6B: LIMITATIONS & EXPLICIT NON-CLAIMS

**Document**: Scientific Boundaries and Non-Claims for Level 6B  
**Repository**: `/home/aswa/Research/QLBM-DamBreak-Production`  
**Date**: September 2026  

---

## 1. Technical Limitations of Level 6B

1. **Second-Order Low-Mach Carleman Truncation**:
   The local collision operator truncates higher-order convective terms ($j_a j_b \delta\rho / \rho_0^2 \sim \mathcal{O}(\text{Ma}^2 \delta\rho)$). The formulation is restricted to weakly-compressible low-Mach flows ($\text{Ma} \le 0.1$).
2. **Fixed Reference Viscosity Relaxation**:
   The Carleman collision matrix utilizes a mean fixed relaxation time $\tau_f = 3\bar{\nu} + 0.5$ around $\rho_0 = 1.0$.
3. **Classical-Quantum Roundtrip Overhead**:
   Because Level 6B is a Hybrid $K=1$ architecture, macroscopic populations are reconstructed classically at every timestep. It does not perform measurement-free multi-timestep evolution.
4. **Classical Surface Tension Calculation**:
   Brackbill Continuum Surface Force $\mathbf{F}_s = \sigma \kappa \nabla \alpha$ is calculated via classical spatial finite-difference stencils rather than on-chip quantum arithmetic.

---

## 2. Explicit Non-Claims (Prohibited Scientific Statements)

- **DO NOT** claim a "fully quantum Lattice Boltzmann solver".
- **DO NOT** claim an "autonomous measurement-free multi-timestep solver".
- **DO NOT** claim "quantum speedup" on classical simulators.
- **DO NOT** claim "exact nonlinear Navier-Stokes solution".
- **DO NOT** claim "real physical IBM Quantum execution" without verified QPU job identifiers.
