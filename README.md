# Quantum Two-Phase Dam-Break Lattice Boltzmann Method (QLBM)

[![Python 3.10+](https://img.shields.io/badge/python-3.10%2B-blue.svg)](https://www.python.org/)
[![Qiskit 2.5.2](https://img.shields.io/badge/Qiskit-2.5.2-purple.svg)](https://qiskit.org/)
[![Pytest 336 Passing](https://img.shields.io/badge/Tests-336%20Passing-brightgreen.svg)]()
[![Classification LEVEL B](https://img.shields.io/badge/Scientific%20Status-LEVEL%20B-orange.svg)]()
[![Level-6B Verified](https://img.shields.io/badge/Level--6B%20SHA--256-Verified-blue.svg)]()

A comprehensive research ecosystem for the **Quantum Two-Phase Dam-Break Lattice Boltzmann Method (QLBM)** on discrete D2Q9 lattices with conservative phase fields ($f, g$) and Continuum Surface Force (CSF) surface tension.

---

## 1. Scientific Classification & Invariants

- **Scientific Classification**: **`LEVEL B — quantum circuit/hardware-transpilation demonstration; real QPU execution not demonstrated.`**
- **Formulation**: Discrete computational-basis open-system CPTP Stinespring realization of the nonlinear two-phase BGK+CSF evolution map.
- **Physical Baseline Integrity**: Level-6B hybrid solver frozen with permanent SHA-256 integrity (`2a306f5a413945adc1acd10f3f63340c3d3617e4ef1c94981a92e8ebad8742c8`).
- **No Quantum Advantage Claim**: No quantum speedup or practical advantage over classical solvers is claimed.
- **Hardware Access Gate**: Physical execution on IBM Quantum processors is strictly protected by double opt-in safety guards (`QLBM_ENABLE_REAL_QPU=1`, `QLBM_CONFIRM_REAL_QPU=YES`).

---

## 2. Research Landscape & Architecture Tiers

The repository consolidates four primary research tiers:

```text
1. GROUND-TRUTH REFERENCES:
   - classical/level4_two_phase.py: Pure classical LBM validated against Martin & Moyce (1952) (<3.8% error).
   - quantum/level6b_hybrid_solver.py: Stable hybrid K=1 local Carleman solver (SHA-256 frozen).

2. FAULT-TOLERANT SCALABLE REVERSIBLE ARCHITECTURE (Phases F27–F31):
   - quantum/f29_scalable_circuit.py & quantum/f31_reduced_architecture.py
   - Exact reversible arithmetic (C^-1 C = I) in Q4.16 precision across 4x4, 8x8, 16x16 meshes.
   - Resource-reduced environment compression (560 qubits/node, 15,232 Toffolis/node).

3. NISQ HARDWARE DEMONSTRATOR (Phases F33–F38):
   - quantum/f33_hardware_demo.py & quantum/f38_qpu_executor.py
   - Condensed 16-qubit gate-level circuit (2x2 grid, depth 19, 16 ECR gates on 127Q IBM Sherbrooke).
   - Multi-layer validation across Ideal, Noisy, and Transpiled states (SNR > 15).

4. PRESERVED SCIENTIFIC FAILURE ARTIFACTS:
   - quantum/f15_carleman_collision.py: Carleman truncation closure breakdown (>1400% error).
   - docs/F18_FORENSIC_VALIDATION.md: Proof of non-injectivity of dissipative BGK mapping.
```

---

## 3. What Works vs. What is Not Yet Achieved

| Research Capability | Scientific Status | Detailed Grounding |
| :--- | :---: | :--- |
| **Classical Two-Phase Hydrodynamics** | **VALIDATED** | Martin & Moyce surge front and residual height matched ($<3.8\%$ error). |
| **Frozen Physical Reference** | **VERIFIED** | Level-6B SHA-256 checksum verified 100% intact. |
| **Quantum State Preparation ($U_{\text{prep}}$)** | **VALIDATED** | Deterministic Pauli-$X$ basis initialization ($100\%$ fidelity). |
| **Quantum Coordinate Streaming ($S$)** | **VALIDATED** | Exact spatial SWAP network on quantum wires ($S^\dagger S = I$). |
| **Quantum Boundary Reflections ($B$)** | **VALIDATED** | Exact wall bounce-back involution ($B^2 = I$). |
| **Reversible Arithmetic Logic** | **VALIDATED** | Gate-level invertibility ($C^{-1} C = I$) verified in clean-room engine. |
| **Noisy Hardware Emulation** | **VALIDATED** | Executed on 127-qubit heavy-hex model (`FakeSherbrooke`, SNR $> 15$). |
| **Cloud QPU Submission Gateway** | **READY** | Double opt-in safety guards verified; zero fabricated data. |
| **Real IBM QPU Cloud Execution** | **BLOCKED** | Requires user-provided live IBM Quantum cloud API token. |
| **Quantum Computational Advantage** | **NOT CLAIMED** | Algorithmic speedup over classical CFD is not demonstrated. |

---

## 4. Quick Start & Execution

### Installation
```bash
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
```

### Run Regression Test Suite (336 Tests)
```bash
./.venv/bin/pytest -q tests/
```

### Run NISQ Demonstrator
```bash
# Mode A: Ideal Statevector Simulator
./.venv/bin/python scripts/run_phase_f38_ideal.py

# Mode B: Noisy 127-Qubit Hardware Emulation (FakeSherbrooke)
./.venv/bin/python scripts/run_phase_f38_noisy.py

# Mode C: Hardware Transpilation & Gate Resource Audit
./.venv/bin/python scripts/run_phase_f38_dryrun.py

# Master Multi-Tier Validation
./.venv/bin/python scripts/run_phase_f38_validation.py
```

### Run Scalable Fault-Tolerant Circuit (Phases F29–F31)
```bash
./.venv/bin/python scripts/run_phase_f29_validation.py
./.venv/bin/python scripts/run_phase_f31_validation.py
```

---

## 5. Verification & Key Documentation

- [CONSOLIDATION_FINAL_REPORT.md](docs/CONSOLIDATION_FINAL_REPORT.md): Complete repository archaeology and zero-loss verification.
- [FINAL_PRIMARY_QLBM_PROTOTYPE.md](docs/FINAL_PRIMARY_QLBM_PROTOTYPE.md): Definitive executable prototype specification.
- [FINAL_END_TO_END_DEPENDENCY_GRAPH.md](docs/FINAL_END_TO_END_DEPENDENCY_GRAPH.md): End-to-end import and data-flow map.
- [FINAL_SCIENTIFIC_STATUS.md](docs/FINAL_SCIENTIFIC_STATUS.md): Conservative capability classification matrix.
- [FINAL_QUANTUM_CLAIM_AUDIT.md](docs/FINAL_QUANTUM_CLAIM_AUDIT.md): Quantum vs. classical component boundaries.
- [FINAL_RESOURCE_AUDIT.md](docs/FINAL_RESOURCE_AUDIT.md): Resource estimates across NISQ and FTQC tiers.
- [CLEAN_CHECKOUT_REPRODUCIBILITY.md](docs/CLEAN_CHECKOUT_REPRODUCIBILITY.md): Clean checkout verification report.
- [PROFESSOR_REPRODUCTION_GUIDE.md](docs/PROFESSOR_REPRODUCTION_GUIDE.md): Concise command guide for external evaluation.
