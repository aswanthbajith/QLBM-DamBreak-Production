# PHASE F16: MATHEMATICAL MODEL EXTRACTION & CLASSIFICATION
## Formal Classification of All Two-Phase D2Q9 LBM Operations

**Document**: Mathematical Model Extraction & Operation Taxonomy  
**Project**: Quantum Lattice Boltzmann Method (QLBM) for Two-Phase Flow  
**Repository**: `/home/aswa/Research/QLBM-DamBreak-Production`  
**Branch**: `feature/direct-encoding-two-phase-qlbm`  
**Date**: September 2026  

---

## 1. D2Q9 Two-Phase Discrete Population State

At each spatial lattice node $\mathbf{x} = (x, y)$, the local state is:
$$\mathbf{z} = \begin{bmatrix} \mathbf{f} \\ \mathbf{g} \end{bmatrix} \in \mathbb{R}^{18}, \quad f_0 \dots f_8 \text{ (hydrodynamic)}, \ g_0 \dots g_8 \text{ (phase field)}$$

---

## 2. Complete Operation Classification Taxonomy

$$\begin{array}{|l|l|l|l|}
\hline
\textbf{Physical Quantity} & \textbf{Mathematical Definition} & \textbf{Mathematical Class} & \textbf{Quantum Realizability} \\
\hline
\text{Density } \rho & \sum_{i=0}^8 f_i = \mathbf{1}_9^T \mathbf{f} & \textbf{LINEAR} & \text{Exact In-Place Adder} \\
\text{Phase Order } \alpha & \sum_{i=0}^8 g_i = \mathbf{1}_9^T \mathbf{g} & \textbf{LINEAR} & \text{Exact In-Place Adder} \\
\text{Momentum } \mathbf{j} & \sum_{i=0}^8 f_i \mathbf{c}_i & \textbf{LINEAR} & \text{Exact Signed Adder} \\
\text{Fluid Viscosity } \nu(\alpha) & \alpha \nu_L + (1-\alpha)\nu_G & \textbf{LINEAR / AFFINE} & \text{Exact Linear MAC} \\
\text{Relaxation Rate } \omega_f(\alpha) & 1 / (3\nu(\alpha) + 0.5) & \textbf{RATIONAL} & \text{Reversible Divider / Taylor} \\
\text{Fluid Velocity } \mathbf{u} & (\mathbf{j} + \frac{1}{2}\mathbf{F}) / \rho & \textbf{RATIONAL} & \text{Reversible Divider} \\
\text{Velocity Square } |\mathbf{u}|^2 & u_x^2 + u_y^2 & \textbf{QUADRATIC} & \text{Reversible Multiplier} \\
\text{Equilibrium } f_i^{\text{eq}} & w_i \rho [1 + 3\mathbf{c}_i\cdot\mathbf{u} + \frac{9}{2}(\mathbf{c}_i\cdot\mathbf{u})^2 - \frac{3}{2}|\mathbf{u}|^2] & \textbf{QUADRATIC / RATIONAL} & \text{Reversible Polynomial MAC} \\
\text{Equilibrium } g_i^{\text{eq}} & w_i \alpha [1 + 3\mathbf{c}_i\cdot\mathbf{u}] & \textbf{BILINEAR / RATIONAL} & \text{Reversible Bilinear MAC} \\
\text{Guo Forcing } S_i & (1 - \frac{1}{2\tau}) w_i [3\frac{\mathbf{c}_i-\mathbf{u}}{c_s^2} + 9\frac{(\mathbf{c}_i\cdot\mathbf{u})\mathbf{c}_i}{c_s^4}] \cdot \mathbf{F} & \textbf{QUADRATIC} & \text{Reversible MAC} \\
\text{CSF Force } \mathbf{F}_s & \sigma \kappa \nabla \alpha, \quad \kappa = -\nabla \cdot (\nabla\alpha/|\nabla\alpha|) & \textbf{NONLOCAL NON-POLYNOMIAL} & \text{Spatial Stencil Shifts} \\
\text{Spatial Streaming } S_{\text{arith}} & f_i(\mathbf{x}+\mathbf{c}_i) \leftarrow f_i^*(\mathbf{x}) & \textbf{EXACT PERMUTATION} & \text{Unitary Coordinate Wire Swap} \\
\text{Boundary Mask } B_{\text{mask}} & f_{\bar{i}} \leftarrow f_i^* \text{ on solid boundary} & \textbf{EXACT INVOLUTION } (B^2=I) & \text{Unitary Register Swap} \\
\hline
\end{array}$$
