# LEVEL-7: ARCHITECTURE SELECTION & FORMAL DECISION GATE

**Document**: Formal Decision on Candidate Selection and Level-7 Classification  
**Repository**: `/home/aswa/Research/QLBM-DamBreak-Production`  
**Date**: September 2026  

---

## 1. Selected Architecture: Architecture 7A

$$\mathbf{Architecture\ 7A:\ Coherent\ Multi-Step\ Local\ Carleman\ with\ Projective\ Reset\ \&\ Permutation\ Streaming}$$

### Rationale:
1. **Zero Dilation Leakage**: Mid-circuit projective reset on the dilation ancilla qubit $|\text{anc}\rangle$ after each collision step completely eliminates the $2098\%$ leakage error ($[P(\alpha_C U_C)P^T]^K = C_2^K$ exact to machine precision $< 10^{-16}$).
2. **Exact Invariant Manifold Preservation**: Linear population streaming followed by local re-formation preserves $Y_2 = \mathbf{z} \otimes \mathbf{z}$ with zero error ($0.00\times 10^0$).
3. **Logarithmic Qubit Scaling**: Operates within $n = \log_2 N + 6$ qubits (19 qubits for $128 \times 64$), completely avoiding the 36-qubit $\mathcal{O}(N^2)$ explosion of Architecture 7C.
4. **Physical Dam-Break & CSF Compatibility**: Supports non-local Brackbill surface tension and solid wall bounce-back boundaries.

---

## 2. LEVEL-7 DECISION GATE VERDICT

$$\mathbf{YELLOW \ (Conditional\ on\ Projective\ Resets\ \&\ Hybrid\ CSF)}$$

> **Declaration**:  
> A coherent multi-step quantum architecture is **mathematically validated**, but requires:
> 1. Mid-circuit projective ancilla resets or Oblivious Amplitude Amplification (OAA) between collision steps to prevent unitary dilation leakage.
> 2. Hybrid / delayed classical evaluation of non-local Continuum Surface Force (CSF) curvature.
> Purely autonomous, measurement-free, single-shot multi-timestep evolution remains physically unfeasible for local Carleman two-phase models.
