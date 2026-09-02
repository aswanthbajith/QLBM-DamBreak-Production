# PHASE F13: COHERENT VELOCITY & PARAMETER GENERATION
## Reversible Division, Goldschmidt Iteration, and Quantum Low-Mach Limiter

**Document**: Reversible Velocity & Physical Parameter Generation Specification  
**Project**: Quantum Lattice Boltzmann Method (QLBM) for Two-Phase Flow  
**Repository**: `/home/aswa/Research/QLBM-DamBreak-Production`  
**Branch**: `feature/direct-encoding-two-phase-qlbm`  
**Date**: September 2026  

---

## 1. Reversible Shifted Velocity ($U_{\text{vel}}$)

$$\mathbf{j}_{\text{shifted}}(x, y) = \mathbf{j}(x, y) + \frac{1}{2}\mathbf{F}(x, y)$$
$$\mathbf{u}(x, y) = \frac{\mathbf{j}_{\text{shifted}}(x, y)}{\rho_{\text{safe}}(x, y)}$$

- **Division Engine**: 3-step Goldschmidt reciprocal iteration ($x_{k+1} = x_k (2 - d x_k)$) yielding $< 2.4 \times 10^{-4}$ error in $Q4.12$.
- **Low-Mach Stability Limiter**: Reversible comparator checks $u_x^2 + u_y^2 > 0.0225$. If triggered, scales $u \to 0.15 u / u_{\text{mag}}$.

---

## 2. Reversible Relaxation Rates

$$\nu_{\text{mix}}(\alpha) = \alpha \nu_L + (1 - \alpha)\nu_G, \quad \tau_f = 3\nu_{\text{mix}} + 0.5, \quad \omega_f = \frac{1}{\tau_f}$$
$$\omega_g = \frac{1}{\tau_g}$$
All computed directly in fixed-point registers without floating-point ALU coprocessors.
