# LEVEL-4 IMMEDIATE ACTION CHECKLIST

This document lists the concrete execution tasks for advancing the Two-Phase QLBM project through the Level-4 research pipeline.

---

## Phase A: Classical Two-Phase Formulation & Reference Benchmarking

- [ ] **Action 1.1**: Formalize the mathematical definition of the coupled conservative phase-field D2Q9 LBM with interfacial chemical potential $\mu_\phi$ and surface tension $\mathbf{F}_s$.
- [ ] **Action 1.2**: Implement the independent high-resolution classical reference solver in `classical/two_phase_solver.py` supporting configurable grid sizes ($32 \times 32$, $64 \times 64$, $128 \times 128$).
- [ ] **Action 1.3**: Implement the Martin & Moyce (1952) / OpenFOAM VOF experimental benchmark dataset and validation metric calculators ($x^*(t^*)$, $h^*(t^*)$, kinetic energy).
- [ ] **Action 1.4**: Run spatial and temporal convergence studies and record $L_2$ convergence rates $\mathcal{O}(\Delta x^2)$.

---

## Phase B: Coupled Polynomial & Carleman Derivation

- [ ] **Action 2.1**: Derive the exact polynomial expansion of the surface-tension coupled collision operator.
- [ ] **Action 2.2**: Compute the local second-order Carleman matrices $M_1 \in \mathbb{R}^{18 \times 18}$ and $M_2 \in \mathbb{R}^{18 \times 324}$ incorporating interfacial force terms.
- [ ] **Action 2.3**: Verify local Carleman step accuracy against high-resolution classical field solutions.

---

## Phase C: Quantum Circuit Synthesis & Resource Study

- [ ] **Action 3.1**: Build the unified quantum circuit generator for $N_x \times N_y$ grids ($n = \log_2 N + 5$ qubits).
- [ ] **Action 3.2**: Transpile the complete Level-4 quantum timestep to IBM Quantum Heavy-Hex architecture.
- [ ] **Action 3.3**: Perform fault-tolerant resource estimation (logical qubit count, T-depth, magic state distillation, and OAA postselection factor $\alpha$).
