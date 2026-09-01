# LEVEL-6B: CHRONOLOGICAL RESEARCH DIARY (PHASES 1 THROUGH 16)
## Evolution of the Quantum Lattice Boltzmann Method for Two-Phase Dam-Break Flow

**Document**: Master Historical Progression & Scientific Decision Log  
**Repository**: `/home/aswa/Research/QLBM-DamBreak-Production`  
**Date**: September 2026  

---

### Phase 1: Classical LBM Foundations
- **Problem**: Understanding standard D2Q9 lattice velocity discretization and BGK collision.
- **Method**: Single-phase isothermal Bhatnagar-Gross-Krook model with low-Mach expansion.
- **Implementation**: Basic streaming and equilibrium distribution functions.
- **Result**: Validated single-phase Poiseuille and Taylor-Green vortex flows.
- **Scientific Lesson**: Linear spatial streaming is an exact permutation on discrete lattice grids.
- **Decision**: Establish D2Q9 as the standard lattice framework.

---

### Phase 2: D2Q9 Implementation & Boundary Involutions
- **Problem**: Implementing direction-selective boundary conditions for closed fluid domains.
- **Method**: Half-way bounce-back solid wall reflection: $f_{\text{opp}(i)}(\mathbf{x}_{\text{wall}}) = f_i^*(\mathbf{x}_{\text{wall}})$.
- **Implementation**: Directional opposite velocity mapping `OPPOSITE = [0, 3, 4, 1, 2, 7, 8, 5, 6]`.
- **Result**: Exact involution $B^2 = I$, conserving local mass and momentum reflection.
- **Scientific Lesson**: Solid boundary reflection is an exact unitary involution in discrete velocity space.
- **Decision**: Lock boundary involution operator into core codebase.

---

### Phase 3: Two-Phase Free-Surface Formulation
- **Problem**: Capturing fluid-fluid interfaces and liquid-gas density contrasts.
- **Method**: Conservative phase-field index distributions $g_i$ coupled to hydrodynamic distributions $f_i$.
- **Implementation**: Phase fraction $\alpha = \sum g_i$, density mixture $\rho(\alpha) = \alpha \rho_L + (1-\alpha)\rho_G$.
- **Result**: Conservative interface advection without artificial numerical diffusion.
- **Scientific Lesson**: Independent phase distributions $g_i$ allow clean decoupling of mass and interface geometry.
- **Decision**: Adopt 18-variable coupled state vector $\mathbf{z}(\mathbf{x}) = [\mathbf{f}(\mathbf{x}); \mathbf{g}(\mathbf{x})]$.

---

### Phase 4: Classical Dam-Break Physical Validation
- **Problem**: Validating against experimental dam-break benchmarks (Martin & Moyce, 1952).
- **Method**: Added gravitational buoyancy $\mathbf{F}_g = (\rho - \rho_G)\mathbf{g}_{\text{acc}}$ and Brackbill Continuum Surface Force $\mathbf{F}_s = \sigma \kappa \nabla \alpha$.
- **Implementation**: Level-4 classical solver (`classical/level4_two_phase.py`).
- **Result**: Surge front $x^*(t^*)$ and column collapse $h^*(t^*)$ matched benchmark data within $< 7\%$.
- **Scientific Lesson**: CSF surface tension with central difference curvature stabilizes free-surface dynamics.
- **Decision**: Freeze Level 4 as the authoritative classical ground truth.

---

### Phase 5: Initial Quantum State Preparation
- **Problem**: Encoding classical 18-variable state into quantum registers.
- **Method**: Amplitude encoding into normalized state vector $|\Psi\rangle = \sum z_a |a\rangle$.
- **Implementation**: 5-qubit velocity/species selector register.
- **Result**: High-fidelity state preparation with amplitude reconstruction $< 10^{-4}$.
- **Scientific Lesson**: Quantum state normalization factor $M = \sum |z_a|$ must be tracked classically.
- **Decision**: Maintain explicit classical normalization tracking.

---

