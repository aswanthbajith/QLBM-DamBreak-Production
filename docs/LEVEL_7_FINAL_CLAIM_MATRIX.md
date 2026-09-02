# LEVEL-7: FINAL CLAIM MATRIX & TECHNICAL QUALIFICATIONS

**Document**: Master Inventory of Qualified Scientific Claims for Thesis and Publication  
**Repository**: `/home/aswa/Research/QLBM-DamBreak-Production`  
**Date**: September 2026  

---

## 1. Master Claim Inventory & Scientific Qualification

| Claim Ref | Raw Formulation | Identified Defect | Approved Qualified Formulation | Thesis Section |
| :--- | :--- | :--- | :--- | :---: |
| **CLM-01** | *"Fully coherent multi-step quantum solver"* | Wave-function collapse on ancilla and local quadratic re-lifting occur at each step. | *"Projected multi-step block-encoded quantum evolution with intermediate ancilla resets"* | Chapter 5 / Sec 5.2 |
| **CLM-02** | *"Autonomous quantum two-phase solver"* | Non-local CSF surface tension $\mathbf{F}_s = \sigma \kappa \nabla\alpha$ and moment decoding are evaluated on classical CPU. | *"Hybrid Quantum-Classical (HQC) two-phase lattice Boltzmann solver"* | Chapter 4 / Sec 4.3 |
| **CLM-03** | *"NISQ Tractable"* | Transpiled depth $> 3.76\text{M}$ with $> 831\text{k}$ 2Q ECR gates yields fidelity $\approx 0$ under NISQ noise. | *"Prospective Fault-Tolerant Quantum Computing (FTQC) logical architecture"* | Chapter 6 / Sec 6.4 |
| **CLM-04** | *"8 OAA queries achieves >99% success"* | 8 counts only forward $U_C$ calls; true execution requires 8 $U_C$ + 7 $U_C^\dagger$ + 14 reflections = 29 total operations. | *"m=7 Grover iterations (15 unitaries + 14 reflections) achieves 99.93% success probability"* | Chapter 5 / Sec 5.4 |
| **CLM-05** | *"19 total logical qubits"* | 19 qubits covers data registers only; full autonomous execution requires 2 additional algorithmic ancillas. | *"19 data logical qubits (21 total algorithmic logical qubits for 128x64 grid)"* | Chapter 6 / Sec 6.1 |
| **CLM-06** | *"Proved O(Ma^2) truncation scaling"* | Empirical power-law regression fit over discrete data points, not an analytic formal proof. | *"Empirical numerical scaling consistent with O(Ma^2) over the tested Mach range (Ma <= 0.1)"* | Chapter 4 / Sec 4.5 |
| **CLM-07** | *"First derivation of spatial streaming obstruction"* | Abstract tensor non-invariance is known; novelty lies in specific kinetic lattice derivation. | *"Candidate theoretical contribution: derivation of the local Carleman streaming obstruction in discrete velocity lattices"* | Chapter 5 / Sec 5.1 |
| **CLM-08** | *"Exact block-encoding composition"* | Applies strictly when projective ancilla resets are executed; unprojected dilation fails. | *"Exact power composition [P (alpha U) P^T]^K = C_2^K via mid-circuit projective ancilla reset"* | Chapter 5 / Sec 5.3 |
