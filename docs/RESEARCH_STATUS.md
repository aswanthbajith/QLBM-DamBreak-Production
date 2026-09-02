# Detailed Research Status & Scientific Boundary

**Project**: Quantum Lattice Boltzmann Method (QLBM) for Two-Phase Dam-Break Flow  
**Baseline Milestone**: Phase F20 (`7e6d5a7`)  
**Date**: September 2026  

---

## 1. Explicit Scientific Status

### A. Classical Two-Phase LBM
- **Status**: **VALIDATED**
- **Evidence**: Level-4 high-fidelity D2Q9 solver with conservative phase-field interface capturing, surface tension, and gravity body forcing.

### B. Coupled Two-Phase Formulation
- **Status**: **VALIDATED WITHIN TESTED REGIME**
- **Evidence**: Coupled hydrodynamic ($f_i$) and phase fraction ($g_i$) populations evolve accurately across tested density contrasts and low Mach numbers ($M < 0.15$).

### C. Quantum State Encoding
- **Status**: **IMPLEMENTED / VALIDATED FOR TESTED CASES**
- **Evidence**: Direct spatial and velocity register Hilbert space $\mathcal{H}_x \otimes \mathcal{H}_y \otimes \mathcal{H}_{\text{vel}} \otimes \mathcal{H}_{\text{phase}}$.

### D. Quantum Streaming
- **Status**: **VALIDATED**
- **Evidence**: Exact unitary coordinate wire permutation $S_{\text{arith}}$ ($S^\dagger S = I$, $0.0000$ unitarity error).

### E. Quantum Boundary Operation
- **Status**: **VALIDATED**
- **Evidence**: Exact quantum bounce-back involution $B_{\text{mask}}$ ($B^2 = I$).

### F. Quantum Collision
- **Status**: **VALIDATED WITH SCOPE LIMITATIONS**
- **Evidence**: Dissipative BGK collision embedded into a finite-register unitary via Stinespring environmental dilation.

### G. F20 BGK Channel
- **Status**: **VALIDATED AS COMPUTATIONAL-BASIS STATISTICAL/CPTP REPRESENTATION**
- **Evidence**: Induced channel $\mathcal{E}(\rho) = \operatorname{Tr}_E [ U (\rho \otimes |0\rangle\langle 0|_E) U^\dagger ] = \sum_x \langle x|\rho|x\rangle |F(x)\rangle\langle F(x)|$. Proven Completely Positive Trace-Preserving ($\lambda_{\min}(J) \ge 0$, $\sum K_\mu^\dagger K_\mu = I$).
- **Limitation**: Evaluates classical statistical ensembles in the computational basis; does not claim coherent non-diagonal superposition evolution.

### H. Fully Autonomous Coherent Nonlinear Quantum CFD
- **Status**: **NOT ESTABLISHED**
- **Reason**: The dissipative nature of macroscopic Navier-Stokes / BGK fluid dynamics requires open-system entropy discard (environmental tracing).

### I. Full Quantum CSF / Surface-Tension Evolution
- **Status**: **EXPERIMENTAL / FUTURE WORK**
- **Reason**: The F20 baseline sets $\sigma = 0$; full quantum CSF stencil channels remain an active research topic.

### J. Real IBM QPU Execution
- **Status**: **NOT ESTABLISHED**
- **Reason**: Local statevector and Qiskit Aer simulation only; real hardware is interlocked by safety policies (`QLBM_ENABLE_REAL_QPU=0`).

### K. Quantum Speedup
- **Status**: **NOT ESTABLISHED**
- **Reason**: Linear systems algorithms for nonlinear CFD face input/output and state preparation bottlenecks; no asymptotic or empirical quantum speedup is claimed.

### L. Fault-Tolerant Resource Feasibility
- **Status**: **FUTURE WORK**
- **Reason**: Requires error correction and logical qubit scaling beyond current NISQ capabilities.
