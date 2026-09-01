# REDUCED TWO-PHASE LATTICE BOLTZMANN DAM-BREAK MODEL SPECIFICATION

**Date**: 2026-08-25  
**Author**: Lead Quantum-CFD Implementation Specialist  
**Repository**: `/home/aswa/Research/QLBM-DamBreak/`  

---

## 1. Governing Physical Model & Philosophy

To formulate a reduced, quantum-representable, and physically consistent two-phase model, we adopt a **Coupled Hydrodynamic-Phase Field Lattice Boltzmann Model** on the standard 2D nine-velocity ($D2Q9$) lattice.

The system is defined by two continuous fields:
1. **Order Parameter (Phase Field) $\phi(x, y, t) \in [0, 1]$**:
   * $\phi = 1$: Pure liquid phase (e.g., water, $\rho_l = 1.0$)
   * $\phi = 0$: Pure gas phase (e.g., air, $\rho_g = 0.1$)
   * $0 < \phi < 1$: Diffuse interface layer of finite thickness $W$.
2. **Hydrodynamic Momentum Field $\rho u(x, y, t)$**:
   * Couples macroscopic fluid velocity $u = (u_x, u_y)$ to phase-dependent density $\rho(\phi)$ and downward gravity $F_g$.

---

## 2. Mathematical Equations

### 2.1 Macroscopic Phase & Momentum Evolution
The continuous governing equations in the incompressible / low Mach limit are:
$$\frac{\partial \phi}{\partial t} + \nabla \cdot (\phi u) = M \nabla^2 \mu_\phi$$
$$\frac{\partial (\rho u)}{\partial t} + \nabla \cdot (\rho u \otimes u) = -\nabla p + \nabla \cdot \left[ \mu (\nabla u + (\nabla u)^T) \right] + F_g + F_s$$

where:
* $M$ is the interface mobility parameter.
* $\mu_\phi$ is the chemical potential.
* $\mu(\phi) = \phi \mu_l + (1-\phi) \mu_g$ is dynamic viscosity.
* $F_g = (0, -g (\rho - \rho_g))^T$ is the buoyancy-corrected gravitational body force.
* $F_s = \mu_\phi \nabla \phi$ is the Korteweg interfacial surface tension force.

### 2.2 Discrete LBM Kinetic Formulation
The kinetic system employs two sets of discrete distribution functions $\{f_i\}_{i=0}^8$ and $\{g_i\}_{i=0}^8$ on the D2Q9 lattice:

1. **Phase Field Kinetics ($g_i$)**:
   $$g_i(x + c_i \Delta t, t + \Delta t) = g_i^*(x, t) = g_i(x, t) - \frac{1}{\tau_\phi} \left( g_i(x, t) - g_i^{\text{eq}}(x, t) \right)$$
   $$g_i^{\text{eq}}(\phi, u) = w_i \phi \left[ 1 + \frac{c_i \cdot u}{c_s^2} \right]$$
   $$\phi(x, t) = \sum_{i=0}^8 g_i(x, t)$$

2. **Hydrodynamic Kinetics ($f_i$)**:
   $$f_i(x + c_i \Delta t, t + \Delta t) = f_i^*(x, t) = f_i(x, t) - \frac{1}{\tau_f} \left( f_i(x, t) - f_i^{\text{eq}}(x, t) \right) + S_i(F_g)$$
   $$f_i^{\text{eq}}(\rho, u) = w_i \rho \left[ 1 + \frac{c_i \cdot u}{c_s^2} + \frac{(c_i \cdot u)^2}{2 c_s^4} - \frac{u \cdot u}{2 c_s^2} \right]$$
   $$\rho(x, t) = \sum_{i=0}^8 f_i(x, t), \quad \rho u(x, t) = \sum_{i=0}^8 c_i f_i(x, t) + \frac{\Delta t}{2} F_g$$

3. **Guo Forcing Source Term $S_i(F)$**:
   $$S_i(F) = \left( 1 - \frac{1}{2 \tau_f} \right) w_i \left[ \frac{c_i - u}{c_s^2} + \frac{c_i \cdot u}{c_s^4} c_i \right] \cdot F$$

---

## 3. Material Properties & Linear Mixture Rule

The physical properties of the two immiscible fluid phases are explicitly specified:

| Parameter | Symbol | Liquid Phase | Gas Phase | Mixture Relation |
| :--- | :--- | :--- | :--- | :--- |
| **Density** | $\rho$ | $\rho_l = 1.0$ | $\rho_g = 0.1$ | $\rho(\phi) = \phi \rho_l + (1-\phi) \rho_g$ |
| **Kinematic Viscosity** | $\nu$ | $\nu_l = 0.10$ | $\nu_g = 0.05$ | $\nu(\phi) = \phi \nu_l + (1-\phi) \nu_g$ |
| **Relaxation Time** | $\tau_f$ | $\tau_l = 3\nu_l + 0.5 = 0.8$ | $\tau_g = 3\nu_g + 0.5 = 0.65$ | $\tau_f(\phi) = \phi \tau_l + (1-\phi) \tau_g$ |
| **Phase Relaxation** | $\tau_\phi$ | $\tau_\phi = 0.70$ | $\tau_\phi = 0.70$ | Uniform mobility $M = c_s^2 (\tau_\phi - 0.5)$ |
| **Lattice Sound Speed** | $c_s$ | $c_s = 1/\sqrt{3}$ | $c_s = 1/\sqrt{3}$ | $c_s^2 = 1/3$ (lattice constant) |
| **Gravity Acceleration** | $g$ | $g = 0.001$ | $g = 0.001$ | Direction: $-\hat{y}$ |

### Scientific Note on Density Mixture Rule:
The linear relation $\rho(\phi) = \phi \rho_l + (1 - \phi) \rho_g$ is standard in diffuse-interface phase-field formulations with moderate density ratios ($\rho_l / \rho_g \approx 10$). For extreme density ratios ($\rho_l / \rho_g \sim 1000$), conservative weighted formulations (such as Inamuro or Fakhari) are required. In our reduced proof-of-concept quantum solver, $\rho_l/\rho_g = 10$ provides clean numerical stability while maintaining true two-phase hydrodynamics.

---

## 4. Boundary Conditions

Solid walls (bottom, top, left, right) are modeled with **Half-Way Bounce-Back**:
$$f_{\bar{i}}(x_b, t + \Delta t) = f_i^*(x_b, t)$$
$$g_{\bar{i}}(x_b, t + \Delta t) = g_i^*(x_b, t)$$
where $\bar{i} = \text{OPPOSITE}[i]$ denotes the reversed velocity vector ($c_{\bar{i}} = -c_i$).

This ensures strict no-slip velocity ($u=0$) on all solid enclosure walls and exact mass conservation for both fluid phases.

---

## 5. Explicit Identification of Model Approximations

1. **Low Mach Approximation**: The BGK equilibrium expansion assumes $|u|/c_s \ll 1$ ($Ma < 0.1$).
2. **Diffuse Interface**: The interface between liquid and gas has finite width $W \approx 1-2$ lattice spacings.
3. **Density Ratio**: Fixed at $\rho_l / \rho_g = 10$ to ensure linear Carleman stability.
4. **Isothermal**: Thermal fluctuations and energy equations are decoupled.
