# PHASE 5 QUANTUM RESOURCE SCALING & ASYMPTOTIC COMPLEXITY

**Status**: Verified Asymptotic & Empirical Resource Analysis  
**Date**: 2026-08-19  

---

## 1. Multi-Scale Resource Table

| Lattice Nodes ($N$) | Grid ($N_x \times N_y$) | Carleman Dimension ($D_C$) | Logical Qubits ($n_{\text{tot}}$) | Matrix Non-Zeros ($NNZ$) | Sparse RAM (MB) | Dense RAM (GB) | Classification |
| :--- | :--- | :--- | :--- | :--- | :--- | :--- | :--- |
| **$N = 1$** | $1 \times 1$ | 342 | 10 | 4,212 | 0.05 | 0.001 | **MEASURED** |
| **$N = 8$** | $4 \times 2$ | 2,736 | 13 | 33,696 | 0.41 | 0.06 | **MEASURED** |
| **$N = 32$** | $8 \times 4$ | 10,944 | 15 | 134,784 | 1.65 | 0.95 | **MEASURED** |
| **$N = 128$** | $16 \times 8$ | 43,776 | 17 | 539,136 | 6.58 | 15.26 | **SIMULATED** |
| **$N = 512$** | $32 \times 16$ | 175,104 | 19 | 2,156,544 | 26.33 | 245.29 | **SIMULATED** |
| **$N = 2,048$** | $64 \times 32$ | 700,416 | 21 | 8,626,176 | 105.31 | 3,924.6 | **SIMULATED** |
| **$N = 30,000$** | $300 \times 100$ | 10,260,000 | 25 | 126,360,000 | 1,542.4 | $842,150$ | **ANALYTICAL** |

---

## 2. Asymptotic Scaling Laws
1. **Logical Qubit Requirement**:
   $$n_{\text{qubits}}(N) = \left\lceil \log_2(342 \cdot N) \right\rceil + 1 = \lceil \log_2(N) \rceil + 10$$
   Qubits scale strictly **logarithmically** $\mathcal{O}(\log N)$.
2. **Matrix Sparsity**:
   The number of non-zero entries per row in $A_C$ is strictly bounded by $K_{\max} = 18 + 18 \times 18 = 342$. Hence, $NNZ(A_C) = \mathcal{O}(N)$ (linear in grid points).
3. **Dense vs. Sparse Storage at Production Scale ($300 \times 100$)**:
   * Storing $A_C$ as a dense $10.26M \times 10.26M$ complex matrix requires **$842.15$ Terabytes of RAM** (impossible on classical single nodes).
   * Storing $A_C$ as a sparse matrix requires only **$1.54$ Gigabytes of RAM**.
   * Quantum block encoding encodes this linear operator into **25 qubits**.
