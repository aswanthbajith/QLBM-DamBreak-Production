# Project File Inventory: QLBM Two-Phase Dam-Break Research Repository

**Repository Root**: `/home/aswa/Research/QLBM-DamBreak/`  
**Audit Date**: August 19, 2026  
**Auditor**: Lead Computational Fluid Dynamics & Quantum Algorithm Auditor  

---

## 1. Inventory Classification Schema
Every file in the repository is cataloged with the following metadata:
- **Path**: Relative path from repository root.
- **Type**: Code (`.py`), Test (`.py`), Spec/Config (`.toml`, `.yml`, `.txt`), Equation/Theory (`.md`), Validation/Audit (`.md`), Data (`.csv`), Figure (`.png`), Knowledge/Paper (`.md`, `.pdf`).
- **Purpose**: Specific role in the research pipeline.
- **Dependencies**: Key libraries and module imports.
- **Executable**: Yes / No.
- **Tested**: Verified in automated test suite (`pytest`) or test script.
- **Scientific Importance**: Critical / High / Medium / Low / Supporting.
- **Status**: Authoritative / Generated / Baseline Archive / Obsolete / Duplicate.

---

## 2. Master Repository File Table

| Path | Type | Purpose | Dependencies | Executable | Tested | Scientific Importance | Status |
| :--- | :--- | :--- | :--- | :---: | :---: | :---: | :---: |
| `pyproject.toml` | Spec | Python build and pytest configuration | setuptools, pytest | No | Yes | High | Authoritative |
| `requirements.txt` | Spec | Pinned runtime and test dependencies | pip | No | Yes | High | Authoritative |
| `environment.yml` | Spec | Conda environment specification | conda | No | Yes | High | Authoritative |
| `.gitignore` | Config | Git ignore rules for virtualenv and caches | git | No | N/A | Low | Authoritative |
| `README.md` | Doc | General project overview | markdown | No | N/A | Medium | Authoritative |
| `FINAL_THESIS_QLBM_REPORT.md` | Theory/Doc | 24-section master scientific thesis report | markdown | No | N/A | Critical | Authoritative |
| **Classical Engine (`classical/`)** | | | | | | | |
| `classical/two_phase_physics.py` | Code | Variable density/viscosity, CSF surface tension, Laplace droplet | numpy | Yes | Yes (`test_two_phase_physics.py`) | Critical | Authoritative |
| `classical/phase_field.py` | Code | D2Q9 Conservative Allen-Cahn interface capturing | numpy | Yes | Yes (`test_two_phase_physics.py`) | Critical | Authoritative |
| `classical/forcing.py` | Code | Guo external body forcing (gravity, CSF) | numpy | Yes | Yes (`test_two_phase_physics.py`) | High | Authoritative |
| `classical/two_phase_lbm.py` | Code | Main coupled 2D two-phase D2Q9 velocity-based solver | numpy, scipy | Yes | Yes (`test_two_phase_physics.py`) | Critical | Authoritative |
| `classical/dam_break_sim.py` | Code | Dam-break simulation wrapper with diagnostics | numpy | Yes | Yes (`test_two_phase_physics.py`) | High | Authoritative |
| `classical/run_and_validate.py` | Code | Classical benchmark runner vs Martin & Moyce (1952) | numpy, matplotlib | Yes | Yes (Executed) | Critical | Authoritative |
| `classical/matrix_two_phase_lbm.py` | Code | Matrix-vector algebraic LBM with unitary permutation $\mathbf{S}$ | numpy, scipy.sparse | Yes | Yes (`test_polynomial_system.py`) | Critical | Authoritative |
| `classical/verify_matrix_equivalence.py` | Code | Verification of matrix vs procedural solver equivalence | numpy, scipy.sparse | Yes | Yes (Executed) | High | Authoritative |
| **Quantum Engine (`quantum/`)** | | | | | | | |
| `quantum/carleman_lbm.py` | Code | Carleman state lifting ($342N$) & linear operator assembly | numpy, scipy.sparse | Yes | Yes (`test_carleman_lifting.py`) | Critical | Authoritative |
| `quantum/block_encoding.py` | Code | Canonical CS/Halmos unitary block encoding in Qiskit | numpy, scipy.linalg, qiskit | Yes | Yes (`test_block_encoding.py`) | Critical | Authoritative |
| `quantum/qsvt_solver.py` | Code | QSVT Chebyshev polynomial matrix inversion circuit solver | numpy, scipy.linalg, qiskit | Yes | Yes (`test_qsvt.py`, `test_quantum_solver.py`) | Critical | Authoritative |
| `quantum/dam_break_qlbm_sim.py` | Code | End-to-end QLBM simulation & observable extraction engine | numpy, scipy, qiskit | Yes | Yes (`test_dam_break_observables.py`) | Critical | Authoritative |
| `quantum/verify_block_encoding.py` | Code | Matrix norm verification of block encoding submatrices | numpy, scipy, qiskit | Yes | Yes (Executed) | High | Authoritative |
| `quantum/compare_three_solvers.py` | Code | 4-way solver benchmark (Direct, GMRES, Ideal QSVT, Noisy) | numpy, scipy, qiskit | Yes | Yes (Executed) | Critical | Authoritative |
| `quantum/run_end_to_end_validation.py` | Code | Master driver for end-to-end QLBM run & figure generation | numpy, matplotlib | Yes | Yes (Executed) | Critical | Authoritative |
| `quantum/resource_analysis.py` | Code | Asymptotic quantum resource accounting and Clifford+T | numpy | Yes | Yes (`test_quantum_resources.py`) | High | Authoritative |
| `quantum/dam_break_qlbm.py` | Code | Legacy prototype QLBM runner (grand matrix approach) | numpy, scipy, qiskit | Yes | No | Low | Baseline/Legacy |
| `quantum/run_dam_break_qlbm.py` | Code | Legacy runner for grand matrix QLBM | numpy, scipy, qiskit | Yes | No | Low | Baseline/Legacy |
| `quantum/run_quantum_pipeline.py` | Code | Legacy test driver for Level 5-7 milestone | numpy, scipy, qiskit | Yes | No | Low | Baseline/Legacy |
| **Automated Test Suite (`tests/`)** | | | | | | | |
| `tests/test_two_phase_physics.py` | Test | Physics unit tests (Laplace, density, gravity, mass) | unittest, numpy | Yes | Yes (pytest) | Critical | Authoritative |
| `tests/test_polynomial_system.py` | Test | Matrix operator and permutation unitarity tests | unittest, numpy | Yes | Yes (pytest) | Critical | Authoritative |
| `tests/test_carleman_lifting.py` | Test | Carleman state lifting and Kronecker structure tests | unittest, numpy | Yes | Yes (pytest) | Critical | Authoritative |
| `tests/test_carleman_equivalence.py` | Test | Carleman operator step stability and sparsity tests | unittest, numpy | Yes | Yes (pytest) | Critical | Authoritative |
| `tests/test_block_encoding.py` | Test | Block encoding dilation unitarity and accuracy tests | unittest, numpy, qiskit | Yes | Yes (pytest) | Critical | Authoritative |
| `tests/test_qsvt.py` | Test | QSVT Chebyshev polynomial boundedness and circuit tests | unittest, numpy, qiskit | Yes | Yes (pytest) | Critical | Authoritative |
| `tests/test_quantum_solver.py` | Test | QSVT solver residual and quantum fidelity tests | unittest, numpy, qiskit | Yes | Yes (pytest) | Critical | Authoritative |
| `tests/test_dam_break_observables.py` | Test | Macroscopic observable bounds and finite shot sampling | unittest, numpy | Yes | Yes (pytest) | High | Authoritative |
| `tests/test_quantum_resources.py` | Test | Logarithmic qubit and circuit depth scaling tests | unittest, numpy | Yes | Yes (pytest) | High | Authoritative |
| **Scripts (`scripts/`)** | | | | | | | |
| `scripts/run_parameter_study.py` | Code | Parameter sensitivity sweep (density, viscosity, surface tension) | numpy, matplotlib | Yes | Yes (Executed) | High | Authoritative |
| `scripts/run_carleman_study.py` | Code | Truncation error convergence study ($N_C=1$ vs $N_C=2$) | numpy, matplotlib | Yes | Yes (Executed) | High | Authoritative |
| `scripts/generate_final_research_benchmarks.py` | Code | Benchmark table and labeled scaling plot generator | numpy, matplotlib, qiskit | Yes | Yes (Executed) | High | Authoritative |
| `scripts/ingest_paper.py` | Utility | PDF text extraction utility for knowledge base | pypdf | Yes | N/A | Low | Utility |
| **Mathematical Equations (`equations/`)** | | | | | | | |
| `equations/QUANTUM_STATE_ENCODING.md` | Theory | Hilbert space register allocation & physical amplitude mapping | markdown, latex | No | N/A | Critical | Authoritative |
| `equations/discrete_two_phase_lbm.md` | Theory | Discrete nonlinear evolution equations & Kowalski lifting | markdown, latex | No | N/A | Critical | Authoritative |
| `equations/two_phase_physics_complete.md`| Theory | Continuum Navier-Stokes, Allen-Cahn, and CSF derivations | markdown, latex | No | N/A | Critical | Authoritative |
| `equations/two_phase_model.md` | Theory | Early physical model derivation | markdown, latex | No | N/A | Medium | Baseline |
| `equations/classical_lbm.md` | Theory | Standard D2Q9 lattice definitions | markdown, latex | No | N/A | Medium | Baseline |
| `equations/phase_field.md` | Theory | Phase field transport equations | markdown, latex | No | N/A | Medium | Baseline |
| `equations/dam_break.md` | Theory | Dam-break physical parameters and non-dimensionalization | markdown, latex | No | N/A | Medium | Baseline |
| `equations/qlbm.md` | Theory | General QLBM formulation notes | markdown, latex | No | N/A | Medium | Baseline |
| **Mappings & Polynomial Analysis (`mappings/`)** | | | | | | | |
| `mappings/COMPLETE_POLYNOMIAL_DEGREE_AUDIT.md` | Theory | Formal algebraic proof of quadratic/cubic Kowalski lifting | markdown, latex | No | N/A | Critical | Authoritative |
| `mappings/BLOCK_ENCODING_DESIGN.md` | Theory | CS/Halmos block encoding dilation mathematics | markdown, latex | No | N/A | Critical | Authoritative |
| `mappings/NONLINEARITY_AUDIT.md` | Theory | Detailed term-by-term audit of hydrodynamic non-linearities | markdown, latex | No | N/A | High | Authoritative |
| `mappings/carleman.md` | Theory | Kronecker power indexing and truncation theory | markdown, latex | No | N/A | High | Baseline |
| `mappings/classical_to_matrix.md` | Theory | Vectorization rules for spatial grids | markdown, latex | No | N/A | High | Baseline |
| `mappings/nonlinear_terms.md` | Theory | Initial classification of nonlinear terms | markdown, latex | No | N/A | Medium | Baseline |
| `mappings/quantum_encoding.md` | Theory | Early state encoding schema | markdown, latex | No | N/A | Medium | Baseline |
| **Validation Artifacts & Reports (`validation/`)** | | | | | | | |
| `validation/FINAL_ADVERSARIAL_AUDIT.md` | Audit | Master adversarial audit report classifying all claims | markdown | No | N/A | Critical | Authoritative |
| `validation/ACTUAL_QUANTUM_PIPELINE_TRACE.md`| Audit | Step-by-step code and dimensional execution trace | markdown | No | N/A | Critical | Authoritative |
| `validation/QSVT_AUTHENTICITY_AUDIT.md` | Audit | Deep-dive verification of QSVT circuit and SVD calculus | markdown | No | N/A | Critical | Authoritative |
| `validation/OBSERVABLE_MAPPING_AUDIT.md` | Audit | Spatial coordinate mapping and node resolution analysis | markdown | No | N/A | Critical | Authoritative |
| `validation/END_TO_END_QLBM_VALIDATION.md` | Audit | Quantitative summary of end-to-end QLBM simulation | markdown | No | N/A | Critical | Authoritative |
| `validation/BLOCK_ENCODING_VALIDATION.md` | Audit | Machine precision verification of block encoding | markdown | No | N/A | High | Authoritative |
| `validation/CARLEMAN_TRUNCATION_STUDY.md` | Audit | Quantitative Carleman truncation convergence study | markdown | No | N/A | High | Authoritative |
| `validation/CLASSICAL_VS_QSVT_SOLVER_REPORT.md`| Audit | Benchmark report comparing 4 linear system solvers | markdown | No | N/A | Critical | Authoritative |
| `validation/EXACT_MATRIX_EQUIVALENCE.md` | Audit | Numerical proof of matrix vs procedural equivalence | markdown | No | N/A | High | Authoritative |
| `validation/FINAL_INDEPENDENT_AUDIT.md` | Audit | Previous independent audit document | markdown | No | N/A | High | Authoritative |
| `validation/QUANTUM_FAILURE_ANALYSIS.md` | Audit | Failure mode analysis and finite-shot sensitivity table | markdown | No | N/A | High | Authoritative |
| `validation/classical_two_phase_validation.md` | Audit | Detailed Martin & Moyce (1952) validation metrics | markdown | No | N/A | Critical | Authoritative |
| `validation/parameter_sensitivity_study.md` | Audit | Results of parameter sweeps | markdown | No | N/A | High | Authoritative |
| `validation/raw_quantum_classical_comparison.csv`| Data | Raw step-by-step observable data table | csv | No | N/A | Critical | Generated |
| `validation/reference_data/martin_moyce_1952.csv`| Data | Digitized experimental benchmark dataset | csv | No | N/A | Critical | Authoritative |
| **Archival Baseline Directories (`baseline/`, `classical/baseline_v0_simplified/`)** | | | | | | | |
| `baseline/classical_validated/*` | Archive | Frozen classical stage snapshot (commit `0779537`) | python, md | Yes | N/A | High | Frozen Baseline |
| `classical/baseline_v0_simplified/*` | Archive | Pre-refactor constant density baseline solver | python | Yes | N/A | Low | Obsolete Archive |

---

## 3. Scientific Authority Summary
- **Authoritative Executable Pipeline**: `classical/two_phase_lbm.py` $\to$ `classical/matrix_two_phase_lbm.py` $\to$ `quantum/carleman_lbm.py` $\to$ `quantum/block_encoding.py` $\to$ `quantum/qsvt_solver.py` $\to$ `quantum/dam_break_qlbm_sim.py`.
- **Authoritative Test Suite**: All 9 test files in `tests/` (26 test cases, 100% pass rate).
- **Authoritative Validation Reports**: `validation/FINAL_ADVERSARIAL_AUDIT.md`, `validation/END_TO_END_QLBM_VALIDATION.md`, `FINAL_THESIS_QLBM_REPORT.md`.
