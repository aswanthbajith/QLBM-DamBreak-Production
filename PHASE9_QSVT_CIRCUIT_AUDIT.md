# PHASE 9 QSVT CIRCUIT HARDWARE AUDIT (STAGE 9.5)

**Status**: Verified QSVT Circuit Architecture & Emulation Demarcation  
**Date**: 2026-08-19  

---

## 1. QSVT Subsystem Demarcation
* **A. Polynomial Mathematics**: Chebyshev expansion $P(x) \approx 1/(\alpha x)$ satisfies $|P(x)| \le 0.95$ and odd parity $P(-x) = -P(x)$ across all degrees $d \in [3, 31]$.
* **B. Phase Sequence**: Sequence $\Phi = (\phi_0, \dots, \phi_{d-1})$ is computed classically and embedded as $R_z(2\phi_j)$ gates on the dilation ancilla.
* **C. Circuit Synthesis**: `QSVTSolver._build_qsvt_circuit` constructs the full alternating Qiskit `QuantumCircuit`. Depth is exactly $2d$ and block queries equal $\lfloor d/2 \rfloor + 1$.
* **D. Multi-Step Dynamical Evaluation**: In `dam_break_qlbm_sim.py`, time evolution is evaluated via **classical CPU SVD functional calculus emulation** ($x = V P(\Sigma) U^\dagger b$).

---

## 2. Hardware Feasibility
Small QSVT circuits ($n=2$, degrees $d=3, 5$) transpile to $\le 10$ CNOTs and depth $\le 45$, making them **directly executable on real IBM QPUs**.
