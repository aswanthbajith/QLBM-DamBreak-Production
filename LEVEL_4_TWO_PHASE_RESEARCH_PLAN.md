# LEVEL-4 TWO-PHASE & FREE-SURFACE QLBM RESEARCH PLAN

**Project**: Quantum Lattice Boltzmann Method for Two-Phase Flow and Dam-Break Dynamics  
**Milestone**: Transition from Level-3 Hybrid Prototype to Level-4 High-Fidelity Two-Phase QLBM  
**Repository**: `/home/aswa/Research/QLBM-DamBreak-Production`  

---

## 1. Core Architectural Paradigm

To ensure physical validity and scientific rigor, the Level-4 program follows the strict five-stage methodology:

```text
┌─────────────────────────────────────────────────────────────┐
│ 1. Classical Two-Phase Mathematical Model First             │
│    (Conservative Phase-Field / Cahn-Hilliard Formulation)   │
└──────────────────────────────┬──────────────────────────────┘
                               │
                               ▼
┌─────────────────────────────────────────────────────────────┐
│ 2. Independent Reference Validation Second                  │
│    (Benchmark against OpenFOAM VOF & Martin-Moyce Data)     │
└──────────────────────────────┬──────────────────────────────┘
                               │
                               ▼
┌─────────────────────────────────────────────────────────────┐
│ 3. Coupled Nonlinear Formulation Third                      │
│    (Exact Polynomial Degree, Surface Tension F_s = μ ∇ϕ)    │
└──────────────────────────────┬──────────────────────────────┘
                               │
                               ▼
┌─────────────────────────────────────────────────────────────┐
│ 4. Carleman Linearization & Truncation Fourth               │
│    (Local Kronecker Decoupled Tensor Lifting 342N)          │
└──────────────────────────────┬──────────────────────────────┘
                               │
                               ▼
┌─────────────────────────────────────────────────────────────┐
│ 5. Quantum State Encoding & Resource Estimation Last        │
│    (Power-of-Two Register Mapping, Gate Depth, OAA Steps)   │
└─────────────────────────────────────────────────────────────┘
```

---

## 2. Stage 1: Classical Two-Phase Mathematical Model

### A. Kinetic Equations
* **Hydrodynamic Distribution**: $f_i(\mathbf{x}, t)$ evolves the Navier-Stokes velocity and pressure fields with density ratio $\rho_L / \rho_G = 10$:
  $$f_i(\mathbf{x} + \mathbf{c}_i \Delta t, t + \Delta t) - f_i(\mathbf{x}, t) = -\frac{1}{\tau_f} [f_i(\mathbf{x}, t) - f_i^{\text{eq}}(\rho, \mathbf{u})] + \Delta f_i^{\text{body}} + \Delta f_i^{\text{surface}}$$
* **Order-Parameter Distribution**: $g_i(\mathbf{x}, t)$ evolves the conservative Allen-Cahn / Cahn-Hilliard interface capturing equation:
  $$g_i(\mathbf{x} + \mathbf{c}_i \Delta t, t + \Delta t) - g_i(\mathbf{x}, t) = -\frac{1}{\tau_g} [g_i(\mathbf{x}, t) - g_i^{\text{eq}}(\phi, \mathbf{u})] + \Delta g_i^{\text{interface}}$$

### B. Interfacial Thermodynamics & Surface Tension
* **Chemical Potential**: $\mu_\phi = 4 \beta \phi (\phi - 1) (\phi - 0.5) - \kappa \nabla^2 \phi$.
* **Surface Tension Force**: $\mathbf{F}_s = \mu_\phi \nabla \phi = \sigma \kappa_{\text{curv}} \mathbf{n} \delta_s$.

---

## 3. Stage 2: Independent Reference Validation Framework

* **Benchmark Problem**: Martin & Moyce (1952) 2D Dam-Break Column Collapse in an Enclosed Cavity.
* **Validation Datasets**:
  1. Non-dimensional surge wave front location: $x^*(t^*) = x(t) / L$ vs $t^* = t \sqrt{g / L}$.
  2. Non-dimensional residual column height: $h^*(t^*) = h(t) / H$ vs $t^* = t \sqrt{g / H}$.
  3. Total kinetic energy dissipation and interfacial area evolution.
* **Mesh Independence Study**: Spatial convergence tested across $32 \times 32$, $64 \times 64$, and $128 \times 128$ lattices.

---

## 4. Stage 3: Coupled Polynomial Formulation

* Determine the exact polynomial expansion of $f_i^{\text{eq}}(\rho, \mathbf{u})$, $g_i^{\text{eq}}(\phi, \mathbf{u})$, and forcing increments $\Delta f_i(\phi, \mathbf{u}, \nabla \phi)$.
* Ensure non-dimensional velocity Mach number $\text{Ma} \ll 1$ maintains polynomial truncation error $< 10^{-4}$.

---

## 5. Stage 4: High-Fidelity Carleman Linearization

* Derive local Carleman evaluation operator $A_{\text{eval}} \in \mathbb{R}^{18 \times d_k}$ for Order-2 ($d_2 = 342$) and Order-3 ($d_3 = 6156$) lifting.
* Characterize truncation error $E(t) = \|\Psi' \otimes \Psi' - (M_1 \otimes M_1)(\Psi \otimes \Psi)\|$ as a function of Reynolds number $\text{Re}$ and Weber number $\text{We}$.

---

## 6. Stage 5: Quantum Encoding, Transpilation & Scaling

* Logarithmic spatial qubit scaling: $n = \lceil\log_2 N_x\rceil + \lceil\log_2 N_y\rceil + 5$ qubits.
* Power-of-two Sz.-Nagy unitary dilation on $2^{n+1}$ Hilbert space.
* Full gate compilation and resource budgeting targeting fault-tolerant logical architectures (T-depth, Clifford counts, and Oblivious Amplitude Amplification overhead).
