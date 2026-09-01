# TWO-PHASE QUANTUM LATTICE BOLTZMANN DAM-BREAK IMPLEMENTATION PLAN

**Author**: Lead Quantum-CFD Implementation Researcher  
**Repository**: `/home/aswa/Research/QLBM-DamBreak/`  
**Date**: 2026-08-20  

---

## 1. Audit of Existing Reusable Modules
* **Classical Core (`classical/`)**:
  * `d2q9.py`: Lattice constants $C_X, C_Y, W, CS2, \text{OPPOSITE}$.
  * `equilibrium.py`: Second-order BGK polynomial equilibrium $\rho, u \mapsto f^{\text{eq}}$.
  * `collision.py`: Single-relaxation-time collision operator with external forcing.
  * `streaming.py`: Periodic spatial streaming permutations.
  * `boundary.py`: Half-way bounce-back walls and no-slip enclosures.
* **Carleman Core (`carleman/`)**:
  * `linearize.py`, `operator.py`, `truncation.py`, `validation.py`: State lifting $x \mapsto [x, x^{\otimes 2}]$ and discrete step construction.
* **Quantum Core (`quantum/`)**:
  * `quantum/local_carleman/`: Node-level local Carleman relaxation and dynamic circuit handling.
  * `quantum/streaming.py`: Reversible spatial shift permutation oracles ($\\mathcal{O}(\\log N)$ CX).
  * `backends/`: Aer ideal/noisy, Fake IBM Eagle 127Q (`GenericBackendV2`), and IBM Quantum `SamplerV2` wrapper with dual-lock safety.

---

## 2. Reduced Two-Phase Mathematical Model
We formulate a physically grounded **Reduced Two-Phase Lattice Boltzmann Model**:
* **Phase Indicator $\phi(x, y, t) \in [0, 1]$**:
  * $\phi = 1$: Pure liquid phase ($\\rho_l = 1.0$).
  * $\phi = 0$: Pure gas phase ($\\rho_g = 0.1$).
  * $0 < \phi < 1$: Diffuse interface layer.
* **Order Parameter Advection-Diffusion**:
  $$\\partial_t \phi + \nabla \cdot (\phi u) = M \nabla^2 \mu_\phi$$
  In discrete LBM form with order-parameter distribution $g_i$:
  $$g_i(x + c_i, t + \Delta t) = g_i^*(x, t) = g_i(x, t) - \frac{1}{\tau_\phi} (g_i - g_i^{\text{eq}})$$
  $$g_i^{\text{eq}} = w_i \phi [1 + 3(c_i \cdot u)]$$
* **Hydrodynamic Momentum & Density**:
  $$\\rho(\phi) = \phi \rho_l + (1 - \phi) \rho_g$$
  $$f_i(x + c_i, t + \Delta t) = f_i^*(x, t) = f_i(x, t) - \frac{1}{\tau} (f_i - f_i^{\text{eq}}) + S_i(F_g)$$
  where $F_g = (0, g (\\rho - \rho_g))^T$ is the downward gravitational buoyancy force.

---

## 3. Quantum Architecture & Register Layout
To encode a 2D lattice ($N_x \times N_y$), 9 discrete velocities, and phase indicator:
1. **Spatial Register**:
   * $q_{x}$: $n_x = \lceil \log_2 N_x \rceil$ qubits (for $N_x=4 \implies 2$ qubits).
   * $q_{y}$: $n_y = \lceil \log_2 N_y \rceil$ qubits (for $N_y=4 \implies 2$ qubits).
2. **Velocity Register**:
   * $q_{\text{vel}}$: $4$ qubits (encoding 9 D2Q9 velocities in $|0\rangle \dots |8\rangle$).
3. **Phase Register**:
   * $q_{\text{phase}}$: $1$ qubit ($|0\rangle = \text{gas}, |1\rangle = \text{liquid}$, superposition $\alpha|0\rangle + \beta|1\rangle$ represents diffuse interface with $\phi = |\beta|^2$).
4. **Total Qubits for $4 \times 4$ Mesh**: $2 (x) + 2 (y) + 4 (\text{vel}) + 1 (\text{phase}) = 9$ qubits.

---

## 4. End-to-End Pipeline & Execution Milestones
1. **Classical Reference**: `classical/two_phase.py` and `tests/test_two_phase_classical.py`.
2. **Quantum Encoding & Initialization**: `quantum/two_phase_encoding.py` and `tests/test_two_phase_encoding.py`.
3. **Quantum Collision & Streaming**: `quantum/two_phase_collision.py`, `quantum/two_phase_boundary.py`, and `tests/test_two_phase_quantum_streaming.py`.
4. **End-to-End Quantum Step & Observable Reconstruction**: `quantum/two_phase_step.py`, `tests/test_two_phase_measurement.py`, and `tests/test_two_phase_end_to_end.py`.
5. **Driver & Multi-Backend Benchmarking**: `scripts/run_quantum_two_phase_dambreak.py` supporting `aer_ideal`, `aer_noisy`, `fake_ibm`, and `real_ibm` (dry-run gated).
