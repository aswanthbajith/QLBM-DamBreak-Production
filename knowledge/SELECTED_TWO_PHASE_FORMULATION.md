# Selected Two-Phase LBM Formulation for Dam-Break Simulation

**Document Status**: Lead Numerical Fluid-Dynamics Formulation Dossier  
**Primary Reference**: Watanabe & Hu (2026) / Fakhari et al. (2017) / Liang et al. (2014) / Geier et al. (2015)  
**Target Flow**: Two-Phase Liquid-Gas Dam-Break Flow with Density Contrast, Gravity, and Free-Surface Impact  

---

## 1. Explicit Literature Comparison & Formulation Selection

| Formulation | Governing Interface PDE | Density & Viscosity Treatment | Surface Tension Model | Strengths | Weaknesses for Classical & QLBM Pipeline | Selection Decision |
| :--- | :--- | :--- | :--- | :--- | :--- | :---: |
| **Conservative Allen-Cahn Phase-Field** (Fakhari 2017, Watanabe & Hu 2026) | $\partial_t \phi + \nabla \cdot (\phi \mathbf{u}) = \nabla \cdot \left[ M \left(\nabla \phi - \frac{1-4(\phi-0.5)^2}{W}\mathbf{n}\right)\right]$ | Continuous smooth profile $\rho(\phi) = \rho_G + \phi(\rho_L - \rho_G)$, $\nu(\phi) = \nu_G + \phi(\nu_L - \nu_G)$ | Potential / CSF force $\mathbf{F}_s = \sigma \kappa_I \nabla \phi$ or $\mu_\phi \nabla \phi$ | 2nd-order PDE, exact interface width preservation, D2Q9 lattice for both fields, high-density ratio stable | Slight mobility tuning required for diffusion balance | **SELECTED (PRIMARY)** |
| **Cahn-Hilliard Phase-Field** (He 1999, Lee & Lin 2005, Shao 2024) | $\partial_t \phi + \nabla \cdot (\phi \mathbf{u}) = \nabla \cdot (M \nabla \mu_\phi)$, $\mu = 4\beta(\phi^3-\phi) - \kappa \nabla^2 \phi$ | Linear or harmonic interpolation | Chemical potential gradient $\mathbf{F}_s = \mu \nabla \phi$ | Rigorous thermodynamic free energy, mass conservation | 4th-order derivative $\nabla^4 \phi$, higher numerical stiffness, requires larger stencils | Rejected (Overly stiff 4th-order terms) |
| **Volume-of-Fluid (VOF-LBM)** (Scardovelli 1999, Chen 2013) | Geometric advection of volume fraction $C$ | Sharp jump at reconstructed interface | CSF force with curvature $\kappa = \nabla \cdot \mathbf{n}$ | Sharp interface, strict mass conservation | Geometric PLIC reconstruction is non-algebraic; incompatible with Carleman/matrix representations | Rejected (Non-algebraic PLIC) |
| **Free-Surface LBM** (Körner 2005, Bogner 2015) | Bubble/mass tracking across cell conversion flags | Fluid-only simulation (gas neglected) | Laplace pressure boundary condition | Very efficient for open free surfaces | Discontinuous cell state switching (fluid/interface/gas), loses gas-phase impact cushioning | Rejected (Non-differentiable state transitions) |
| **Shan-Chen Pseudopotential** (Shan & Chen 1993, Sbragaglia 2007) | Intermolecular interaction potential $V(\psi)$ | Equation of State (EOS) based | Emergent non-local force $\mathbf{F} = -G \psi(\mathbf{x}) \sum w_i \psi(\mathbf{x}+\mathbf{c}_i)\mathbf{c}_i$ | Simple single-distribution formulation | Spurious currents at high density ratio, non-independent tuning of $\rho_L/\rho_G$ and $\sigma$ | Rejected (Spurious currents & high-ratio instability) |

---

## 2. Full Mathematical Formulation of Selected Primary Model

### A. Governing Macroscopic Equations (Two-Phase Incompressible Navier-Stokes)
1. **Continuity Equation**:
   $$ \nabla \cdot \mathbf{u} = 0 $$
2. **Momentum Equation**:
   $$ \rho(\phi) \left( \frac{\partial \mathbf{u}}{\partial t} + \mathbf{u} \cdot \nabla \mathbf{u} \right) = -\nabla p + \nabla \cdot \left[ \rho(\phi) \nu(\phi) \left(\nabla \mathbf{u} + (\nabla \mathbf{u})^T\right) \right] + \mathbf{F}_s + \mathbf{F}_g + \mathbf{F}_{ext} $$
