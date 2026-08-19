# Forensic Discrete Time-Step Map & Polynomial Operation Audit

**Author**: Lead Mathematical Scientist & Senior Numerical Analyst  
**Date**: August 19, 2026  
**Repository**: `/home/aswa/Research/QLBM-DamBreak/`  

---

## 1. Trace of the Computational Execution Path

Every discrete timestep of the classical two-phase LBM solver executes the following mathematical pipeline:

```
[State Ψ(t) = [g(t); h(t)] ∈ R^(18N)]
                 │
                 ▼
     [Macroscopic Reconstruction]
        φ = Σ h_i (Linear)
        j = Σ g_i c_i (Linear)
        p = ρ(φ) c_s^2 Σ g_i (Affine/Linear)
                 │
                 ▼
   [Local Physical Properties]
        ρ(φ) = ρ_G + φ Δρ (Affine)
        μ(φ) = μ_G + φ Δμ (Affine)
        τ_v(φ) = 3 μ(φ)/ρ(φ) + 0.5 (Rational)
                 │
                 ▼
       [Forces & Acceleration]
        F_g = (ρ(φ) - ρ_G) g (Linear)
        F_s = σ κ(φ) ∇φ (Nonlinear / Diffuse Stencil)
        F = F_g + F_s
                 │
                 ▼
       [Shifted Fluid Velocity]
        u = j + 0.5 F / ρ(φ) (Rational / Shifted Linear)
                 │
                 ▼
     [Phase Collision (Allen-Cahn)]
        h_i^{eq} = w_i φ [1 + (c_i . u)/c_s^2] (Bilinear / Quadratic)
        S_i = (1 - 0.5/τ_φ) w_i (c_i . F_φ)/c_s^2 (Quadratic)
        h_i^{post} = h_i - (1/τ_φ)(h_i - h_i^{eq}) + S_i
                 │
                 ▼
    [Hydrodynamic Collision (Guo BGK)]
        g_i^{eq} = w_i [ p/(ρ c_s^2) + (c_i.u)/c_s^2 + (c_i.u)^2/(2 c_s^4) - |u|^2/(2 c_s^2) ] (Quadratic)
        F_i = (1 - 0.5/τ_v) w_i [ (c_i - u).F/(ρ c_s^2) + (c_i.u)(c_i.F)/(ρ c_s^4) ] (Bilinear / Quadratic)
        g_i^{post} = g_i - (1/τ_v)(g_i - g_i^{eq}) + F_i
                 │
                 ▼
     [Spatial Streaming & Boundaries]
        Ψ(t+1) = S · Ψ^{post} (Strictly Unitary Linear Permutation)
```

---

## 2. Term-by-Term Operation Classification

| Operation | Mathematical Formula | Code Location | Classification | Polynomial Degree |
| :--- | :--- | :--- | :---: | :---: |
| **Phase Fraction** | $\phi = \sum_{i=0}^8 h_i$ | `classical/phase_field.py:L79` | **LINEAR** | 1 |
| **Fluid Momentum** | $\mathbf{j} = \sum_{i=0}^8 g_i \mathbf{c}_i$ | `classical/two_phase_lbm.py:L142` | **LINEAR** | 1 |
| **Density Field** | $\rho(\phi) = \rho_G + \phi(\rho_L - \rho_G)$ | `classical/two_phase_physics.py:L48` | **AFFINE / LINEAR** | 1 |
| **Viscosity Field** | $\mu(\phi) = \mu_G + \phi(\mu_L - \mu_G)$ | `classical/two_phase_physics.py:L53` | **AFFINE / LINEAR** | 1 |
| **Relaxation Time** | $\tau_v(\phi) = 3 \mu(\phi)/\rho(\phi) + 0.5$ | `classical/two_phase_physics.py:L64` | **RATIONAL** | Non-poly (Closed via $\xi$) |
| **Buoyancy Force** | $\mathbf{F}_g = (\rho(\phi) - \rho_G) \mathbf{g}$ | `classical/forcing.py:L37` | **LINEAR** | 1 |
| **Surface Force** | $\mathbf{F}_s = \sigma \kappa(\phi) \nabla \phi$ | `classical/two_phase_physics.py:L112` | **QUADRATIC / NONLINEAR** | 2 |
| **Convective Flux** | $\frac{w_i}{2 c_s^4} (\mathbf{c}_i \cdot \mathbf{u})^2 - \frac{w_i}{2 c_s^2} |\mathbf{u}|^2$ | `classical/two_phase_lbm.py:L150` | **QUADRATIC** | 2 |
| **Phase Advection**| $\frac{w_i}{c_s^2} \phi (\mathbf{c}_i \cdot \mathbf{u})$ | `classical/phase_field.py:L102` | **BILINEAR / QUADRATIC** | 2 |
| **Counter-Gradient**| $\frac{M}{W} [1 - 4(\phi - 0.5)^2] \mathbf{n}$ | `classical/phase_field.py:L92` | **QUADRATIC** | 2 |
| **Streaming & BC** | $\mathbf{\Psi}(t+1) = \mathbf{S} \mathbf{\Psi}^{post}$ | `classical/matrix_two_phase_lbm.py:L74` | **UNITARY PERMUTATION** | 1 |
