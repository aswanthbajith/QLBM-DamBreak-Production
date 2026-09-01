# LEVEL-6: EXACT LEVEL-4 COMPUTATIONAL DEPENDENCY GRAPH & ALGEBRAIC CLASSIFICATION

**Target Reference**: [`classical/level4_two_phase.py`](file:///home/aswa/Research/QLBM-DamBreak-Production/classical/level4_two_phase.py)  
**Objective**: Complete computational dependency graph and algebraic taxonomy of all operations in the Level-4 classical reference solver.

---

## 1. Computational Dependency Graph

```text
                                        [ f_i(x,y,t), g_i(x,y,t) ]
                                                     │
                         ┌───────────────────────────┴───────────────────────────┐
                         ▼                                                       ▼
                [ rho = sum_i f_i ]                                   [ alpha = sum_i g_i ]
                         │                                                       │
                         │                                                       ▼
                         │                                            [ clip(alpha, 0, 1) ]
                         │                                                       │
                         │                                    ┌──────────────────┴──────────────────┐
                         │                                    ▼                                     ▼
                         │                         [ nu = alpha nu_L + ... ]             [ grad(alpha) (stencil) ]
                         │                                    │                                     │
                         │                                    ▼                                     ▼
                         │                         [ tau = 3nu + 0.5 ]               [ n = grad / |grad| ]
                         │                                    │                                     │
                         │                                    ▼                                     ▼
                         │                         [ omega_f = 1/tau ]               [ div(n) -> kappa ]
                         │                                    │                                     │
                         ▼                                    │                                     ▼
                [ F_g = (rho - rho_G) g ]                     │                       [ F_s = sigma kappa grad(alpha) ]
                         │                                    │                                     │
                         └────────────────────────────┬───────┴─────────────────────────────────────┘
                                                      │
                                                      ▼
                                            [ F = F_g + F_s ]
                                                      │
                                      ┌───────────────┴───────────────┐
                                      ▼                               ▼
                      [ j = sum_i c_i f_i ]               [ S_i(F, u) Guo forcing ]
                                      │                               │
                                      ▼                               │
                      [ u* = (j + 0.5 F) / rho ]                      │
                                      │                               │
                                      ▼                               │
                      [ u = clamp(u*, 0.15) ]                         │
                                      │                               │
                      ┌───────────────┴───────────────┐               │
                      ▼                               ▼               │
             [ f_eq(rho, u) ]                 [ g_eq(alpha, u) ]      │
                      │                               │               │
                      └───────────────┬───────────────┘               │
                                      │                               │
                                      ▼                               ▼
                         [ f* = f - omega_f (f - f_eq) + S_i ]
                         [ g* = g - omega_g (g - g_eq) ]
                                      │
                                      ▼
                         [ Streaming: f(x+c_i, t+1) = f* ]
                         [ Boundary: Half-Way Bounce-Back ]
```

---

## 2. Complete Algebraic Classification Table

| Category | Component / Operation | Mathematical Formula | Algebraic Type | Quantum Implementation Feasibility |
| :--- | :--- | :--- | :---: | :--- |
| **1. Linear** | Hydrodynamic Density | $\rho = \sum_{i=0}^8 f_i$ | Exact Linear | Trivial in $M_1$ / Quantum Observable |
| **1. Linear** | Phase Fraction | $\alpha = \sum_{i=0}^8 g_i$ | Exact Linear | Trivial in $M_1$ / Quantum Observable |
| **1. Linear** | Linear Momentum Flux | $\mathbf{j} = \sum_{i=0}^8 \mathbf{c}_i f_i$ | Exact Linear | Trivial in $M_1$ / Quantum Observable |
| **1. Linear** | Gravitational Buoyancy | $\mathbf{F}_g = (\rho - \rho_G)\mathbf{g}_{\text{acc}}$ | Exact Linear | Exact in $M_1$ / Quantum Body Force |
| **1. Linear** | Linear Advection Term | $3 w_i (\mathbf{c}_i \cdot \mathbf{j})$ | Exact Linear | Exact in $M_1$ |
| **2. Quadratic Polynomial** | Convective Momentum (Fixed Density) | $\frac{9}{2} w_i \frac{(\mathbf{c}_i \cdot \mathbf{j})^2}{\rho_0} - \frac{3}{2} w_i \frac{|\mathbf{j}|^2}{\rho_0}$ | Exact Quadratic in $\mathbf{f}\otimes\mathbf{f}$ | Exact in $M_2$ / Second-Order Carleman |
| **2. Quadratic Polynomial** | Phase Advection (Fixed Density) | $3 w_i \frac{\alpha (\mathbf{c}_i \cdot \mathbf{j})}{\rho_0}$ | Exact Bilinear in $\mathbf{g}\otimes\mathbf{f}$ | Exact in $M_2$ / Second-Order Carleman |
| **2. Quadratic Polynomial** | Guo Velocity Shift | $9 (\mathbf{c}_i \cdot \mathbf{u})(\mathbf{c}_i \cdot \mathbf{F})$ | Exact Quadratic in $\mathbf{z}\otimes\mathbf{z}$ | Exact in $M_2$ |
| **3. Rational** | Exact Momentum Convection | $\frac{j_a j_b}{\rho}$ with $\rho = \sum f_k$ | Rational Degree 2/1 | Requires Taylor expansion around $\rho_0$ or auxiliary lifting |
| **3. Rational** | Exact Phase Advection | $\frac{\alpha j_a}{\rho}$ with $\rho = \sum f_k$ | Rational Degree 2/1 | Requires Taylor expansion around $\rho_0$ or auxiliary lifting |
| **3. Rational** | Viscosity Relaxation | $\omega_f(\alpha) = \frac{1}{3(\alpha \nu_L + (1-\alpha)\nu_G) + 0.5}$ | Rational Degree 0/1 in $\alpha$ | Requires fixed mean $\tau_0$ or auxiliary expansion |
| **4. Non-Polynomial / Stencil** | Interfacial Normal Vector | $\mathbf{n} = \frac{\nabla \alpha}{\sqrt{|\nabla\alpha|^2} + 10^{-12}}$ | Non-polynomial Nonlocal | Requires finite difference oracle / classical hybrid |
| **4. Non-Polynomial / Stencil** | Interfacial Curvature | $\kappa = -\nabla \cdot \mathbf{n}$ | Non-polynomial Nonlocal | Requires multi-qubit spatial stencil / classical hybrid |
| **4. Non-Polynomial / Stencil** | Continuum Surface Force | $\mathbf{F}_s = \sigma \kappa \nabla \alpha$ | Non-polynomial Nonlocal | Classical hybrid preprocessing or spatial multi-ancilla |
| **5. Piecewise / Clipping** | Volume Fraction Regularization | $\text{clip}(\alpha, 0, 1)$ | Piecewise Linear | Measurement / postselection / state normalization |
| **5. Piecewise / Clipping** | Low-Mach Velocity Clamping | $|\mathbf{u}| \le 0.15$ | Non-polynomial Clip | Validated low-Mach operating regime ($\text{Ma} \le 0.1$) |
| **6. Unitary Permutations** | Spatial Streaming | $f_i(\mathbf{x}+\mathbf{c}_i, t+1) = f_i^*$ | Permutation $S$ | Exact Unitary Operator $\|S^\dagger S - I\| = 0$ |
| **6. Unitary Permutations** | Solid Wall Bounce-Back | $f_{\text{opp}(i)}(\mathbf{x}_{\text{wall}}) = f_i^*$ | Involution $B$ | Exact Unitary Operator $\|B^\dagger B - I\| = 0, B^2 = I$ |
