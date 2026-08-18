# Mathematical Audit of Nonlinearities in Two-Phase LBM & Carleman Linearization

**Author**: Independent Peer Reviewer  
**Audit Target**: `/home/aswa/Research/QLBM-DamBreak/`  
**Date**: August 2026  

---

## 1. Executive Summary & Polynomial Degree Verdict

| Physics Component | Implemented Code Polynomial Degree | Full Multiphase Physics Degree | Reviewer Classification |
| :--- | :---: | :---: | :---: |
| **Hydrodynamic Convection ($\mathbf{u} \otimes \mathbf{u}$)** | **Degree 2 (Quadratic)** | **Degree 2 (Quadratic)** | **VERIFIED** |
| **Phase-Field Advection ($\phi \mathbf{u}$)** | **Degree 2 (Bilinear)** | **Degree 2 (Bilinear)** | **VERIFIED** |
| **Guo Body Forcing ($\mathbf{u} \cdot \mathbf{F}$)** | **Degree 2 (Bilinear)** | **Degree 2 (Bilinear)** | **VERIFIED** |
| **Density Contrast $\rho(\phi) = \rho_L \phi + \rho_G(1-\phi)$** | **Degree 0 (Constant $\rho_0$)** | **Non-Polynomial Rational $1/\rho(\phi)$** | **INCORRECT (Claim of Full Multiphase)** |
| **Viscosity Contrast $\nu(\phi) = \nu_L \phi + \nu_G(1-\phi)$** | **Degree 0 (Constant $\tau_v$)** | **Non-Polynomial Rational $1/\tau_v(\phi)$** | **INCORRECT (Claim of Full Multiphase)** |
| **Cahn-Hilliard Chemical Potential ($\phi^3$)** | **Omitted (Zero)** | **Degree 3 (Cubic)** | **INCORRECT (Claim of Allen-Cahn/Cahn-Hilliard)** |
| **Surface Tension Force ($\mathbf{F}_{st} = \mu \nabla \phi$)** | **Omitted (Zero)** | **Degree 4 (Quartic Polynomial)** | **NOT IMPLEMENTED** |

---

## 2. Detailed Symbolic & Algebraic Expansion of Implemented Model

### A. State Vector Definition
The discrete state vector $\mathbf{\Psi}(\mathbf{x}_n, t) \in \mathbb{R}^{18}$ at each lattice node $\mathbf{x}_n$ consists of:
$$
\mathbf{\Psi}(\mathbf{x}_n, t) = \begin{bmatrix} g_0(\mathbf{x}_n, t), \dots, g_8(\mathbf{x}_n, t), & h_0(\mathbf{x}_n, t), \dots, h_8(\mathbf{x}_n, t) \end{bmatrix}^T
$$

### B. Macroscopic Moment Map
At every node $\mathbf{x}_n$, the macroscopic moments are exact linear combinations of the state vector:
1. **Order Parameter (Liquid Phase Fraction)**:
   $$ \phi(\mathbf{x}_n) = \sum_{q=0}^8 h_q(\mathbf{x}_n) = \mathbf{L}_\phi \mathbf{\Psi}(\mathbf{x}_n) \quad (\text{Degree 1 Linear}) $$
2. **Hydrodynamic Pressure**:
   $$ p(\mathbf{x}_n) = c_s^2 \sum_{q=0}^8 g_q(\mathbf{x}_n) = \mathbf{L}_p \mathbf{\Psi}(\mathbf{x}_n) \quad (\text{Degree 1 Linear}) $$
3. **Gravitational Body Force**:
   $$ \mathbf{F}(\mathbf{x}_n) = \phi(\mathbf{x}_n) \rho_0 \mathbf{g}_{grav} = \rho_0 \mathbf{g}_{grav} \left(\sum_{q=0}^8 h_q(\mathbf{x}_n)\right) \quad (\text{Degree 1 Linear in } \mathbf{h}) $$
