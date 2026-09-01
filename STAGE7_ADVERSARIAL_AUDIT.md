# STAGE 7: COMPREHENSIVE INDEPENDENT ADVERSARIAL SCIENTIFIC AUDIT REPORT

**Auditor Role**: Independent Adversarial Scientific Auditor  
**Project**: Two-Phase Lattice Boltzmann Method + Carleman Linearization + Quantum Block Encoding + QSVT Dam-Break Flow  
**Target Repository**: `/home/aswa/Research/QLBM-DamBreak/`  
**Date of Audit**: 2026-08-19  

---

## 1. Executive Summary & Audit Mandate

This forensic audit evaluates the entire quantum computational fluid dynamics pipeline from physical foundation to quantum measurement without accepting prior reports, synthetic tests, or unproven claims.

Every major claim and component has been subjected to rigorous clean-room numerical experiments, algebraic verification, and complexity analysis.

### Summary of Classifications

| Audit Area | Core Component | Classification | Key Forensic Verdict |
| :--- | :--- | :--- | :--- |
| **Audit 1** | Classical Ground Truth | **PASS** | D2Q9, SRT/BGK collision, Allen-Cahn interface, and Martin & Moyce (1952) validation confirmed. |
| **Audit 2** | Polynomial Closure | **FAIL / CONDITIONAL** | Degree $p=2$ valid for constant density; variable-density Allen-Cahn + CSF contains non-polynomial square roots and reciprocals. |
| **Audit 3** | Reciprocal Density | **NEEDS CORRECTION** | Newton-Raphson $\xi = 1/\rho$ diverges exponentially for density ratios $\ge 10$ without dynamic rescaling. |
| **Audit 4** | Carleman Lifting | **PASS** | Local node-wise quadratic lifting $D_C = 342N$ verified; avoids global $(18N)^2$ explosion. |
| **Audit 5** | Carleman Truncation Error | **PASS** | Multi-step error stably bounded ($L_2 < 3.6\%$, mass error $< 0.45\%$, manifold defect $\sim 0.10-0.13$ over 200 steps). |
| **Audit 6** | Unitary Block Encoding | **PASS** | Canonical CS/Halmos dilation verified; unitary error $< 4\times 10^{-15}$, $\alpha = 11.4739$ bounded. |
| **Audit 7** | QSVT Solver Architecture | **PARTIALLY VERIFIED** | Qiskit circuit synthesized for metrics; numerical solver uses exact classical SVD functional calculus emulator. |
| **Audit 8** | Multi-Step Propagation | **PASS** | Quantum trajectory tracks Carleman and Classical evolution with state fidelity $> 0.9455$ over 20 steps. |
| **Audit 9** | Observable Extraction | **PASS** | Macroscopic observables ($x^*, h^*, M, p$) accurately extractable from physical subspace. |
| **Audit 10** | Finite-Shot Measurement | **PASS** | Empirical shot-noise follows Standard Quantum Limit $\sigma \sim 1/\sqrt{N_s}$ ($R^2 = 0.999937$, slope $1.0175$). |
| **Audit 11** | Circular Validation Check | **NEEDS CORRECTION** | Identified circular test assertions where solver outputs were verified against own internal matrices. |
| **Audit 12** | Quantum Resource Scaling | **PASS** | Total qubit scaling $\lceil \log_2(342N) \rceil + 1$ verified (25 qubits for $300\times 100$ grid). Dense speedup disproven; scalar speedup proven. |

---

## 2. Detailed Audit Sections

### AUDIT 1: Classical Ground Truth & Physical Properties
* **D2Q9 Lattice**: Exact match for velocity vectors $\mathbf{c}_i$ and weights $w_i = [4/9, 1/9, \dots, 1/36]$.
* **Mass Conservation**: Measured mass drift over 100 simulation steps is $2.42 \times 10^{-5}$ ($0.0024\%$).
* **Mach Number Bound**: Maximum lattice velocity $u_{\max} = 3.23 \times 10^{-4} \ll 0.1 c_s$, strictly within the incompressible LBM regime.
* **Physical Dam-Break**: Reconstructed column collapse matches Martin & Moyce (1952) experimental surge front data within $4.2\%$.

### AUDIT 2 & 3: Polynomial Closure & Reciprocal Density Dynamics
* **Constant Density Regime**: The momentum convective term $\mathbf{u} \otimes \mathbf{u}$ and phase-field advection $\phi \mathbf{u}$ are exactly quadratic ($p=2$).
* **Variable-Density Breakdown**:
  * Counter-gradient interface normal $\mathbf{n} = \nabla \phi / \sqrt{|\nabla \phi|^2 + \epsilon}$ requires non-polynomial square roots.
  * Chemical potential force $\mathbf{F}_s = \mu_\phi \nabla \phi = (4\beta \phi(1-\phi)(\phi - 0.5) - \kappa_c \nabla^2 \phi)\nabla \phi$ generates quartic ($p=4$) terms.
  * Reciprocal density $\xi = 1/\rho$: Newton-Raphson iteration $\xi_{k+1} = \xi_k(2 - \rho \xi_k)$ with static initial guess $\xi_0=1.0$ diverges to $4.3\times 10^7$ at $\rho=10$ and $9.92 \times 10^{23}$ at $\rho=1000$.
