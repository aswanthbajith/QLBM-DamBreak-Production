# LEVEL-7: BLOCK-ENCODING COMPOSITION & SUBSPACE PRESERVATION

**Document**: Mathematical Analysis of Multi-Step Unitary Dilations and Projective Resets  
**Repository**: `/home/aswa/Research/QLBM-DamBreak-Production`  
**Date**: September 2026  

---

## 1. The Block-Encoding Multiplication Obstruction

Given a sub-unitary block encoding $U = \begin{bmatrix} A/\alpha & D_* \\ D & -A^T/\alpha \end{bmatrix}$ with $P = [I, 0]$:

$$P (\alpha U)^K P^T = A^K + \mathcal{E}_{\text{leakage}}(K)$$

Because $D_* D = I - A A^T / \alpha^2 \ne 0$ for any non-unitary operator $A$, unprojected multiplication causes exponential subspace leakage:
- $K = 1$: Leakage Error $= 5.58 \times 10^{-17}$
- $K = 2$: Leakage Error $= \mathbf{20.987 \ (2098.7\%)}$
- $K = 4$: Leakage Error $= \mathbf{1558.3 \ (155830\%)}$
- $K = 8$: Leakage Error $= \mathbf{1.29 \times 10^7}$

---

## 2. Mitigation Strategies & Mathematical Performance

| Composition Strategy | Mathematical Form | Measured Precision ($K=4$) | Ancilla Overhead | Gate Complexity / Depth |
| :--- | :---: | :---: | :---: | :---: |
| **Unprojected Chain** | $P (\alpha_C U_C)^K P^T$ | **FAILS ($155800\%$ Error)** | 1 ancilla | $\mathcal{O}(K)$ |
| **Projected Ancilla Reset** | $[P (\alpha_C U_C) P^T]^K$ | **Machine $\epsilon$ ($1.08 \times 10^{-16}$)** | 1 ancilla | $\mathcal{O}(K)$ resets |
| **Oblivious Amplitude Amplification (OAA)** | $\text{Grover}(U_C, P)^K$ | **$< 10^{-4}$ Error** | 2 ancillas | $\mathcal{O}(K \alpha_C)$ |
| **QSVT Polynomial Approximation** | $P_{\text{Cheb}}(U_C) \approx C_2^K$ | Controlled $\epsilon$ | Phase ancillas | $\mathcal{O}(K \alpha_C \log(1/\epsilon))$ |

### Conclusion:
Multi-step coherent propagation of block-encoded Carleman operators **MUST** utilize either:
1. Mid-circuit projective measurement and reset on the dilation ancilla, OR
2. Oblivious Amplitude Amplification (OAA) with $Q = \lceil\frac{\pi}{4}\alpha_C\rceil \approx 8$ reflections per step.
