# PHASE 5 SCIENTIFIC SCOPE CORRECTION & FORENSIC REPAIR

**Authoritative Directive**: Independent Adversarial Audit Stage 7  
**Date**: 2026-08-19  
**Status**: ACTIVE & BINDING  

---

## 1. Scope Correction Table

| Item | Previous Claim | Failure Cause | Corrected Scientific Claim | Mathematical & Numerical Consequence | Documentation Changed | Tests Affected |
| :--- | :--- | :--- | :--- | :--- | :--- | :--- |
| **SC-01** | Exact cubic polynomial closure ($p=3$) for full two-phase variable-density LBM | Interface normal $\mathbf{n} = \nabla\phi / \sqrt{\|\nabla\phi\|^2+\epsilon}$ and CSF chemical potential involve non-polynomial operations | Implemented QLBM represents a **constant-density quadratic surrogate** ($p=2$) | Model is restricted to $\rho_0 = \text{const}$ with exact quadratic advective closure | `mappings/COMPLETE_POLYNOMIAL_DEGREE_AUDIT.md`, `README.md` | `test_polynomial_system.py` |
| **SC-02** | Newton-Raphson $\xi=1/\rho$ dynamic auxiliary variable achieves complete variable-density lifting | Static initialization $\xi_0=1.0$ diverged exponentially ($10^7$ to $10^{23}$) for density ratios $\ge 10$ | Auxiliary reciprocal lifting is an analytical concept requiring adaptive multi-scale scaling | Full 1000:1 water-air density ratio is retained exclusively in Classical Ground Truth | `RECIPROCAL_DENSITY_CLOSURE_AUDIT.md` | `test_two_phase_physics.py` |
| **SC-03** | Exponential quantum speedup for full-field CFD velocity and phase tomography | Holevo theorem and state tomography lower bounds dictate $\mathcal{O}(N \log N / \epsilon^2)$ measurements to extract full spatial fields | Quantum speedup is restricted to **global scalar observables** via Quantum Amplitude Estimation (QAE) | No dense spatial speedup; quadratic query advantage $\mathcal{O}(1/\epsilon)$ for scalar observables | `FINAL_THESIS_QLBM_REPORT.md`, `QUANTUM_ADVANTAGE_SCOPE.md` | `test_dam_break_observables.py` |
| **SC-04** | Execution on physical quantum hardware / Fault-tolerant quantum execution | Qiskit circuits are synthesized for resource counting, but dynamical multi-step simulation is evaluated via classical SVD functional calculus | Multi-step simulation is a **verified hybrid SVD emulator** with verified circuit synthesis | Results reflect exact quantum algorithmic mathematics without claiming hardware execution | `QUANTUM_EXECUTION_STATUS.md`, `PHASE5_FINAL_SCIENTIFIC_REPORT.md` | `test_quantum_solver.py` |
| **SC-05** | Production dam break ($300\times 100$, 30,000 nodes) executed quantumly on 25 qubits | 25 qubits is the theoretical register dimension $\lceil \log_2(342N) \rceil + 1$; 10.26M-dim state cannot be simulated classically in dense form | 25 qubits is an **analytical resource extrapolation**; benchmark execution is demonstrated on reduced grids ($N=8$) | Clear separation between demonstrated benchmarks and asymptotic scaling | `PHASE5_RESOURCE_SCALING.md` | `test_quantum_resources.py` |

---

## 2. Superseded Historical Documents
The following historical audit files are preserved for archival integrity but are hereby marked **SUPERSEDED BY STAGE 7**:
* `01_FORENSIC_AUDIT_REPORT.md`
* `CLAIM_AUDIT.md`
* `FINAL_THESIS_QLBM_REPORT.md`
* `validation/FINAL_ADVERSARIAL_AUDIT.md`
* `validation/INDEPENDENT_AUDIT.md`
