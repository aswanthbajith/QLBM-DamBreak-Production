# PHASE F20: EXACT CLASSICAL COLLISION REFERENCE

## 1. Scope and Purpose
This document specifies the exact classical collision operator reconstructed directly from the high-fidelity reference solver [`classical/level4_two_phase.py`](file:///home/aswa/Research/QLBM-DamBreak-Production/classical/level4_two_phase.py) and the frozen hybrid baseline [`quantum/level6b_hybrid_solver.py`](file:///home/aswa/Research/QLBM-DamBreak-Production/quantum/level6b_hybrid_solver.py).

The exact discrete map is defined as:
$$F_{\text{LBM}}: (f_i, g_i) \mapsto (f_i^*, g_i^*), \quad i \in \{0, \dots, 8\}$$
where $f_i$ represents the weakly-compressible hydrodynamic distribution and $g_i$ represents the conservative phase-field interface distribution.

---

## 2. Mathematical Definition of the Classical Map

### 2.1 Macroscopic Moments
At each lattice node $\mathbf{x} = (x, y)$:
$$\rho = \sum_{i=0}^8 f_i, \qquad \alpha = \text{clip}\left(\sum_{i=0}^8 g_i, 0.0, 1.0\right)$$
where $\alpha \in [0, 1]$ is the liquid phase fraction ($\alpha=1$ liquid, $\alpha=0$ gas).

To prevent division-by-zero singularities in the low-density gas phase:
$$\rho_{\text{safe}} = \max(\rho, \rho_G)$$

### 2.2 Shifted Hydrodynamic Velocity
The shifted fluid velocity incorporating half the external body force $\mathbf{F} = (F_x, F_y)^T$ is:
$$u_x = \frac{1}{\rho_{\text{safe}}} \left( \sum_{i=0}^8 c_{ix} f_i + \frac{1}{2} F_x \right), \qquad u_y = \frac{1}{\rho_{\text{safe}}} \left( \sum_{i=0}^8 c_{iy} f_i + \frac{1}{2} F_y \right)$$

To preserve low-Mach weakly-compressible stability, a physical velocity limiter is applied:
$$u_{\text{mag}} = \sqrt{u_x^2 + u_y^2}, \qquad \text{scale} = \min\left(1.0, \frac{u_{\text{max}}}{u_{\text{mag}} + 10^{-12}}\right) \quad \text{with } u_{\text{max}} = 0.15$$
$$\mathbf{u} \leftarrow \mathbf{u} \cdot \text{scale}$$

### 2.3 Phase-Coupled Relaxation Parameters
The local kinematic viscosity is interpolated linearly across the interface:
$$\nu(\alpha) = \alpha \nu_L + (1 - \alpha) \nu_G$$
$$\tau_f = 3 \nu(\alpha) + 0.5, \qquad \omega_f = \frac{1}{\tau_f}$$
$$\tau_g = \tau_\phi = 0.7, \qquad \omega_g = \frac{1}{\tau_g} \approx 1.42857$$

### 2.4 Equilibrium Distributions
For D2Q9 lattice velocities $\mathbf{c}_i \in \{0, \pm 1\}^2$ and lattice weights $w_0 = 4/9$, $w_{1..4} = 1/9$, $w_{5..8} = 1/36$:
$$f_i^{\text{eq}}(\rho, \mathbf{u}) = w_i \rho \left[ 1 + 3(\mathbf{c}_i \cdot \mathbf{u}) + \frac{9}{2}(\mathbf{c}_i \cdot \mathbf{u})^2 - \frac{3}{2}\mathbf{u}^2 \right]$$
$$g_i^{\text{eq}}(\alpha, \mathbf{u}) = w_i \alpha \left[ 1 + 3(\mathbf{c}_i \cdot \mathbf{u}) \right]$$

### 2.5 Guo Second-Order External Body Forcing
The Guo forcing term $S_i$ accounts for discrete lattice effects:
$$S_i = \left(1 - \frac{1}{2}\omega_f\right) w_i \left[ 3(\mathbf{c}_i \cdot \mathbf{F}) + 9(\mathbf{c}_i \cdot \mathbf{u})(\mathbf{c}_i \cdot \mathbf{F}) - 3(\mathbf{u} \cdot \mathbf{F}) \right]$$
where the total force $\mathbf{F} = \mathbf{F}_{\text{buoyancy}} + \mathbf{F}_{\text{CSF}}$ consists of:
- Gravitational buoyancy: $\mathbf{F}_{\text{buoyancy}} = (0, (\rho - \rho_G) g_{\text{acc}})^T$
- Continuum Surface Force: $\mathbf{F}_{\text{CSF}} = \sigma \kappa \nabla \alpha$

### 2.6 Local BGK Collision Operator
$$f_i^* = f_i - \omega_f (f_i - f_i^{\text{eq}}(\rho, \mathbf{u})) + S_i$$
$$g_i^* = g_i - \omega_g (g_i - g_i^{\text{eq}}(\alpha, \mathbf{u}))$$

---

## 3. Finite-Precision and Saturation Boundaries
In the digital and quantum fixed-point implementations (such as $Q4.12$ and $Q4.16$):
1. **Saturation**: Values exceeding representation ranges are clamped.
2. **Positivity Guard**: Populations satisfying $f_i^* < 0$ or $g_i^* < 0$ are clamped to $0$ to prevent negative density emergence.
3. **Mass Conservation Correction**: Any truncation error in $\sum f_i^*$ is restored by redistributing residuals onto the rest population $f_0$.

This exact classical map forms the target benchmark for all quantum channel derivations.
