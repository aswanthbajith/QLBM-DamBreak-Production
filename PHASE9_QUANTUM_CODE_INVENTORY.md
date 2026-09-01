# PHASE 9 QUANTUM CODEBASE INVENTORY (STAGE 9.1)

**Status**: Verified Quantum Codebase Discovery (60 Components)  
**Date**: 2026-08-19  

---

## 1. Summary of Quantum Code Constructs
* **Total Python Files Analyzed**: 39 files
* **Quantum Functions / Classes Identified**: 60
* **Explicit Qiskit `QuantumCircuit` Instantiations**: 2 primary circuit builders (`QuantumBlockEncoding._build_qiskit_circuit`, `QSVTSolver._build_qsvt_circuit`)
* **Statevector / Simulation Modules**: `dam_break_qlbm_sim.py`, `compare_three_solvers.py`, `run_batch2.py`
* **Classical Functional Calculus Modules**: `carleman_lbm.py`, `qsvt_solver.py` (via `la.svd`)

See [`PHASE9_QUANTUM_CODE_INVENTORY.csv`](PHASE9_QUANTUM_CODE_INVENTORY.csv) for the exhaustive registry.
