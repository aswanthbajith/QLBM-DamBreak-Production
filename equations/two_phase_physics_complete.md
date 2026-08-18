# Complete Two-Phase Fluid Physics & Lattice Boltzmann Formulation

**Author**: Lead Numerical Fluid-Dynamics Researcher & Scientific Software Engineer  
**Reference Document**: Mathematical Foundation for Two-Phase Gas-Liquid Dam-Break Simulation  
**Primary Literature Grounding**: Watanabe & Hu (2026), Fakhari et al. (2017), Liang et al. (2014), Geier et al. (2015)  

---

## 1. Dimensional & Lattice Unit Definitions

| Symbol | Description | Physical SI Unit | Lattice Unit (LU) |
| :--- | :--- | :---: | :---: |
| $\Delta x$ | Lattice spatial step | $\text{m}$ | $1.0$ |
| $\Delta t$ | Lattice time step | $\text{s}$ | $1.0$ |
| $c = \Delta x / \Delta t$ | Lattice speed | $\text{m/s}$ | $1.0$ |
| $c_s = 1/\sqrt{3}$ | Speed of sound | $\text{m/s}$ | $1/\sqrt{3} \approx 0.57735$ |
| $\rho_L$ | Liquid phase density | $\text{kg/m}^3$ | $\sim 1.0$ |
| $\rho_G$ | Gas phase density | $\text{kg/m}^3$ | $\sim 0.001 - 0.1$ |
| $\nu_L$ | Liquid kinematic viscosity | $\text{m}^2/\text{s}$ | $0.005 - 0.05$ |
| $\nu_G$ | Gas kinematic viscosity | $\text{m}^2/\text{s}$ | $0.005 - 0.05$ |
| $\sigma$ | Surface tension coefficient | $\text{N/m}$ | $0.001 - 0.01$ |
| $g_y$ | Gravitational acceleration | $\text{m/s}^2$ | $-10^{-4} \text{ to } -10^{-3}$ |
| $W$ | Interface transition thickness | $\text{m}$ | $3.0 - 5.0$ lattice nodes |
| $M$ | Phase-field interface mobility | $\text{m}^2/\text{s}$ | $0.05 - 0.1$ |

---

## 2. Continuum Governing Equations

### A. Interface Capturing: Conservative Allen-Cahn Equation
$$
\frac{\partial \phi}{\partial t} + \nabla \cdot (\phi \mathbf{u}) = \nabla \cdot \left[ M \left( \nabla \phi - \frac{1 - 4(\phi - 0.5)^2}{W} \mathbf{n} \right) \right]
$$
- **Symbols**: $\phi \in [0, 1]$ (order parameter, $\phi=1$ liquid, $\phi=0$ gas), $\mathbf{u} = (u, v)$ (fluid velocity), $M$ (mobility), $W$ (interface width), $\mathbf{n} = \frac{\nabla \phi}{|\nabla \phi| + \epsilon}$ (interface unit normal).
- **Assumptions**: Smooth diffuse interface of equilibrium profile $\phi(z) = 0.5 + 0.5 \tanh(2z/W)$, conservative formulation with zero net mass loss.
- **Source**: Geier et al. (2015), Fakhari et al. (2017), Watanabe & Hu (2026).
- **Nonlinear Terms**: $\phi \mathbf{u}$ (advective flux, degree 2 bilinear), $\phi^2 \mathbf{n}$ (counter-gradient sharpening flux, degree 2 polynomial in $\phi$).

### B. Continuity Equation
$$
\nabla \cdot \mathbf{u} = 0
$$
- **Assumptions**: Incompressible flow in both liquid and gas phases at low Mach number ($\text{Ma} = |\mathbf{u}| / c_s \ll 1$).

### C. Incompressible Two-Phase Momentum Equation
$$
\rho(\phi) \left( \frac{\partial \mathbf{u}}{\partial t} + \mathbf{u} \cdot \nabla \mathbf{u} \right) = -\nabla p + \nabla \cdot \left[ \mu(\phi) \left( \nabla \mathbf{u} + (\nabla \mathbf{u})^T \right) \right] + \mathbf{F}_s + \mathbf{F}_g + \mathbf{F}_{ext}
$$
- **Symbols**: $p$ (macroscopic hydrodynamic pressure), $\rho(\phi)$ (local mixture density), $\mu(\phi) = \rho(\phi)\nu(\phi)$ (local dynamic shear viscosity), $\mathbf{F}_s$ (surface tension force), $\mathbf{F}_g$ (gravity).
- **Nonlinear Terms**: $\mathbf{u} \cdot \nabla \mathbf{u}$ (convective acceleration, quadratic), $\rho(\phi) \mathbf{u} \cdot \nabla \mathbf{u}$ (density-modulated convection), $\mathbf{F}_s$ (surface tension force).

---

## 3. Constitutive Relations & Property Interpolation

### A. Density Model
$$
\rho(\phi) = \rho_G + \phi (\rho_L - \rho_G)
$$
- **Assumptions**: Linear volume-fraction weighted mixture density across diffuse interface.

### B. Dynamic & Kinematic Viscosity Model
$$
\mu(\phi) = \mu_G + \phi (\mu_L - \mu_G) = \rho_G \nu_G + \phi (\rho_L \nu_L - \rho_G \nu_G)
$$
$$
\nu(\phi) = \frac{\mu(\phi)}{\rho(\phi)} = \frac{\mu_G + \phi(\mu_L - \mu_G)}{\rho_G + \phi(\rho_L - \rho_G)}
$$
- **Relaxation Time Relation**:
  $$ \tau_v(\phi) = \frac{\nu(\phi)}{c_s^2 \Delta t} + 0.5 = 3 \nu(\phi) + 0.5 $$

