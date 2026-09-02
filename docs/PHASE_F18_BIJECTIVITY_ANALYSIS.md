# PHASE F18: BIJECTIVITY & DISSIPATION ANALYSIS
## Mathematical Proof of Non-Injectivity in the Discrete BGK Collision Map

**Document**: Bijectivity & Information Loss Specification  
**Project**: Quantum Lattice Boltzmann Method (QLBM) for Two-Phase Flow  
**Repository**: `/home/aswa/Research/QLBM-DamBreak-Production`  
**Branch**: `feature/direct-encoding-two-phase-qlbm`  
**Date**: September 2026  

---

## 1. Mathematical Proof of Non-Injectivity

In D2Q9 BGK collision with relaxation parameter $\omega = 1.0$, the physical map is:
$$f_i^* = f_i^{\text{eq}}(\rho(\mathbf{f}), \mathbf{u}(\mathbf{f}))$$

Consider two distinct states $\mathbf{f}^{(1)} \ne \mathbf{f}^{(2)}$ defined such that:
$$\sum_{i=0}^8 f_i^{(1)} = \sum_{i=0}^8 f_i^{(2)} = \rho, \quad \sum_{i=0}^8 f_i^{(1)} \mathbf{c}_i = \sum_{i=0}^8 f_i^{(2)} \mathbf{c}_i = \mathbf{j}$$
Then $\mathbf{u}(\mathbf{f}^{(1)}) = \mathbf{u}(\mathbf{f}^{(2)})$, which implies:
$$f_i^*(\mathbf{f}^{(1)}) = f_i^{\text{eq}}(\rho, \mathbf{u}) = f_i^*(\mathbf{f}^{(2)}) \quad \forall i \in \{0 \dots 8\}$$

$$\mathbf{Conclusion:\ The\ physical\ map\ F\ is\ strictly\ many-to-one.}$$

---

## 2. Experimental Counterexample in $Q4.12$

$$\begin{array}{|l|c|c|c|c|}
\hline
\textbf{State} & \textbf{Density } \rho & \textbf{Momentum } \mathbf{j} & \text{Non-Equilibrium Perturbation } \Delta f & \text{Post-Collision Output } F(\mathbf{f}) \\
\hline
\text{State 1 } (\mathbf{f}^{(1)}) & 1.0000 & (0.0, 0.0) & 0.0000 & \mathbf{f}^{\text{eq}}(1.0, \mathbf{0}) \\
\text{State 2 } (\mathbf{f}^{(2)}) & 1.0000 & (0.0, 0.0) & \Delta f_1 = +\delta, \Delta f_3 = +\delta, \Delta f_2 = -\delta, \Delta f_4 = -\delta & \mathbf{f}^{\text{eq}}(1.0, \mathbf{0}) \\
\hline
\end{array}$$

$$\|\mathbf{f}^{(1)} - \mathbf{f}^{(2)}\|_{L_1} = 328 \quad \longrightarrow \quad \|F(\mathbf{f}^{(1)}) - F(\mathbf{f}^{(2)})\|_{L_1} = 0$$