3. **Conservative Allen-Cahn Interface Capturing Equation**:
   $$ \frac{\partial \phi}{\partial t} + \nabla \cdot (\phi \mathbf{u}) = \nabla \cdot \left[ M \left( \nabla \phi - \frac{1 - 4(\phi - 0.5)^2}{W} \frac{\nabla \phi}{|\nabla \phi|} \right) \right] $$

### B. Property Interpolation
- **Density**:
  $$ \rho(\phi) = \rho_G + \phi (\rho_L - \rho_G) $$
- **Dynamic Viscosity**:
  $$ \mu(\phi) = \rho(\phi) \nu(\phi) = \mu_G + \phi (\mu_L - \mu_G) $$
- **Kinematic Viscosity**:
  $$ \nu(\phi) = \frac{\mu(\phi)}{\rho(\phi)} $$

### C. Surface Tension & Body Forces
- **Surface Tension Force (Continuum Surface Force - CSF)**:
  $$ \mathbf{F}_s = \sigma \kappa_I \nabla \phi = \sigma \left[ -\nabla \cdot \left( \frac{\nabla \phi}{|\nabla \phi|} \right) \right] \nabla \phi $$
  where $\sigma$ is physical surface tension coefficient, and $\kappa_I$ is local interface curvature.
- **Gravitational Body Force**:
  $$ \mathbf{F}_g = (\rho(\phi) - \rho_0) \mathbf{g}_{grav} $$
  where $\rho_0$ is ambient reference density.
- **Total Body Force**:
  $$ \mathbf{F} = \mathbf{F}_s + \mathbf{F}_g $$

---

## 3. Lattice Boltzmann Realization (D2Q9 Velocity-Based Architecture)

### A. Hydrodynamic Distribution $g_i$
- **Equilibrium Distribution**:
  $$ g_i^{eq} = w_i \left[ p^* + \frac{\mathbf{c}_i \cdot \mathbf{u}}{c_s^2} + \frac{(\mathbf{c}_i \cdot \mathbf{u})^2}{2 c_s^4} - \frac{|\mathbf{u}|^2}{2 c_s^2} \right] $$
  where $p^* = \frac{p}{\rho(\phi) c_s^2}$ is the normalized pressure.
- **Collision & Forcing**:
  $$ g_i^{post} = g_i - \frac{1}{\tau_v(\phi)} (g_i - g_i^{eq}) + F_i $$
  where $\tau_v(\phi) = \frac{\nu(\phi)}{c_s^2 \Delta t} + 0.5$, and $F_i$ is the Guo forcing term:
  $$ F_i = \left(1 - \frac{1}{2\tau_v(\phi)}\right) w_i \left[ \frac{(\mathbf{c}_i - \mathbf{u})\cdot \mathbf{F}}{\rho(\phi) c_s^2} + \frac{(\mathbf{c}_i \cdot \mathbf{u})(\mathbf{c}_i \cdot \mathbf{F})}{\rho(\phi) c_s^4} \right] $$
- **Macroscopic Hydrodynamic Moments**:
  $$ p = \rho(\phi) c_s^2 \sum_{i=0}^8 g_i $$
  $$ \mathbf{u} = \sum_{i=0}^8 g_i \mathbf{c}_i + \frac{\Delta t}{2 \rho(\phi)} \mathbf{F} $$

### B. Phase-Field Distribution $h_i$
- **Equilibrium Distribution**:
  $$ h_i^{eq} = w_i \phi \left[ 1 + \frac{\mathbf{c}_i \cdot \mathbf{u}}{c_s^2} \right] $$
- **Interface Normal & Curvature Source Term $S_i$**:
  $$ S_i = w_i \frac{\mathbf{c}_i \cdot \left[ M \left( \nabla \phi - \frac{1 - 4(\phi - 0.5)^2}{W} \mathbf{n} \right) \right]}{c_s^2} $$
- **Collision**:
  $$ h_i^{post} = h_i - \frac{1}{\tau_\phi} (h_i - h_i^{eq}) + S_i $$
  where $\tau_\phi = \frac{M}{c_s^2 \Delta t} + 0.5$.
- **Order Parameter**:
  $$ \phi = \sum_{i=0}^8 h_i $$

---

## 4. Suitability for QLBM & Quantum Bridge
1. **Separation of Linear Streaming**: Spatial advection of both $g_i$ and $h_i$ remains exact linear permutations $\mathbf{S}$.
2. **Controlled Polynomial Expansion**:
   - For constant or low density ratio ($\rho_L/\rho_G \approx 1 \sim 10$), the collision operators are strictly low-degree polynomials.
   - For high density ratios, the velocity-based formulation ensures that the primary advective terms remain quadratic polynomials in $(\mathbf{g}, \mathbf{h})$, with density fractions $\rho(\phi)$ acting as smooth polynomial weighting functions.
