# Mathematical Polynomial Formulation of the Two-Phase Discrete LBM

**Author**: Lead Mathematical Modeler & Numerical Analyst  
**Date**: August 19, 2026  
**Repository**: `/home/aswa/Research/QLBM-DamBreak/`  

---

## 1. Complete Global Discrete Time-Step Equation

The discrete evolution of the global state $\mathbf{\Psi}(t) \in \mathbb{R}^{18 N}$ is expressed as:

$$ \mathbf{\Psi}(t+1) = \mathbf{F}(\mathbf{\Psi}(t)) = \mathbf{S} \cdot \left[ \mathbf{M}_1 \mathbf{\Psi}(t) + \mathbf{M}_2 (\mathbf{\Psi}(t) \otimes_{local} \mathbf{\Psi}(t)) + \mathbf{b}_{force} \right] $$

where:
- $\mathbf{S} \in \{0, 1\}^{18N \times 18N}$: Exact unitary spatial streaming and wall reflection permutation matrix ($\mathbf{S}^T \mathbf{S} = \mathbf{I}$).
- $\mathbf{M}_1 \in \mathbb{R}^{18N \times 18N}$: Block-diagonal linear collision relaxation matrix.
- $\mathbf{M}_2 \in \mathbb{R}^{18N \times 324N}$: Block-diagonal quadratic contraction tensor for local convective ($\mathbf{u} \otimes \mathbf{u}$) and advective ($\phi \mathbf{u}$) fluxes.
- $\mathbf{b}_{force} \in \mathbb{R}^{18N}$: Affine constant body force vector.

---

## 2. Derivation of Equilibrium Distribution Polynomial Structure

For D2Q9 velocity-based hydrodynamics, the equilibrium distribution $g_i^{eq}$ is:
$$ g_i^{eq}(\mathbf{x}, t) = w_i \left[ \frac{p}{\rho_0 c_s^2} + \frac{\mathbf{c}_i \cdot \mathbf{u}}{c_s^2} + \frac{(\mathbf{c}_i \cdot \mathbf{u})^2}{2 c_s^4} - \frac{|\mathbf{u}|^2}{2 c_s^2} \right] $$

Substituting the state expansion $\mathbf{u}(\mathbf{x}) = \frac{1}{\rho_0} \sum_{q=0}^8 g_q(\mathbf{x}) \mathbf{c}_q$:
$$ g_i^{eq}(\mathbf{x}) = w_i \left[ \sum_{q=0}^8 g_q + \frac{1}{\rho_0 c_s^2} \sum_{q=0}^8 (\mathbf{c}_i \cdot \mathbf{c}_q) g_q + \frac{1}{2 \rho_0^2 c_s^4} \sum_{q_1, q_2} (\mathbf{c}_i \cdot \mathbf{c}_{q1})(\mathbf{c}_i \cdot \mathbf{c}_{q2}) g_{q1} g_{q2} - \frac{1}{2 \rho_0^2 c_s^2} \sum_{q_1, q_2} (\mathbf{c}_{q1} \cdot \mathbf{c}_{q2}) g_{q1} g_{q2} \right] $$

- Linear in $g_q$: $\sum_q w_i [ 1 + \frac{\mathbf{c}_i \cdot \mathbf{c}_q}{\rho_0 c_s^2} ] g_q$ $\implies$ **Degree 1**
- Quadratic in $g_{q1} g_{q2}$: $\sum_{q1, q2} \frac{w_i}{2 \rho_0^2 c_s^2} \left[ \frac{(\mathbf{c}_i \cdot \mathbf{c}_{q1})(\mathbf{c}_i \cdot \mathbf{c}_{q2})}{c_s^2} - (\mathbf{c}_{q1} \cdot \mathbf{c}_{q2}) \right] g_{q1} g_{q2}$ $\implies$ **Degree 2**

For phase-field distribution $h_i^{eq}$:
$$ h_i^{eq}(\mathbf{x}) = w_i \phi \left[ 1 + \frac{\mathbf{c}_i \cdot \mathbf{u}}{c_s^2} \right] = w_i \left( \sum_{q_1=0}^8 h_{q1} \right) \left[ 1 + \frac{1}{\rho_0 c_s^2} \sum_{q_2=0}^8 (\mathbf{c}_i \cdot \mathbf{c}_{q2}) g_{q2} \right] $$
$$ = w_i \sum_{q_1} h_{q1} + \frac{w_i}{\rho_0 c_s^2} \sum_{q_1, q_2} (\mathbf{c}_i \cdot \mathbf{c}_{q2}) h_{q1} g_{q2} $$
- Linear in $h_{q1}$: $w_i \sum_{q1} h_{q1}$ $\implies$ **Degree 1**
- Cross-product $h_{q1} g_{q2}$: Bilinear coupling between phase and fluid $\implies$ **Degree 2**

---

## 3. Kowalski Reciprocal Auxiliary Variable Lifting
For full variable density with $\xi(\mathbf{x}) = \frac{1}{\rho(\mathbf{x})}$:
$$ \mathbf{u}(\mathbf{x}) = \xi(\mathbf{x}) \sum_{q=0}^8 g_q(\mathbf{x}) \mathbf{c}_q $$
- Convective term $(\mathbf{c}_i \cdot \mathbf{u})^2 = \xi^2 \sum (\mathbf{c}_i \cdot \mathbf{c}_{q1})(\mathbf{c}_i \cdot \mathbf{c}_{q2}) g_{q1} g_{q2}$ $\implies$ **Degree 4 in $[\mathbf{\Psi}; \xi]$**
- Under step-by-step quasi-linear state propagation, the maximum polynomial degree is strictly **$p = 3$ or $p = 4$**, with closed finite polynomial structure.
