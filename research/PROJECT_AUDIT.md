# PROJECT AUDIT: QLBM-DamBreak Codebase & Artifact Forensics

**Date**: 2026-08-20  
**Author**: Lead Quantum-CFD Implementation Researcher  
**Repository**: `/home/aswa/Research/QLBM-DamBreak/`  

---

## 1. Executive Summary & Environment Audit
* **Operating System**: Linux 6.6.137+
* **Python Environment**: Python 3.14.4 (Virtualenv at `.venv/`)
* **Qiskit Core Version**: 2.5.2
* **NumPy Version**: 2.5.2
* **SciPy Version**: 1.18.0
* **Pytest Version**: 9.1.1
* **Test Suite Status**: 74 / 74 Pytest unit tests passing (`./run_phase15_validation.sh` exit code 0)

---

## 2. Complete Inventory of Existing Code & Artifacts

| File / Component | Primary Purpose | Current Status | Working? | Tested? | Reusable? | Modification / Extension Needed? |
| :--- | :--- | :--- | :--- | :--- | :--- | :--- |
| `classical/two_phase_lbm.py` | Full 2-phase D2Q9 LBM solver with Allen-Cahn interface tracking | Validated Baseline | Yes | Yes (Pytest) | Yes | Keep as physical CFD reference |
| `classical/matrix_two_phase_lbm.py` | Exact matrix operator representations of Streaming $S$ and Collision $M_1$ | Validated Baseline | Yes | Yes (Pytest) | Yes | Reusable for exact linear operator verification |
| `quantum/carleman_lbm.py` | Global quadratic Carleman linearization ($D_C = 342 N$) | Validated Baseline | Yes | Yes (Pytest) | Yes | Reusable; need local Carleman decoupling |
| `quantum/block_encoding.py` | Dense CS/Halmos unitary block encoding dilation | Validated Baseline | Yes | Yes (Pytest) | Yes | High CX cost ($\mathcal{O}(4^n)$); keep as dense comparison baseline |
| `quantum/qsvt_solver.py` | QSVT polynomial inversion using Chebyshev approximations ($d=3..31$) | Validated Baseline | Yes | Yes (Pytest) | Yes | Reusable for quantum linear systems |
| `quantum/dam_break_qlbm_sim.py` | Classical SVD functional calculus CPU emulator for multi-step time evolution | Validated Baseline | Yes | Yes (Pytest) | Yes | Reusable as multi-step reference |
| `PHASE11_STREAMING_ORACLE.py` | Structured D2Q9 spatial coordinate shift permutation circuit | Validated Baseline | Yes | Yes (Pytest) | Yes | Directly reusable ($\mathcal{O}(\log N)$ CX) |
| `PHASE11_STRUCTURED_QSVT.py` | Structured local collision circuit and 13Q $4	imes 2$ LCU oracle | Validated Baseline | Yes | Yes (Pytest) | Yes | Directly reusable ($73,500	imes$ CX reduction) |
| `quantum_hardware/01_block_encoding_demo.py` | 2-qubit CS block encoding demonstration | Validated Baseline | Yes | Yes | Yes | Directly reusable as Level 1 hardware test |
| `quantum_hardware/02_qsvt_demo.py` | 3-qubit QSVT polynomial demonstration | Validated Baseline | Yes | Yes | Yes | Directly reusable as Level 3 hardware test |
| `quantum_hardware/03_measurement_demo.py` | Measurement register & sampling test | Validated Baseline | Yes | Yes | Yes | Directly reusable |
| `quantum_hardware/run_real_qpu.py` | IBM Quantum Runtime submission script with dry-run interlock | Validated Baseline | Yes | Yes | Yes | Needs update to current `SamplerV2` stack |
| `quantum_hardware/transpile_hardware.py` | IBM Heavy-Hex transpilation harness | Validated Baseline | Yes | Yes | Yes | Reusable |

---

## 3. IBM Connection & Authentication Audit
* **Qiskit IBM Runtime**: `qiskit_ibm_runtime` is installed.
* **Credentials**: Currently not saved in local keyring / environment; safety interlock correctly defaults to `DRY_RUN = True`.
* **Hardware Target**: IBM Eagle-127 Heavy-Hex architecture (`GenericBackendV2` dry-run target).
