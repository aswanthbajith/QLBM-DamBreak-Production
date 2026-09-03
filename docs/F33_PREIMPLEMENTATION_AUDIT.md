# PHASE F33: PRE-IMPLEMENTATION AUDIT & HARDWARE ROADMAP
## Real Quantum-Hardware Two-Phase Dam-Break LBM Demonstrator

**Document**: Pre-Implementation Hardware Audit  
**Project**: Quantum Lattice Boltzmann Method (QLBM) for Two-Phase Flow  
**Repository**: `/home/aswa/Research/QLBM-DamBreak-Production`  
**Development Branch**: `feature/direct-encoding-two-phase-qlbm`  
**Checkpoint Commit**: `cc3eef3` (Phase F31)  
**Baseline Level-6B SHA-256**: `2a306f5a413945adc1acd10f3f63340c3d3617e4ef1c94981a92e8ebad8742c8` (**100% Intact**)  
**Audit Date**: September 2026  

---

## 1. Safety and Repository Integrity

- **Branch**: `feature/direct-encoding-two-phase-qlbm`
- **Milestone History**:
  - `cc3eef3` (F31: Resource-reduced reversible architecture)
  - `8797c32` (F30: Scaling and resource validation)
  - `f90e503` (F29: Scalable small-lattice gate-level QLBM validation)
- **Baseline Test Suite**: **299 / 299 Passing Tests**.
- **Level-6B Frozen Baseline**: SHA-256 verified 100% intact.
- **Original Archive (`/home/aswa/Research/QLBM-DamBreak`)**: Clean on `master`.
- **Professor Release Branch**: Frozen.

---

## 2. Hardware Environment Inspection

- **Qiskit Version**: `2.5.2`
- **Qiskit Aer Version**: `0.17.2`
- **Qiskit IBM Runtime**: Installed and available.
- **Available Noise Emulators**: `FakeManilaV2`, `FakeSherbrooke`, `FakeBrisbane`, `FakeKyoto`.
- **Real QPU Credentials**: Checked environment; currently no live API token configured.
- **Safety Protocol**: Real QPU execution is guarded by double opt-in (`QLBM_ENABLE_REAL_QPU=1` and `QLBM_CONFIRM_REAL_QPU=YES`).

---

## 3. Execution Modes Defined

1. **Mode A — Ideal Quantum Simulation**: Statevector / exact unitary simulation via Qiskit Aer to verify logical circuit design.
2. **Mode B — Noisy Quantum Simulation**: Qiskit Aer simulation with realistic noise model (`FakeManilaV2` / `FakeSherbrooke`) including $T_1/T_2$ relaxation, CNOT depolarizing errors, and readout errors.
3. **Mode C — Real Quantum Hardware**: Live QPU execution via IBM Quantum Runtime with strict error mitigation and safety guards.
