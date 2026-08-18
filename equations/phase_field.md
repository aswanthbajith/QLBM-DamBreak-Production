# Phase-Field Interface Capturing Formulations

## 1. Conservative Allen-Cahn / Cahn-Hilliard Model
The interface order parameter $\phi \in [-1, 1]$ (or $\phi \in [0, 1]$) evolves under advection and diffusion:

### Conservative Allen-Cahn Equation (Chiu & Lin / Geier et al.):
$$
\frac{\partial \phi}{\partial t} + \nabla \cdot (\phi \mathbf{u}) = \nabla \cdot \left[ M \left( \nabla \phi - \frac{\nabla \phi}{|\nabla \phi|} \frac{1 - \phi^2}{W} \right) \right]
$$
where $M$ is interface mobility and $W$ is interface interfacial thickness.

### Classic Cahn-Hilliard Equation:
$$
\frac{\partial \phi}{\partial t} + \nabla \cdot (\phi \mathbf{u}) = \nabla \cdot (M \nabla \mu_{\phi})
$$
where the bulk chemical potential $\mu_{\phi}$ is derived from the Ginzburg-Landau free energy density $\Psi(\phi, \nabla \phi) = \beta (\phi^2 - 1)^2 + \frac{\kappa}{2} |\nabla \phi|^2$:
$$
\mu_{\phi} = \frac{\delta \mathcal{F}}{\delta \phi} = 4 \beta \phi (\phi^2 - 1) - \kappa \nabla^2 \phi = 4 \beta (\phi^3 - \phi) - \kappa \nabla^2 \phi
$$

## 2. Lattice Boltzmann Equation for Phase Field
Let $h_i(\mathbf{x}, t)$ be the phase-field distribution function:
$$
h_i(\mathbf{x} + \mathbf{c}_i \Delta t, t + \Delta t) - h_i(\mathbf{x}, t) = -\frac{1}{\tau_{\phi}} [h_i(\mathbf{x}, t) - h_i^{eq}(\mathbf{x}, t)]
$$
where:
$$
h_i^{eq}(\phi, \mathbf{u}, \mu_{\phi}) = w_i \phi \left( 1 + \frac{\mathbf{c}_i \cdot \mathbf{u}}{c_s^2} \right) + w_i \Gamma_i \mu_{\phi}
$$
The macroscopic phase order parameter is recovered as:
$$
\phi(\mathbf{x}, t) = \sum_{i=0}^{Q-1} h_i(\mathbf{x}, t)
$$
