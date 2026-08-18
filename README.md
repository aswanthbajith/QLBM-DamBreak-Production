# Quantum Lattice Boltzmann Method (QLBM) for Two-Phase Dam-Break Hydrodynamics

A rigorous research and development framework for transforming classical multiphase Lattice Boltzmann Method (LBM) simulations into quantum-compatible algorithms (Carleman linearization, block encoding, QSVT, and quantum linear systems algorithms).

---

## 1. Research Objectives

1. **Classical Benchmark**: Formulate, implement, and validate a classical two-phase LBM dam-break simulation based on conservative phase-field interface tracking and velocity-based LBM (e.g., Watanabe & Hu 2026, OpenLB/OpenFOAM baselines).
2. **Mathematical Vector/Matrix Abstraction**: Systematically decouple linear streaming operators ($\mathbf{S}$) and local nonlinear collision operators ($\mathbf{C}(\mathbf{f}, \phi)$), characterizing all polynomial and non-polynomial nonlinearities.
3. **Carleman Linearization**: Apply $k$-th order Carleman linearization to lift nonlinear differential/algebraic discrete Boltzmann equations into a finite-dimensional linear system.
4. **Quantum Encoding & QSVT Mapping**: Construct block encodings for the lifted Carleman system and formulate Quantum Linear System Algorithms (QLSA / QSVT) for time-marching hydrodynamic states.
5. **Resource & Complexity Analysis**: Rigorously quantify qubit counts, circuit depths, condition number scaling $\kappa(T)$, Carleman truncation errors, and quantum state readout/tomography bottlenecks.

---

## 2. Research Ladder (Level 0 – Level 9)

```
LEVEL 0: Physics (Two-Phase Incompressible Navier-Stokes + Phase-Field Cahn-Hilliard / Allen-Cahn)
   │
   ▼
LEVEL 1: Classical Two-Phase LBM Formulation (Velocity-Based / Pressure-Evolution D2Q9 & D3Q27)
   │
   ▼
LEVEL 2: Classical Dam-Break Benchmark & Validation (Wavefront evolution, obstacle impact pressure)
   │
   ▼
LEVEL 3: Exact Vector & Matrix Representation (Separation of local collision and nonlocal streaming)
   │
   ▼
LEVEL 4: Rigorous Nonlinearity Classification (Kinetic flux, cubic chemical potential, forcing)
   │
   ▼
LEVEL 5: Carleman Linearization & Truncation (Tensor product states y = [f, f⊗f, ...]^T)
   │
   ▼
LEVEL 6: Grand Linear System Construction & Block Encoding (A x = b, sparsity, oracles)
   │
   ▼
LEVEL 7: Quantum State Evolution via QSVT / QLSA (Polynomial eigenvalue transformation)
   │
   ▼
LEVEL 8: Two-Phase Dam-Break QLBM Framework (State vector |f, φ⟩, interface evolution)
   │
   ▼
LEVEL 9: Quantum Resource, Error & Complexity Bounds (Condition number, T-gates, NISQ vs. FTQC)
```

---

## 3. Directory Structure

```
QLBM-DamBreak/
├── README.md                          # Project overview and research roadmap
├── papers/                            # Repository for source research papers (PDFs)
│   ├── classical/                     # Foundational LBM papers (D2Q9/D3Q27, MRT, boundary conditions)
│   ├── multiphase/                    # Two-phase, phase-field, color-gradient, Shan-Chen papers
│   ├── dam_break/                     # Dam-break experimental benchmarks and numerical validations
│   └── quantum/                       # QLBM, Carleman linearization, QSVT, quantum collision operators
├── knowledge/                         # Structured paper extraction markdown dossiers
├── equations/                         # Canonical equation sets and symbol registries
│   ├── classical_lbm.md               # Standard single-phase LBM equations
│   ├── two_phase_model.md             # Velocity-based & phase-field two-phase LBM
│   ├── phase_field.md                 # Cahn-Hilliard / conservative Allen-Cahn interface equations
│   ├── dam_break.md                   # Benchmark geometries, dimensionless numbers (Re, We, Fr)
│   └── qlbm.md                        # Quantum formulations and state definitions
├── mappings/                          # Mathematical transformations
│   ├── classical_to_matrix.md         # Discrete operator matrix representations
│   ├── nonlinear_terms.md             # Classification of nonlinear terms (quadratic, cubic, rational)
│   ├── carleman.md                    # Carleman lifting matrices and truncation error analysis
│   └── quantum_encoding.md            # Block encoding, oracle specifications, and state preparation
├── classical/                         # Classical reference implementations (Python / C++)
├── quantum/                           # Quantum circuit models, QSVT polynomial approximations, Carleman solvers
└── validation/                        # Comparative benchmark logs, pressure curves, and error metrics
```

---

## 4. Paper Extraction Protocol

When a PDF is placed in `papers/`, the paper-analysis agent extracts the following structured profile into `knowledge/<paper_identifier>.md`:

1. **Citation & Metadata** (Authors, Year, Journal, DOI)
2. **Research Objective & Core Contribution**
3. **Physical Model & Governing PDEs**
4. **Lattice Discrete Velocity Set & Weight Vectors** ($D_d Q_q$)
5. **Equilibrium Distribution Functions** ($f_i^{eq}$)
6. **Collision & Relaxation Mechanics** (SRT, TRT, MRT, Entropic)
7. **Streaming & Advection Operator**
8. **Multiphase & Interface Capturing Model** (Phase field, chemical potential, surface tension)
9. **Forcing Schemes** (Guo, He, Shan-Chen force terms)
10. **Boundary Conditions** (Bounce-back, wet-node, free-slip, non-equilibrium extrapolation)
11. **Dam-Break Setup & Benchmark Metrics** (Domain, grid size, liquid column dimensions, sensor positions)
12. **Nonlinear vs. Linear Term Catalog** (Explicit categorization of each mathematical expression)
13. **Carleman Linearization Mapping Suitability**
14. **Quantum Encoding & Algorithmic Relevance**
15. **Known Limitations & Classical/Quantum Bottlenecks**

---

## 5. Mathematical Notation Standards

- Discrete velocity directions: $i \in \{0, 1, \dots, Q-1\}$ with lattice velocities $\mathbf{c}_i$.
- Hydrodynamic distribution functions: $f_i(\mathbf{x}, t)$.
- Order parameter / phase field: $\phi(\mathbf{x}, t)$ or index distribution $g_i(\mathbf{x}, t)$.
- Macroscopic velocity: $\mathbf{u}(\mathbf{x}, t) = \frac{1}{\rho}\sum_i f_i \mathbf{c}_i$.
- Carleman lifted state vector: $\mathbf{y}(t) = \bigoplus_{k=1}^K \mathbf{f}^{\otimes k}(t) \in \mathbb{R}^{\sum_{k=1}^K N^k}$.
- Quantum state: $|\Psi(t)\rangle \propto \sum_j y_j(t) |j\rangle$.
