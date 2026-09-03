# PHASE F34: HARDWARE EXECUTION PROTOCOL & SAFETY ARCHITECTURE
## Double Opt-In Execution Gates and Cloud Submission Pipeline

**Document**: Hardware Execution Protocol  
**Project**: Quantum Lattice Boltzmann Method (QLBM) for Two-Phase Flow  
**Repository**: `/home/aswa/Research/QLBM-DamBreak-Production`  
**Development Branch**: `feature/direct-encoding-two-phase-qlbm`  
**Audit Date**: September 2026  

---

## 1. Safety Double Opt-In Protocol

Real QPU submissions are strictly guarded. A hardware job will only be dispatched if:
1. `QLBM_ENABLE_REAL_QPU=1`
2. `QLBM_CONFIRM_REAL_QPU=YES`
3. A valid IBM Quantum API token is present in the environment (`QISKIT_IBM_TOKEN` or `IBM_QUANTUM_TOKEN`).

In any other circumstance, the runner executes in safe dry-run mode, transpiling and archiving circuit statistics without consuming cloud quantum credits.
