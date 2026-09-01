# LEVEL-5: COUPLED CARLEMAN DESIGN & TRUNCATION STRATEGY

This document establishes the theoretical justification, block structures, and dimension scaling for the coupled Level-5 Carleman linearization.

---

## 1. Evaluation of Carleman Truncation Strategies

| Truncation Order | Local Dimension per Node ($d_k$) | Global Decoupled Dimension ($d_k N$) for $8\times 8$ | Polynomial Terms Captured | Evaluation & Justification |
| :---: | :---: | :---: | :---: | :--- |
| **Order 1 ($N_C = 1$)** | 18 | 1,152 | Linear advection & mass diffusion | **Insufficient**: Loses all convective momentum $\rho u_a u_b$ and nonlinear phase advection $\alpha u_a$. |
| **Order 2 ($N_C = 2$)** | $18 + 324 = \mathbf{342}$ | $\mathbf{21,888}$ | Linear + All quadratic convection + Bilinear phase coupling | **OPTIMAL**: Captures the complete weakly-compressible Navier-Stokes and phase advection dynamics to machine precision for low-Mach flow. |
| **Order 3 ($N_C = 3$)** | $18 + 324 + 5,832 = 6,174$ | $395,136$ | Quadratic + Cubic compressibility corrections $\mathcal{O}(\text{Ma}^3)$ | **Excessive Overhead**: 18x dimension increase with negligible accuracy gain for low Mach numbers ($\text{Ma} < 0.1$). |

**Conclusion**: **Second-Order Carleman Linearization ($N_C = 2, d_2 = 342$)** is the mathematically optimal and computationally tractable choice for the coupled two-phase D2Q9 system.

---

## 2. Autonomous Closed vs. Hybrid Observable Carleman Evolution

1. **Formulation A: Hybrid Observable Re-Lifting**:
   - At each timestep, evaluate the updated physical populations: $\mathbf{z}_{t+1}^* = A_{\text{eval}} \mathbf{Y}_t$, where $\mathbf{Y}_t = [\mathbf{z}_t; \mathbf{z}_t \otimes \mathbf{z}_t]$.
   - Perform spatial streaming $S$ and boundary reflection $B$.
   - Re-lift the quadratic layer $\mathbf{z}_{t+1} \otimes \mathbf{z}_{t+1}$ from the updated physical state.
   - *Advantage*: Guarantees exact polynomial closure and long-term multi-step stability without higher-order tensor divergence.

2. **Formulation B: Autonomous Closed Carleman Evolution**:
   - Advance the full 342-dimensional lifted state via matrix multiplication:
     $$\mathbf{Y}_{t+1} = C_2 \mathbf{Y}_t, \quad C_2 = \begin{bmatrix} M_1 & M_2 \\ 0 & M_1 \otimes M_1 \end{bmatrix} \in \mathbb{R}^{342 \times 342}$$
   - *Truncation Error*:
     $$E_2(t) = \|\mathbf{z}' \otimes \mathbf{z}' - (M_1 \otimes M_1)(\mathbf{z} \otimes \mathbf{z})\|_2$$
     Captures dropped quadratic-quadratic interactions ($M_1 \mathbf{z} \otimes M_2(\mathbf{z}\otimes\mathbf{z})$ and $M_2(\mathbf{z}\otimes\mathbf{z}) \otimes M_2(\mathbf{z}\otimes\mathbf{z})$).
