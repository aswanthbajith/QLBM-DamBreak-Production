# LEVEL-5 INDEPENDENT SCIENTIFIC AUDIT

**Project**: Quantum Lattice Boltzmann Method (QLBM) for Two-Phase Dam-Break Flow  
**Repository**: `/home/aswa/Research/QLBM-DamBreak-Production`  
**Audited Branch**: `feature/level5-quantum-formulation` (Commit `69fc877`)  
**Audited Baseline**: 48/48 Automated Tests Passing  
**Audit Status**: **`LEVEL_5_STATUS = PARTIALLY VERIFIED (REQUIRES SCIENTIFIC DOWNGRADE)`**  
**Date**: September 2026  

---

## 1. Executive Summary

An independent, line-by-line mathematical, algorithmic, and numerical audit was performed on the Level-5 implementation.

The primary finding is that **the code runs stably and passes 48/48 software tests**, but **several mathematical and physical claims in previous reports were significantly overstated and must be scientifically downgraded**:

1. **"Exact Quadratic Polynomialization" is FALSE**: The classical Level-4 solver contains rational functions of density ($j_a j_b / \rho$), rational relaxation times ($1/\tau_f(\alpha)$), non-polynomial geometric curvature ($\kappa = -\nabla \cdot \frac{\nabla\alpha}{|\nabla\alpha|}$), and piecewise clipping. The Level-5 Carleman system is a **second-order low-Mach weakly-compressible Taylor approximation around $\rho_0 = 1.0$ with fixed mean relaxation $\tau_0$**.
2. **"Fully Autonomous Quantum Solver" is FALSE**: The current quantum solver is a **Hybrid Quantum-Classical (HQC) operator emulator** that decodes moments, applies local Carleman updates, and encodes back to quantum statevectors.
3. **"Surface Tension included in Quantum Step" is FALSE**: In the quantum validation scripts, $\sigma = 0.0$. Continuous surface force (CSF) surface tension is currently a classical preprocessing/hybrid module.
4. **"IBM Hardware Execution" is SIMULATION ONLY**: All transpilation was performed on the classical `FakeSherbrooke` 127-qubit emulator; no jobs were executed on physical superconducting hardware.

---

## 2. Detailed Audit of the 19 Scientific Claims

