# Research Codebase Status & Classification

This document provides a clear, module-by-module scientific status of the Quantum Lattice Boltzmann Method (QLBM) codebase.

---

## 1. Summary Status Matrix

| Module / Path | Status | Purpose | Validated? | Scope & Scientific Notes |
|---|---|---|---|---|
| `classical/d2q9.py` | **VALIDATED** | Discrete D2Q9 lattice velocity vectors, weights, opposites | **YES** | Exact lattice constants |
| `classical/equilibrium.py` | **VALIDATED** | Maxwell-Boltzmann equilibrium distribution | **YES** | Exact discrete expansion |
| `classical/streaming.py` | **VALIDATED** | Spatial streaming operator | **YES** | Exact spatial shifts |
| `classical/boundary.py` | **VALIDATED** | Half-way bounce-back wall boundaries | **YES** | Momentum-conserving no-slip walls |
| `classical/level4_two_phase.py` | **VALIDATED** | Ground-truth high-fidelity two-phase LBM solver | **YES** | Coupled hydrodynamic ($f$) and phase-field ($g$) fields with CSF surface tension |
| `quantum/d2q9_constants.py` | **VALIDATED** | Quantum register velocity constants | **YES** | Exact integer / fixed-point mappings |
| `quantum/spatial_index.py` | **VALIDATED** | Spatial Hilbert space 2D coordinate indexing | **YES** | Canonical $|y\rangle|x\rangle$ tensor product |
| `quantum/streaming.py` | **VALIDATED** | Exact unitary quantum streaming ($S^\dagger S = I$) | **YES** | Coordinate wire permutation |
| `quantum/boundary_quantum.py` | **VALIDATED** | Exact quantum bounce-back involution ($B^2 = I$) | **YES** | Inversion of velocity register bits on solid walls |
| `quantum/f17_reversible_primitives.py` | **VALIDATED** | Fixed-point $Q4.12$ reversible arithmetic | **YES** | Exact reversible addition, subtraction, multiplication, division |
| `quantum/f18_audit.py` | **VALIDATED** | Non-injective BGK collision bijectivity analysis | **YES** | Mathematical proof of kinetic mode relaxation |
| `quantum/f19_reversible_embedding.py`| **VALIDATED** | Stinespring dilation ($U\|x\rangle\|0\rangle_E = \|F(x)\rangle\|x\rangle_E$) | **YES** | Unitary permutation on enlarged state space |
| `quantum/f20_kraus.py` | **VALIDATED** | Kraus representation $K_\mu = \|F(\mu)\rangle\langle\mu\|$ | **YES** | Exact trace preservation: $\|\sum K_\mu^\dagger K_\mu - I\|_2 = 0$ |
| `quantum/f20_choi.py` | **VALIDATED** | Choi matrix $J(\mathcal{E})$ construction and audit | **YES** | Completely positive: $\lambda_{\min}(J) \ge 0$, $\text{Tr}(J)=1$ |
| `quantum/f20_channel.py` | **VALIDATED** | Quantum channel comparison engine | **YES** | Exact equivalence to statistical dephasing + BGK map |
| `quantum/f20_solver.py` | **VALIDATED** | Autonomous multi-step CPTP two-phase solver | **YES** | Validated across $T=1 \dots 16$ with 0 intermediate classical reads |
| `hardware/preflight.py` | **SUPPORTING** | Safety interlocks for real IBM QPU execution | **YES** | Prevents unintended remote quantum device jobs |
| `hardware/isa_transpile.py` | **SUPPORTING** | IBM Heavy-Hex (FakeSherbrooke) transpilation | **YES** | Hardware feasibility & gate synthesis analysis |

---

## 2. Research Architecture Classifications

1. **VALIDATED CLASSICAL**: High-fidelity reference solver (`classical/level4_two_phase.py`).
2. **VALIDATED QUANTUM KERNELS**: Exact unitary streaming, exact bounce-back boundary, direct spatial/population state preparation.
3. **VALIDATED QUANTUM CHANNEL (CPTP)**: Stinespring environmental dilation of dissipative BGK collision (`quantum/f20_*.py`).
4. **EXPERIMENTAL / FUTURE WORK**: Nonzero CSF surface tension channel integration and high-density-ratio multi-phase scaling ($\rho_L / \rho_G \ge 1000$).
