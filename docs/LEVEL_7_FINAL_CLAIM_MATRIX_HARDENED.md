# LEVEL-7: HARDENED CLAIM MATRIX & SCIENTIFIC VOCABULARY
## Master Inventory of Claims, Supporting Evidence, and Approved Academic Formulations

**Document**: Definitive Claim Classification Matrix for Thesis and Manuscript  
**Repository**: `/home/aswa/Research/QLBM-DamBreak-Production`  
**Date**: September 2026  

---

## 1. Master Hardened Claim Matrix

| Claim / Research Area | Mathematical / Numerical Evidence | Scientific Status | Approved Hardened Wording |
| :--- | :--- | :---: | :--- |
| **Classical Two-Phase LBM Baseline** | Replicated Martin & Moyce experimental surge front within $< 7\%$ error (`classical/level4_two_phase.py`). | **GREEN** | *"Validated classical two-phase Lattice Boltzmann (D2Q9) dam-break baseline"* |
| **Coupled Carleman Representation** | Matrix dimension $342 \times 342$, polynomial error $\mathcal{O}(\text{Ma}^2)$ verified. | **GREEN** | *"Coupled second-order Carleman-linearized low-Mach representation"* |
| **Quantum Block Encoding** | $\|P (\alpha_C U_C) P^T - C_2\| < 10^{-12}$; $\|U_C^\dagger U_C - I\| < 10^{-15}$. | **GREEN** | *"10-Qubit Sz.-Nagy unitary dilation block encoding"* |
| **Spatial Tensor Streaming Repair** | Permutation streaming on linear sector + local re-lifting achieves $0.000000 \times 10^0$ error. | **GREEN** | *"Exact invariant manifold preservation via linear permutation streaming and local quadratic re-lifting"* |
| **Unprojected Multi-Step Coherence** | Diverges with $2098\%$ error at $K=2$ due to defect leakage. | **RED (Defect Proven)** | *"Unprojected dilation multiplication fails due to defect-subspace leakage; not established as a viable solver"* |
| **Projected Multi-Step Evolution** | $[P (\alpha_C U_C) P^T]^K = C_2^K$ verified within $< 1.71 \times 10^{-15}$ up to $K=32$. | **YELLOW (Conditional Prototype)** | *"Projected multi-step block-encoded quantum evolution with intermediate ancilla resets"* |
| **Measurement-Free Multi-Step** | Not achieved; ancilla resets are mathematically mandatory. | **RED (Not Achieved)** | *"Not demonstrated in the present architecture; intermediate resets are required"* |
| **Fully Quantum CSF Surface Tension** | Curvature $\kappa$ is evaluated on classical CPU using finite differences. | **RED (Not Achieved)** | *"Hybrid classical Continuum Surface Force (CSF) feedback"* |
| **NISQ Hardware Execution** | Transpiled depth $> 3.76\text{M}$ with $> 831\text{k}$ ECR gates yields $F_{\text{circuit}} \approx 0$ under NISQ noise. | **RED (Not Viable)** | *"Not NISQ-practical at demonstrated resource scale; prospective Fault-Tolerant (FTQC) logical architecture"* |
| **FTQC Prospective Compilation** | 21 logical qubits derived ($128\times 64$ lattice); depth $> 3.76\text{M}$. | **BLUE (Prospective Architecture)** | *"Prospective logical fault-tolerant quantum computing architecture"* |
| **Real IBM QPU Execution** | Simulated backend profiling only; safety interlocks active. | **RED (Not Executed)** | *"Simulated FakeSherbrooke hardware resource estimation (no real-QPU execution)"* |
| **Quantum Speedup / Advantage** | Classical simulation scales exponentially in qubit count. | **RED (Not Demonstrated)** | *"Quantum speedup / advantage not demonstrated; polynomial advantage requires fault-tolerant logical QPUs"* |
| **Research Novelty Claims** | Prior literature benchmarked; spatial obstruction and 2-phase block encoding unaddressed in prior art. | **YELLOW (Candidate Contribution)** | *"Candidate theoretical and methodological research contributions"* |
