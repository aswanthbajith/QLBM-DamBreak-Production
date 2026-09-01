# LEVEL-5: EXACT MATHEMATICAL SPECIFICATION OF THE VALIDATED TWO-PHASE LBM

**Source Implementation**: [`classical/level4_two_phase.py`](file:///home/aswa/Research/QLBM-DamBreak-Production/classical/level4_two_phase.py)  
**Status**: Authoritative Reference Specification  

---

## 1. State Variables & Physical Fields

| Symbol | Mathematical Definition | Code Variable | Spatial Dimension | Physical Meaning |
| :--- | :--- | :--- | :---: | :--- |
| $f_i(\mathbf{x}, t)$ | D2Q9 populations ($i=0\dots 8$) | `self.f` | `(9, ny, nx)` | Hydrodynamic velocity/pressure distributions |
| $g_i(\mathbf{x}, t)$ | D2Q9 populations ($i=0\dots 8$) | `self.g` | `(9, ny, nx)` | Order-parameter (phase-field) distributions |
| $\alpha(\mathbf{x}, t)$ | $\alpha = \sum_{i=0}^8 g_i \in [0, 1]$ | `self.alpha` | `(ny, nx)` | Liquid volume fraction ($1=$ water, $0=$ gas) |
| $\rho(\mathbf{x}, t)$ | $\rho = \sum_{i=0}^8 f_i = \alpha \rho_L + (1-\alpha)\rho_G$ | `self.rho` | `(ny, nx)` | Macroscopic fluid mixture density |
| $\mathbf{u}(\mathbf{x}, t)$ | $\mathbf{u} = \frac{\sum_{i=0}^8 \mathbf{c}_i f_i + 0.5 \mathbf{F}}{\rho}$ | `self.u` | `(2, ny, nx)` | Macroscopic barycentric velocity field |

---

## 2. Kinetic Evolution Equations

### A. Macroscopic Moments & Shifted Velocity
$$\rho(\mathbf{x}, t) = \sum_{i=0}^8 f_i(\mathbf{x}, t), \quad \alpha(\mathbf{x}, t) = \text{clip}\left( \sum_{i=0}^8 g_i(\mathbf{x}, t), 0, 1 \right)$$
$$\mathbf{u}(\mathbf{x}, t) = \frac{\sum_{i=0}^8 \mathbf{c}_i f_i(\mathbf{x}, t) + 0.5 \mathbf{F}(\mathbf{x}, t)}{\max(\rho(\mathbf{x}, t), 10^{-6})}$$
$$\mathbf{u}_{\text{clamped}} = \mathbf{u} \cdot \min\left(1, \frac{u_{\text{max}}}{|\mathbf{u}| + 10^{-12}}\right), \quad u_{\text{max}} = 0.15$$

### B. Equilibrium Distributions
1. **Hydrodynamic Equilibrium ($f_i^{\text{eq}}$)**:
   $$f_i^{\text{eq}}(\rho, \mathbf{u}) = w_i \rho \left[ 1 + 3 (\mathbf{c}_i \cdot \mathbf{u}) + \frac{9}{2} (\mathbf{c}_i \cdot \mathbf{u})^2 - \frac{3}{2} |\mathbf{u}|^2 \right]$$
2. **Phase-Field Equilibrium ($g_i^{\text{eq}}$)**:
   $$g_i^{\text{eq}}(\alpha, \mathbf{u}) = w_i \alpha \left[ 1 + 3 (\mathbf{c}_i \cdot \mathbf{u}) \right]$$

### C. Total Body and Interfacial Forces ($\mathbf{F} = \mathbf{F}_g + \mathbf{F}_s$)
1. **Gravitational Buoyancy Force ($\mathbf{F}_g$)**:
   $$\mathbf{F}_g = \begin{bmatrix} 0 \\ (\rho - \rho_G) g_{\text{acc}} \end{bmatrix}$$
2. **Continuum Surface Force ($\mathbf{F}_s = \sigma \kappa \nabla \alpha$)**:
   - Gradients: $\nabla \alpha = \left[ \frac{\alpha(x+1, y) - \alpha(x-1, y)}{2}, \frac{\alpha(x, y+1) - \alpha(x, y-1)}{2} \right]^T$
   - Interface Unit Normal: $\mathbf{n} = \frac{\nabla \alpha}{|\nabla \alpha| + 10^{-12}}$ (masked where $|\nabla \alpha| > 10^{-3}$, 0 elsewhere)
   - Curvature: $\kappa = \text{clip}(-\nabla \cdot \mathbf{n}, -2.0, 2.0)$
   - Surface Force: $\mathbf{F}_s = \sigma \kappa \nabla \alpha$

### D. Collision with Guo Forcing
$$f_i^* = f_i - \omega_f(\alpha) (f_i - f_i^{\text{eq}}) + S_i(\mathbf{F}, \mathbf{u})$$
$$g_i^* = g_i - \omega_g (g_i - g_i^{\text{eq}})$$
where:
$$\nu(\alpha) = \alpha \nu_L + (1-\alpha)\nu_G, \quad \tau_f(\alpha) = 3\nu(\alpha) + 0.5, \quad \omega_f(\alpha) = \frac{1}{\tau_f(\alpha)}, \quad \omega_g = \frac{1}{\tau_\phi}$$
$$S_i = \left(1 - \frac{\omega_f}{2}\right) w_i \left[ 3 (\mathbf{c}_i \cdot \mathbf{F}) + 9 (\mathbf{c}_i \cdot \mathbf{u})(\mathbf{c}_i \cdot \mathbf{F}) - 3 (\mathbf{u} \cdot \mathbf{F}) \right]$$

### E. Spatial Streaming & Boundary Involution
1. **Streaming**: $f_i(\mathbf{x} + \mathbf{c}_i, t + \Delta t) = f_i^*(\mathbf{x}, t)$, $g_i(\mathbf{x} + \mathbf{c}_i, t + \Delta t) = g_i^*(\mathbf{x}, t)$
2. **Solid Wall Involution**: On solid wall boundary nodes $\mathbf{x} \in \partial\Omega$:
   $$f_{\text{opp}(i)}(\mathbf{x}_{\text{solid}}) = f_i^*(\mathbf{x}_{\text{solid}}), \quad g_{\text{opp}(i)}(\mathbf{x}_{\text{solid}}) = g_i^*(\mathbf{x}_{\text{solid}})$$

---

## 3. Nonlinear Term Breakdown

| Operation | Code Line / Method | Mathematical Expression | Algebraic Nature | Carleman Impact |
| :--- | :--- | :--- | :---: | :--- |
| Convective Momentum | `_compute_equilibrium` | $\rho (\mathbf{c}_i \cdot \mathbf{u})^2 = \frac{(\mathbf{c}_i \cdot \mathbf{j})^2}{\rho}$ | Rational $\mathcal{O}(j^2 / \rho)$ | Approximated as quadratic in $\mathbf{j}$ for low-Mach flow |
| Phase Advection | `_compute_equilibrium` | $\alpha (\mathbf{c}_i \cdot \mathbf{u}) = \frac{\alpha (\mathbf{c}_i \cdot \mathbf{j})}{\rho}$ | Bilinear / Rational | Linearized via reference density $\rho_0$ |
| Surface Tension Force | `compute_surface_tension_force` | $\sigma \kappa(\alpha) \nabla \alpha$ | Nonlinear Differential | Handled via spatial stencil expansion |
| Guo Velocity Shift | `compute_total_force` | $9 (\mathbf{c}_i \cdot \mathbf{u})(\mathbf{c}_i \cdot \mathbf{F})$ | Cross-Coupled Quadratic | Quadratic polynomial term |
