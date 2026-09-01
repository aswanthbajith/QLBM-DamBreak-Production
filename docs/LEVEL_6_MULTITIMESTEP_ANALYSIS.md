# LEVEL-6: COHERENT MULTI-TIMESTEP QUANTUM PROPAGATION REQUIREMENTS

This document establishes the theoretical requirements, closure conditions, and stability criteria for propagating a quantum two-phase Lattice Boltzmann state across multiple timesteps ($|\Psi(t+N_t)\rangle = \mathcal{U}^{N_t} |\Psi(t)\rangle$) without full intermediate state extraction.

---

## 1. Systematic Comparison of Multi-Timestep Quantum Paradigms

| Paradigm | Autonomous? | Measurement-Free? | Reinitialization-Free? | Exact vs. Approximate | Physically Complete? | Hardware Feasibility |
| :--- | :---: | :---: | :---: | :---: | :---: | :---: |
| **1. Fixed Linear Operator** | Yes | Yes | Yes | Approximate (Loses non-linear convection $\rho u_a u_b$) | No (Stokes flow only) | NISQ / Early FTQC |
| **2. Local Carleman Lift ($C_2 \in \mathbb{R}^{342\times 342}$)** | **Yes (for $K$ steps)** | **Yes (for $K$ steps)** | **Yes (for $K$ steps)** | **Approximate ($\mathcal{O}(\text{Ma}^3)$ unclosed truncation)** | **Yes (Navier-Stokes + Phase)** | **Early FTQC ($K \le 5$)** |
| **3. Global Spacetime QLSA / QSVT ($L \mathbf{y}=\mathbf{b}$)** | Yes | Yes | Yes | Approximate ($\epsilon$-polynomial inversion) | Moderate (Static $L$ only) | Mature FTQC |
| **4. Ancilla-Mediated Non-linear Evaluation** | Yes | No (requires mid-circuit resets) | Partial | Exact | Yes | Dynamic Circuits |
| **5. Reversible Arithmetic Oracles** | Yes | Yes | Yes | Exact (to float precision) | Yes | Extreme Overheads ($> 10^7$ gates) |
| **6. Hybrid Quantum-Classical (HQC)** | No | No | No | Exact Level-4 physics | Yes | **Immediate / NISQ** |

---

## 2. Closure & Stability of Local Carleman Multi-Timestep Evolution

For $K$ autonomous steps under the second-order Carleman operator $C_2 = \begin{bmatrix} M_1 & M_2 \\ 0 & M_1 \otimes M_1 \end{bmatrix}$:
1. **Spectral Stability**: $\rho(C_2) = \max(\rho(M_1), \rho(M_1 \otimes M_1)) = \rho(M_1)^2 = 1.0000$ (non-divergent, neutrally stable).
2. **Truncation Accumulation**: Truncation error grows as $\mathcal{O}(K \cdot \text{Ma}^3)$. For $\text{Ma} = 0.05$, $K=3$ produces $< 0.4\%$ accumulated drift.
3. **Optimal Block Size ($K^*$)**:
   - $K = 1$: Standard HQC (highest classical overhead, exact closure).
   - $K = 2 \dots 4$: **Optimal Local Carleman sweet spot** (reduces measurement overhead by $2\times - 4\times$, maintains $< 2\%$ physical truncation error).
   - $K > 10$: Dilation compounding ($\alpha_C^K$) requires high-depth amplitude amplification.
