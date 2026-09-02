# PHASE F11: MULTI-PHASE COUPLING & FORCE INTEGRATION
## Buoyancy, Surface Tension (CSF), and Kinematic Viscosity Formulation

**Document**: Multi-Phase Fluid Kinematics & Body-Force Formulation  
**Project**: Quantum Lattice Boltzmann Method (QLBM) for Two-Phase Flow  
**Repository**: `/home/aswa/Research/QLBM-DamBreak-Production`  
**Branch**: `feature/direct-encoding-two-phase-qlbm`  
**Date**: September 2026  

---

## 1. Multi-Phase Equations of State & Fluid Properties

The two-phase fluid mixture density and kinematic viscosity vary linearly with local phase fraction $\alpha(x, y) \in [0, 1]$:

$$\rho(\alpha) = \alpha \rho_L + (1 - \alpha) \rho_G, \quad (\rho_L = 1.0, \ \rho_G = 0.1)$$
$$\nu_{\text{mix}}(\alpha) = \alpha \nu_L + (1 - \alpha) \nu_G, \quad (\nu_L = 0.05, \ \nu_G = 0.05)$$
$$\tau_f(\alpha) = 3 \nu_{\text{mix}}(\alpha) + 0.5, \quad \omega_f(\alpha) = \frac{1}{\tau_f(\alpha)}$$
$$\tau_\phi = 0.70, \quad \omega_g = \frac{1}{\tau_\phi}$$

---

## 2. Force Coupling & Continuum Surface Force (CSF)

$$\mathbf{F}_{\text{total}}(x, y) = \mathbf{F}_{\text{buoyancy}}(x, y) + \mathbf{F}_{\text{CSF}}(x, y)$$

1. **Gravitational Buoyancy Force**:
   $$\mathbf{F}_{\text{buoyancy}} = \begin{bmatrix} 0 \\ (\rho(x, y) - \rho_G) g_{\text{acc}} \end{bmatrix}, \quad (g_{\text{acc}} = -0.0005)$$
2. **Continuum Surface Force (CSF)**:
   $$\mathbf{F}_{\text{CSF}} = \sigma \kappa \nabla \alpha, \quad \kappa = -\nabla \cdot \left(\frac{\nabla \alpha}{|\nabla \alpha|}\right), \quad (\sigma = 0.001)$$

---

## 3. Parameter-Fed Quantum Collision Dilation

The combined local operator $C(\alpha, \mathbf{u}, \mathbf{F}/\rho)$ is dilated via 6-qubit Sz.-Nagy unitary embedding $U_C \in \mathbb{U}(64)$:

$$U_C = \begin{bmatrix} C / \alpha_C & D_* \\ D & -C^\dagger / \alpha_C \end{bmatrix}, \quad \alpha_C \ge \|C\|_2$$

Success probability per node is $p_0 = 1/\alpha_C^2 \approx 0.82$.

---

## 4. Quantum vs Hybrid Classification of CSF & Forcing

> [!IMPORTANT]
> In Phase F11, the calculation of $\nabla \alpha$, interface curvature $\kappa$, and shifted macroscopic velocity $\mathbf{u}$ is explicitly classified as **Hybrid / Classical Macroscopic Feedback**. The populations $f_i, g_i$ are evolved via **quantum-realized streaming ($S_{\text{arith}}$)** and **quantum boundary involution ($B_{\text{mask}}$)**, with parameterized collision executed via unitary dilation ($U_C$).
