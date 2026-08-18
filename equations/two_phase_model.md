# Two-Phase Velocity-Based Lattice Boltzmann Model (Watanabe & Hu Framework)

## 1. Physical Motivation & Decoupling
In large density ratio two-phase systems (e.g. water-air, $\rho_l / \rho_g \approx 800 - 1000$), standard density-based LBM suffers from severe numerical instabilities at interface nodes due to stiff density gradients and parasitic currents.
The velocity-based (or incompressible pressure-velocity) LBM tracks:
1. **Flow Field (Velocity & Pressure)**: Evolution of velocity distribution functions $g_i$ (or $f_i$) where density variation is decoupled from momentum advection.
2. **Interface Field (Phase Field Order Parameter $\phi$)**: Evolution of index distribution functions $h_i$ governing interface advection and surface tension.

## 2. Incompressible Navier-Stokes Evolution for Multiphase Systems
$$
\nabla \cdot \mathbf{u} = 0
$$
$$
\rho(\phi) \left( \frac{\partial \mathbf{u}}{\partial t} + \mathbf{u} \cdot \nabla \mathbf{u} \right) = -\nabla p + \nabla \cdot \left[ \mu(\phi) (\nabla \mathbf{u} + (\nabla \mathbf{u})^T) \right] + \mathbf{F}_s + \mathbf{F}_g
$$
where:
- $\rho(\phi) = \frac{\rho_l + \rho_g}{2} + \frac{\rho_l - \rho_g}{2} \phi$
- $\mu(\phi) = \frac{\mu_l + \mu_g}{2} + \frac{\mu_l - \mu_g}{2} \phi$
- $\mathbf{F}_s = \mu_{\phi} \nabla \phi = (\phi^3 - \phi - \kappa \nabla^2 \phi) \nabla \phi$ (Surface tension force / Korteweg stress)
- $\mathbf{F}_g = (\rho(\phi) - \rho_{ref}) \mathbf{g}$ (Gravity / buoyancy body force)

## 3. Hydrodynamic Distribution Function Evolution
$$
g_i(\mathbf{x} + \mathbf{c}_i \Delta t, t + \Delta t) - g_i(\mathbf{x}, t) = -\frac{1}{\tau_v(\phi)} [g_i(\mathbf{x}, t) - g_i^{eq}(\mathbf{x}, t)] + \Delta t \, F_i^{(g)}(\mathbf{x}, t)
$$
where the velocity-based equilibrium $g_i^{eq}$ is formulated directly in terms of kinematic pressure $p^* = p / \rho(\phi)$ and velocity $\mathbf{u}$:
$$
g_i^{eq} = w_i p^* + w_i \left[ \frac{\mathbf{c}_i \cdot \mathbf{u}}{c_s^2} + \frac{(\mathbf{c}_i \cdot \mathbf{u})^2}{2 c_s^4} - \frac{\mathbf{u} \cdot \mathbf{u}}{2 c_s^2} \right] \quad (i > 0)
$$
$$
g_0^{eq} = (w_0 - 1) p^* + w_0 \left[ -\frac{\mathbf{u} \cdot \mathbf{u}}{2 c_s^2} \right]
$$

## 4. Macroscopic Velocity and Pressure Recovery
$$
\mathbf{u}(\mathbf{x}, t) = \sum_{i=0}^{Q-1} g_i(\mathbf{x}, t) \mathbf{c}_i + \frac{\Delta t}{2 \rho(\phi)} \mathbf{F}_{total}
$$
$$
p^*(\mathbf{x}, t) = \sum_{i=0}^{Q-1} g_i(\mathbf{x}, t) + \frac{\Delta t}{2} (\mathbf{u} \cdot \nabla \ln \rho(\phi))
$$
