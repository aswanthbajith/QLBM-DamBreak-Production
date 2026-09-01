# MATHEMATICAL SPECIFICATION OF THE TWO-PHASE LBM MODEL & CODE MAPPING

**Date**: 2026-08-25  
**Author**: Lead Quantum-CFD Algorithm Engineer & Verification Specialist  
**Repository**: `/home/aswa/Research/QLBM-DamBreak/`  

---

## 1. Mathematical Formulation

### 1.1 Lattice Kinematics & Discrete Velocities (D2Q9)
The discrete velocity set $\{c_i\}_{i=0}^8$ and lattice weights $\{w_i\}_{i=0}^8$ for the 2D nine-velocity lattice are:
$$c_0 = (0, 0)$$
$$c_1 = (1, 0), \quad c_2 = (0, 1), \quad c_3 = (-1, 0), \quad c_4 = (0, -1)$$
$$c_5 = (1, 1), \quad c_6 = (-1, 1), \quad c_7 = (-1, -1), \quad c_8 = (1, -1)$$

$$w_0 = \frac{4}{9}, \quad w_{1..4} = \frac{1}{9}, \quad w_{5..8} = \frac{1}{36}$$
$$c_s^2 = \frac{1}{3}, \quad \bar{i} = \text{OPPOSITE}[i] = [0, 3, 4, 1, 2, 7, 8, 5, 6]$$

* **Code Location**: [`classical/d2q9.py:10-25`](file:///home/aswa/Research/QLBM-DamBreak/classical/d2q9.py#L10-L25)

---

### 1.2 Two-Phase State Variables & Macroscopic Fields
The state is described by two kinetic distribution sets $\{f_i(x, y, t)\}_{i=0}^8$ and $\{g_i(x, y, t)\}_{i=0}^8$:
1. **Order Parameter (Phase Field) $\phi(x, y, t) \in [0, 1]$**:
   $$\phi(x, y, t) = \sum_{i=0}^8 g_i(x, y, t)$$
   * $\phi = 1$: Pure liquid phase ($\rho_l = 1.0$)
   * $\phi = 0$: Pure gas phase ($\rho_g = 0.1$)
   * $0 < \phi < 1$: Diffuse interface layer.
   * **Code Location**: [`classical/two_phase.py:39-44`](file:///home/aswa/Research/QLBM-DamBreak/classical/two_phase.py#L39-L44)

2. **Macroscopic Fluid Density $\rho(x, y, t)$**:
   $$\rho(x, y, t) = \sum_{i=0}^8 f_i(x, y, t)$$
   * **Code Location**: [`classical/two_phase.py:47-50`](file:///home/aswa/Research/QLBM-DamBreak/classical/two_phase.py#L47-L50)

3. **Macroscopic Fluid Velocity $u(x, y, t) = (u_x, u_y)$**:
   $$\rho u(x, y, t) = \sum_{i=0}^8 c_i f_i(x, y, t) \implies u(x, y, t) = \frac{\sum_{i=0}^8 c_i f_i(x, y, t)}{\rho(x, y, t)}$$
   * **Code Location**: [`classical/two_phase.py:53-59`](file:///home/aswa/Research/QLBM-DamBreak/classical/two_phase.py#L53-L59)

4. **Linear Mixture Equations**:
   $$\rho(\phi) = \phi \rho_l + (1 - \phi) \rho_g$$
   $$\nu(\phi) = \phi \nu_l + (1 - \phi) \nu_g, \quad \tau_f(\phi) = 3\nu(\phi) + \frac{1}{2}$$
   * **Code Location**: [`classical/two_phase.py:26`](file:///home/aswa/Research/QLBM-DamBreak/classical/two_phase.py#L26)

---

### 1.3 Equilibrium Distributions
1. **Hydrodynamic Equilibrium $f_i^{\text{eq}}(\rho, u)$**:
   $$f_i^{\text{eq}}(\rho, u) = w_i \rho \left[ 1 + \frac{c_i \cdot u}{c_s^2} + \frac{(c_i \cdot u)^2}{2 c_s^4} - \frac{u \cdot u}{2 c_s^2} \right]$$
   * **Code Location**: [`classical/equilibrium.py:10-25`](file:///home/aswa/Research/QLBM-DamBreak/classical/equilibrium.py#L10-L25)

2. **Order-Parameter Equilibrium $g_i^{\text{eq}}(\phi, u)$**:
   $$g_i^{\text{eq}}(\phi, u) = w_i \phi \left[ 1 + \frac{c_i \cdot u}{c_s^2} \right]$$
   * **Code Location**: [`classical/two_phase.py:32-35`](file:///home/aswa/Research/QLBM-DamBreak/classical/two_phase.py#L32-L35), [`classical/two_phase.py:70-72`](file:///home/aswa/Research/QLBM-DamBreak/classical/two_phase.py#L70-L72)

---

### 1.4 Collision Operators & Body Forcing
1. **Phase Field Relaxation**:
   $$g_i^*(x, t) = g_i(x, t) - \frac{1}{\tau_g} \left( g_i(x, t) - g_i^{\text{eq}}(\phi, u) \right)$$
   * **Code Location**: [`classical/two_phase.py:68-73`](file:///home/aswa/Research/QLBM-DamBreak/classical/two_phase.py#L68-L73)

2. **Hydrodynamic Collision with Gravitational Buoyancy**:
   $$f_i^*(x, t) = f_i(x, t) - \frac{1}{\tau_f} \left( f_i(x, t) - f_i^{\text{eq}}(\rho, u) \right) + S_i(F_g)$$
   where downward gravitational buoyancy force is $F_g = (0, -g (\rho - \rho_g))^T$ and Guo source term is:
   $$S_i(F_g) = \left( 1 - \frac{1}{2\tau_f} \right) w_i \left[ \frac{c_i - u}{c_s^2} + \frac{c_i \cdot u}{c_s^4} c_i \right] \cdot F_g$$
   * **Code Location**: [`classical/two_phase.py:75-86`](file:///home/aswa/Research/QLBM-DamBreak/classical/two_phase.py#L75-L86)

---

### 1.5 Spatial Streaming & Wall Boundary Conditions
1. **Periodic Streaming**:
   $$f_i^{\text{stream}}(x + c_i \Delta t, y + c_i \Delta t) = f_i^*(x, y, t)$$
   $$g_i^{\text{stream}}(x + c_i \Delta t, y + c_i \Delta t) = g_i^*(x, y, t)$$
   * **Code Location**: [`classical/streaming.py:10-20`](file:///home/aswa/Research/QLBM-DamBreak/classical/streaming.py#L10-L20)

2. **Half-Way Bounce-Back Wall Enclosure**:
   For any solid perimeter wall node $(x_b, y_b) \in \partial \Omega$:
   $$f_{\bar{i}}(x_b, y_b, t + \Delta t) = f_i^*(x_b, y_b, t)$$
   $$g_{\bar{i}}(x_b, y_b, t + \Delta t) = g_i^*(x_b, y_b, t)$$
   * **Code Location**: [`classical/boundary.py:13-35`](file:///home/aswa/Research/QLBM-DamBreak/classical/boundary.py#L13-L35)