4. **Physical Macroscopic Velocity** (with half-step Guo force correction):
   $$ \mathbf{u}(\mathbf{x}_n) = \frac{1}{\rho_0} \sum_{q=0}^8 g_q(\mathbf{x}_n) \mathbf{c}_q + \frac{\Delta t}{2 \rho_0} \mathbf{F}(\mathbf{x}_n) = \frac{1}{\rho_0} \sum_{q=0}^8 g_q(\mathbf{x}_n) \mathbf{c}_q + \frac{\Delta t}{2} \mathbf{g}_{grav} \sum_{q=0}^8 h_q(\mathbf{x}_n) $$
   **Key Finding**: Because reference density $\rho_0 = \text{const}$ is constant, $\mathbf{u}(\mathbf{x}_n)$ is a **strictly linear affine function** of $\mathbf{\Psi}(\mathbf{x}_n)$:
   $$ \mathbf{u}(\mathbf{x}_n) = \mathbf{C}_g \mathbf{g}(\mathbf{x}_n) + \mathbf{C}_h \mathbf{h}(\mathbf{x}_n) \quad (\text{Degree 1 Linear}) $$

---

## 3. Algebraic Analysis of Collision Nonlinearities

### A. Hydrodynamic Equilibrium $g_i^{eq}$
The incompressible velocity-based equilibrium (Jennings et al. 2025 Eq. 3) is:
$$
g_i^{eq} = \frac{p}{\rho_0 c_s^2} w_i + \rho_0 w_i \left[ \frac{\mathbf{c}_i \cdot \mathbf{u}}{c_s^2} + \frac{(\mathbf{c}_i \cdot \mathbf{u})^2}{2 c_s^4} - \frac{|\mathbf{u}|^2}{2 c_s^2} \right]
$$
Substituting the linear form of $p$ and $\mathbf{u}$:
1. $\frac{p}{\rho_0 c_s^2} w_i + \rho_0 w_i \frac{\mathbf{c}_i \cdot \mathbf{u}}{c_s^2}$ is **Degree 1 (Linear)** in $\mathbf{g}$ and $\mathbf{h}$.
2. $\rho_0 w_i \left[ \frac{(\mathbf{c}_i \cdot \mathbf{u})^2}{2 c_s^4} - \frac{|\mathbf{u}|^2}{2 c_s^2} \right]$ is **Degree 2 (Quadratic)**:
   $$ \mathbf{u} \otimes \mathbf{u} = (\mathbf{C}_g \mathbf{g} + \mathbf{C}_h \mathbf{h}) \otimes (\mathbf{C}_g \mathbf{g} + \mathbf{C}_h \mathbf{h}) = \mathbf{C}_g^{\otimes 2} (\mathbf{g} \otimes \mathbf{g}) + 2 \mathbf{C}_g \mathbf{C}_h (\mathbf{g} \otimes \mathbf{h}) + \mathbf{C}_h^{\otimes 2} (\mathbf{h} \otimes \mathbf{h}) $$
   Contains only monomials of degree 2: $g_j g_k$, $g_j h_k$, $h_j h_k$.

### B. Phase-Field Equilibrium $h_i^{eq}$
The phase-field advection equilibrium (line 127 of `two_phase_lbm.py`) is:
$$
h_i^{eq} = w_i \phi \left(1 + \frac{\mathbf{c}_i \cdot \mathbf{u}}{c_s^2}\right) = w_i \phi + \frac{w_i}{c_s^2} \phi (\mathbf{c}_i \cdot \mathbf{u})
$$
1. $w_i \phi = w_i \sum_k h_k$ is **Degree 1 (Linear)**.
2. $\phi (\mathbf{c}_i \cdot \mathbf{u}) = \left(\sum_k h_k\right) \left(\frac{1}{\rho_0} \sum_m g_m (\mathbf{c}_i \cdot \mathbf{c}_m) + \frac{\Delta t}{2} (\mathbf{c}_i \cdot \mathbf{g}_{grav}) \sum_m h_m\right)$:
   - The cross term $\mathbf{h} \otimes \mathbf{g}$ is **Degree 2 (Bilinear)**.
   - The self-coupling term $\mathbf{h} \otimes \mathbf{h}$ is **Degree 2 (Quadratic)**.

