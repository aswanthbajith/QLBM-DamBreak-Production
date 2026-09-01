# LEVEL-6A-R: 16-CRITERIA ARCHITECTURAL COMPARISON & SCORECARD

**Document**: Comparative Evaluation of Candidate QLBM Architectures  
**Repository**: `/home/aswa/Research/QLBM-DamBreak-Production`  
**Date**: September 2026  

---

## 1. Candidate Architectures Evaluated

- **Architecture A**: Naive $S \otimes S$ Lifted Local Carleman (Evaluated in Level 6A).
- **Architecture B**: Global Bipartite Spatial Tensor ($324 N^2$ full cross-node representation).
- **Architecture C**: Local Carleman Collision with Mid-Circuit Ancilla Reset & Local Re-coupling ($K$-Step Block).
- **Architecture D**: **Hybrid $K=1$ Local Carleman QLBM** (Exact unitary streaming $S$, exact boundary $B$, classical re-lifting per step).
- **Architecture E**: Global Spacetime QSVT / QLSA ($L \mathbf{y} = \mathbf{b}$).

---

## 2. Comprehensive 16-Criteria Scorecard

| Evaluation Criterion (1 to 5) | Arch A | Arch B | Arch C | Arch D (Hybrid $K=1$) | Arch E (QSVT) |
| :--- | :---: | :---: | :---: | :---: | :---: |
| **01. Mathematical Correctness** | 1 | 4 | 4 | **5** | **5** |
| **02. Physical Dam-Break Fidelity** | 2 | 3 | 3 | **5** | 2 |
| **03. Invariant Manifold Preserved** | 1 | **5** | 4 | **5** | 3 |
| **04. Quantum Coherence Horizon** | 4 | 4 | 3 | 2 | **5** |
| **05. Measurement & Readout Burden** | **5** | 4 | 3 | 2 | 4 |
| **06. State Preparation Burden** | **5** | 1 | 3 | 2 | **5** |
| **07. Qubit Count Efficiency** | 4 | 1 | 4 | **5** | 3 |
| **08. Gate Count & Circuit Depth** | 4 | 1 | 3 | **5** | 1 |
| **09. Dilation Success Probability** | 1 | 2 | 3 | **5** | 3 |
| **10. Exact Bounce-Back Boundary** | 2 | 3 | 4 | **5** | 3 |
| **11. CSF Surface Tension Compatibility** | 1 | 1 | 2 | **5** | 1 |
| **12. Multi-Grid Spatial Scalability** | 2 | 1 | 4 | **5** | 4 |
| **13. NISQ / Early FTQC Feasibility** | 2 | 1 | 3 | **5** | 1 |
| **14. Thesis & Literature Novelty** | 3 | 4 | 4 | **5** | 4 |
| **15. Validation & Debuggability** | 2 | 2 | 3 | **5** | 2 |
| **16. Non-Divergent Trajectory** | 1 | 3 | 3 | **5** | 2 |
| **TOTAL SCORE (out of 80)** | **40 (50.0%)** | **40 (50.0%)** | **53 (66.2%)** | **71 (88.8%)** | **48 (60.0%)** |

---

## 3. Scientific Rationale for Selecting Architecture D (Hybrid $K=1$ Local Carleman)

1. **Exact Invariant Manifold Preservation**: By re-forming the quadratic tensor $\mathbf{Y}_{\text{quad}}(\mathbf{x}) = \mathbf{z}(\mathbf{x}) \otimes \mathbf{z}(\mathbf{x})$ at each timestep, Architecture D completely avoids the $746\%$ tensor streaming mismatch and maintains density error below **$0.023\%$** ($2.33 \times 10^{-4}$).
2. **Zero Dilation Subspace Leakage**: Operates at $K=1$ where the block encoding is exact ($\|P (\alpha_C U_C) P^T - C_2\| < 10^{-15}$).
3. **Full Continuum Surface Force (CSF) Compatibility**: Exactly incorporates Brackbill CSF surface tension $\mathbf{F}_s = \sigma \kappa \nabla \alpha$ via standard spatial finite-difference stencils between steps.
4. **Logarithmic Qubit Scaling**: Requires only $n = \log_2 N + 6$ qubits (19 qubits for $128 \times 64$), whereas Architecture B requires 36 qubits ($> 80$ GB state space).
5. **Experimental Hardware Tractability**: Can be executed on existing quantum emulators and near-term superconducting QPUs today.
