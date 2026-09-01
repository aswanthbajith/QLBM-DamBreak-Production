# LEVEL-6A-S: SCIENTIFIC STABILITY AND ROOT CAUSE FAILURE ANALYSIS

**Document**: Scientific Diagnosis of Multi-Timestep Divergence in Local Carleman QLBM  
**Branch**: `feature/level6a-local-carleman-core`  
**Date**: September 2026  

---

## 1. Executive Summary & Diagnostic Findings

Level-6A established that while single-timestep ($K=1$) local Carleman collision achieves excellent precision ($\rho$ error $\approx 2.33 \times 10^{-4}$, $\alpha$ error $\approx 2.67 \times 10^{-4}$), multi-timestep coherent execution ($K \ge 2$) without intermediate classical reconstruction exhibits a sharp jump in density error to $\approx 39.9\%$ at $K=2$ and $\approx 61.7\%$ at $K=3$.

The 15 diagnostic experiments conducted in Level 6A-S have conclusively isolated the root causes:

```text
                               ┌────────────────────────────────────────────────────────┐
                               │           Identified Dual Root Causes                  │
                               └───────────────────────────┬────────────────────────────┘
                                                           │
                      ┌────────────────────────────────────┴────────────────────────────────────┐
                      ▼                                                                         ▼
   ┌─────────────────────────────────────────┐               ┌─────────────────────────────────────────┐
   │            Root Cause 1                 │               │            Root Cause 2                 │
   │    Spatial Tensor Advection Mismatch    │               │     Unitary Dilation Subspace Leakage   │
   │  (S_lifted vs z_streamed (x) z_streamed)│               │          (P U_C^K P != C_2^K)           │
   │  - Causes 746% tensor inconsistency     │               │  - Relative dilation error = 2098%      │
   │    at K=1, corrupting K=2 convection    │               │    at K=2 without intermediate ancilla  │
   │    linear feedback                      │               │    postselection / reset            │
   └─────────────────────────────────────────┘               └─────────────────────────────────────────┘
```

---

## 2. Quantitative Evidence from the 15 Diagnostic Experiments

### A. Isolated Single-Site Carleman Collision (Experiment 5)
When spatial streaming and boundaries are removed, repeated application of the local Carleman collision map $C_2^K \mathbf{Y}_0$ to a single lattice site remains **highly accurate**:
- Liquid Node: Step 1 = $2.54 \times 10^{-4}$, Step 2 = $7.59 \times 10^{-4}$, Step 3 = $9.36 \times 10^{-4}$, Step 4 = $1.38 \times 10^{-3}$ ($0.138\%$).
- Gas Node: Step 1 = $8.70 \times 10^{-5}$, Step 2 = $2.71 \times 10^{-4}$, Step 3 = $3.18 \times 10^{-4}$, Step 4 = $4.84 \times 10^{-4}$ ($0.048\%$).
*Verdict*: The local algebraic Carleman collision tensor $C_2 = \begin{bmatrix} M_1 & M_2 \\ 0 & M_1 \otimes M_1 \end{bmatrix}$ is **mathematically sound and stable** for single-site ODE dynamics.

### B. Spatial Tensor Advection Inconsistency (Experiment 4)
In a spatial Lattice Boltzmann framework, spatial streaming shifts linear populations along $\mathbf{c}_a$:
$$z_a^*(\mathbf{x}) = z_a(\mathbf{x} - \mathbf{c}_a)$$
The true physical quadratic cross-term at destination node $\mathbf{x}$ is:
$$\left( \mathbf{z}^*(\mathbf{x}) \otimes \mathbf{z}^*(\mathbf{x}) \right)_{ab} = z_a(\mathbf{x} - \mathbf{c}_a) \cdot z_b(\mathbf{x} - \mathbf{c}_b)$$
However, independent Kronecker product streaming $S \otimes S$ shifts the cross-term by the sum of velocities $(\mathbf{c}_a + \mathbf{c}_b)$:
$$\mathbf{Y}_{\text{quad}, ab}^*(\mathbf{x}) = z_a(\mathbf{x} - \mathbf{c}_a - \mathbf{c}_b) \cdot z_b(\mathbf{x} - \mathbf{c}_a - \mathbf{c}_b)$$
- **Measured Inconsistency**:
  - $K = 0$: $E_{\text{tensor}} = 0.00\%$
  - $K = 1$: $E_{\text{tensor}} = 746.6\%$
  - $K = 2$: $E_{\text{tensor}} = 886.5\%$
