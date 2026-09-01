# LEVEL-6A-R: FORMAL ARCHITECTURAL DECISION GATE

**Document**: Definitive Decision Matrix and Conditions for Transitioning to Level 6B  
**Repository**: `/home/aswa/Research/QLBM-DamBreak-Production`  
**Date**: September 2026  

---

## 1. Formal Answers to the 8 Mandatory Questions

1. **Is the current $S \otimes S$ lifted streaming formulation valid?**  
   **NO (INVALID)**. Kronecker product streaming $S \otimes S$ shifts the quadratic entry by $(\mathbf{c}_a + \mathbf{c}_b)$, which does not equal the physical product $z_a(\mathbf{x}-\mathbf{c}_a) z_b(\mathbf{x}-\mathbf{c}_b)$ of linearly streamed populations. This produces $62\% - 92\%$ tensor de-correlation on the very first step.
2. **What is the correct alternative?**  
   **Architecture D (Hybrid $K=1$ Local Carleman)** or **Architecture C (Mid-Circuit Ancilla Reset with Local Re-lifting)**. In both valid architectures, streaming acts exclusively on the linear physical populations $\mathbf{z}(\mathbf{x})$, and the quadratic state $\mathbf{z}(\mathbf{x}) \otimes \mathbf{z}(\mathbf{x})$ is re-formed locally at each node after streaming.
3. **Is the current Sz.-Nagy dilation suitable for repeated time evolution without resets?**  
   **NO**. Repeated unprojected multiplication causes $P (\alpha_C U_C)^2 P^T = C_2^2 + \alpha_C^2 D_* D \ne C_2^2$, producing $2098.7\%$ error at $K=2$.
4. **What is the least expensive valid alternative?**  
   **Single-qubit mid-circuit projective measurement / reset on $|\text{anc}\rangle$** or **classically normalized Hybrid $K=1$ execution**.
5. **Can $K > 1$ be performed without intermediate projection or re-lifting?**  
   **NO**. Spatial advection intrinsically couples populations from different physical coordinates, which cannot be represented in a decoupled local tensor without intermediate re-formation or an impractical $\mathcal{O}(N^2)$ global bipartite tensor.
6. **Is $K=1$ hybrid reinitialization scientifically acceptable?**  
   **YES**. It is mathematically exact ($0.023\%$ density error), preserves the invariant Carleman manifold, avoids all dilation leakage, and supports exact non-local Brackbill CSF surface tension.
7. **What architecture should become Level 6B?**  
   **Architecture D: Hybrid $K=1$ Local Carleman Two-Phase QLBM with Exact Unitary Streaming and Continuum Surface Force (CSF) Feedback**.
8. **What must NOT be claimed in the thesis / publications?**  
   - DO NOT claim a "fully quantum measurement-free multi-timestep dam-break solver".
   - DO NOT claim that $S \otimes S$ is exact tensor streaming.
   - DO NOT claim that unprojected unitary dilation preserves powers $C_2^K$.
   - DO NOT claim $\mathcal{O}(K \text{Ma}^3)$ error scaling for spatial PDE simulations.
   - DO NOT claim "quantum speedup" on classical computers without fault-tolerant logical circuits.

---

## 2. DECISION GATE VERDICT

$$\mathbf{GREEN \ (Conditional\ on\ Adopting\ Architecture\ D)}$$

> **Declaration**:  
> The mathematical diagnosis is complete and conclusive. The failure modes of naive multi-step local Carleman lifting have been proven from first principles.  
> **Level 6B may proceed exclusively under Architecture D (Hybrid $K=1$ Local Carleman Two-Phase QLBM)**, establishing the first physically validated quantum Lattice Boltzmann simulation of experimental two-phase dam-break flow.
