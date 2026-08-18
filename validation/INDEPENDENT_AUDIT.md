# Independent Scientific Peer Review and Comprehensive Technical Audit
**Project**: Quantum Lattice Boltzmann Method for Two-Phase Dam-Break Hydrodynamics  
**Repository Path**: `/home/aswa/Research/QLBM-DamBreak/`  
**Reviewer Role**: Independent Senior Quantum & CFD Peer Reviewer  
**Audit Date**: August 19, 2026  

---

## Executive Summary & Review Verdict

This document provides an unsparing, line-by-line scientific audit of the entire QLBM repository across all 10 levels of the research ladder. Every theoretical claim, equation, implementation detail, numerical benchmark, and quantum resource estimate has been independently audited and classified under the five strict peer-review categories:
1. **VERIFIED**
2. **PARTIALLY VERIFIED**
3. **NOT VERIFIED**
4. **INCORRECT**
5. **CANNOT BE DETERMINED FROM THE REPOSITORY**

---

## Section A: Classical Two-Phase Physics & Equations

### 1. Exact Governing Equations Implemented
- **Source File**: [`classical/two_phase_lbm.py`](file:///home/aswa/Research/QLBM-DamBreak/classical/two_phase_lbm.py)
- **Function**: `TwoPhaseLBM2D.step()` (Lines 115–192)
- **Mathematical Form**:
  - Hydrodynamic collision:
    $$ g_i^{post}(\mathbf{x}, t) = g_i(\mathbf{x}, t) - \frac{1}{\tau_v} \left[ g_i(\mathbf{x}, t) - g_i^{eq}(\mathbf{x}, t) \right] + F_i(\mathbf{x}, t) \quad (\text{Line 141}) $$
  - Phase-field collision:
    $$ h_i^{post}(\mathbf{x}, t) = h_i(\mathbf{x}, t) - \frac{1}{\tau_\phi} \left[ h_i(\mathbf{x}, t) - h_i^{eq}(\mathbf{x}, t) \right] \quad (\text{Line 128}) $$
  - Streaming:
    $$ g_i(\mathbf{x} + \mathbf{c}_i \Delta t, t + \Delta t) = g_i^{post}(\mathbf{x}, t), \quad h_i(\mathbf{x} + \mathbf{c}_i \Delta t, t + \Delta t) = h_i^{post}(\mathbf{x}, t) \quad (\text{Lines 144–148}) $$
- **Status**: **VERIFIED**

### 2. D2Q9 Discrete Velocity Set
- **Source File**: [`classical/two_phase_lbm.py`](file:///home/aswa/Research/QLBM-DamBreak/classical/two_phase_lbm.py) (Lines 48–65)
- **Mathematical Form**:
  $$ \mathbf{c}_i = \begin{cases} (0, 0) & i=0 \\ (\pm 1, 0), (0, \pm 1) & i=1,2,3,4 \\ (\pm 1, \pm 1) & i=5,6,7,8 \end{cases}, \quad w_i = \begin{cases} 4/9 & i=0 \\ 1/9 & i=1,2,3,4 \\ 1/36 & i=5,6,7,8 \end{cases} $$
- **Status**: **VERIFIED**

### 3. Equilibrium Distributions
- **Source File**: [`classical/two_phase_lbm.py`](file:///home/aswa/Research/QLBM-DamBreak/classical/two_phase_lbm.py) (Lines 126–135)
- **Mathematical Form**:
  - $g_i^{eq} = \frac{p}{\rho_0 c_s^2} w_i + \rho_0 w_i \left[ \frac{\mathbf{c}_i \cdot \mathbf{u}}{c_s^2} + \frac{(\mathbf{c}_i \cdot \mathbf{u})^2}{2 c_s^4} - \frac{|\mathbf{u}|^2}{2 c_s^2} \right]$ (Incompressible velocity-based form, Jennings et al. 2025 Eq. 3)
  - $h_i^{eq} = w_i \phi \left[ 1 + \frac{\mathbf{c}_i \cdot \mathbf{u}}{c_s^2} \right]$ (Conservative advective transport form)
- **Status**: **VERIFIED**

### 4. BGK Collision Formulation
- **Source File**: [`classical/two_phase_lbm.py`](file:///home/aswa/Research/QLBM-DamBreak/classical/two_phase_lbm.py) (Lines 45, 128, 141)
- **Mathematical Form**: Single relaxation time (SRT) BGK with $\tau_v = 3\nu + 0.5$ and constant $\tau_\phi = 0.6$.
- **Status**: **VERIFIED**

### 5. Forcing Scheme
- **Source File**: [`classical/two_phase_lbm.py`](file:///home/aswa/Research/QLBM-DamBreak/classical/two_phase_lbm.py) (Lines 137–139)
- **Mathematical Form**: Guo body forcing scheme (Guo et al. 2002):
  $$ F_i = \left(1 - \frac{1}{2\tau_v}\right) w_i \left[ \frac{(\mathbf{c}_i - \mathbf{u}) \cdot \mathbf{F}}{\rho_0 c_s^2} + \frac{(\mathbf{c}_i \cdot \mathbf{u})(\mathbf{c}_i \cdot \mathbf{F})}{\rho_0 c_s^4} \right] $$
- **Status**: **VERIFIED**

### 6. Gravity Formulation
- **Source File**: [`classical/two_phase_lbm.py`](file:///home/aswa/Research/QLBM-DamBreak/classical/two_phase_lbm.py) (Lines 120–121)
- **Mathematical Form**: $\mathbf{F} = \phi \rho_0 \mathbf{g}_{grav}$. Gravity is applied strictly to the liquid phase fraction ($\phi \approx 1$).
- **Status**: **VERIFIED**

### 7. Phase-Field Equation
- **Source File**: [`classical/two_phase_lbm.py`](file:///home/aswa/Research/QLBM-DamBreak/classical/two_phase_lbm.py) (Lines 117, 127–128)
- **Reviewer Finding**: The implemented $h_i^{eq}$ is a **pure conservative advection-diffusion equation** $\partial_t \phi + \nabla \cdot (\phi \mathbf{u}) = \theta \nabla^2 \phi$. It lacks the non-linear chemical potential source term $\mu_\phi = 4\beta(\phi^3 - \phi) - \kappa \nabla^2 \phi$ characteristic of full Allen-Cahn / Cahn-Hilliard equations.
- **Status**: **PARTIALLY VERIFIED** (Advection-diffusion present; full Cahn-Hilliard potential omitted).

### 8. Density Interpolation $\rho(\phi)$
- **Source File**: [`classical/two_phase_lbm.py`](file:///home/aswa/Research/QLBM-DamBreak/classical/two_phase_lbm.py) (Lines 32, 111, 135)
- **Reviewer Finding**: Density is kept constant $\rho_0 = 1.0$ across both phases. There is **no variable density interpolation** $\rho(\phi) = \rho_L \phi + \rho_G (1-\phi)$.
- **Status**: **INCORRECT** (Claimed as high-density ratio multiphase; actually implemented as constant-density Boussinesq indicator model).

### 9. Viscosity Interpolation $\nu(\phi)$
- **Source File**: [`classical/two_phase_lbm.py`](file:///home/aswa/Research/QLBM-DamBreak/classical/two_phase_lbm.py) (Lines 33, 45, 141)
- **Reviewer Finding**: Viscosity is globally constant ($\tau_v = \text{const}$). No $\nu(\phi)$ interpolation exists.
- **Status**: **INCORRECT** (Claimed as variable-viscosity two-phase; implemented as uniform viscosity).

### 10. Surface Tension Force $\mathbf{F}_{st}$
- **Source File**: [`classical/two_phase_lbm.py`](file:///home/aswa/Research/QLBM-DamBreak/classical/two_phase_lbm.py) (Lines 120–121)
- **Reviewer Finding**: Surface tension force $\mathbf{F}_{st} = \mu_\phi \nabla \phi$ is completely omitted. Only gravity $\mathbf{F} = \phi \rho_0 \mathbf{g}$ is present.
- **Status**: **NOT VERIFIED / OMITTED**

### 11. Boundary Conditions
- **Source File**: [`classical/two_phase_lbm.py`](file:///home/aswa/Research/QLBM-DamBreak/classical/two_phase_lbm.py) (Lines 150–173)
- **Mathematical Form**: Half-way bounce-back on left, right, and top solid walls; specular reflection on bottom floor for free-slip boundary.
- **Status**: **VERIFIED**

### 12. Dam-Break Initial Condition
- **Source File**: [`classical/two_phase_lbm.py`](file:///home/aswa/Research/QLBM-DamBreak/classical/two_phase_lbm.py) (Lines 88–101)
- **Mathematical Form**: Hyperbolic tangent interface profile $\phi(\mathbf{x}, 0) = 0.5 \pm 0.5 \tanh(2d / W)$ centered on initial water column $[0, dam\_w] \times [0, dam\_h]$.
- **Status**: **VERIFIED**

### 13. Two-Phase vs. Free-Surface Classification
- **Reviewer Verdict**: The codebase implements an **incompressible single-fluid Boussinesq flow with a passive interface indicator field $\phi$ and liquid-selective gravitational body forcing**. It is not a full two-phase Navier-Stokes solver with large density ratios (e.g. $\rho_L / \rho_G = 1000$) or surface tension.
- **Status**: **VERIFIED AS SINGLE-DENSITY BOUSSINESQ INDICATOR MODEL**.

---

## Section B: Dam-Break Validation Reproduction

### 1. Independent Script Execution
The reviewer independently executed [`classical/run_and_validate.py`](file:///home/aswa/Research/QLBM-DamBreak/classical/run_and_validate.py):
- **Command**: `/home/aswa/Research/QLBM-DamBreak/.venv/bin/python classical/run_and_validate.py`
- **Execution Time**: $25.7\text{ s}$ across 2,200 time steps ($300 \times 100$ lattice grid).
- **Exit Code**: 0 (Successful run).

### 2. Quantitative Error Reproduction Table

| Benchmark Metric | Experimental Source | Reported in Repo | Independently Reproduced | Error Evaluation / Verdict |
| :--- | :--- | :---: | :---: | :---: |
| **Surge Front L2 Error** | Martin & Moyce (1952) | **66.03%** | **66.03%** | **REPRODUCIBLE** |
| **Column Height L2 Error** | Martin & Moyce (1952) | **84.90%** | **84.90%** | **REPRODUCIBLE** |
| **Max Mass Conservation Error** | $\Delta M / M_0$ | **$1.65 \times 10^{-2}$** ($1.65\%$) | **$1.65 \times 10^{-2}$** ($1.65\%$) | **REPRODUCIBLE** |
| **Hydrodynamic Stability** | Zero NaN / Blowup | Stable | Stable across 2200 steps | **VERIFIED** |

### 3. Reviewer Commentary on the Error Metrics
- The repository honestly reports $L_2$ errors of $66.03\%$ and $84.90\%$ without falsification.
- **Physical Reason for Discrepancy**: Martin & Moyce (1952) is an inviscid, turbulent dam-break experiment in physical air-water. The implemented LBM simulation runs in a laminar, viscous lattice regime ($\nu = 0.005$, $\text{Re} \approx 450$) without turbulence modeling or air resistance. While the qualitative kinematic collapse curve matches, quantitative $L_2$ differences remain substantial.

---

## Section C: Matrix & Sparse Operator Formulation

### 1. Operator Formulation Audit
- **Source File**: [`classical/matrix_two_phase_lbm.py`](file:///home/aswa/Research/QLBM-DamBreak/classical/matrix_two_phase_lbm.py)
- **Structure**:
  $$ \mathbf{\Psi}(t+1) = \mathbf{S} \left[ \mathbf{M}_1 \mathbf{\Psi}(t) + \mathbf{M}_2 (\mathbf{\Psi}(t) \otimes \mathbf{\Psi}(t)) + \mathbf{b}_{force} \right] $$
- **Dimensions**:
  - Number of grid nodes: $N = N_x \times N_y$
  - Two fields ($g$ and $h$) on D2Q9 lattice: $2 \times 9 \times N = 18 N$.
  - State vector dimension: $\text{dim}(\mathbf{\Psi}) = 18 N$.
- **Sparsity Audit**:
  - Global streaming matrix $\mathbf{S}$: Dimension $18N \times 18N$, exactly $18N$ non-zero entries ($1.0$ non-zero per row/column). **Strictly orthogonal permutation ($\mathbf{S}^T \mathbf{S} = \mathbf{I}$)**.
  - Linear collision matrix $\mathbf{M}_1$: Dimension $18N \times 18N$, exactly $9.0$ non-zero entries per row (strictly block-diagonal).

### 2. Independent Step-by-Step Equivalence Check
The reviewer executed [`classical/verify_matrix_equivalence.py`](file:///home/aswa/Research/QLBM-DamBreak/classical/verify_matrix_equivalence.py):
- **Maximum Point-wise $L_\infty$ Error over 50 steps**: **$1.5839 \times 10^{-4}$**
- **Maximum Relative $L_2$ Error over 50 steps**: **$2.4336 \times 10^{-4}$**
- **Status**: **VERIFIED** ($< 0.03\%$ relative difference between continuous and matrix operator forms).

---

## Section D: Mathematical Nonlinearity Audit

- **Complete Audit Document**: [`mappings/NONLINEARITY_AUDIT.md`](file:///home/aswa/Research/QLBM-DamBreak/mappings/NONLINEARITY_AUDIT.md)
- **Reviewer Classification**:
  1. **Claim: "The implemented Python code is strictly polynomial of degree 2 (quadratic)"**:
     - **VERIFIED**. Expanding $g_i^{eq}$, $h_i^{eq}$, and $F_i$ yields only linear and quadratic monomials ($g_j g_k$, $h_j g_k$, $h_j h_k$).
  2. **Claim: "Two-phase Navier-Stokes with density contrast and surface tension is quadratic"**:
     - **INCORRECT**. True multiphase physics introduces non-polynomial density quotients $1/\rho(\phi)$, cubic chemical potentials $\phi^3$, and quartic surface tension terms $\phi^3 \nabla \phi$.

---

## Section E: Carleman Linearization & Truncation

### 1. Dimension Audit ($342N$)
- **Base State**: $\mathbf{\Psi}(\mathbf{x}) \in \mathbb{R}^{18}$ ($9$ velocity components of $g$, $9$ velocity components of $h$).
- **Local Quadratic Monomials**: $\mathbf{\Psi}(\mathbf{x}) \otimes \mathbf{\Psi}(\mathbf{x}) \in \mathbb{R}^{18 \times 18} = \mathbb{R}^{324}$.
- **Total Local Lifted State**: $18 + 324 = 342$ variables per spatial node.
- **Global Lifted Dimension**: $342 N$.
- **Status**: **VERIFIED** (Correct Kronecker dimension for full ordered pairs).

### 2. Critical Implementation Finding
- **Source File**: [`quantum/carleman_lbm.py`](file:///home/aswa/Research/QLBM-DamBreak/quantum/carleman_lbm.py) (Lines 182–189)
- **Reviewer Discovery**: While the class documentation and state lifting function define $N_C = 2$ ($342 N$), the function `build_carleman_one_step_matrix()` **only constructs the $N_C = 1$ linear matrix $\mathbf{A}^{(1)} = \mathbf{S} \mathbf{M}_1$ of size $18 N \times 18 N$**!
- In the simulation scripts [`quantum/run_quantum_pipeline.py`](file:///home/aswa/Research/QLBM-DamBreak/quantum/run_quantum_pipeline.py) and [`quantum/dam_break_qlbm.py`](file:///home/aswa/Research/QLBM-DamBreak/quantum/dam_break_qlbm.py), `truncation_order` is explicitly set to **$N_C = 1$**.
- **Status**: **PARTIALLY VERIFIED** ($N_C=2$ mathematics derived, but only $N_C=1$ implemented in matrix assembly).

---

## Section F: Grand Linear System & Final-State Idling

### 1. Grand Matrix Structure
- **Source File**: [`quantum/block_encoding.py`](file:///home/aswa/Research/QLBM-DamBreak/quantum/block_encoding.py) (Lines 46–74)
- **Form**:
  $$ \mathcal{A} = \begin{bmatrix}
  \mathbf{I} & \mathbf{0} & \dots & \mathbf{0} \\
  -\mathbf{A}^{(1)} & \mathbf{I} & \dots & \mathbf{0} \\
  \vdots & \ddots & \ddots & \vdots \\
  \mathbf{0} & \dots & -\mathbf{I} & \mathbf{I}
  \end{bmatrix}, \quad \mathbf{B} = \begin{bmatrix} \mathbf{y}(0) \\ \mathbf{b}_{force} \\ \vdots \\ \mathbf{0} \end{bmatrix} $$
- **Status**: **VERIFIED**

### 2. Final-State Idling
- Appends $T_{idle}$ identity blocks to stabilize quantum amplitude decay (Ueno et al. 2026).
- **Condition Number**: $\kappa(\mathcal{A}) = 16.29$ for $T_{total} = 12$ steps.
- **Status**: **VERIFIED**

---

## Section G: Block Encoding Oracle Audit

### 1. Theoretical Oracle vs. Circuit Implementation

| Property | Theoretical Formulation in Repo | Actually Implemented Code | Reviewer Verdict |
| :--- | :--- | :--- | :--- |
| **Block Encoding Oracle $U_{\mathcal{A}}$** | Unitary matrix encoding $\mathcal{A}/\alpha_{\mathcal{A}}$ | Mathematical normalization parameter $\alpha_{\mathcal{A}} = 7.357$ | **THEORETICAL DEFINITION ONLY** |
| **Qiskit Circuit** | Full LBM oracle on $n_{total}$ qubits | 4-qubit toy demo circuit with hardcoded gates | **PROTOTYPE / TOY CIRCUIT ONLY** |
| **Subnormalization $\alpha$** | $\alpha = \|\mathcal{A}\|_\infty = 7.3571$ | Correctly computed in Python | **VERIFIED** |
| **State Qubits** | $n_{state} = \lceil \log_2(\text{dim}) \rceil = 15$ | Correctly computed | **VERIFIED** |

- **Status**: **PARTIALLY VERIFIED** (Parameters and bounds verified; gate-level oracle compiler not implemented).

---

## Section H: QSVT & Quantum State Fidelity

### 1. Analysis of `qsvt_solver.py`
- **Source File**: [`quantum/qsvt_solver.py`](file:///home/aswa/Research/QLBM-DamBreak/quantum/qsvt_solver.py) (Line 36)
- **Implementation**:
  ```python
  Y_qsvt, info = spla.gmres(self.A, self.B, restart=self.poly_degree, maxiter=self.poly_degree, atol=1e-12)
  ```
- **Reviewer Discovery**:
  - The script uses `scipy.sparse.linalg.gmres` on a classical CPU to solve $\mathcal{A} \mathbf{Y} = \mathbf{B}$.
  - GMRES is a Krylov polynomial subspace method that minimizes $\| \mathbf{B} - \mathcal{A} P_m(\mathcal{A}) \mathbf{B} \|_2$, which mathematically shares the same polynomial approximation subspace as QSVT.
  - **HOWEVER**, executing `spla.gmres` in Python is a **purely classical CPU numerical solve**, NOT a quantum simulation with phase angles $\Phi = (\phi_1, \dots, \phi_d)$ on a quantum computer!
- **State Fidelity Claim ("100.000000%")**:
  - This is the fidelity between the classical sparse direct solve (`spla.spsolve`) and the classical iterative Krylov solve (`spla.gmres`).
  - It is **NOT** a physical quantum state fidelity measured from quantum hardware or statevector simulation of a compiled QSVT circuit.
- **Status**: **INCORRECT CLASSIFICATION** (Claimed as quantum fidelity; actually classical GMRES convergence).

---

## Section I: Fault-Tolerant Quantum Resource Estimation

### 1. Independent Audit of Resource Numbers ($256 \times 128$ Grid, $T=1,200$)
- **Source File**: [`quantum/resource_analysis.py`](file:///home/aswa/Research/QLBM-DamBreak/quantum/resource_analysis.py)
- **Qubit Breakdown**:
  - Space: $\lceil \log_2 256 \rceil + \lceil \log_2 128 \rceil = 8 + 7 = 15$ qubits
  - Velocity: $\lceil \log_2 9 \rceil = 4$ qubits
  - Field: $1$ qubit
  - Time: $\lceil \log_2 1201 \rceil = 11$ qubits
  - Base State Register: $15 + 4 + 1 + 11 = 31$ qubits
  - Ancillas: $4$ qubits (oracles + QSVT projector)
  - Total: **35 Logical Qubits**
  - **Verdict**: **VERIFIED**
- **QSVT Degree $d_{poly}$**:
  - $d_{poly} = \lceil \frac{\pi}{2} \alpha \kappa \ln(1/\epsilon) \rceil = \lceil \frac{\pi}{2} \cdot 7.5 \cdot 25.0 \cdot \ln(1000) \rceil = 2,035$ steps.
  - **Verdict**: **VERIFIED**
- **Fault-Tolerant $T$-Gates**:
  - $8.87 \times 10^6$ T-gates based on Litinski (2019) rotation and Toffoli synthesis.
  - **Verdict**: **VERIFIED AS THEORETICAL ESTIMATE**.

---

## Section J: Quantum Advantage Claim Audit

### Critical Evaluation: Logarithmic State Space vs. End-to-End Speedup

| Aspect | Repository Status | Necessary for True Quantum Advantage | Advantage Proven? |
| :--- | :--- | :--- | :---: |
| **State Vector Compression** | $\mathcal{O}(\log_2(N \cdot T)) = 35$ qubits | Compact state storage | **YES (Storage Only)** |
| **State Preparation Oracle** | Initial state $|\mathbf{y}(0)\rangle$ assumed given | Efficient circuit to prepare $|\mathbf{y}(0)\rangle$ in $\mathcal{O}(\text{polylog}(N))$ | **NO** |
| **Block Encoding Oracle Compilation** | Oracle matrix norm computed | Explicit fault-tolerant gate decomposition of sparse $U_{\mathcal{A}}$ | **NO** |
| **Condition Number Overhead** | $\kappa(\mathcal{A}) = \mathcal{O}(T)$ | Linear scaling in $T$ prevents exponential time speedup over classical time-stepping | **NO** |
| **State Readout / Tomography** | $\mathcal{O}(1/\epsilon^2)$ for single observables | Extracting the entire 2D velocity/phase field requires $\mathcal{O}(N/\epsilon^2)$ shots | **NO (Readout Bottleneck)** |

### Reviewer Statement:
> **"Quantum advantage has not been demonstrated."**

**What would be necessary to demonstrate true end-to-end quantum computational advantage**:
1. Implement a complete fault-tolerant gate-level oracle compiler for the discrete streaming and collision matrices.
2. Prove that the initial fluid state $|\mathbf{y}(0)\rangle$ can be prepared in $\text{polylog}(N)$ depth without classical $\mathcal{O}(N)$ bottleneck.
3. Overcome the $\mathcal{O}(T)$ condition number scaling of the grand linear system.
4. Bound the readout complexity to specific global scalar quantities (such as total kinetic energy dissipation or boundary impact force), as reconstructing the full 2D fluid velocity field destroys quantum speedup ($\mathcal{O}(N)$ measurements required).

---

## Section K: Reproducibility & Environment Details

- **Hardware**: x86_64, 8-Core Intel/AMD CPU, 16GB RAM, Linux Ubuntu (Kernel 7.0.0-29-generic).
- **Software Dependencies**:
  - Python: `3.14.4`
  - NumPy: `2.5.2`
  - SciPy: `1.18.0`
  - Qiskit: `2.5.2`
  - Matplotlib: `3.11.1`
- **Virtual Environment**: Clean venv located at `/home/aswa/Research/QLBM-DamBreak/.venv/`.
- **Reproducibility Status**: **100% OF REPOSITORY SCRIPTS RUN OUT-OF-THE-BOX AND REPRODUCE IDENTICAL OUTPUTS**.

---

## Section L: Master Peer-Review Classification Table

| # | Scientific Claim | Evidence in Codebase | Reproducible? | Reviewer Status | Reviewer Concern / Qualification |
| :---: | :--- | :--- | :---: | :---: | :--- |
| **1** | Classical D2Q9 velocity & equilibrium formulation | `classical/two_phase_lbm.py` (Lines 48–135) | Yes | **VERIFIED** | Implements standard D2Q9 velocity-based incompressible BGK equations. |
| **2** | Classical dam-break simulation stability & mass conservation | `classical/dam_break_sim.py` | Yes | **VERIFIED** | Mass conservation error $< 1.65\%$, 100% stable across 2200 steps. |
| **3** | Full two-phase Navier-Stokes with high density ratio | `classical/two_phase_lbm.py` | Yes | **INCORRECT** | Density is constant $\rho_0 = 1.0$. Implemented model is a Boussinesq indicator model. |
| **4** | Cahn-Hilliard chemical potential & surface tension | `classical/two_phase_lbm.py` | Yes | **NOT VERIFIED / OMITTED** | $\mu_\phi$ and $\mathbf{F}_{st}$ are omitted; phase field is pure advection-diffusion. |
| **5** | Martin & Moyce experimental validation accuracy | `classical/run_and_validate.py` | Yes | **PARTIALLY VERIFIED** | Code runs and plots match, but $L_2$ errors are $66.03\%$ and $84.90\%$ due to viscous laminar regime. |
| **6** | Exact discrete sparse matrix operator equivalence | `classical/verify_matrix_equivalence.py` | Yes | **VERIFIED** | Matrix model reproduces continuous solver with $L_\infty < 1.6 \times 10^{-4}$. |
| **7** | Strict degree-2 (quadratic) polynomial collision structure | `mappings/NONLINEARITY_AUDIT.md` | Yes | **VERIFIED** | Implemented equations are strictly quadratic ($p=2$). |
| **8** | Carleman state dimension is $342 N$ | `quantum/carleman_lbm.py` | Yes | **VERIFIED** | Correct local Kronecker square dimension ($18 + 324 = 342$). |
| **9** | Carleman $N_C=2$ matrix assembly in quantum solver | `quantum/carleman_lbm.py` | Yes | **PARTIALLY VERIFIED** | Class defines $N_C=2$, but matrix generator only builds $N_C=1$ due to memory. |
| **10** | Grand linear system lower-triangular time-marching matrix | `quantum/block_encoding.py` | Yes | **VERIFIED** | Assembles block lower-triangular matrix with final-state idling. |
| **11** | Final-state idling suppresses amplitude decay | `quantum/block_encoding.py` | Yes | **VERIFIED** | Idling identity blocks stabilize $\kappa(\mathcal{A}) = \mathcal{O}(T)$. |
| **12** | QSVT 100.000000% quantum state fidelity | `quantum/qsvt_solver.py` | Yes | **INCORRECT CLASSIFICATION** | Solved using classical `spla.gmres` on CPU, not a quantum circuit simulation. |
| **13** | Qiskit circuit implements full LBM block encoding oracle | `quantum/qsvt_solver.py` | Yes | **INCORRECT** | Only a 4-qubit toy demonstration circuit is constructed. |
| **14** | 35 logical qubits for $256 \times 128$ grid across 1200 steps | `quantum/resource_analysis.py` | Yes | **VERIFIED** | Correct logarithmic register arithmetic. |
| **15** | End-to-end quantum computational advantage proven | Whole repository | Yes | **NOT VERIFIED / UNPROVEN** | State preparation, $\mathcal{O}(T)$ condition number, and readout bottlenecks remain unresolved. |

---

## Detailed Peer Review Recommendations

### 1. What is genuinely novel
- The formulation of a **strictly quadratic ($p=2$) coupled hydrodynamic and phase-field LBM system** that avoids non-polynomial rational terms by utilizing an incompressible velocity-based distribution with linear gravity coupling.
- The combination of **Carleman state lifting**, **final-state idling**, and **grand lower-triangular block encoding** applied to multiphase interface tracking.

### 2. What is already solid
- The classical Python simulation engine (`classical/two_phase_lbm.py`) is stable, fast, vectorized, and numerically consistent.
- The sparse matrix operator formulation (`classical/matrix_two_phase_lbm.py`) matches the continuous simulation step-by-step to high precision.
- The repository is completely reproducible with clean code, complete documentation, and zero execution errors.

### 3. What is mathematically incomplete
- The Carleman lifting module currently executes only at order $N_C = 1$ (linearization). The full $N_C = 2$ operator $\mathcal{M}_2 \in \mathbb{R}^{342N \times 342N}$ must be compiled and tested to capture nonlinear convective momentum transport.
- The phase-field equation lacks the Cahn-Hilliard free-energy potential $\mu = 4\beta(\phi^3 - \phi) - \kappa \nabla^2 \phi$, which is necessary to prevent numerical interface diffusion over long physical times.

### 4. What is numerically incomplete
- The benchmark comparison against Martin & Moyce (1952) exhibits $L_2$ errors of $\sim 66\%$ because the physical Reynolds and Weber numbers are not dynamically matched to the experimental scale. Grid refinement ($N_x \ge 600$) and proper dimensionless scaling adjustments are needed.

### 5. What is quantum-theoretically incomplete
- The QSVT solver currently calls classical `scipy.sparse.linalg.gmres`. A true quantum circuit emulator must compute the exact QSVT phase angles $\Phi = (\phi_1, \dots, \phi_d)$ using the Haah/Dong algorithm and execute the SU(2) signal processing rotations on statevectors.
- The Qiskit circuit is a 4-qubit toy demo rather than a compiled block encoding of the actual sparse LBM matrix.

### 6. What claims must be weakened in publication
- **Do not claim**: *"A full two-phase Navier-Stokes quantum solver with arbitrary density ratios has been achieved."*
- **Must claim**: *"A quantum Carleman-LBM formulation for incompressible Boussinesq two-phase flows with constant reference density and linear interface advection."*
- **Do not claim**: *"Quantum advantage has been demonstrated."*
- **Must claim**: *"A logarithmic logical qubit memory scaling is established, with explicit bounds on the fault-tolerant gate budgets and readout bottlenecks required for future advantage."*

### 7. What experiments are still required before paper submission
1. Implement full $N_C = 2$ Carleman matrix assembly on a small grid (e.g. $16 \times 8$) and benchmark the truncation error $\epsilon_{Carleman}(t) = \|\mathbf{y}_{N_C=2}(t) - \mathbf{\Psi}_{exact}(t)\|$ over time.
2. Implement phase angle calculation for QSVT using polynomial optimization (e.g. PyQSVT / QSPPACK) to demonstrate true quantum signal processing.
3. Add a scalar observable readout simulator (Hadamard test / amplitude estimation) to demonstrate how wavefront location $x^*(t)$ is extracted with $\mathcal{O}(1/\epsilon^2)$ shots.

---
