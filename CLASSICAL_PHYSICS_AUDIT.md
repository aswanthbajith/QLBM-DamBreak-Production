# Comprehensive Classical Physics Audit & Mathematical Mapping

**Auditor Role**: Senior CFD & Lattice Boltzmann Method Specialist  
**Repository**: `/home/aswa/Research/QLBM-DamBreak/`  
**Date**: August 19, 2026  

---

## 1. Physical Equation to Source Code Mapping

| Physical Equation | Mathematical Expression | Implementation File | Class & Function | Variable Names | Units | Numerical Approximation | Boundary Treatment | Test Coverage | Potential Weakness |
| :--- | :--- | :--- | :--- | :--- | :--- | :--- | :--- | :--- | :--- |
| **1. Variable Density Interpolation** | $\rho(\phi) = \rho_G + \phi(\rho_L - \rho_G)$ | `classical/two_phase_physics.py` | `TwoPhaseProperties.density` (L48–51) | `phi`, `rho_L`, `rho_G` | Lattice $[M/L^3]$ | Linear interpolation with $\text{clip}(\phi, 0, 1)$ | Inherited from $\phi$ | `tests/test_two_phase_physics.py:test_01_density_bounds` | Smears at high density ratio $\rho_L/\rho_G > 50$ |
| **2. Dynamic Viscosity Interpolation** | $\mu(\phi) = \mu_G + \phi(\mu_L - \mu_G)$ | `classical/two_phase_physics.py` | `TwoPhaseProperties.dynamic_viscosity` (L53–56) | `phi`, `mu_L`, `mu_G` | Lattice $[M/(LT)]$ | Linear interpolation with $\text{clip}(\phi, 0, 1)$ | Inherited from $\phi$ | `tests/test_two_phase_physics.py:test_01_density_bounds` | Viscosity jumps at sharp diffuse fronts |
| **3. Hydrodynamic Relaxation Time** | $\tau_v(\phi) = 3 \frac{\mu(\phi)}{\rho(\phi)} + 0.5$ | `classical/two_phase_physics.py` | `TwoPhaseProperties.relaxation_time` (L64–68) | `nu`, `tau_v` | Lattice $[T]$ | $\tau_v = \nu / c_s^2 + 0.5$ with $c_s^2 = 1/3$ | Internal field | `tests/test_two_phase_physics.py:test_01_density_bounds` | Must maintain $\tau_v > 0.5$ for BGK stability |
| **4. Isotropic D2Q9 Gradient Stencil** | $\nabla \psi = 3 \sum_{i=1}^8 w_i \mathbf{c}_i \psi(\mathbf{x} + \mathbf{c}_i)$ | `classical/two_phase_physics.py` | `TwoPhaseProperties.compute_gradient` (L69–90) | `grad_x`, `grad_y`, `wi`, `cx`, `cy` | Lattice $[1/L]$ | 4th-order isotropic 8-neighbor stencil | Zero-gradient Neumann extrapolation at walls | `tests/test_two_phase_physics.py:test_05_laplace_surface_tension` | Near-wall gradient truncation error |
| **5. Isotropic D2Q9 Laplacian Stencil** | $\nabla^2 \psi = 6 \sum_{i=1}^8 w_i [\psi(\mathbf{x} + \mathbf{c}_i) - \psi(\mathbf{x})]$ | `classical/two_phase_physics.py` | `TwoPhaseProperties.compute_laplacian` (L92–110) | `lap`, `wi` | Lattice $[1/L^2]$ | 2nd-order isotropic stencil | Zero boundary value clamp | `tests/test_two_phase_physics.py:test_05_laplace_surface_tension` | Clamped boundary neglects wall curvature |
| **6. Continuum Surface Force (CSF)** | $\mathbf{F}_s = \sigma \kappa_I \nabla \phi$ | `classical/two_phase_physics.py` | `TwoPhaseProperties.compute_curvature_and_csf` (L112–134) | `Fx_s`, `Fy_s`, `kappa` | Lattice $[M/(L^2 T^2)]$ | $\kappa = -\nabla \cdot (\nabla \phi / |\nabla \phi|_\epsilon)$ | Evaluated on interior domain | `tests/test_two_phase_physics.py:test_05_laplace_surface_tension` | Parasitic currents at high surface tension |
| **7. Gravitational Buoyancy Force** | $\mathbf{F}_g = (\rho(\phi) - \rho_G) \mathbf{g}$ | `classical/forcing.py` | `TwoPhaseForcing.compute_total_force` (L29–50) | `Fx_g`, `Fy_g`, `gx`, `gy` | Lattice $[M/(L^2 T^2)]$ | Background gas density subtraction | Uniform body force | `tests/test_two_phase_physics.py:test_04_gravity_direction` | None; prevents gas domain artificial acceleration |
| **8. Guo Body Forcing Expansion** | $F_i = (1 - \frac{1}{2\tau_v}) w_i [\frac{(\mathbf{c}_i - \mathbf{u})\cdot \mathbf{F}}{\rho c_s^2} + \frac{(\mathbf{c}_i \cdot \mathbf{u})(\mathbf{c}_i \cdot \mathbf{F})}{\rho c_s^4}]$ | `classical/forcing.py` | `TwoPhaseForcing.compute_guo_force_term` (L52–75) | `Fi`, `coeff`, `term1`, `term2` | Lattice $[M/(L^3 T)]$ | 2nd-order velocity expansion | Local to each node | `tests/test_two_phase_physics.py:test_04_gravity_direction` | Division by $\rho$ requires $\rho_{safe} > 10^{-12}$ |
| **9. Conservative Allen-Cahn Interface** | $\frac{\partial \phi}{\partial t} + \nabla \cdot (\phi \mathbf{u}) = \nabla \cdot [M(\nabla \phi - \frac{1-4(\phi-0.5)^2}{W} \mathbf{n})]$ | `classical/phase_field.py` | `PhaseFieldLBM2D.step` (L79–127) | `h`, `h_post`, `F_phi_x`, `F_phi_y` | Dimensionless $\phi \in [0, 1]$ | D2Q9 lattice collision-streaming with counter-gradient source | Wetting / contact angle bounce-back | `tests/test_two_phase_physics.py:test_02_phase_bounds`, `test_03_mass_conservation` | Interface width $W$ must span $\ge 3$ nodes |
| **10. Velocity-Based D2Q9 Hydrodynamic Collision** | $g_i^{post} = g_i - \frac{1}{\tau_v}(g_i - g_i^{eq}) + F_i$ | `classical/two_phase_lbm.py` | `TwoPhaseLBM2D.step` (L121–152) | `g`, `g_post`, `geq`, `p_star` | Lattice $[L/T]$ | Incompressible BGK with $p^* = p / (\rho c_s^2)$ | Solid wall half-way bounce-back / free-slip floor | `tests/test_two_phase_physics.py:test_06_dam_break_initialization` | Limited to low Mach number $\text{Ma} < 0.15$ |

---

## 2. Boundary Condition Formulation
- **Top, Left, Right Solid Walls**: Half-way bounce-back $g_{\bar{i}}(\mathbf{x}_w, t+1) = g_i^{post}(\mathbf{x}_w, t)$ where $\bar{i} = \text{opp}[i]$.
- **Bottom Floor**: Free-slip specular reflection $g_{\text{refl}}(\mathbf{x}_f, t+1) = g_i^{post}(\mathbf{x}_f, t)$ where $(c_x, c_y) \to (c_x, -c_y)$.
