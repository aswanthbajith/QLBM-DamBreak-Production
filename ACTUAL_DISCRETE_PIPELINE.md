# Mathematical Trace of the Discrete Two-Phase LBM Timestep Pipeline

**Author**: Lead Mathematical Modeler & Numerical Analyst  
**Date**: August 19, 2026  
**Repository**: `/home/aswa/Research/QLBM-DamBreak/`  

---

## 1. Single Discrete Timestep Operator Decomposition

The classical two-phase Lattice Boltzmann solver advances the state over one discrete timestep $\Delta t = 1$ via the following sequential algebraic pipeline:

```
[State at time t: Psi(t) = [g(t); h(t)] in R^(18 N)]
                         │
                         ▼
             [1. Macroscopic Recovery]
   phi(x) = sum_i h_i(x),   p(x) = rho(phi) c_s^2 sum_i g_i(x)
                 j(x) = sum_i g_i(x) c_i
                         │
                         ▼
        [2. Density & Viscosity Field Evaluation]
          rho(x) = rho_G + phi(x) * (rho_L - rho_G)
          mu(x)  = mu_G  + phi(x) * (mu_L  - mu_G)
          tau_v(x) = 3 mu(x)/rho(x) + 0.5
                         │
                         ▼
        [3. Interfacial & Gravitational Forcing]
          F_g(x) = (rho(x) - rho_G) * g
          F_s(x) = sigma * kappa(phi) * grad(phi)
          F(x)   = F_g(x) + F_s(x)
                         │
                         ▼
            [4. Velocity Moment Shift]
          u(x) = j(x) + 0.5 * F(x) / rho(x)
                         │
                         ▼
        [5. Phase-Field Allen-Cahn Collision]
          F_phi(x) = M * [ grad(phi) - (1 - 4(phi - 0.5)^2)/W * n ]
          h_i^{eq}(x) = w_i phi(x) [ 1 + (c_i . u) / c_s^2 ]
          S_i(x) = (1 - 0.5/tau_phi) w_i (c_i . F_phi) / c_s^2
          h_i^{post}(x) = h_i(x) - (1/tau_phi)[h_i(x) - h_i^{eq}(x)] + S_i(x)
                         │
                         ▼
         [6. Hydrodynamic Collision (Guo BGK)]
          g_i^{eq}(x) = w_i [ p/(rho c_s^2) + (c_i.u)/c_s^2 + (c_i.u)^2/(2 c_s^4) - |u|^2/(2 c_s^2) ]
          F_i(x) = (1 - 0.5/tau_v) w_i [ (c_i - u).F/(rho c_s^2) + (c_i.u)(c_i.F)/(rho c_s^4) ]
          g_i^{post}(x) = g_i(x) - (1/tau_v)[g_i(x) - g_i^{eq}(x)] + F_i(x)
                         │
                         ▼
        [7. Spatial Streaming & Boundary Reflection]
          g_i(x + c_i, t+1) = g_i^{post}(x, t)  (with wall bounce-back S)
          h_i(x + c_i, t+1) = h_i^{post}(x, t)  (with wall bounce-back S)
                         │
                         ▼
[State at time t+1: Psi(t+1) = S * Psi^{post}(Psi(t)) in R^(18 N)]
```

---

## 2. Dimensional Data-Flow Accounting

| Stage | Operation | Source Code Function | Input Dimensions | Output Dimensions |
| :--- | :--- | :--- | :---: | :---: |
| **0. Input State** | $\mathbf{\Psi}(t) = [\mathbf{g}; \mathbf{h}]$ | `classical/two_phase_lbm.py` | $\mathbb{R}^{18 N}$ | $\mathbb{R}^{18 N}$ |
| **1. Macroscopic** | $\phi = \sum h_i, \mathbf{j} = \sum g_i \mathbf{c}_i$ | `TwoPhaseLBM2D.step` | $\mathbb{R}^{18 N}$ | $\phi \in \mathbb{R}^N, \mathbf{j} \in \mathbb{R}^{2N}$ |
| **2. Properties** | $\rho(\phi), \mu(\phi), \tau_v(\phi)$ | `TwoPhaseProperties.density` | $\mathbb{R}^N$ | $\rho, \tau_v \in \mathbb{R}^N$ |
| **3. Forcing** | $\mathbf{F} = \mathbf{F}_g + \mathbf{F}_s$ | `TwoPhaseForcing.compute_total_force` | $\mathbb{R}^N, \mathbb{R}^N$ | $\mathbf{F} \in \mathbb{R}^{2N}$ |
| **4. Velocity** | $\mathbf{u} = \mathbf{j} + \frac{1}{2\rho}\mathbf{F}$ | `TwoPhaseLBM2D.step` | $\mathbb{R}^{2N}, \mathbb{R}^N, \mathbb{R}^{2N}$ | $\mathbf{u} \in \mathbb{R}^{2N}$ |
| **5. Phase Collision** | $\mathbf{h}^{post} = \mathbf{h} - \frac{1}{\tau_\phi}(\mathbf{h} - \mathbf{h}^{eq}) + \mathbf{S}$ | `PhaseFieldLBM2D.step` | $\mathbb{R}^{9N}, \mathbb{R}^{2N}$ | $\mathbf{h}^{post} \in \mathbb{R}^{9N}$ |
| **6. Fluid Collision** | $\mathbf{g}^{post} = \mathbf{g} - \frac{1}{\tau_v}(\mathbf{g} - \mathbf{g}^{eq}) + \mathbf{F}$ | `TwoPhaseLBM2D.step` | $\mathbb{R}^{9N}, \mathbb{R}^{2N}, \mathbb{R}^{2N}$ | $\mathbf{g}^{post} \in \mathbb{R}^{9N}$ |
| **7. Streaming** | $\mathbf{\Psi}(t+1) = \mathbf{S} \mathbf{\Psi}^{post}$ | `MatrixTwoPhaseLBM2D.step` | $\mathbb{R}^{18 N}$ | $\mathbb{R}^{18 N}$ |
