# PHASE F15: MATHEMATICAL FORMULATION OF TWO-PHASE COLLISION
## Exact Collision Structure, Low-Mach Expansion, and Polynomial Approximation

**Document**: Mathematical Formulation & Low-Mach Derivation  
**Project**: Quantum Lattice Boltzmann Method (QLBM) for Two-Phase Flow  
**Repository**: `/home/aswa/Research/QLBM-DamBreak-Production`  
**Branch**: `feature/direct-encoding-two-phase-qlbm`  
**Date**: September 2026  

---

## 1. Exact Two-Phase LBM Collision Map

At each grid node $\mathbf{x} = (x, y)$, the discrete population state vector is:
$$\mathbf{z} = \begin{bmatrix} \mathbf{f} \\ \mathbf{g} \end{bmatrix} \in \mathbb{R}^{18}$$

The macroscopic moments are strictly linear in $\mathbf{z}$:
$$\rho = \sum_{i=0}^8 f_i = \mathbf{1}_9^T \mathbf{f}, \quad \alpha = \sum_{i=0}^8 g_i = \mathbf{1}_9^T \mathbf{g}, \quad \mathbf{j} = \sum_{i=0}^8 f_i \mathbf{c}_i = C_{\text{vel}} \mathbf{f}$$

The shifted velocity is a **rational function** of $\mathbf{z}$:
$$\mathbf{u} = \frac{\mathbf{j} + \frac{1}{2}\mathbf{F}}{\rho}$$

---

## 2. Controlled Low-Mach Polynomial Expansion

Expanding the rational reciprocal $1/\rho$ around reference density $\rho_0 = 1.0$:
$$\frac{1}{\rho} = \frac{1}{1 + (\rho - 1)} \approx 2 - \rho$$

Substituting into the shifted velocity:
$$\mathbf{u} \approx \left( \mathbf{j} + \frac{1}{2}\mathbf{F} \right) (2 - \rho)$$

The equilibrium distributions become exact quadratic polynomials in $\mathbf{z}$:
$$f_i^{\text{eq}}(\rho, \mathbf{u}) = w_i \rho \left[ 1 + 3\mathbf{c}_i \cdot \mathbf{u} + \frac{9}{2}(\mathbf{c}_i \cdot \mathbf{u})^2 - \frac{3}{2}|\mathbf{u}|^2 \right]$$
$$g_i^{\text{eq}}(\alpha, \mathbf{u}) = w_i \alpha \left[ 1 + 3\mathbf{c}_i \cdot \mathbf{u} \right]$$

Post-collision state:
$$\mathbf{z}^* = M_1 \mathbf{z} + M_2 (\mathbf{z} \otimes \mathbf{z}) + \mathbf{s}_0$$
where $M_1 \in \mathbb{R}^{18 \times 18}$ is the linear collision matrix and $M_2 \in \mathbb{R}^{18 \times 324}$ is the quadratic interaction tensor.
