# PHASE F35: SAFETY GATE ENFORCEMENT & PRE-FLIGHT VERIFICATION
## Dual-Flag Opt-In Protocol for Cloud QPU Job Dispatch

**Document**: Safety Guard Report  
**Project**: Quantum Lattice Boltzmann Method (QLBM) for Two-Phase Flow  
**Repository**: `/home/aswa/Research/QLBM-DamBreak-Production`  
**Development Branch**: `feature/direct-encoding-two-phase-qlbm`  
**Audit Date**: September 2026  

---

## 1. Safety Gate Rules

1. **Rule 1 (Pytest Immunity)**: Unit tests and automated regression suites (`pytest`) are strictly isolated and never dispatch network calls or cloud jobs.
2. **Rule 2 (Double Opt-In)**: Real QPU jobs require both:
   $$\text{QLBM\_ENABLE\_REAL\_QPU} = 1, \quad \text{QLBM\_CONFIRM\_REAL\_QPU} = \text{YES}$$
3. **Rule 3 (Dry-Run Safety)**: Dry-run execution generates complete transpiled metrics and archives data without submitting live jobs.
