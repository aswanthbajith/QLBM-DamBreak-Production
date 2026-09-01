# LEVEL-6B: COMPREHENSIVE CLAIM AUDIT & VOCABULARY PURIFICATION

**Document**: Scientific Claim Verification, Qualification, and Vocabulary Audit  
**Repository**: `/home/aswa/Research/QLBM-DamBreak-Production`  
**Date**: September 2026  

---

## 1. Claim Classification Matrix

| Search Term / Phrase | Audited Status | Scientific Assessment & Evidence | Recommended Professor-Safe Wording |
| :--- | :---: | :--- | :--- |
| **"Fully quantum solver"** | **RED (Removed)** | The solver is explicitly Hybrid $K=1$. Streaming, boundary, CSF, and moment decoding occur classically. | *"Hybrid Quantum-Classical (HQC) QLBM Solver"* |
| **"Measurement-free multi-timestep"** | **RED (Removed)** | Classical decoding / projection occurs at every physical timestep ($K=1$) to prevent dilation leakage and tensor mismatch. | *"One-step quantum Carleman collision block with intermediate classical reconstruction"* |
| **"Autonomous quantum PDE solver"** | **RED (Removed)** | Spatial coupling and non-local CSF are evaluated classically in hybrid loop. | *"Hybrid quantum-classical timestep architecture"* |
| **"Quantum speedup / advantage"** | **RED (Removed)** | Emulation runtime on classical CPU is exponential in qubit count; physical speedup requires fault-tolerant logical QPUs. | *"Quantum algorithmic formulation with logarithmic spatial qubit addressing"* |
| **"Exact Navier-Stokes solution"** | **RED (Removed)** | Second-order Carleman is a weakly compressible, low-Mach approximation ($\mathcal{E} \propto \text{Ma}^2$). | *"Second-order Carleman-linearized low-Mach approximation"* |
| **"100% of error from Carleman"** | **YELLOW (Qualified)** | Controlled Exp B drops discrepancy to machine precision ($0.000000$), but relaxation and density offsets also contribute minor shares. | *"Carleman convective truncation is the dominant identified error source (~88.5% empirical attribution)"* |
| **"Formal spatial convergence"** | **YELLOW (Qualified)** | Refinement from $16\times 8$ to $256\times 128$ shows monotonic error drop ($31.7\% \to 5.97\%$), but asymptotic rate is $p \approx 0.54$. | *"Monotonic refinement trend observed over tested multi-grid lattices"* |
| **"Exact mass conservation"** | **YELLOW (Qualified)** | Classical Level 4 and Level 6B both exhibit a slight mass drift ($\le 1.528\%$ across 50 steps). | *"Strictly bounded mass drift ($\le 1.53\%$ across 50 timesteps)"* |
| **"Exact linear streaming"** | **GREEN (Verified)** | Spatial streaming on 18 linear populations is an exact permutation ($L_2$ norm diff $< 10^{-12}$). | *"Exact permutation streaming on linear population sector"* |
| **"Exact local tensor re-lifting"** | **GREEN (Verified)** | $\mathbf{Y}(\mathbf{x}) = [\mathbf{z}(\mathbf{x}); \mathbf{z}(\mathbf{x}) \otimes \mathbf{z}(\mathbf{x})]$ preserves invariant manifold $\mathcal{M}$ to machine precision ($0.00\times 10^0$). | *"Exact local quadratic Kronecker re-lifting per timestep"* |
| **"Unitary block encoding"** | **GREEN (Verified)** | 10-qubit Sz.-Nagy unitary dilation $U_C \in \mathbb{U}(1024)$ satisfies $\|U_C^\dagger U_C - I\| < 10^{-12}$ and $\|P(\alpha_C U_C)P^T - C_2\| < 10^{-12}$. | *"Unitary dilation block encoding of the second-order Carleman collision matrix"* |
| **"Real IBM QPU execution"** | **GREEN (Verified Safe)** | Safety interlocks `QLBM_ENABLE_REAL_QPU=0` and `QLBM_CONFIRM_REAL_QPU=NO` verified active. Transpilation is mock backend profiling. | *"Simulated IBM Heavy-Hex hardware resource estimation"* |

---

## 2. Vocabulary Enforcement Rules for Thesis & Presentation

1. Use **"Hybrid Quantum-Classical (HQC)"** unconditionally. Never refer to the solver as "fully quantum".
2. Use **"Second-order Carleman approximation"**. Never claim "exact polynomialization".
3. Use **"Monotonic refinement trend"**. Avoid claiming "proven asymptotic second-order continuum convergence".
4. Use **"Empirical error attribution"**. Never claim "mathematically additive linear error budget".
5. Use **"Transpilation / Resource Estimation"**. Never claim "IBM hardware execution" without physical job IDs.