### C. Guo Forcing Term $F_i$
The Guo body forcing source (lines 137–139 of `two_phase_lbm.py`) is:
$$
F_i = \left(1 - \frac{1}{2\tau_v}\right) w_i \left[ \frac{(\mathbf{c}_i - \mathbf{u})\cdot \mathbf{F}}{\rho_0 c_s^2} + \frac{(\mathbf{c}_i \cdot \mathbf{u})(\mathbf{c}_i \cdot \mathbf{F})}{\rho_0 c_s^4} \right]
$$
1. $\mathbf{c}_i \cdot \mathbf{F} = \rho_0 (\mathbf{c}_i \cdot \mathbf{g}_{grav}) \phi$ is **Degree 1 (Linear)** in $\mathbf{h}$.
2. $-\mathbf{u} \cdot \mathbf{F} = -(\mathbf{C}_g \mathbf{g} + \mathbf{C}_h \mathbf{h}) \cdot (\rho_0 \mathbf{g}_{grav} \phi)$ is **Degree 2 (Bilinear/Quadratic)**.
3. $(\mathbf{c}_i \cdot \mathbf{u})(\mathbf{c}_i \cdot \mathbf{F}) = (\mathbf{c}_i \cdot (\mathbf{C}_g \mathbf{g} + \mathbf{C}_h \mathbf{h})) (\rho_0 (\mathbf{c}_i \cdot \mathbf{g}_{grav}) \phi)$ is **Degree 2 (Bilinear/Quadratic)**.

### D. Global Conclusion for the Implemented Code
For the specific equations written in `classical/two_phase_lbm.py` and `classical/matrix_two_phase_lbm.py`, **the total polynomial degree is strictly $p=2$ (Quadratic)**. There are NO degree 3, degree 4, or rational non-polynomial terms.

---

## 4. Nonlinearities in Full Two-Phase Physical Models (Unimplemented)

If one were to implement full two-phase Navier-Stokes with true phase-field interface physics (e.g. Watanabe & Hu 2026 or Fakhari et al. 2017), the following higher-order nonlinearities emerge:

### A. Variable Density $\rho(\phi) = \rho_L \phi + \rho_G (1-\phi)$
The macroscopic velocity would be:
$$ \mathbf{u} = \frac{\sum g_i \mathbf{c}_i}{\rho_L \phi + \rho_G (1-\phi)} $$
- **Non-polynomial Rational Function**: Requires Taylor expansion or introduction of auxiliary reciprocal variables $z = 1/\rho(\phi)$, creating an infinite Carleman hierarchy!

### B. Cahn-Hilliard Bulk Free Energy & Chemical Potential
$$ \mu = 4\beta \phi (\phi - 1) (\phi - 0.5) - \kappa \nabla^2 \phi = 4\beta(\phi^3 - 1.5\phi^2 + 0.5\phi) - \kappa \nabla^2 \phi $$
- **Cubic Polynomial ($p=3$)**: Requires $N_C \ge 3$ Carleman lifting.

### C. Surface Tension Force
$$ \mathbf{F}_{st} = \mu \nabla \phi = \left[ 4\beta(\phi^3 - 1.5\phi^2 + 0.5\phi) - \kappa \nabla^2 \phi \right] \nabla \phi $$
- **Quartic Polynomial ($p=4$)**: Contains the term $\phi^3 \nabla \phi$, which requires $N_C \ge 4$ Carleman lifting and introduces spatial gradient tensor contractions.

---

## 5. Peer Review Verdict on Nonlinearity Claims
1. **Claim: "The implemented two-phase LBM model is strictly degree 2 (quadratic)"**:
   - **Verdict**: **VERIFIED** for the actual Python codebase in `classical/` and `quantum/`.
2. **Claim: "Full two-phase Navier-Stokes with surface tension and density contrast is quadratic"**:
   - **Verdict**: **INCORRECT**. Full two-phase physics is quartic ($p=4$) with non-polynomial density fractions. The repository simplifies the problem to a constant-density Boussinesq indicator model to preserve $p=2$.
