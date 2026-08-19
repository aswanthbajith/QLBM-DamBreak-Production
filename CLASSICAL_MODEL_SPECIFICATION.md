# Master Classical Two-Phase Model Specification

**Author**: Lead CFD Physics Engineer & Numerical Analyst  
**Date**: August 19, 2026  
**Repository**: `/home/aswa/Research/QLBM-DamBreak/`  

---

## 1. Physical Classification
The physical model implemented in this repository is:
**Coupled Incompressible Velocity-Based D2Q9 Lattice Boltzmann Method with Conservative Allen-Cahn Phase-Field Interface Capturing, Variable Density, Variable Viscosity, Continuum Surface Force (CSF), and Gravitational Buoyancy.**

### Component Implementation Verification Table

| Component | Implemented? | Governing Equation | Primary Code Location | Verification Status |
| :--- | :---: | :--- | :--- | :---: |
| **Incompressible Navier-Stokes** | **YES** | $\nabla \cdot \mathbf{u} = 0$, $\rho(\phi) [\frac{\partial \mathbf{u}}{\partial t} + \mathbf{u}\cdot\nabla\mathbf{u}] = -\nabla p + \nabla \cdot [\mu(\phi)(\nabla\mathbf{u} + (\nabla\mathbf{u})^T)] + \mathbf{F}_s + \mathbf{F}_g$ | `classical/two_phase_lbm.py:TwoPhaseLBM2D` | **VERIFIED** |
| **Phase-Field Interface Model** | **YES** | Conservative Allen-Cahn: $\frac{\partial \phi}{\partial t} + \nabla \cdot (\phi \mathbf{u}) = \nabla \cdot [M(\nabla \phi - \frac{1-4(\phi-0.5)^2}{W} \mathbf{n})]$ | `classical/phase_field.py:PhaseFieldLBM2D` | **VERIFIED** |
| **Variable Density** | **YES** | $\rho(\phi) = \rho_G + \phi(\rho_L - \rho_G)$ with $\rho_L / \rho_G = 10.0$ | `classical/two_phase_physics.py:density` | **VERIFIED** |
| **Variable Viscosity** | **YES** | $\mu(\phi) = \mu_G + \phi(\mu_L - \mu_G)$, $\tau_v(\phi) = 3 \mu(\phi)/\rho(\phi) + 0.5$ | `classical/two_phase_physics.py:dynamic_viscosity` | **VERIFIED** |
| **Surface Tension (CSF)** | **YES** | $\mathbf{F}_s = \sigma \kappa_I \nabla \phi$, $\kappa = -\nabla \cdot (\nabla \phi / |\nabla \phi|_\epsilon)$ | `classical/two_phase_physics.py:compute_curvature_and_csf` | **VERIFIED** |
| **Gravitational Buoyancy** | **YES** | $\mathbf{F}_g = (\rho(\phi) - \rho_G) \mathbf{g}_{grav}$ | `classical/forcing.py:compute_total_force` | **VERIFIED** |
| **Discrete Guo Body Forcing** | **YES** | $F_i = (1 - \frac{1}{2\tau_v}) w_i [\frac{(\mathbf{c}_i - \mathbf{u})\cdot \mathbf{F}}{\rho c_s^2} + \frac{(\mathbf{c}_i \cdot \mathbf{u})(\mathbf{c}_i \cdot \mathbf{F})}{\rho c_s^4}]$ | `classical/forcing.py:compute_guo_force_term` | **VERIFIED** |
| **Volume-of-Fluid (VOF)** | **NO** | Geometric PLIC interface reconstruction | N/A (Excluded by design in favor of Phase-Field) | **NOT IMPLEMENTED (BY DESIGN)** |
| **Cahn-Hilliard 4th-Order** | **NO** | $\frac{\partial \phi}{\partial t} + \nabla \cdot (\phi \mathbf{u}) = \nabla \cdot (M \nabla \mu_{ch})$ | N/A (Excluded in favor of 2nd-order Allen-Cahn) | **NOT IMPLEMENTED (BY DESIGN)** |

---

## 2. Discrete Two-Phase D2Q9 Architecture

