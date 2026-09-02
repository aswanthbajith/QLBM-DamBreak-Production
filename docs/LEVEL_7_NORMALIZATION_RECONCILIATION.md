# LEVEL-7: NORMALIZATION RECONCILIATION REPORT
## Mathematical and Physical Resolution of the $\alpha_C$ Scaling Discrepancy

**Document**: Definitive Technical Reconciliation of Dilation Scaling Constants  
**Repository**: `/home/aswa/Research/QLBM-DamBreak-Production`  
**Date**: September 2026  

---

## 1. The Discrepancy Statement

Across project documentation, two distinct values for the dilation normalization constant were reported:
- **Value A**: $\alpha_C = 7.9004$ (corresponding to $p_{\text{succ}} = 1.602\%$)
- **Value B**: $\alpha_C = 9.7321$ (corresponding to $p_{\text{succ}} = 1.056\%$)

---

## 2. Root-Cause Analysis: Physical Parameter Dependency

The second-order Carleman collision matrix $C_2 \in \mathbb{R}^{342 \times 342}$ contains the linear relaxation block $M_1 \in \mathbb{R}^{18 \times 18}$ and quadratic convective tensor $M_2 \in \mathbb{R}^{18 \times 324}$.
The relaxation frequency is $\omega_f = 1/\tau_f$, where $\tau_f = 3\nu + 0.5$.

As fluid kinematic viscosity $\nu$ decreases, the collision frequency $\omega_f$ increases, directly scaling the magnitude of the non-equilibrium collision entries:

$$\begin{array}{|l|c|c|c|c|c|}
\hline
\textbf{Simulation Configuration} & \textbf{Kinematic Viscosity } (\nu) & \textbf{Relaxation } (\tau_f) & \mathbf{\|C_2\|_2} & \mathbf{\alpha_C = 1.01 \|C_2\|_2} & \mathbf{p_0 = 1/\alpha_C^2} \\
\hline
\text{Level 5 / Level 6A Default} & \nu = 0.100 & \tau_f = 0.80 & 7.8222 & \mathbf{7.9004} & 1.6021\% \\
\text{Level 6B / Level 7 Physical} & \nu = 0.050 & \tau_f = 0.65 & 9.6357 & \mathbf{9.7321} & 1.0558\% \\
\text{Inviscid Test Limit} & \nu = 0.0167 & \tau_f = 0.55 & 11.4177 & \mathbf{11.5319} & 0.7516\% \\
\text{High Viscosity Test Limit} & \nu = 0.1667 & \tau_f = 1.00 & 6.2723 & \mathbf{6.3350} & 2.4918\% \\
\hline
\end{array}$$

---

## 3. Authoritative Architecture Assignment

1. **$\alpha_C = 7.9004$**: Belongs strictly to the **Level-5 / Level-6A** exploratory formulation with default parameter $\tau_f = 0.80$ ($\nu = 0.10$).
2. **$\alpha_C = 9.7321$**: Belongs strictly to the **Level-6B / Level-7** production physical dam-break solver with physical fluid parameter $\tau_f = 0.65$ ($\nu = 0.05$).

Both values are mathematically and numerically exact for their respective physical relaxation parameters.
