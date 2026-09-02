# PHASE F13: BASELINE FREEZE RECORD
## Fully Coherent Quantum Two-Phase Dam-Break LBM & Elimination of Classical Control Interfaces

**Document**: Baseline Freeze, Hash Verification & Execution Graph Audit  
**Project**: Quantum Lattice Boltzmann Method (QLBM) for Two-Phase Flow  
**Repository**: `/home/aswa/Research/QLBM-DamBreak-Production`  
**Branch**: `feature/direct-encoding-two-phase-qlbm`  
**Previous Commit**: `4144bbe` (*"QLBM Phase F12: Autonomous Multi-Step Quantum Two-Phase Dam-Break LBM"*)  
**Date**: September 2026  

---

## 1. Frozen Baseline Verification

- **Level-6B File**: `quantum/level6b_hybrid_solver.py`
- **Level-6B SHA-256**: `2a306f5a413945adc1acd10f3f63340c3d3617e4ef1c94981a92e8ebad8742c8` (**VERIFIED INTACT**)
- **Original Archive**: `/home/aswa/Research/QLBM-DamBreak` (**STRICTLY UNTOUCHED ON `master`**)
- **Pre-Audit Test Status**: 174 / 174 tests passing (100%)
- **Working Tree**: Clean.

---

## 2. Execution Graph of F12 Timestep Operations (Pre-F13 Baseline)

$$\begin{array}{|l|l|c|c|c|}
\hline
\textbf{Subsystem / Kernel} & \textbf{Physical Operation} & \textbf{Quantum?} & \textbf{Hybrid?} & \textbf{Classical?} \\
\hline
\text{State Storage} & |\Psi_t\rangle \propto \sum [f_i|x,y,i,0\rangle + g_i|x,y,i,1\rangle] & \checkmark & \text{No} & \text{No} \\
\text{Moment Accumulation} & \rho(x,y), \alpha(x,y), j_x(x,y), j_y(x,y) & \text{No} & \checkmark & \text{No} \\
\text{Shifted Velocity} & \mathbf{u} = (\mathbf{j} + \frac{1}{2}\mathbf{F})/\rho_{\text{safe}}, \ u \le 0.15 & \text{No} & \checkmark & \text{No} \\
\text{Capillary Tension (CSF)} & \mathbf{F}_{\text{CSF}} = \sigma \kappa \nabla \alpha & \text{No} & \checkmark & \text{No} \\
\text{Collision Construction} & C(\alpha, \mathbf{u}, \mathbf{F}/\rho) = \text{block\_diag}(M_f, M_g) & \text{No} & \checkmark & \text{No} \\
\text{Collision Execution} & \text{Sz.-Nagy Unitary Dilation } U_C \in \mathbb{U}(64) & \checkmark & \text{No} & \text{No} \\
\text{Arithmetic Streaming} & S_{\text{arith}}|x,y,i,p\rangle = |x+c_{ix}, y+c_{iy}, i, p\rangle & \checkmark & \text{No} & \text{No} \\
\text{Boundary Involution} & B_{\text{mask}}|x,y,i,p\rangle = |x,y,\text{opp}(i), p\rangle \ (B^2=I) & \checkmark & \text{No} & \text{No} \\
\text{Timestep Transition} & |\Psi_{t+1}\rangle \text{ formed without re-encoding} & \checkmark & \text{No} & \text{No} \\
\hline
\end{array}$$
