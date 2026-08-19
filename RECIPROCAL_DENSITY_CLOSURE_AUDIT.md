# Reciprocal Density Auxiliary Variable Lifting & Closure Audit

**Author**: Lead Mathematical Scientist & Senior Numerical Analyst  
**Date**: August 19, 2026  
**Repository**: `/home/aswa/Research/QLBM-DamBreak/`  

---

## 1. Physical Role of Reciprocal Density
In the full variable-density Navier-Stokes LBM, the local fluid density is an affine function of the phase field:
$$ \rho(\mathbf{x}, t) = \rho_G + \phi(\mathbf{x}, t) (\rho_L - \rho_G) $$
However, the macroscopic velocity recovery and Guo body forcing require division by $\rho$:
$$ \mathbf{u}(\mathbf{x}, t) = \frac{\mathbf{j}(\mathbf{x}, t)}{\rho(\mathbf{x}, t)} = \frac{1}{\rho(\mathbf{x}, t)} \sum_{q=0}^8 g_q(\mathbf{x}, t) \mathbf{c}_q $$

Because $1/\rho(\phi)$ is a rational function of $\phi$, treating $\mathbf{\Psi} = [\mathbf{g}; \mathbf{h}]$ alone requires an infinite Taylor expansion if $\rho$ varies substantially.

---

## 2. Kowalski Auxiliary State Lifting $\xi = 1/\rho$
To close the system as a finite polynomial map, we introduce the auxiliary reciprocal density variable:
$$ \xi(\mathbf{x}, t) \equiv \frac{1}{\rho(\mathbf{x}, t)} \in \mathbb{R} $$
Augmented state vector:
$$ \mathbf{\Psi}_{aug}(t) = \begin{bmatrix} \mathbf{g}(t) \\ \mathbf{h}(t) \\ \mathbf{\xi}(t) \end{bmatrix} \in \mathbb{R}^{19 N} $$

### Exact Substitution into Governing Equations:
1. **Macroscopic Velocity**: $\mathbf{u}(\mathbf{x}) = \xi(\mathbf{x}) \sum_q g_q(\mathbf{x}) \mathbf{c}_q$ $\implies$ **Bilinear (Degree 2 in $[\mathbf{\Psi}, \xi]$)**.
2. **Phase Advection Flux**: $\phi \mathbf{u} = (\sum h_q) \xi (\sum g_q \mathbf{c}_q)$ $\implies$ **Trilinear (Degree 3 in $[\mathbf{\Psi}, \xi]$)**.
3. **Hydrodynamic Convection**: $\mathbf{u} \otimes \mathbf{u} = \xi^2 (\sum g_q \mathbf{c}_q) \otimes (\sum g_q \mathbf{c}_q)$ $\implies$ **Degree 4 in $[\mathbf{\Psi}, \xi]$**.

---

## 3. Dynamic Evolution of the Auxiliary Variable $\xi$
Since $\rho(\mathbf{x}, t+1) = \rho(\mathbf{x}, t) + \Delta \rho \Delta \phi(\mathbf{x}, t)$, the exact evolution law for $\xi$ is:
$$ \xi(\mathbf{x}, t+1) = \frac{1}{\rho(\mathbf{x}, t) + \Delta \rho \Delta \phi(\mathbf{x}, t)} = \frac{\xi(\mathbf{x}, t)}{1 + \xi(\mathbf{x}, t) \Delta \rho \Delta \phi(\mathbf{x}, t)} $$
Using second-order polynomial truncation for small phase increments $|\xi \Delta \rho \Delta \phi| \ll 1$:
$$ \xi(\mathbf{x}, t+1) \approx \xi(\mathbf{x}, t) - \xi^2(\mathbf{x}, t) \Delta \rho \Delta \phi(\mathbf{x}, t) + \mathcal{O}((\Delta \phi)^2) $$

### Conclusion:
- **Degree in Physical State $\mathbf{\Psi}$ alone**: Degree 2 (Quadratic under reference $\rho_0$).
- **Degree in Augmented State $[\mathbf{\Psi}, \xi]$**: Degree 3 (Cubic for advection/density evolution) to Degree 4 (Convective flux).
- **Closure Status**: **ALGEBRAICALLY CLOSED AT CUBIC DEGREE ($p=3$) UNDER QUASI-LINEAR CONVECTIVE APPROXIMATION**.
