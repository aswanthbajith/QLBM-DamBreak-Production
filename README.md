# Quantum Lattice Boltzmann Method for Two-Phase Dam-Break Hydrodynamics

A rigorous research implementation and evaluation framework for **Quantum Lattice Boltzmann Methods (QLBM)** applied to two-phase free-surface flows (dam-break hydrodynamic collapse).

---

## 1. Research Overview & Problem Formulation

This project investigates the formulation, reversibility, and quantum channel properties of the Lattice Boltzmann Method (LBM) for multiphase fluid dynamics. The physical problem studied is the 2D liquid–gas dam-break benchmark inside an enclosed rectangular cavity bounded by solid no-slip walls.

The hydrodynamic system is modeled using the D2Q9 lattice:
- **Hydrodynamic Field ($f_i$)**: Governs total fluid mass and momentum conservation under gravity body forcing.
- **Phase-Field Interface Capturing ($g_i$)**: Governs the conservative liquid volume fraction $\alpha \in [0, 1]$ and phase-dependent fluid properties.

---

## 2. Core Architecture & Scientific Progression

The repository documents the rigorous scientific progression of quantum fluid formulations:

1. **Classical Level-4 Reference Solver (`classical/level4_two_phase.py`)**:
   - Canonical D2Q9 two-phase solver with phase-dependent density $\rho(\alpha)$, viscosity $\nu(\alpha)$, Continuum Surface Force (CSF) $\mathbf{F}_s = \sigma \kappa \nabla \alpha$, and Guo body forcing.
   - Provides ground-truth hydrodynamic trajectories.

2. **Direct Spatial and Population Quantum Encoding (`quantum/`)**:
   - Direct Hilbert space factorization: $\mathcal{H} = \mathcal{H}_x \otimes \mathcal{H}_y \otimes \mathcal{H}_{\text{vel}} \otimes \mathcal{H}_{\text{phase}}$.
   - Avoids exponentially growing Carleman polynomial liftings.

3. **Exact Unitary Streaming & Bounce-Back Boundaries**:
   - **Streaming ($S$)**: Exact coordinate wire permutation operator satisfying $S^\dagger S = I$ with $0.0000$ numerical unitarity error.
   - **Boundary Involution ($B$)**: Exact velocity register bit-inversion on solid walls satisfying $B^2 = I$.

4. **CPTP Quantum Collision Channel (Phase F20)**:
   - Formulates the dissipative, non-injective BGK collision relaxation as a Completely Positive Trace-Preserving (CPTP) quantum channel via Stinespring environmental dilation:
     $$U |x\rangle_S |0\rangle_E = |F(x)\rangle_S |x\rangle_E$$
   - Kraus representation: $K_\mu = |F(\mu)\rangle \langle \mu|$, with exact trace preservation $\|\sum_\mu K_\mu^\dagger K_\mu - I_S\|_2 = 0.0000$.
   - Validated on computational-basis statistical distributions matching classical LBM multi-step time evolution.

---

## 3. Quick Start & Reproducibility

### Environment Setup
```bash
# 1. Clone repository and checkout release branch
git clone https://github.com/aswanthbajith/QLBM-DamBreak-Production.git
cd QLBM-DamBreak-Production
git checkout professor/final-research-code

# 2. Create and activate a clean virtual environment
python3 -m venv .venv
source .venv/bin/activate

# 3. Install validated dependencies
pip install -r requirements.txt
```

### Running Automated Test Suite
```bash
# Run all 212 automated unit, regression, and physics tests
pytest -q
```

### Minimal Reproducible CLI Runs
```bash
# Run canonical classical reference solver (ground truth)
python run.py --mode classical --nx 4 --ny 4 --timesteps 2 --no-plots

# Run direct quantum statevector solver
python run.py --mode quantum --nx 4 --ny 4 --timesteps 2 --no-plots

# Run F20 CPTP channel equivalence master audit
python scripts/run_phase_f20_channel_equivalence.py
```

---

## 4. Current Scientific Status & Boundaries

| Component / Claim | Scientific Status | Evidence & Notes |
|---|---|---|
| **Classical Two-Phase LBM** | **VALIDATED** | Exact Level-4 D2Q9 dam-break benchmark |
| **Direct Quantum Encoding** | **VALIDATED** | Statevector preparation at $t=0$ |
| **Quantum Spatial Streaming** | **VALIDATED** | Exact closed unitary coordinate permutation ($S^\dagger S = I$) |
| **Quantum Boundary Operation** | **VALIDATED** | Exact closed unitary bounce-back involution ($B^2 = I$) |
| **Quantum BGK Collision** | **VALIDATED (CPTP Channel)** | Open-system Stinespring dilation ($J(\mathcal{E}) \succeq 0$) |
| **Fully Coherent Nonlinear BGK** | **NOT ESTABLISHED** | Dissipative nature requires environmental entropy discard |
| **Quantum CSF Surface Tension** | **EXPERIMENTAL / FUTURE** | Baseline F20 evaluated at $\sigma = 0$ |
| **Real IBM QPU Execution** | **NOT ESTABLISHED** | Transpilation analysis only; real QPU execution interlocked |
| **Quantum Speedup** | **NOT ESTABLISHED** | No asymptotic or empirical speedup claimed |

---

## 5. Repository Structure

```
QLBM-DamBreak-Production/
├── classical/          # Validated Level-1 to Level-4 classical LBM solvers
├── quantum/            # Direct encoding, streaming, boundary, and F20 CPTP channel modules
├── tests/              # 212 comprehensive automated test suites
├── scripts/            # Milestone execution runners and audit scripts
├── docs/               # Detailed mathematical derivations, audits, and reproducibility guides
│   ├── ARCHITECTURE.md
│   ├── CODE_STATUS.md
│   ├── RESEARCH_STATUS.md
│   ├── REPRODUCIBILITY.md
│   ├── REFERENCES.md
│   └── FINAL_VALIDATION_MATRIX.md
├── hardware/           # IBM Heavy-Hex FakeSherbrooke preflight & transpilation
├── config/             # Register layout and physical simulation parameters
├── run.py              # Main CLI entry point
├── requirements.txt    # Minimal reproducible dependencies
└── README.md           # Master documentation overview
```

---

## 6. Hardware Safety Interlocks

To ensure safety, physical execution on remote quantum devices is disabled by default:
```bash
export QLBM_ENABLE_REAL_QPU=0
export QLBM_CONFIRM_REAL_QPU=NO
```
All quantum simulations run via local statevector and Qiskit Aer emulators.
