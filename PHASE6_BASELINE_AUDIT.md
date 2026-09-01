# PHASE 6 BASELINE AUDIT & REPOSITORY INTEGRITY REPORT (STAGE 6.1)

**Auditor Role**: Lead Research Scientist & Independent Reproducibility Auditor  
**Date**: 2026-08-19  
**Repository**: `/home/aswa/Research/QLBM-DamBreak/`  
**Phase 5 Status**: **FROZEN & AUTHORITATIVE (CONDITIONAL PASS)**  

---

## 1. Executive Summary & Baseline Integrity Confirmation

This report establishes the forensic baseline for **Phase 6** (Independent Benchmarking, Resource Analysis, Error Characterization, and Noise Robustness).

As mandated by Phase 6 scientific rules:
1. The **Phase 5 Ground Truth** (Classical Two-Phase LBM + Conservative Allen-Cahn + CSF Surface Tension) is frozen and unmodified.
2. The **Phase 5 Quantum Surrogate Model** (Constant-Density Quadratic Two-Phase LBM, $p=2$, $D_C = 342N$, CS/Halmos block encoding, $d=15$ Chebyshev QSVT inversion) is frozen and unmodified.
3. All 44 existing Phase 5 unit and regression tests have been executed in a clean environment and passed with $100\%$ success ($44/44$ passed).

---

## 2. Environment & System Specifications

The execution environment has been recorded in [`phase6_baseline_environment.json`](phase6_baseline_environment.json):

* **Operating System**: Linux (Kernel 7.0.0-29-generic, x86_64, glibc 2.43)
* **CPU Model**: Intel(R) Core(TM) i5-10300H CPU @ 2.50GHz (8 logical cores)
* **Total System RAM**: $14.95\text{ GB}$ (Available: $11.07\text{ GB}$)
* **Python Runtime**: Python 3.14.4 (GCC 15.2.0)
* **Virtual Environment**: `/home/aswa/Research/QLBM-DamBreak/.venv`
* **Key Package Versions**:
  * `qiskit`: **2.5.2**
  * `numpy`: **2.5.2**
  * `scipy`: **1.18.0**
  * `pytest`: **9.1.1**

---

## 3. Phase 5 Repository Inventory

### 3.1 Core Source Code
* **Classical Ground Truth Solver**:
  * [`classical/two_phase_lbm.py`](classical/two_phase_lbm.py): Full two-phase D2Q9 Navier-Stokes + Allen-Cahn solver.
  * [`classical/phase_field.py`](classical/phase_field.py): Conservative Allen-Cahn order parameter evolution.
  * [`classical/forcing.py`](classical/forcing.py): Gravity and CSF surface tension forcing terms.
  * [`classical/run_and_validate.py`](classical/run_and_validate.py): Martin & Moyce (1952) physical dam-break benchmark driver.
* **Polynomial & Matrix Transformations**:
  * [`classical/matrix_two_phase_lbm.py`](classical/matrix_two_phase_lbm.py): Discrete matrix operator representation ($M_1, M_2, S$).
  * [`classical/verify_matrix_equivalence.py`](classical/verify_matrix_equivalence.py): Matrix-vs-pointwise equivalence verifier.
* **Quantum Linear Algebra & Simulation Pipeline**:
  * [`quantum/carleman_lbm.py`](quantum/carleman_lbm.py): Order $N_C=2$ local quadratic Carleman lifting ($D_C = 342N$).
  * [`quantum/block_encoding.py`](quantum/block_encoding.py): Canonical CS/Halmos unitary block encoding ($U_A$).
  * [`quantum/qsvt_solver.py`](quantum/qsvt_solver.py): QSVT Chebyshev matrix inversion solver & Qiskit circuit builder.
  * [`quantum/dam_break_qlbm_sim.py`](quantum/dam_break_qlbm_sim.py): End-to-end multi-step classical vs. Carleman vs. QSVT simulation engine.
  * [`quantum/verify_block_encoding.py`](quantum/verify_block_encoding.py): Block encoding unitarity and submatrix test driver.
  * [`quantum/run_end_to_end_validation.py`](quantum/run_end_to_end_validation.py): Automated end-to-end validation runner.

### 3.2 Phase 5 Test Suite (15 Test Files, 44 Automated Tests)
1. `tests/test_block_encoding.py` (3 tests)
2. `tests/test_carleman_equivalence.py` (3 tests)
3. `tests/test_carleman_lifting.py` (3 tests)
4. `tests/test_carleman_truncation_limits.py` (1 test)
5. `tests/test_classical_ground_truth_regression.py` (3 tests)
6. `tests/test_dam_break_observables.py` (2 tests)
7. `tests/test_independent_carleman_audit.py` (3 tests)
8. `tests/test_polynomial_system.py` (3 tests)
9. `tests/test_qsvt.py` (2 tests)
10. `tests/test_qsvt_condition_spectrum.py` (4 tests)
11. `tests/test_quantum_block_encoding_independent.py` (6 tests)
12. `tests/test_quantum_resources.py` (2 tests)
13. `tests/test_quantum_solver.py` (2 tests)
14. `tests/test_shot_noise_statistics.py` (1 test)
15. `tests/test_two_phase_physics.py` (6 tests)

