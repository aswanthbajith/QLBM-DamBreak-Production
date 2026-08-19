# Forensic Nonlinearity Audit & Polynomial Classification Map

**Author**: Lead Mathematical Modeler & Numerical Analyst  
**Date**: August 19, 2026  
**Repository**: `/home/aswa/Research/QLBM-DamBreak/`  

---

## 1. Forensic Operation-by-Operation Classification Table

| Physical / Numerical Operation | Mathematical Expression | Code Location | Affected State Variables | Classification | Polynomial Degree | Exact Polynomial Representation Exists? |
| :--- | :--- | :--- | :--- | :---: | :---: | :---: |
| **1. Spatial Streaming $\mathbf{S}$** | $g_i(\mathbf{x} + \mathbf{c}_i) = g_i^{post}(\mathbf{x})$ | `classical/matrix_two_phase_lbm.py:L74-116` | $\mathbf{g}, \mathbf{h}$ | **LINEAR** | 1 | **YES (Exact Unitary Permutation $\mathbf{S}$)** |
| **2. Wall Bounce-Back Boundaries** | $g_{\bar{i}}(\mathbf{x}_w) = g_i^{post}(\mathbf{x}_w)$ | `classical/matrix_two_phase_lbm.py:L98-107` | $\mathbf{g}, \mathbf{h}$ | **LINEAR** | 1 | **YES (Included in Permutation $\mathbf{S}$)** |
| **3. Linear Collision Relaxation** | $-\frac{1}{\tau}(f_i - f_i^{eq, linear})$ | `classical/matrix_two_phase_lbm.py:L118-158` | $\mathbf{g}, \mathbf{h}$ | **LINEAR** | 1 | **YES (Block-Diagonal Matrix $\mathbf{M}_1$)** |
| **4. Hydrodynamic Convection** | $\frac{w_i}{2 c_s^4} (\mathbf{c}_i \cdot \mathbf{u})^2 - \frac{w_i}{2 c_s^2} |\mathbf{u}|^2$ | `classical/two_phase_lbm.py:L150` | $\mathbf{g} \otimes \mathbf{g}$ | **QUADRATIC** | 2 | **YES (Local Tensor $\mathbf{M}_2$)** |
| **5. Phase Advection Flux** | $\frac{w_i}{c_s^2} \phi (\mathbf{c}_i \cdot \mathbf{u})$ | `classical/phase_field.py:L102` | $\mathbf{h} \otimes \mathbf{g}$ | **BILINEAR / QUADRATIC** | 2 | **YES (Local Tensor $\mathbf{M}_2$)** |
| **6. Counter-Gradient Sharpening** | $\frac{M}{W} (1 - 4(\phi - 0.5)^2) \mathbf{n} = \frac{4M}{W} \phi(1-\phi) \mathbf{n}$ | `classical/phase_field.py:L92` | $\mathbf{h} \otimes \mathbf{h}$ | **QUADRATIC** | 2 | **YES (Quadratic Kernel)** |
| **7. Gravitational Buoyancy** | $(\rho(\phi) - \rho_G) \mathbf{g} = \Delta \rho \phi \mathbf{g}$ | `classical/forcing.py:L37-38` | $\mathbf{h}$ | **LINEAR** | 1 | **YES (Linear Affine Vector)** |
| **8. Guo Forcing Convective Terms** | $(\mathbf{c}_i \cdot \mathbf{u})(\mathbf{c}_i \cdot \mathbf{F})$ | `classical/forcing.py:L72` | $\mathbf{g} \otimes \mathbf{F}$ | **BILINEAR / QUADRATIC** | 2 | **YES (Coupled Quadratic Block)** |
| **9. Variable Density Quotient** | $\frac{1}{\rho(\phi)} = \frac{1}{\rho_G + \phi \Delta \rho}$ | `classical/forcing.py:L63-64` | $\mathbf{h}$ | **RATIONAL** | Non-poly | **YES (Via Kowalski Lifting $\xi = 1/\rho \implies$ Cubic Degree 3)** |
| **10. Interface Unit Normal** | $\mathbf{n} = \frac{\nabla \phi}{\sqrt{\|\nabla \phi\|^2 + \epsilon^2}}$ | `classical/two_phase_physics.py:L122-123` | $\mathbf{h}$ | **ALGEBRAIC / RATIONAL** | Non-poly | **APPROXIMATE (Regularized Fixed Width Stencil)** |
| **11. Phase Order Parameter Clamping** | $\text{clip}(\phi, 0, 1) = \max(0, \min(1, \phi))$ | `classical/phase_field.py:L127` | $\mathbf{h}$ | **PIECEWISE LINEAR** | Piecewise | **SMOOTH ANALYTICAL SATURATION (Tanh)** |

---

## 2. Summary of Polynomial Degree Status
- **Standard Moderate Density Regime ($\rho_L / \rho_G \sim 1 \dots 10$)**: System is **strictly quadratic ($p = 2$)**.
- **Full Variable Density Regime with Auxiliary Lifting ($\xi = 1/\rho$)**: System is **strictly closed cubic ($p = 3$)**.
