# PHASE F36: SAFETY GUARD & DOUBLE OPT-IN ENFORCEMENT
## Dual-Flag Opt-In Protocol for Cloud QPU Job Dispatch

**Document**: Safety Guard Report  
**Project**: Quantum Lattice Boltzmann Method (QLBM) for Two-Phase Flow  
**Repository**: `/home/aswa/Research/QLBM-DamBreak-Production`  
**Development Branch**: `feature/direct-encoding-two-phase-qlbm`  
**Audit Date**: September 2026  

---

## 1. Safety Guard Invariants

1. **Rule 1 (Test Suite Isolation)**: `pytest` executions never dispatch network requests or cloud QPU submissions.
2. **Rule 2 (Double Opt-In Gate)**: Live QPU submissions strictly require:
   $$\text{QLBM\_ENABLE\_REAL\_QPU} = 1, \quad \text{QLBM\_CONFIRM\_REAL\_QPU} = \text{YES}$$
3. **Rule 3 (Dry-Run Mode)**: Dry-run execution generates complete transpiled metrics and archives data without submitting live jobs.