### 3.3 Phase 5 Authoritative Reports & Artifacts
* [`PHASE5_FINAL_SCIENTIFIC_REPORT.md`](PHASE5_FINAL_SCIENTIFIC_REPORT.md): 22-section final Phase 5 publication report.
* [`PHASE5_SCOPE_CORRECTION.md`](PHASE5_SCOPE_CORRECTION.md): Detailed scope correction and historical audit log.
* [`PHASE5_QUANTUM_SURROGATE_SPECIFICATION.md`](PHASE5_QUANTUM_SURROGATE_SPECIFICATION.md): Formal CDQ-QLBM model specification.
* [`VARIABLE_DENSITY_CLOSURE_LIMITATIONS.md`](VARIABLE_DENSITY_CLOSURE_LIMITATIONS.md): Mathematical non-polynomiality proof.
* [`QUANTUM_EXECUTION_STATUS.md`](QUANTUM_EXECUTION_STATUS.md): Breakdown of verified, emulated, and simulated components.
* [`PHASE5_RESOURCE_SCALING.md`](PHASE5_RESOURCE_SCALING.md): Asymptotic resource scaling laws.
* [`PHASE5_OBSERVABLE_DEFINITIONS.md`](PHASE5_OBSERVABLE_DEFINITIONS.md): Physical observable measurement specifications.
* [`QUANTUM_ADVANTAGE_SCOPE.md`](QUANTUM_ADVANTAGE_SCOPE.md): Complexity and readout bottleneck bounds.
* [`PHASE5_FINAL_CLAIM_MATRIX.csv`](PHASE5_FINAL_CLAIM_MATRIX.csv): 17-point scientific claim matrix.
* [`phase5_final_status.json`](phase5_final_status.json): Machine-readable Phase 5 status file.
* [`scripts/run_phase5_validation.sh`](scripts/run_phase5_validation.sh): Automated one-command validation script.

---

## 4. Phase 5 Baseline Test Execution Results

```text
============================= test session starts ==============================
platform linux -- Python 3.14.4, pytest-9.1.1, pluggy-1.6.0
rootdir: /home/aswa/Research/QLBM-DamBreak
configfile: pyproject.toml
testpaths: tests
collected 44 items

44 passed in 159.83s (0:02:39) [100% PASS]
```

---

## 5. Detected Risks & Computational Boundaries for Phase 6

1. **Dense Matrix Memory Limit**:
   For grid sizes $N \ge 128$ ($16 \times 8$), Carleman dimension $D_C = 43,776$ requires $> 15\text{ GB}$ for dense complex matrices. Experiments beyond $N=32$ must use sparse matrix linear algebra (`scipy.sparse`) or matrix-free Krylov/SVD evaluations to prevent Out-Of-Memory (OOM) crashes.
2. **Qiskit Statevector Simulation Limit**:
   Classical full-statevector simulation is limited to $\le 14$ qubits ($\sim 16,384$ amplitudes). Higher-dimensional circuits ($N \ge 32$) must be analyzed via transpiled circuit metrics and classical sparse SVD emulation rather than dense statevector evolution.
3. **Condition Number Sensitivity**:
   Studying large time steps $\Delta t > 0.05$ in Stage 6.5 may increase $\kappa(I + \Delta t A_C)$, requiring higher polynomial degree $d > 21$ for QSVT inversion convergence.

---

## 6. Proposed Phase 6 Experiment Execution Roadmap

1. **Stage 6.2**: Independent Classical Reference Benchmark ($4\times 2, 8\times 4, 16\times 8, 32\times 16, 64\times 32, 300\times 100$).
2. **Stage 6.3**: Carleman Accuracy vs. Time ($t \in [1, 200]$ error evolution).
3. **Stage 6.4**: QSVT Polynomial Degree Study ($d \in [3, 31]$ convergence sweep).
4. **Stage 6.5**: Condition Number Study ($\Delta t \in [0.001, 0.1]$ spectrum analysis).
5. **Stage 6.6**: Grid Scaling Analysis ($N \in [1, 30000]$ resource matrix).
6. **Stage 6.7**: Quantum Circuit Resource & Transpilation Analysis (Optimization levels 0..3).
7. **Stage 6.8**: Classical Direct vs. Carleman vs. Hybrid SVD Performance Comparison.
8. **Stage 6.9**: Observable Estimation & QAE Quantum Advantage Bounds.
9. **Stage 6.10**: Shot-Noise Statistics & Comprehensive Error Budget.
10. **Stage 6.11**: Quantum Noise Robustness Study (Depolarizing and gate error models in Qiskit).
11. **Stage 6.12**: Adversarial Failure Boundary Characterization.
12. **Stage 6.13 - 6.18**: Publication Figures, Tables, Final Claim Matrix, Test Suite, and Final Scientific Report.
