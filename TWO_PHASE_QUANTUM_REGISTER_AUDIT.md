# Two-Phase Hydrodynamic and Phase-Field Quantum Register Integrity Audit

**Author**: Lead Quantum Algorithm Engineer & Quantum Linear Algebra Specialist  
**Date**: August 19, 2026  
**Repository**: `/home/aswa/Research/QLBM-DamBreak/`  

---

## 1. Multi-Sector Quantum Register Integrity

To prevent unphysical cross-contamination between the hydrodynamic fluid populations ($\mathbf{g}$) and the phase-field order parameter populations ($\mathbf{h}$), the basis states are strictly partitioned and tracked:

```
Subspace Sector             Basis Index Range            Qubit State Mapping |k, q, x, y>
───────────────────────────────────────────────────────────────────────────────────────────
Hydrodynamic (g)            0       ..   9N - 1          |k=0> |q_g in 0..8>   |x, y>
Phase-Field (h)             9N      ..  18N - 1          |k=0> |q_h in 9..17>  |x, y>
Quadratic (g x g)           18N     ..  99N - 1          |k=1> |(q1, q2) in g x g> |x, y>
Quadratic (g x h)           99N     .. 180N - 1          |k=1> |(q1, q2) in g x h> |x, y>
Quadratic (h x g)          180N     .. 261N - 1          |k=1> |(q1, q2) in h x g> |x, y>
Quadratic (h x h)          261N     .. 342N - 1          |k=1> |(q1, q2) in h x h> |x, y>
Padding / Unused           342N     .. D_pad - 1         |k_pad> (Decoupled Identity subspace)
```

---

## 2. Sector Decoupling & Basis Invariance Tests
1. **Linear Hydrodynamic Sector**: A pure hydrodynamic excitation $\mathbf{\psi} = [\mathbf{g}; \mathbf{0}]$ evolves under $\mathbf{M}_{1, g}$ with zero spurious leakage into $\mathbf{h}$.
2. **Linear Phase-Field Sector**: A pure phase-field excitation $\mathbf{\psi} = [\mathbf{0}; \mathbf{h}]$ evolves under $\mathbf{M}_{1, h}$ with zero spurious leakage into $\mathbf{g}$.
3. **Quadratic Coupling Sector**: Non-linear momentum advection ($\phi \mathbf{u}$) and convective transport ($\mathbf{u} \otimes \mathbf{u}$) couple *exclusively* through the designated off-diagonal blocks of $\mathbf{M}_{2, node}$, exactly reproducing the physical Navier-Stokes and Allen-Cahn nonlinearities.