*Verdict*: Linear spatial shift on the quadratic tensor $\mathbf{Y}_{\text{quad}}$ does **NOT** equal the tensor product of linearly shifted states ($\mathcal{S}(z \otimes z) \ne \mathcal{S}(z) \otimes \mathcal{S}(z)$). This creates spatial tensor de-correlation at $K=1$, feeding corrupted momentum flux into $M_2 \mathbf{Y}_{\text{quad}}$ at $K=2$.

### C. Multi-Step Unitary Dilation Subspace Leakage (Experiment 3)
For a Sz.-Nagy unitary dilation $U_C = \begin{bmatrix} C_2/\alpha_C & D_* \\ D & -C_2^T/\alpha_C \end{bmatrix}$:
- At $K=1$: $\|P (\alpha_C U_C) P^T - C_2\|_2 = 6.34 \times 10^{-16}$ (Exact block encoding).
- At $K=2$: $\|P (\alpha_C U_C)^2 P^T - C_2^2\|_2 = 94.68$ (Relative error = $2098.7\%$).
*Verdict*: Applying an unmeasured unitary dilation $U_C$ repeatedly leaks quantum amplitude into the auxiliary dilation subspace $D$. Without intermediate ancilla measurement / postselection after every step, $U_C^K$ does **NOT** compute $(C_2/\alpha_C)^K$.

### D. Empirical Rejection of the $\mathcal{O}(K \text{Ma}^3)$ Scaling Claim (Experiment 6)
- **Fitted Mach exponent**: $E \propto \text{Ma}^{0.00}$ (error is completely independent of Mach number in spatial flow).
- **Fitted Timestep exponent**: $E \propto K^{5.59}$ (sharp jump from $K=1$ to $K=2$).
*Verdict*: The previous theoretical claim that spatial multi-timestep Carleman error scales as $\mathcal{O}(K \cdot \text{Ma}^3)$ is **EMPIRICALLY REJECTED**.

---

## 3. Classification of Failure Modes

| Potential Failure Cause | Status | Contribution to $K \ge 2$ Error |
| :--- | :---: | :--- |
| **A. Carleman Collision Truncation (Single Site)** | **Negligible** | Local error is $< 0.14\%$ across 4 steps. |
| **B. Invalid Low-Mach Taylor Regime** | **Minor** | Mach number remains $\le 0.05$ during initial steps. |
| **C. Tensor-Sector Spatial Streaming Inconsistency** | **PRIMARY CAUSE** | $746\%$ tensor de-correlation caused by $\mathcal{S}(z\otimes z) \ne \mathcal{S}(z)\otimes\mathcal{S}(z)$. |
| **D. Unitary Dilation Subspace Leakage** | **PRIMARY CAUSE** | $2098\%$ error in $P U_C^2 P$ vs $C_2^2$ due to unprojected dilation cross-terms. |
| **E. Boundary Treatment** | **Secondary** | Contributes to localized wall reflections but not bulk instability. |
| **F. Parameter Mismatch** | **None** | Physical parameters $\tau_f, \tau_g, g_{\text{acc}}, w_i$ are identical. |

---

## 4. Formal Answers to Key Questions

1. **Does the Level-6A lifted map itself reproduce the Level-4 nonlinear map?**  
   **YES (for single step)**. At $K=1$, density error is $2.33 \times 10^{-4}$ ($0.023\%$) and local single-site error is $< 0.14\%$.
2. **Does the tensor sector remain consistent?**  
   **NO**. Spatial streaming causes $746\%$ tensor inconsistency at $K=1$.
3. **Does repeated unitary dilation reproduce repeated Carleman evolution?**  
   **NO**. $P U_C^K P \ne C_2^K$ due to subspace leakage into dilation blocks.
4. **Is the $\mathcal{O}(K \text{Ma}^3)$ claim supported?**  
   **NO (REJECTED)**. Fitted scaling is $E \propto \text{Ma}^{0.00}$ and $E \propto K^{5.59}$.
5. **What causes the $K=2 \approx 40\%$ density error?**  
   The combination of spatial tensor advection mismatch ($\mathcal{S}_{\text{lifted}}$) and dilation subspace leakage.
6. **Decision Gate Verdict**: **YELLOW** (Coherent single-step propagation and local Carleman collision are verified, but spatial multi-step tensor re-coupling / stabilization is required before full Level-6B scale-up).
7. **What exact mathematical change is required before Level-6B?**  
   Introduce a **Local Carleman Tensor Re-Coupling Operator** or mid-circuit ancilla reset / postselection between spatial steps to prevent tensor drift and dilation leakage.