### Lattice Velocity Vectors & Isotropic Weights:
$$ \mathbf{c}_i = \begin{bmatrix} 0 & 1 & 0 & -1 & 0 & 1 & -1 & -1 & 1 \\ 0 & 0 & 1 & 0 & -1 & 1 & 1 & -1 & -1 \end{bmatrix}, \quad w_i = \begin{cases} 4/9 & i=0 \\ 1/9 & i=1..4 \\ 1/36 & i=5..8 \end{cases} $$

### Hydrodynamic Distribution Function $g_i$:
$$ g_i(\mathbf{x} + \mathbf{c}_i \Delta t, t + \Delta t) = g_i(\mathbf{x}, t) - \frac{1}{\tau_v(\phi)} [g_i(\mathbf{x}, t) - g_i^{eq}(\mathbf{x}, t)] + F_i(\mathbf{x}, t) \Delta t $$
$$ g_i^{eq} = w_i \left[ \frac{p}{\rho(\phi) c_s^2} + \frac{\mathbf{c}_i \cdot \mathbf{u}}{c_s^2} + \frac{(\mathbf{c}_i \cdot \mathbf{u})^2}{2 c_s^4} - \frac{|\mathbf{u}|^2}{2 c_s^2} \right] $$

### Phase-Field Distribution Function $h_i$:
$$ h_i(\mathbf{x} + \mathbf{c}_i \Delta t, t + \Delta t) = h_i(\mathbf{x}, t) - \frac{1}{\tau_\phi} [h_i(\mathbf{x}, t) - h_i^{eq}(\mathbf{x}, t)] + S_i(\mathbf{x}, t) \Delta t $$
$$ h_i^{eq} = w_i \phi \left[ 1 + \frac{\mathbf{c}_i \cdot \mathbf{u}}{c_s^2} \right], \quad S_i = \left(1 - \frac{1}{2\tau_\phi}\right) w_i \frac{\mathbf{c}_i \cdot \mathbf{F}_\phi}{c_s^2} $$

### Macroscopic Field Reconstruction:
$$ \phi = \sum_{i=0}^8 h_i, \quad p = \rho(\phi) c_s^2 \sum_{i=0}^8 g_i, \quad \mathbf{u} = \sum_{i=0}^8 g_i \mathbf{c}_i + \frac{\Delta t}{2 \rho(\phi)} \mathbf{F} $$

---

## 3. Production Dam-Break Simulation Parameters

| Parameter | Symbol | Dimensional / Lattice Value | Description |
| :--- | :---: | :---: | :--- |
| **Grid Resolution** | $N_x \times N_y$ | $300 \times 100$ nodes | 2D rectangular confinement tank |
| **Liquid Column Width** | $a$ | $45$ lattice units | Initial column width |
| **Liquid Column Height**| $b$ | $45$ lattice units | Initial column height (Aspect ratio $a/b = 1.0$) |
| **Liquid Density** | $\rho_L$ | $1.00$ LU | Heavy fluid phase |
| **Gas Density** | $\rho_G$ | $0.10$ LU | Light ambient phase (Density ratio $10:1$) |
| **Liquid Kinematic Viscosity** | $\nu_L$ | $0.005$ LU | Liquid momentum diffusion |
| **Gas Kinematic Viscosity** | $\nu_G$ | $0.010$ LU | Gas momentum diffusion |
| **Surface Tension** | $\sigma$ | $0.001$ LU | Interfacial surface tension coefficient |
| **Gravity Acceleration** | $g_y$ | $-4.0 \times 10^{-4}$ LU | Downward vertical acceleration |
| **Interface Thickness** | $W$ | $3.5$ lattice units | Numerical diffuse interface width |
| **Phase Mobility** | $M$ | $0.05$ LU | Allen-Cahn interface mobility |
| **Total Timesteps** | $N_{steps}$ | $2,200$ | Physical collapse time horizon ($t^* \approx 6.56$) |
| **Reynolds Number** | $\text{Re} = \frac{\sqrt{g b} b}{\nu_L}$ | $\approx 450$ | Laminar lattice hydrodynamic regime |
| **Froude Number** | $\text{Fr} = \frac{U}{\sqrt{g b}}$ | $\sim 1.0$ | Gravitational collapse regime |
| **Weber Number** | $\text{We} = \frac{\rho_L g b^2}{\sigma}$ | $\approx 810$ | Inertia-dominated free-surface flow |