### Phase 6: Carleman Linearization Formulation
- **Problem**: Linearizing nonlinear convective momentum flux $j_a j_b / \rho$.
- **Method**: Second-order Carleman expansion around reference state $\rho_0 = 1.0$: $\mathbf{Y} = [\mathbf{z}; \mathbf{z}\otimes\mathbf{z}] \in \mathbb{R}^{342}$.
- **Implementation**: Coupled matrices $M_1 \in \mathbb{R}^{18\times 18}, M_2 \in \mathbb{R}^{18\times 324}, C_2 \in \mathbb{R}^{342\times 342}$.
- **Result**: Local collision represented as linear algebraic matrix action $\mathbf{z}^* = M_1 \mathbf{z} + M_2 (\mathbf{z}\otimes\mathbf{z})$.
- **Scientific Lesson**: Truncation error scales quadratically with Mach number: $\mathcal{E} \propto \text{Ma}^2$.
- **Decision**: Adopt second-order Carleman truncation for local collision block.

---

### Phase 7: Quantum Block Encoding & Unitary Dilations
- **Problem**: Embedding non-unitary Carleman matrix $C_2$ into a unitary quantum operator.
- **Method**: Sz.-Nagy unitary dilation $U_C = \begin{bmatrix} C_2/\alpha_C & D_* \\ D & -C_2^T/\alpha_C \end{bmatrix}$ with 1 ancilla qubit.
- **Implementation**: 10-qubit unitary operator in $\mathbb{U}(1024)$ with $\alpha_C = 7.9004$.
- **Result**: $\|P(\alpha_C U_C)P^T - C_2\| < 10^{-12}$ (machine precision embedding).
- **Scientific Lesson**: Dilated unitary operators have a sub-unitary success probability $p_{\text{succ}} = 1/\alpha_C^2 \approx 1.60\%$.
- **Decision**: Lock Sz.-Nagy dilation construction into `quantum/level6_lifted_carleman.py`.

---

### Phase 8: Level-5 Hybrid Quantum-Classical Solver
- **Problem**: Executing single-timestep quantum collision inside a hybrid fluid loop.
- **Method**: State preparation $\to$ Unitary collision $\to$ Postselection $\to$ Classical streaming.
- **Implementation**: First end-to-end hybrid prototype.
- **Result**: 48/48 tests passed; single-step density error $\approx 2.5 \times 10^{-4}$.
- **Scientific Lesson**: Hybrid execution is numerically stable for single timesteps.
- **Decision**: Investigate multi-step autonomous quantum execution.

---

### Phase 9: Level-6 Architecture Investigation
- **Problem**: Determining how to extend quantum evolution across multiple physical timesteps.
- **Method**: Evaluated 5 architectural alternatives across 23 dimensions.
- **Implementation**: Comprehensive literature survey and theoretical blueprint.
- **Result**: Recommended Architecture B (Local Carleman Multi-Timestep Solver).
- **Scientific Lesson**: Multi-step quantum execution requires strict invariant manifold preservation.
- **Decision**: Proceed to Level 6A implementation.

---

### Phase 10: Level-6A Implementation & Failure Discovery
- **Problem**: Implementing autonomous multi-timestep evolution without classical decoding ($K > 1$).
- **Method**: Applied $(B_{\text{lifted}} \cdot S_{\text{lifted}} \cdot C_2)^K$ coherently on 342-dim lifted state.
- **Implementation**: `Level6ALocalCarlemanSolver.step_coherent_k()`.
- **Result**: $K=1$ succeeded ($\rho_{\text{err}} \approx 2.3 \times 10^{-4}$), but $K=2$ diverged sharply ($\rho_{\text{err}} \approx 39.9\%$).
- **Scientific Lesson**: Multi-step coherent propagation fails despite passing single-step benchmarks.
- **Decision**: Halt implementation and launch scientific stability diagnosis (Level 6A-S).

---

### Phase 11: Tensor-Streaming Diagnosis (Level 6A-S)
- **Problem**: Isolating the root cause of the $K=2$ divergence.
- **Method**: 15 diagnostic numerical experiments tracking tensor invariance $E_{\text{tensor}} = \|Y_2 - \mathbf{z}\otimes\mathbf{z}\|$.
- **Implementation**: Diagnostic script `scripts/run_level6a_stability_analysis.py`.
- **Result**: Discovered that spatial streaming $S_{\text{lifted}}(\mathbf{z}\otimes\mathbf{z}) \ne \mathcal{S}(\mathbf{z}) \otimes \mathcal{S}(\mathbf{z})$, creating **$746\%$ tensor mismatch** at step 1.
- **Scientific Lesson**: Physical streaming of products $z_a(\mathbf{x}-\mathbf{c}_a) z_b(\mathbf{x}-\mathbf{c}_b)$ involves populations from distinct spatial nodes; independent local tensor shifts shift entries by $(\mathbf{c}_a + \mathbf{c}_b)$, which is physically false.
- **Decision**: Reject independent spatial streaming of the quadratic sector ($S \otimes S$).

