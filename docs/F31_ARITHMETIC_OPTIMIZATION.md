# PHASE F31: ARITHMETIC OPTIMIZATION & GATE-LEVEL REDUCTIONS
## Fused Linearization, Shared Reciprocal Stencils, and Exact Fixed-Point Multiplier Reduction

**Document**: Reversible Arithmetic Optimization Report  
**Project**: Quantum Lattice Boltzmann Method (QLBM) for Two-Phase Flow  
**Repository**: `/home/aswa/Research/QLBM-DamBreak-Production`  
**Development Branch**: `feature/direct-encoding-two-phase-qlbm`  
**Audit Date**: September 2026  

---

## 1. Arithmetic Optimization Strategies

1. **Equilibrium Weight Factoring**: Grouping populations with identical lattice weights ($w_{1..4} = 1/9$, $w_{5..8} = 1/36$) factors out repeated multiplications by $\rho$ and $\alpha$, reducing equilibrium Toffolis from $3,584 \to 2,048$.
2. **Shared CSF Reciprocal Stencil**: The unit normal vector $\mathbf{n} = \nabla \alpha / |\nabla \alpha|$ and interface curvature $\kappa = -\nabla \cdot \mathbf{n}$ share a single Newton-Raphson reciprocal computation for $1/|\nabla \alpha|$, eliminating 1 full fixed-point divider ($1,792\text{ Toffolis saved}$, reducing CSF from $4,864 \to 3,072$).
3. **Shift-Fused Relaxation**: Utilizing compile-time constant shifts for relaxation frequencies ($\omega_f, \omega_g$) reduces BGK interpolation cost from $8,880 \to 6,272\text{ Toffolis}$.

---

## 2. Component-Level Comparison: Baseline vs Optimized ($16\text{-bit } Q4.12$)

$$\begin{array}{|l|c|c|c|l|}
\hline
\textbf{Component} & \textbf{F30 Baseline Toffoli} & \textbf{F31 Optimized Toffoli} & \textbf{Toffoli Reduction} & \textbf{Optimization Mechanism} \\
\hline
\text{1. Moment Accumulation} & 256 & 256 & 0.0\% & \text{Already minimal CDKM adders} \\
\text{2. Velocity Division} & 3,584 & 3,584 & 0.0\% & \text{Preserves exact quotient precision} \\
\text{3. Reversible CSF Stencils} & 4,864 & 3,072 & \mathbf{36.8\%} & \text{Shared norm reciprocal reuse} \\
\text{4. Symmetric Equilibrium} & 3,584 & 2,048 & \mathbf{42.9\%} & \text{Lattice weight common factoring} \\
\text{5. BGK Relaxation \& Guard} & 8,880 & 6,272 & \mathbf{29.4\%} & \text{Shift-fused linear interpolation} \\
\text{6. Streaming Permutation} & 0 & 0 & - & \text{Exact wire permutation} \\
\text{7. Boundary Bounce-Back} & 0 & 0 & - & \text{Exact wire swap} \\
\hline\hline
\mathbf{Total\ per\ Node\ per\ Step} & \mathbf{21,168\text{ Toffolis}} & \mathbf{15,232\text{ Toffolis}} & \mathbf{28.0\%\ REDUCTION} & \mathbf{Exact\ Fixed\text{-}Point\ Equivalence} \\
\hline
\end{array}$$