### C. Surface Tension Force Formulation
- **Continuum Surface Force (CSF)**:
  $$ \mathbf{F}_s(\mathbf{x}) = \sigma \kappa_I(\mathbf{x}) \nabla \phi(\mathbf{x}) $$
  where local curvature $\kappa_I$ is:
  $$ \kappa_I = -\nabla \cdot \mathbf{n} = -\nabla \cdot \left( \frac{\nabla \phi}{|\nabla \phi| + \epsilon_{reg}} \right) $$
- **Chemical Potential Alternative Form**:
  $$ \mu_\phi = 4\beta \phi(\phi-1)(\phi-0.5) - \kappa_\sigma \nabla^2 \phi, \quad \mathbf{F}_s = \mu_\phi \nabla \phi $$
  with $\sigma = \frac{\sqrt{2\kappa_\sigma \beta}}{6}$ and $W = \sqrt{\frac{8\kappa_\sigma}{\beta}}$.

### D. Gravitational Body Force
$$
\mathbf{F}_g(\mathbf{x}) = (\rho(\phi) - \rho_G) \mathbf{g}_{grav} = \phi (\rho_L - \rho_G) \mathbf{g}_{grav}
$$
- **Assumptions**: Boussinesq-hydrostatic subtraction of background gas hydrostatic head to minimize spurious gas acceleration.

---

## 4. Discrete Lattice Boltzmann Implementation (D2Q9 Architecture)

### A. Discrete Velocity Vectors $\mathbf{c}_i$ & Lattice Weights $w_i$
$$
\mathbf{c}_i = \begin{bmatrix}
0 & 1 & 0 & -1 & 0 & 1 & -1 & -1 & 1 \\
0 & 0 & 1 & 0 & -1 & 1 & 1 & -1 & -1
\end{bmatrix}, \quad
w_i = \begin{cases}
4/9 & i=0 \\
1/9 & i=1,2,3,4 \\
1/36 & i=5,6,7,8
\end{cases}
$$

### B. Hydrodynamic Evolution Equation (Velocity-Based Formulation)
$$
g_i(\mathbf{x} + \mathbf{c}_i \Delta t, t + \Delta t) = g_i(\mathbf{x}, t) - \frac{1}{\tau_v(\phi)} \left[ g_i(\mathbf{x}, t) - g_i^{eq}(\mathbf{x}, t) \right] + F_i(\mathbf{x}, t)
$$
- **Equilibrium Distribution**:
  $$ g_i^{eq} = w_i \left[ \frac{p}{\rho(\phi) c_s^2} + \frac{\mathbf{c}_i \cdot \mathbf{u}}{c_s^2} + \frac{(\mathbf{c}_i \cdot \mathbf{u})^2}{2 c_s^4} - \frac{|\mathbf{u}|^2}{2 c_s^2} \right] $$
- **Guo Body Forcing Term $F_i$**:
  $$ F_i = \left( 1 - \frac{1}{2\tau_v(\phi)} \right) w_i \left[ \frac{(\mathbf{c}_i - \mathbf{u})\cdot \mathbf{F}}{\rho(\phi) c_s^2} + \frac{(\mathbf{c}_i \cdot \mathbf{u})(\mathbf{c}_i \cdot \mathbf{F})}{\rho(\phi) c_s^4} \right] $$
- **Macroscopic Variables**:
  $$ p = \rho(\phi) c_s^2 \sum_{i=0}^8 g_i $$
  $$ \mathbf{u} = \sum_{i=0}^8 g_i \mathbf{c}_i + \frac{\Delta t}{2 \rho(\phi)} \mathbf{F} $$

### C. Phase-Field Evolution Equation
$$
h_i(\mathbf{x} + \mathbf{c}_i \Delta t, t + \Delta t) = h_i(\mathbf{x}, t) - \frac{1}{\tau_\phi} \left[ h_i(\mathbf{x}, t) - h_i^{eq}(\mathbf{x}, t) \right] + S_i(\mathbf{x}, t)
$$
- **Equilibrium Distribution**:
  $$ h_i^{eq} = w_i \phi \left[ 1 + \frac{\mathbf{c}_i \cdot \mathbf{u}}{c_s^2} \right] $$
- **Normal Sharpening Source Term $S_i$**:
  $$ S_i = \left( 1 - \frac{1}{2\tau_\phi} \right) w_i \frac{\mathbf{c}_i \cdot \mathbf{F}_\phi}{c_s^2}, \quad \mathbf{F}_\phi = M \left( \nabla \phi - \frac{1 - 4(\phi - 0.5)^2}{W} \mathbf{n} \right) $$
- **Macroscopic Order Parameter**:
  $$ \phi = \sum_{i=0}^8 h_i $$

---

## 5. Summary of Nonlinear Terms for Downstream Quantum Analysis

1. **Quadratic Convection**: $(\mathbf{c}_i \cdot \mathbf{u})^2 / (2 c_s^4) - |\mathbf{u}|^2 / (2 c_s^2)$ ($\sim \mathbf{u} \otimes \mathbf{u}$)
2. **Bilinear Phase Advection**: $\phi (\mathbf{c}_i \cdot \mathbf{u}) / c_s^2$ ($\sim \phi \mathbf{u}$)
3. **Bilinear Force Coupling**: $\mathbf{u} \cdot \mathbf{F} / c_s^2$ and $(\mathbf{c}_i \cdot \mathbf{u})(\mathbf{c}_i \cdot \mathbf{F}) / c_s^4$
4. **Interface Normal Sharpening**: $\phi^2 \mathbf{n}$ ($\sim \phi^2$)
5. **Density Modulation**: $\frac{1}{\rho(\phi)}$ (treated as polynomial weighting in low-contrast expansion).