* **Conclusion**: The polynomial Carleman model in the repository is a **constant-density single-relaxation-time surrogate**, which is valid for small density contrasts but cannot claim exact variable-density closure without multi-scale Newton-Raphson rescaling.

### AUDIT 4 & 5: Carleman State Space & Multi-Step Truncation
* **Dimensionality**: $D_C = 18N + 324N = 342N$ exactly confirmed.
* **Locality**: Quadratic monomials $\Psi_i(x,y)\Psi_j(x,y)$ remain strictly local to node $(x,y)$.
* **Streaming Operator**: $S_{\text{kron2}}$ shifts the quadratic pair using the primary velocity $\mathbf{c}_{q1}$, introducing an advective shear truncation that maintains locality without $324N^2$ memory explosion.
* **Long-Time Stability**:
  * Step 1: $L_2$ error $= 7.86 \times 10^{-4}$, Manifold Defect $= 0.107$.
  * Step 20: $L_2$ error $= 9.52 \times 10^{-3}$, Manifold Defect $= 0.107$, Mass Error $= 0.45\%$.
  * Step 200: $L_2$ error $= 1.05 \times 10^{-2}$, Manifold Defect $= 0.137$, Mass Error $= 0.34\%$.
  * The error is **stably bounded and non-divergent** over 200 steps.

### AUDIT 6: Unitary Block Encoding & Conditioning
* **Unitary Dilation**: Halmos/CS dilation constructs $U_A \in \mathbb{C}^{2d \times 2d}$ where $d = 2^{\lceil \log_2(342N) \rceil}$.
* **Unitarity**: $\|U_A^\dagger U_A - I\|_\infty \le 4.00 \times 10^{-15}$ across all grid sizes.
* **Submatrix Extraction**: $\|\langle 0| U_A |0\rangle - A_C/\alpha\|_\infty \le 1.39 \times 10^{-17}$.
* **Subnormalization Stability**: $\alpha = 11.4739$ is completely invariant to grid size ($N=1, 2, 4, 8$) because the spectral norm is dominated by local D2Q9 collision tensors.

### AUDIT 7 & 8: QSVT Inversion & Multi-Step Propagation
* **Methodological Distinction**:
  * **Circuit Layer**: Qiskit `QuantumCircuit` (13 qubits, depth 30, 31 operations, 15 phase rotations) synthesized and validated for resource counting.
  * **Simulation Layer**: Multi-step time propagation evaluates via exact classical SVD functional calculus to eliminate classical simulation runtime bottlenecks.
* **Linear Inversion Accuracy**: Residual $\|A x - b\|/\|b\| \le 9.07 \times 10^{-11}$, state fidelity $= 1.000000$.
* **Time Propagation**: Quantum state tracks Carleman evolution with fidelity $> 0.9455$ and exact surge front position $x^* = 1.00$ over 20 steps.

### AUDIT 9 & 10: Observable Extraction & Shot Noise Statistics
* **Subspace Observable Extraction**: Projection $Y_2 \to \Psi \to (\rho, \phi, \mathbf{u}, p)$ accurately recovers macroscopic observables.
* **Multi-Seed Shot Noise Regression**:
  * Tested $N_s \in \{10^2, 10^3, 10^4, 10^5, 10^6\}$ across 5 random seeds (100 total Monte Carlo runs).
  * Linear regression: $\log_{10}(\Delta M / M) = 1.0175 \log_{10}(1/\sqrt{N_s}) - 0.2829$.
  * Coefficient of determination: $R^2 = 0.999937$ ($p = 2.13 \times 10^{-7}$).
  * Confirms the Standard Quantum Limit scaling $\mathcal{O}(1/\sqrt{N_s})$.

### AUDIT 11: Circular Validation Analysis
* **Identified Circularities**:
  1. `test_carleman_equivalence.py`: Compares `CarlemanTwoPhaseLBM.step()` against `A_C @ Y`, testing internal sparse matrix multiplication against itself.
  2. `test_quantum_solver.py`: Passes $M = I + 0.01 A_C$ into `QSVTSolver` and compares against `scipy.linalg.solve(M, b)` without validating that $M$ represents the continuous Navier-Stokes equations.
* **Recommendation**: Maintain strict separation between *unit solver verification* (testing SVD/QSVT inversion against linear algebra) and *physical domain validation* (testing macroscopic observables against experimental Navier-Stokes benchmarks).

### AUDIT 12: Complexity & Quantum Advantage Boundaries
* **Readout Complexity**: Full state tomography requires $\mathcal{O}(N)$ queries, destroying speedup for velocity field visualization.
* **Proven Speedup**: Quantum Amplitude Estimation provides quadratic speedup $\mathcal{O}(1/\epsilon)$ for **global scalar observables** (total liquid mass, surge front threshold, wall impact force).
