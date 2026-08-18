# Knowledge Base Dossier: Xiao et al. (Nanjing Univ & NUS, 2026)

## 1. Citation & Metadata
- **Title**: A Stable and General Quantum Fractional-Step Lattice Boltzmann Method for Incompressible Flows
- **Authors**: Yang Xiao, Liming Yang, Chang Shu, Yinjie Du
- **Year**: March 2026 (arXiv:2603.00558v1)
- **Affiliations**: Nanjing University of Aeronautics and Astronautics (Nanjing, China) & National University of Singapore (Singapore)
- **DOI / URL**: [arXiv:2603.00558](https://arxiv.org/abs/2603.00558)

---

## 2. Research Objective & Core Contribution
- **Objective**: Overcome the fundamental single-Reynolds number restriction ($\tau=1$) and high-Re instabilities in existing quantum LBM algorithms.
- **Core Contribution**:
  - Introduces a **Quantum Fractional-Step LBM (FS-LBM)**:
    - **Predictor Step (Quantum)**: Solves LBM with fixed relaxation time $\tau = 1$ on a unitary quantum circuit (no non-unitary dissipation loss or ancilla post-selection).
    - **Corrector Step (Classical)**: Applies an anti-diffusion correction via finite differences to tune the effective viscosity to arbitrary physical Reynolds numbers.
  - Achieves the **first 3D quantum LBM simulation** of incompressible thermal flows (D3Q27).
  - Develops a **duplication-based initialization circuit** reducing state preparation complexity from $\mathcal{O}(Q \cdot 2^N)$ to $\mathcal{O}(2^N)$.

---

## 3. Physical Model & Governing PDEs
- **Incompressible Navier-Stokes + Energy Equations**:
  $$ \nabla \cdot \mathbf{u} = 0 $$
  $$ \frac{\partial \mathbf{u}}{\partial t} + (\mathbf{u} \cdot \nabla) \mathbf{u} = -\nabla p + \nu \nabla^2 \mathbf{u} + \mathbf{F} $$
  $$ \frac{\partial T}{\partial t} + \mathbf{u} \cdot \nabla T = \alpha \nabla^2 T $$
- **Fractional Step Splitting**:
  - Predictor (Intermediate state $\mathbf{u}^*, T^*$ at $\tau = 1$):
    $$ \mathbf{u}^* = \sum_\alpha \mathbf{e}_\alpha f_\alpha^{eq}, \quad T^* = \sum_\alpha g_\alpha^{eq} $$
  - Corrector (Physical state $\mathbf{u}^{n+1}, T^{n+1}$):
    $$ \mathbf{u}^{n+1} = \mathbf{u}^* + \Delta t (\nu - \nu_0) \nabla^2 \mathbf{u} $$
    $$ T^{n+1} = T^* + \Delta t (\alpha - \alpha_0) \nabla^2 T $$

---

## 4. Lattice Model & Discrete Velocity Set
- **Lattices**: D2Q9 (2D) and D3Q27 (3D).
- **Qubit Allocation**:
  $$ n_{total} = n_x + n_y + n_z + n_Q + n_a $$
  where $n_d = \log_2(M_d)$ (spatial nodes), $n_Q = \lceil \log_2 Q \rceil$, and $n_a = 1$ (ancilla).

---

## 5. Quantum Circuit Architecture & Modules
1. **Initialization with Duplication Sequence**:
   - Encodes scalar density $\rho$ or temperature $T$ into spatial register $|q_x, q_y, q_z\rangle$.
   - Uses Hadamard + CNOT cascade on velocity register $|q_Q\rangle$ to duplicate spatial distribution across all $Q$ directions in $\mathcal{O}(n_Q)$ gates.
2. **Collision Circuit ($\tau = 1$)**:
   - Since $\tau = 1$, post-collision population equals equilibrium $f_\alpha^{eq}$.
   - Evaluated as unitary arithmetic / rotation gates conditioned on local velocity.
3. **Quantum Walk Streaming Operator**:
   - Implemented via controlled spatial increment/decrement arithmetic circuits (Quantum Adders/Subtracters):
     $$ |x\rangle |y\rangle |e_x, e_y\rangle \mapsto |x + e_x\rangle |y + e_y\rangle |e_x, e_y\rangle $$
4. **Macroscopic Moment Computation Circuit**:
   - Applies inverse Walsh-Hadamard / Fourier transformations to project velocity register moments into ancilla register.

---

## 6. Numerical Verification & Benchmarks
- 2D & 3D Taylor-Green vortex flows ($Re = 10 \text{ to } 1000$).
- 2D & 3D Lid-driven cavity flows ($Re = 100, 400, 1000$).
- 2D & 3D Natural convection in a cavity ($Ra = 10^3 \text{ to } 10^5, Pr = 0.71$).

---

## 7. Key Relevance to Two-Phase Dam-Break QLBM
- **High-Density Ratio & Reynolds Number Stability**: Dam-break flows operate at high Reynolds numbers ($Re \sim 10^4 - 10^5$). Standard QLBM with $\tau \to 0.5$ becomes numerically unstable; the Fractional-Step approach allows stable quantum execution at $\tau=1$ while shifting the viscosity/density-ratio correction to an efficient classical step.
- **Multiphase Decoupling**: Provides a direct roadmap for splitting the coupled hydrodynamic-phase field solver into:
  1. Quantum Unitary Predictor ($\tau_v = 1, \tau_\phi = 1$).
  2. Classical / Quantum Phase-Field & Anti-Diffusion Corrector.
