# LEVEL-7: ARCHITECTURE CANDIDATES & COMPARATIVE EVALUATION

**Document**: Formulation and Scoring of the 3 Coherent Architecture Candidates  
**Repository**: `/home/aswa/Research/QLBM-DamBreak-Production`  
**Date**: September 2026  

---

## 1. Candidate Architectures

### Architecture 7A: Coherent Linear Streaming with Mid-Circuit Projective Ancilla Reset & Periodic Re-lifting (Selected)
- **Concept**: Evolve a $K$-step coherent block using 10-qubit Sz.-Nagy block-encoded collisions with mid-circuit projective resets on $|\text{anc}\rangle$ to eliminate leakage.
- **Streaming**: Coherent unitary permutation circuit $S$ on 18 linear populations.
- **Tensor Manifold**: Preserved via local quadratic re-formation at each node.
- **Surface Tension**: Continuum Surface Force (CSF) updated as hybrid feedback every $K$ steps.

### Architecture 7B: Global Spacetime Linear System (QSVT / LCU / QLSA)
- **Concept**: Formulate the full $(N_t + 1) \times 342 N$ spacetime history as a global matrix equation $L \mathbf{y} = \mathbf{b}$ and solve via Quantum Singular Value Transformation (QSVT).
- **Fatal Limitations**: Requires static linear operators; cannot evaluate state-dependent dynamic CSF surface tension $\mathbf{F}_s = \sigma \kappa(\alpha) \nabla\alpha$ without an intractable quantum arithmetic oracle; gate depth $> 10^7$ gates (Fault-Tolerant Only).

### Architecture 7C: Global Bipartite Spatial Tensor ($324 N^2$) with Full Kronecker Streaming
- **Concept**: Explicitly represent all bipartite population cross-products $z_a(\mathbf{x}_1) z_b(\mathbf{x}_2)$ globally across all node pairs $(\mathbf{x}_1, \mathbf{x}_2)$.
- **Fatal Limitations**: Space complexity is $\mathcal{O}(N^2)$. For $128 \times 64$, requires $36$ qubits and $> 160$ GB classical state memory ($2.17 \times 10^{10}$ variables); non-local multi-qubit entangling gates across the entire chip.

---

## 2. Comprehensive 13-Criteria Scorecard (0 to 10 Scale)

| Evaluation Criterion | Arch 7A (Projected Reset Block) | Arch 7B (Spacetime QSVT) | Arch 7C (Global $N^2$ Tensor) |
| :--- | :---: | :---: | :---: |
| **01. Mathematical Correctness** | **9** | 8 | 8 |
| **02. Invariant Manifold Preservation** | **9** | 6 | **9** |
| **03. Block-Encoding Validity (No Leakage)**| **9** | **9** | 8 |
| **04. Quantum Coherence Horizon ($K > 1$)** | 7 | **9** | 8 |
| **05. Two-Phase CSF Compatibility** | **8** | 3 | 2 |
| **06. Boundary Condition Compatibility** | **9** | 7 | 7 |
| **07. Qubit Count Efficiency** | **9** | 6 | 2 |
| **08. Circuit Depth & Gate Scalability** | **8** | 3 | 2 |
| **09. Success Probability ($p_{\text{succ}}$)** | **7** | 6 | 4 |
| **10. Classical Overhead & Memory** | **9** | 6 | 2 |
| **11. Implementation Feasibility** | **9** | 4 | 3 |
| **12. Literature Novelty** | **9** | 8 | 7 |
| **13. Thesis & Scientific Value** | **9** | 7 | 6 |
| **TOTAL SCORE (out of 130)** | **111 (85.4%) [SELECTED]** | **82 (63.1%)** | **68 (52.3%)** |
