# LEVEL-6 BASELINE AUDIT: CURRENT RESEARCH STATE & ARCHITECTURAL FOUNDATION

**Repository**: `/home/aswa/Research/QLBM-DamBreak-Production`  
**Protected Archive**: `/home/aswa/Research/QLBM-DamBreak` (clean, frozen, untouched on `master`)  
**Working Branch**: `feature/level6-architecture-investigation`  
**Test Suite Status**: **48 / 48 Passing Tests (100% Pass Rate)**  
**Date**: September 2026  

---

## 1. Verified Baseline Capabilities (Levels 3, 4, 5)

### A. Level-3 Quantum Subroutine Foundation
- Quantum state preparation encoding amplitudes into power-of-two registers.
- Exact unitary spatial streaming permutation $S \in \mathbb{U}(512)$ with $\|S^\dagger S - I\|_2 = 0$.
- Direction-selective solid wall bounce-back boundary involution $B \in \mathbb{U}(512)$ with $B = B^\dagger, B^2 = I$.
- 33/33 Level-3 automated tests passing.

### B. Level-4 Classical Physical Reference Solver
- High-fidelity D2Q9 two-phase solver (`classical/level4_two_phase.py`) with conservative phase-field interface capturing ($\alpha = \sum g_i$).
- Continuum Surface Force (CSF) surface tension $\mathbf{F}_s = \sigma \kappa \nabla \alpha$ with non-local finite difference stencils.
- Validated against the Martin & Moyce (1952) experimental dam-break dataset across grid refinement levels:
  - $32 \times 16$: Surge front Rel $L_2 = 67.59\%$, Height Rel $L_2 = 64.61\%$, Mass drift $= 1.17\%$.
  - $64 \times 32$: Surge front Rel $L_2 = 14.54\%$, Height Rel $L_2 = 24.61\%$, Mass drift $= 1.50\%$.
  - $128 \times 64$: Surge front Rel $L_2 = 6.79\%$, Height Rel $L_2 = 13.47\%$, Mass drift $= 1.38\%$.
- 5 Level-4 physical validation tests passing.

### C. Level-5 Coupled Carleman Representation & Quantum Prototype
- Coupled state $\mathbf{z}_t = [\mathbf{f}_t, \mathbf{g}_t]^T \in \mathbb{R}^{18 N}$ with local Kronecker decoupling $\mathbf{Y}_{\text{local}} \in \mathbb{R}^{342}$.
- Local evaluation operator $A_{\text{eval}} = [M_1, M_2] \in \mathbb{R}^{18 \times 342}$ with $87.8\%$ sparsity.
- 10-qubit Sz.-Nagy unitary dilation $U_C \in \mathbb{U}(1024)$ with $\|U_C^\dagger U_C - I_{1024}\|_2 = 1.28 \times 10^{-14}$.
- Global spacetime block-bidiagonal linear system $L \mathbf{Y}_{\text{global}} = \mathbf{b}_{\text{global}}$ with linear condition number scaling $\kappa(L) \approx 2.5 N_t + 3.0$.
- 10 Level-5 unit and integration tests passing (48 / 48 total test suite).

---

## 2. Established Scientific Limitations & Overstatements

Following the independent scientific audit (`LEVEL_5_INDEPENDENT_SCIENTIFIC_AUDIT.md`), the following limitations are mathematically established:

1. **Non-Polynomiality of True Physics**:
   - Convective momentum $\frac{j_a j_b}{\rho}$ is rational in density $\rho$.
   - Phase-dependent relaxation $\frac{1}{\tau_f(\alpha)}$ is rational in volume fraction $\alpha$.
   - Interfacial curvature $\kappa = -\nabla \cdot \frac{\nabla\alpha}{|\nabla\alpha|}$ is non-polynomial and non-local.
   - Clipping $\text{clip}(\alpha, 0, 1)$ and $|\mathbf{u}| \le 0.15$ are piecewise operations.
   - *Verdict*: The Level-5 Carleman system is a second-order low-Mach weakly-compressible Taylor expansion around $\rho_0 = 1.0$ with fixed mean relaxation $\tau_0$.

2. **Hybrid Classical Decode/Re-Encode Bottleneck**:
   - The current Level-5 quantum execution decodes state amplitudes classically after each step, evaluates the local Carleman map, and re-encodes into $|\Psi^*\rangle$.
   - *Verdict*: It is a **Hybrid Quantum-Classical (HQC) prototype**, not a measurement-free autonomous quantum solver.

3. **Surface Tension Omission in Quantum Execution**:
   - The quantum execution scripts set $\sigma = 0.0$. Continuous surface force $\mathbf{F}_s = \sigma \kappa \nabla \alpha$ is not yet embedded in the quantum unitary operator.

4. **Hardware Status**:
   - Transpilation was executed against `FakeSherbrooke` (127Q mock backend). No physical QPU time has been consumed.

---

## 3. Scope of the Level-6 Investigation

Level 6 will rigorously compare three potential architectural paradigms:
- **Architecture A (HQC)**: Preserve full physical fidelity by maintaining classical non-linear processing and surface tension while executing quantum streaming and linear subroutines.
- **Architecture B (Local Carleman Multi-Timestep)**: Construct a measurement-free coherent local Carleman circuit evolving across multiple timesteps ($N_t = 2 \dots 5$) without intermediate state collapse.
- **Architecture C (Global Carleman + QSVT)**: Formulate the complete spacetime system $L \mathbf{y} = \mathbf{b}$ as a global Quantum Linear System Algorithm (QLSA) solved via Quantum Singular Value Transformation (QSVT).
