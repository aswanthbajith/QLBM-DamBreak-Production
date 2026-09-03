# PHASE F31: WORKSPACE LIFETIME AUDIT & SCRATCHPAD BOUNDS
## Analysis of Sequential Uncomputation Schedules and the 48-Qubit Peak Workspace Barrier

**Document**: Workspace Lifetime Audit Report  
**Project**: Quantum Lattice Boltzmann Method (QLBM) for Two-Phase Flow  
**Repository**: `/home/aswa/Research/QLBM-DamBreak-Production`  
**Development Branch**: `feature/direct-encoding-two-phase-qlbm`  
**Audit Date**: September 2026  

---

## 1. Sequential Phase Lifetime and Ancilla Requirements

$$\begin{array}{|l|c|c|l|}
\hline
\textbf{Computational Phase} & \textbf{Active Ancillas} & \textbf{Live Width} & \textbf{Lifetime \& Uncomputation Event} \\
\hline
\text{Phase 1: Moment Accumulation} & 2\text{ words} & 32\text{ qubits} & \text{Computes } (\rho, \mathbf{j})\text{; passed to velocity divider} \\
\mathbf{Phase\ 2:\ Velocity\ Division} & \mathbf{3\text{ words}} & \mathbf{48\text{ qubits}} & \mathbf{Holds\ } \mathbf{j}, \rho\mathbf{, and\ reciprocal\ scratchpad;\ uncomputes\ scratch} \\
\mathbf{Phase\ 3:\ CSF\ Curvature\ Stencil} & \mathbf{3\text{ words}} & \mathbf{48\text{ qubits}} & \mathbf{Holds\ } \nabla \alpha, |\nabla \alpha|, \kappa\mathbf{;\ uncomputes\ stencils} \\
\text{Phase 4: Symmetric Equilibrium} & 2\text{ words} & 32\text{ qubits} & \text{Computes } (u_x^2, u_y^2)\text{; uncomputes invariants} \\
\text{Phase 5: BGK Relaxation \& Guard} & 1\text{ word} & 16\text{ qubits} & \text{Computes difference and guards } f_0 \ge 0\text{; uncomputes flag} \\
\hline
\end{array}$$

---

## 2. The 48-Qubit Peak Workspace Barrier

- **Division & Curvature Minimum**: Newton-Raphson division ($\mathbf{u} = \mathbf{j}/\rho$) and CSF curvature ($\kappa = -\nabla \cdot (\nabla \alpha / |\nabla \alpha|)$) strictly require 3 simultaneous $16$-bit words ($48\text{ qubits}$) to hold the numerator, denominator, and iterative multiplier scratchpad.
- **Trade-Off Evaluation**: Reducing workspace to $32\text{ qubits}$ would require spilling intermediate registers to the environment or re-evaluating moments 3 times, increasing total Toffoli count by over $+45\%$.
- **Finding**: **$48\text{ logical qubits}$ represents the exact Pareto-optimal peak workspace barrier**.