---

### Phase 12: Block-Encoding Leakage Diagnosis (Level 6A-S)
- **Problem**: Investigating multi-step powers of unitary dilations without resets.
- **Method**: Multiplied unprojected dilation powers $P U_C^K P^T$ and compared to $C_2^K$.
- **Implementation**: Numerical defect operator analysis.
- **Result**: Unprojected multiplication produces $P U_C^2 P = C_2^2 + \alpha_C^2 D_* D \ne C_2^2$, creating **$2098\%$ leakage error**.
- **Scientific Lesson**: Unitary dilations cannot be chained without intermediate projective measurement/reset.
- **Decision**: Mandate intermediate projective reset or classical re-lifting between steps.

---

### Phase 13: Level-6A-R Mathematical Architecture Resolution
- **Problem**: Formally selecting the correct, physically sound architecture.
- **Method**: 16-criteria scorecard comparing 5 candidates (A: Naive, B: Global $N^2$ tensor, C: Mid-circuit reset, D: Hybrid $K=1$, E: QSVT).
- **Implementation**: Master derivation documents and resolution analysis script.
- **Result**: Architecture D (Hybrid $K=1$ Local Carleman) scored highest (**71 / 80, 88.8%**).
- **Scientific Lesson**: Hybrid $K=1$ preserves the invariant manifold, avoids leakage, and supports exact CSF surface tension.
- **Decision**: Authorize Level 6B under Architecture D exclusively.

---

### Phase 14: Level-6B Production Implementation
- **Problem**: Building the complete production Hybrid $K=1$ two-phase solver.
- **Method**: Exact linear streaming, local quadratic re-lifting, 10-qubit Sz.-Nagy collision block, classical CSF, and bounce-back boundaries.
- **Implementation**: `quantum/level6b_hybrid_solver.py` and test suite (87 tests).
- **Result**: Mass drift strictly bounded at $\le 1.528\%$ across 50 timesteps; surge front matched reference within $< 6\%$.
- **Scientific Lesson**: Hybrid $K=1$ resolves the Level-6A failure modes and establishes long-term stability.
- **Decision**: Run comprehensive independent scientific audit.

---

### Phase 15: Level-6B Scientific Audit
- **Problem**: Investigating why long-term field error reaches $\sim 15\%$ despite small one-step error.
- **Method**: Controlled experiments A-J, Mach-number scaling, and mass/momentum audit.
- **Implementation**: `scripts/run_level6b_scientific_audit.py`.
- **Result**: Controlled Exp B proved $100\%$ of pipeline error is localized in Carleman convective truncation ($\mathcal{E} \propto \text{Ma}^{2.003}$), while the surrounding pipeline is exact ($0.000000$ error).
- **Scientific Lesson**: The $\sim 15\%$ error is the expected theoretical low-Mach Taylor truncation of convective momentum flux.
- **Decision**: Declare GREEN-WITH-LIMITATIONS.

---

### Phase 16: Final Level-6B Verification & Baseline Freeze
- **Problem**: Consolidating reproducibility, purging over-strong claims, and preparing professor defense.
- **Method**: Independent full-matrix rerun, empirical power-law fit, claim audit, and vocabulary purification.
- **Implementation**: `scripts/run_level6b_final_verification.py` and documentation suite.
- **Result**: All 90 tests passing; verified reproducibility across all grids ($16\times 8 \dots 256\times 128$); verified hardware transpilation; purged unsupported claims.
- **Scientific Lesson**: A transparent, scientifically qualified hybrid architecture is academically defensible and publication-ready.
- **Decision**: **FREEZE LEVEL-6B AS THE ACTIVE VALIDATED RESEARCH BASELINE.**