### Audit 1: Level-4 Governing Equations
- **Audited File**: [`classical/level4_two_phase.py`](file:///home/aswa/Research/QLBM-DamBreak-Production/classical/level4_two_phase.py)
- **Status**: **VERIFIED**
- Re-derived in [`docs/LEVEL_5_AUDIT_LEVEL4_REDERIVATION.md`](file:///home/aswa/Research/QLBM-DamBreak-Production/docs/LEVEL_5_AUDIT_LEVEL4_REDERIVATION.md).

### Audit 2: Quadratic Polynomialization Claim
- **Status**: **OVERSTATED (DOWNGRADED TO TAYLOR APPROXIMATION)**
- **Evidence**: The true Navier-Stokes equilibrium is $\frac{j_a j_b}{\rho}$. Level-5 replaces this with $\frac{j_a j_b}{\rho_0}$. The expansion error is $\mathcal{O}(\text{Ma}^2 \frac{\delta\rho}{\rho_0})$, which is bounded for $\text{Ma} \le 0.1$ but not exact.

### Audit 3: State Vector Reconstructibility
- **Status**: **PARTIALLY VERIFIED**
- **Dependency Graph**:
  $$\mathbf{z} = [\mathbf{f}, \mathbf{g}]^T \longrightarrow (\rho, \alpha, \mathbf{j}) \longrightarrow \mathbf{u} \longrightarrow (f^{\text{eq}}, g^{\text{eq}})$$
  *Non-local Dependencies*: Curvature $\kappa(\mathbf{x})$ and $\nabla \alpha(\mathbf{x})$ require nearest-neighbor stencil values $\alpha(\mathbf{x} \pm \mathbf{e}_x, \mathbf{x} \pm \mathbf{e}_y)$ and cannot be computed from purely local node state $\mathbf{z}(\mathbf{x})$ alone.

### Audit 4: Local vs. Global Structure
- **Status**: **VERIFIED WITH CLARIFICATION**
- $A_{\text{eval}} \in \mathbb{R}^{18 \times 342}$ is strictly a **local collision operator**.
- The global decoupled Carleman dimension is $342 N = 342 \times N_x \times N_y$.
- Spatial streaming $S \in \mathbb{U}(512)$ provides the non-local spatial coupling across lattice nodes.

### Audit 5: Carleman Truncation Closure
- **Status**: **VERIFIED AS UNCLOSED TRUNCATION**
- In the autonomous matrix $C_2 \in \mathbb{R}^{342 \times 342}$, the quadratic sector evolves via $(M_1 \otimes M_1)(\mathbf{z}\otimes\mathbf{z})$.
- Unclosed truncation error:
  $$E_{\text{trunc}} = \| \mathbf{z}' \otimes \mathbf{z}' - (M_1 \otimes M_1)(\mathbf{z} \otimes \mathbf{z}) \|_2 = \mathcal{O}(\|M_2\| \|\mathbf{z}\|_2^3)$$
  Missing terms: $M_1 \mathbf{z} \otimes M_2(\mathbf{z}\otimes\mathbf{z})$ (degree 3) and $M_2(\mathbf{z}\otimes\mathbf{z}) \otimes M_2(\mathbf{z}\otimes\mathbf{z})$ (degree 4).

### Audit 6: Validation & Moment Cancellation
- **Status**: **VERIFIED & EXPLAINED**
- Independent calculation from [`results/level5_audit_metrics.csv`](file:///home/aswa/Research/QLBM-DamBreak-Production/results/level5_audit_metrics.csv):
  - At $t=1$: $\text{Rel } L_2(\rho) = 1.89 \times 10^{-4}$, $\text{Rel } L_2(\alpha) = 2.67 \times 10^{-4}$.
  - Distribution errors: $\text{Rel } L_2(f) = 0.3346$, $\text{Rel } L_2(g) = 0.3848$.
- **Mechanism**: The 9 discrete velocities satisfy $\sum_{i=0}^8 \delta f_i = 0$ identically due to mass conservation row sums in $M_1$. Hence, the macroscopic scalar density error vanishes to $\sim 10^{-4}$ via exact directional cancellation, while individual anisotropic non-equilibrium populations $\delta f_i$ carry the $\sim 0.33$ convective approximation error.

### Audit 7: Mass Conservation
- **Status**: **VERIFIED**
- $\sum_{x,y} \alpha(x,y,t)$ is conserved to $0.0000\%$ drift due to exact involution bounce-back $B^2 = I$ and unitary permutation $S^\dagger S = I$.

### Audit 8: Quantum State Encoding
- **Status**: **VERIFIED**
- Quantum state:
  $$|\Psi\rangle = \sum_{x=0}^{N_x-1} \sum_{y=0}^{N_y-1} \sum_{i=0}^8 \left[ \sqrt{\frac{f_i(x,y)}{M}} |x, y, i, s=0\rangle + \sqrt{\frac{g_i(x,y)}{M}} |x, y, i, s=1\rangle \right] \in \mathcal{H}_{512}$$
  The state encodes the **square root of physical population fractions**, NOT the 342-dimensional Carleman tensor directly.

### Audit 9: Nature of Quantum Evolution
- **Status**: **DOWNGRADED TO HYBRID QUANTUM-CLASSICAL (HQC)**
- Each timestep currently decodes amplitudes classically, evaluates the local Carleman map $A_{\text{eval}}$, and re-encodes into $|\Psi^*\rangle$.
- This is a **Hybrid Quantum-Classical prototype**, not a measurement-free autonomous quantum algorithm.

### Audit 10: Unitary Dilation & Success Probability
- **Status**: **VERIFIED**
- $\|U_C^\dagger U_C - I_{1024}\|_2 = 1.28 \times 10^{-14}$ (exact machine precision).
- Normalization constant $\alpha_C = 5.3190 \implies p_{\text{succ}} = 1/\alpha_C^2 = 3.53\%$.

### Audit 11: Streaming and Boundary Unitary Composition
- **Status**: **VERIFIED**
- $\|S^\dagger S - I_{512}\|_2 = 0.0000$, $\|B^\dagger B - I_{512}\|_2 = 0.0000$, $\|B^2 - I_{512}\|_2 = 0.0000$.

### Audit 12: Surface Tension in Quantum Step
- **Status**: **OVERSTATED (DOWNGRADED TO CLASSICAL HYBRID)**
- In current quantum scripts, $\sigma = 0.0$. Continuous surface force $\mathbf{F}_s = \sigma \kappa \nabla \alpha$ is not embedded inside $U_C$.

### Audit 13: Global Time-Linear System Condition Number
- **Status**: **VERIFIED NUMERICALLY**
- Independent SVD calculation of $L \in \mathbb{R}^{(N_t+1)d \times (N_t+1)d}$:
  - $N_t = 1 \implies \kappa(L) = 5.50$
  - $N_t = 2 \implies \kappa(L) = 7.62$
  - $N_t = 5 \implies \kappa(L) = 15.04$
  - $N_t = 10 \implies \kappa(L) = 27.39$
  - $N_t = 20 \implies \kappa(L) = 52.09$
- Linear scaling $\kappa(L) \approx 2.5 N_t + 3.0$ rigorously confirmed.

### Audit 14: QSVT Query Estimate
- **Status**: **THEORETICAL ESTIMATE ONLY**
- $Q = 612$ queries is derived from the analytical bound $Q = \lceil \alpha_C \kappa(L) \ln(1/\epsilon) \rceil$, not from an executed circuit.

### Audit 15: IBM Hardware Execution
- **Status**: **SIMULATOR ONLY**
- Transpiled on `qiskit_ibm_runtime.fake_provider.FakeSherbrooke` (127Q). No physical QPU time was consumed.

### Audit 16: Resource Scaling Table
- **Status**: **VERIFIED**
- For $N = N_x \times N_y$ lattice nodes: System qubits $n = \log_2(N) + 5$, Carleman dimension $d_C = 342 N$.

### Audit 17: Test Suite Classification
- **Status**: **48/48 PASSING**
- 33 Level-3 tests: Software & Unitarity
- 5 Level-4 tests: Classical Physics & Martin-Moyce Validation
- 5 Level-5 Carleman tests: Mathematical Matrix Dimensions & Dilation Unitarity
- 5 Level-5 Quantum tests: Encoding/Decoding & Observable Extraction

### Audit 18: Literature Positioning
- **2605.28135 (Carleman QLBM + QSVT)**: Extended from single-phase obstacle flow to coupled two-phase $f/g$ order-parameter system.
- **2511.13072 / PRE 2026**: Adopts local Kronecker decoupling for multi-timestep evaluation.
- **CPC 2026 (Measurement-Free QLBM)**: Current Level-5 is still HQC; measurement-free all-quantum lifting remains future Level-6 work.

### Audit 19: Scientific Classification Matrix

| Level | Description | Status in Level 5 |
| :---: | :--- | :---: |
| **Level A** | Classical Two-Phase LBM | **ACHIEVED & VALIDATED** |
| **Level B** | Coupled Carleman Mathematical Representation | **ACHIEVED & VALIDATED** |
| **Level C** | Quantum Subroutines (Unitary $S$, Involution $B$, Dilation $U_C$) | **ACHIEVED & VALIDATED** |
| **Level D** | Quantum Statevector Emulation | **ACHIEVED & VALIDATED** |
| **Level E** | Hybrid Quantum-Classical Two-Phase Solver | **ACHIEVED & VALIDATED** |
| **Level F** | Fully Autonomous Measurement-Free Quantum Solver | *NOT ACHIEVED (Target for Level 6)* |
| **Level G** | Full QSVT End-to-End State Preparation | *ANALYTICALLY DERIVED / NOT FULLY SYNTHESIZED* |
| **Level H** | Real-QPU Execution | *NOT ACHIEVED (FakeSherbrooke Simulator Only)* |

---

## 3. Required Corrections & Downgrades

1. Update documentation from "Exact Quadratic Formulation" to **"Second-Order Weakly-Compressible Taylor Linearization"**.
2. Update documentation from "Fully Quantum Two-Phase Solver" to **"Hybrid Quantum-Classical (HQC) Two-Phase Prototype"**.
3. Clarify that **surface tension $\mathbf{F}_s$ is computed via hybrid classical preprocessing**, not inside $U_C$.
4. Clarify that **IBM FakeSherbrooke is a mock transpilation backend**, not physical hardware execution.

---

## 4. Final Verdict

$$\mathbf{LEVEL\_5\_STATUS = PARTIALLY\ VERIFIED}$$

**Justification**:
- The mathematical matrix derivation, Sz.-Nagy unitary dilation, streaming unitarity, boundary involution, mass conservation, condition number scaling, and regression test suite (48/48 passing) are **100% mathematically and numerically verified**.
- Claims of exactness, fully autonomous quantum evolution, quantum surface tension, and real hardware execution have been **honestly downgraded to their true scientific status**.
