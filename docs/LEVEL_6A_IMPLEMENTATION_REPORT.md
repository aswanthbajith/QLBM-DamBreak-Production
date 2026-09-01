# LEVEL-6A IMPLEMENTATION & COHERENT MULTI-TIMESTEP REPORT

**Objective**: Validate coherent multi-timestep evolution under the local Carleman operator without intermediate state decoding.

## 1. Unitary Dilation Verification

- Block dimension of $C_2$: $342 \times 342$
- Unitary dilation size $U_C$: $1024 \times 1024$ (10 qubits)
- Unitarity error: $\|U_C^\dagger U_C - I_{1024}\|_2 = 2.2862e-13$
- Projection error: $\|\alpha_C \langle 0| U_C |0\rangle - C_2\|_2 = 1.0692e-16$
- Dilation scaling factor $\alpha_C$: 7.9004

## 2. Multi-Step Coherent Evolution vs. Level-4 Reference

| Coherent Steps ($K$) | Hydrodynamic $f_i$ Rel $L_2$ | Phase $g_i$ Rel $L_2$ | Density $\rho$ Rel $L_2$ | Phase Fraction $\alpha$ Rel $L_2$ | Postselection Success ($p_{\text{succ}}$) |
| :---: | :---: | :---: | :---: | :---: | :---: |
| $K = 1$ | 3.2500e-04 | 3.2100e-04 | 2.3300e-04 | 2.6700e-04 | 1.0558e-02 |
| $K = 2$ | 4.2700e-01 | 2.3729e-01 | 3.9941e-01 | 2.0491e-01 | 1.1148e-04 |
| $K = 3$ | 7.3472e-01 | 3.0661e-01 | 6.1670e-01 | 1.4853e-01 | 1.1770e-06 |
| $K = 4$ | 7.1037e-01 | 3.0113e-01 | 4.0701e-01 | 2.0496e-01 | 1.2427e-08 |

## 3. Measurement & Reinitialization Reduction

| Coherent Horizon ($K$) | HQC State Readouts | Level-6A State Readouts | Reduction Factor |
| :---: | :---: | :---: | :---: |
| $K = 1$ | 1 | 1 | **1x** |
| $K = 2$ | 2 | 1 | **2x** |
| $K = 3$ | 3 | 1 | **3x** |
| $K = 4$ | 4 | 1 | **4x** |

## 4. Key Scientific Conclusions & Root-Cause Diagnosis

1. **Demonstration of Coherent Multi-Timestep Evolution**: Level 6A successfully propagates the lifted tensor state $\mathbf{Y} \in \mathbb{R}^{342}$ across $K = 2, 3, 4$ steps without intermediate classical decoding or state reconstruction, achieving an exact $K\times$ reduction in measurement roundtrips.
2. **Single-Site Carleman Precision**: When isolated on a single node without spatial streaming, the algebraic Carleman collision map $C_2^K \mathbf{Y}_0$ is highly accurate ($< 0.14\%$ error across 4 steps).
3. **Dual Root Causes of Multi-Step Spatial Divergence**:
   - **Spatial Tensor Advection Mismatch**: $\mathcal{S}_{\text{lifted}}(\mathbf{z} \otimes \mathbf{z}) \ne \mathcal{S}(\mathbf{z}) \otimes \mathcal{S}(\mathbf{z})$, producing $746\%$ tensor de-correlation at $K=1$, which injects corrupted convective momentum into $M_2 \mathbf{Y}_{\text{quad}}$ at $K=2$.
   - **Unitary Dilation Subspace Leakage**: $P U_C^K P \ne C_2^K$, introducing $2098\%$ leakage into the dilation complement subspace without mid-circuit ancilla projection/reset.
4. **Rejection of $\mathcal{O}(K \text{Ma}^3)$ Spatial Scaling**: Empirical scaling fits show $E \propto \text{Ma}^{0.00}$ and $E \propto K^{5.59}$ in spatial simulations.
5. **Decision Gate Verdict**: **YELLOW** — Coherent propagation works algebraically, but spatial tensor re-coupling / mid-circuit ancilla stabilization is required before Level-6B scaling.
