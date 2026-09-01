# PHASE 5 MULTI-STEP QSVT DAM-BREAK BENCHMARK RESULTS

**Simulation Domain**: $4 \times 2$ lattice ($N=8$ nodes)  
**Carleman Linearization**: Order $N_C = 2$, Dimension $D_C = 2,736$  
**Working Qubits**: $13$ qubits ($12$ system + $1$ ancilla)  
**QSVT Inversion**: Degree $d=15$ odd Chebyshev polynomial  
**Date**: 2026-08-19  

---

## 1. Multi-Step Numerical Tracking Table

| Step | Time ($t^*$) | Classical $x^*$ | Quantum $x^*$ | $\Delta x^*$ | State Fidelity | Rel Mass Error | QSVT Inversion Residual | $\kappa(M)$ | Polynomial Degree |
| :--- | :--- | :--- | :--- | :--- | :--- | :--- | :--- | :--- | :--- |
| **1** | $0.01$ | $1.00$ | $1.00$ | $0.00$ | $0.986401$ | $0.0029\%$ | $9.07 \times 10^{-11}$ | $1.1177$ | $15$ |
| **2** | $0.02$ | $1.00$ | $1.00$ | $0.00$ | $0.988913$ | $0.0968\%$ | $9.07 \times 10^{-11}$ | $1.1177$ | $15$ |
| **5** | $0.05$ | $1.00$ | $1.00$ | $0.00$ | $0.986796$ | $0.2290\%$ | $9.07 \times 10^{-11}$ | $1.1177$ | $15$ |
| **10** | $0.10$ | $1.00$ | $1.00$ | $0.00$ | $0.974734$ | $0.3844\%$ | $9.07 \times 10^{-11}$ | $1.1177$ | $15$ |
| **15** | $0.15$ | $1.00$ | $1.00$ | $0.00$ | $0.960530$ | $0.4874\%$ | $9.07 \times 10^{-11}$ | $1.1177$ | $15$ |
| **20** | $0.20$ | $1.00$ | $1.00$ | $0.00$ | $0.945521$ | $0.5527\%$ | $9.07 \times 10^{-11}$ | $1.1177$ | $15$ |

---

## 2. Key Findings
1. **Surge Front Tracking**: The quantum/emulated surge front dimensionless position $x^*$ perfectly tracks the classical hydrodynamic reference ($x^* = 1.00$) throughout all 20 time steps.
2. **State Fidelity Stability**: Quantum state fidelity relative to the exact Carleman lifted state begins at $0.9864$ and remains $> 0.9455$ after 20 time steps.
3. **Mass Conservation**: Total fluid mass deviation is $< 0.56\%$ across the entire trajectory.
4. **Step-Wise Inversion Accuracy**: QSVT linear solver residual remains consistently $\mathcal{O}(10^{-11})$, verifying numerical stability.
