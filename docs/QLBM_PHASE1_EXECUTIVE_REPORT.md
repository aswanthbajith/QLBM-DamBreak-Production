# QUANTUM TWO-PHASE DAM-BREAK LBM (QLBM)
## Phase 1 Executive Research Report: Direct Spatial/Population Encoding & Candidate Evaluation

**Document**: Master First-Stage Deliverable (Items A–M)  
**Project**: Quantum Lattice Boltzmann Method for Two-Phase Dam-Break Flow  
**Repository**: `/home/aswa/Research/QLBM-DamBreak-Production`  
**Branch**: `feature/direct-encoding-two-phase-qlbm`  
**Date**: September 2026  

---

### A. Architecture Comparison
Four candidate architectures were systematically evaluated across 14 rigorous criteria (detailed in [`docs/QLBM_ARCHITECTURE_COMPARISON_MATRIX.md`](file:///home/aswa/Research/QLBM-DamBreak-Production/docs/QLBM_ARCHITECTURE_COMPARISON_MATRIX.md)):
1. **Candidate A (Carleman Lifted Tensor)**: Vulnerable to spatial tensor streaming shift ($419.5\%$) and dilation defect leakage ($2098.7\%$).
2. **Candidate B (Direct Spatial/Population Encoding)**: **Top Recommended Candidate**. Eliminates spatial tensor de-correlation; operates via exact unitary permutation streaming ($S^\dagger S = I$) and boundary involution ($B^2 = I$).
3. **Candidate C (Quantum Arithmetic / QROM)**: Intractable gate depth ($> 10^9$ Toffoli gates for non-local CSF curvature stencils).
4. **Candidate D (Hybrid Quantum Streaming/Collision)**: Production-ready hybrid pairing of Candidate B direct encoding with hybrid CSF surface tension feedback.

---

### B. Mathematical Derivation of Proposed Direct Encoding
The full lattice state is encoded in a unified Hilbert space:
$$\mathcal{H} = \mathcal{H}_x \otimes \mathcal{H}_y \otimes \mathcal{H}_{\text{vel}} \otimes \mathcal{H}_{\text{phase}}$$
with normalized state vector:
$$|\Psi\rangle = \frac{1}{\mathcal{N}} \sum_{x=0}^{N_x-1}\sum_{y=0}^{N_y-1}\sum_{i=0}^8 \Big( f_i(x,y) |x,y,i,0\rangle + g_i(x,y) |x,y,i,1\rangle \Big)$$
where $\mathcal{N} = \sqrt{\sum_{x,y,i} (|f_i|^2 + |g_i|^2)}$.

---

### C. Register & Qubit Allocation
For an $N_x \times N_y$ lattice grid:
- $n_x = \lceil\log_2 N_x\rceil$ spatial column qubits
- $n_y = \lceil\log_2 N_y\rceil$ spatial row qubits
- $n_{\text{vel}} = 4$ discrete velocity qubits ($2^4 = 16 \ge 9$)
- $n_{\text{phase}} = 1$ phase/species qubit ($|0\rangle \to f, |1\rangle \to g$)
- **Total Data Qubits**: $n_{\text{data}} = n_x + n_y + 5$
  - Minimal Prototype ($2 \times 2$): **7 Logical Qubits**
  - Intermediate Grid ($4 \times 4$): **9 Logical Qubits**
  - Target Dam-Break ($128 \times 64$): **18 Logical Qubits**

---

### D. Quantum Streaming Derivation
Streaming acts as a velocity-conditioned modular spatial shift:
$$S |x, y, i, p\rangle = |(x + c_{ix}) \bmod N_x, (y + c_{iy}) \bmod N_y, i, p\rangle$$
Because $(x, y) \mapsto (x+c_{ix}, y+c_{iy})$ is a bijection on the discrete lattice, $S$ is a **permutation matrix**, guaranteeing $S^\dagger S = I$ with **$0.000000\times 10^0$ error**. This completely avoids the Level-6A tensor-streaming breakdown.

---

### E. Quantum Collision Strategy Options
1. **Option 1 (Node-Conditioned Block Encoding)**: Embed local linearized/Carleman collision into a 5-qubit unitary dilation acting on $|i\rangle|p\rangle$.
2. **Option 2 (Hybrid Quantum-Classical Update)**: Perform coherent quantum streaming and boundary reflection on $|\Psi\rangle$, decode macroscopic moments, evaluate nonlinear equilibria and CSF, and execute local collision.
3. **Option 3 (Polynomial Taylor Unitary)**: Low-depth unitary Taylor approximation for weakly-compressible Low-Mach regimes.

---

### F. Two-Phase Representation
Hydrodynamic ($f_i$) and phase-field ($g_i$) populations are simultaneously represented in orthogonal subspaces spanned by $|p=0\rangle$ and $|p=1\rangle$.
- Phase fraction: $\alpha(x,y) = \text{clip}(\mathcal{N}\sum_i \langle x,y,i,1|\Psi\rangle, 0, 1)$
- Density: $\rho(\alpha) = \alpha \rho_L + (1-\alpha) \rho_G$
- Viscosity: $\nu(\alpha) = \alpha \nu_L + (1-\alpha) \nu_G$
- Surface tension: Brackbill CSF $\mathbf{F}_s = \sigma \kappa \nabla\alpha$ coupled to momentum.

---

### G. Minimal $2 \times 2$ Prototype Implementation
Implemented in [`quantum/direct_two_phase_prototype.py`](file:///home/aswa/Research/QLBM-DamBreak-Production/quantum/direct_two_phase_prototype.py) (`DirectTwoPhaseQLBM`) with complete Qiskit quantum circuit compilation (`build_qiskit_circuit()`).

---

### H. Validation Results
Validated across multi-step evolution against the Level-4 classical reference:
- **$2 \times 2$ Grid ($T=10$)**:
  - Max error in $f$: $3.75 \times 10^{-15}$
  - Max error in $g$: $2.72 \times 10^{-15}$
  - Max error in $\rho$: $8.27 \times 10^{-15}$
  - Max error in $\alpha$: $6.52 \times 10^{-15}$
  - Mass drift vs Level 4: **$0.000000 \times 10^0$**
- **$4 \times 4$ Grid ($T=10$)**:
  - Max error in $f$: $2.05 \times 10^{-15}$
  - Max error in $\rho$: $4.44 \times 10^{-15}$
  - Agreement status: **Machine Precision ($< 10^{-14}$)**.

---

### I. Resource Estimates & Hardware Transpilation
Transpiled on **IBM FakeSherbrooke (127Q Heavy-Hex)**:
- **Logical Qubits**: 7
- **Transpiled Depth**: 10,099 (reduced from $> 3.76\text{M}$ in Carleman block encoding)
- **Two-Qubit CX/ECR Gates**: 2,700
- **Compilation Time**: $0.14\text{s}$

---

### J. Failure & Limitation Analysis
- **What was resolved**: Spatial tensor streaming de-correlation is 100% eliminated ($S^\dagger S = I$).
- **What remains a limitation**: Evaluating non-local curvature $\kappa = -\nabla\cdot\mathbf{n}$ for Brackbill CSF is computationally prohibitive to perform via fully autonomous quantum arithmetic ($> 10^9$ Toffoli depth) and is therefore executed in a hybrid feedback loop.

---

### K. Recommendation for Next Implementation Phase
**Proceed to Phase 2/3: Scaling Direct Spatial/Population Encoding to $8 \times 4$ and $16 \times 8$ Lattice Grids with In-Circuit Reversible Arithmetic Shift Adders for Spatial Streaming.**

---

### L. Updated Research Roadmap
1. **Stage 1 (Current - COMPLETED)**: Direct encoding mathematical formulation, $2 \times 2$ prototype, and Level-4 validation.
2. **Stage 2**: Implement reversible quantum adder streaming circuits ($|(x+c_{ix})\bmod N_x\rangle$) using Cuccaro/Draper ripple-carry adders.
3. **Stage 3**: Scaled multi-node benchmark on $16 \times 8$ and $32 \times 16$ grids.
4. **Stage 4**: Quantum circuit compilation and noise-resilience profiling.
5. **Stage 5**: Full two-phase dam-break simulation benchmark against Martin & Moyce (1952).

---

### M. Git Commit Summary
- **Branch**: `feature/direct-encoding-two-phase-qlbm`
- **Files Created**:
  - `quantum/direct_two_phase_prototype.py`
  - `tests/test_direct_two_phase_prototype.py`
  - `scripts/run_direct_encoding_benchmark.py`
  - `docs/QLBM_DIRECT_ENCODING_FOUNDATION.md`
  - `docs/QLBM_ARCHITECTURE_COMPARISON_MATRIX.md`
  - `docs/QLBM_PHASE1_EXECUTIVE_REPORT.md`
  - `results/qlbm_architecture_comparison.csv`
  - `results/qlbm_direct_encoding_validation.csv`
  - `results/qlbm_direct_hardware_metrics.csv`
- **Level-6B Integrity**: 100% Frozen and Intact.
- **Original Archive**: 100% Untouched (`/home/aswa/Research/QLBM-DamBreak`).
