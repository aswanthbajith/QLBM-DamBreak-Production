# Mathematical Carleman State-Space Dimension Analysis

**Author**: Lead Mathematical Modeler & Numerical Analyst  
**Date**: August 19, 2026  
**Repository**: `/home/aswa/Research/QLBM-DamBreak/`  

---

## 1. Carleman Dimension Scaling Formulas

Let $N = N_x \times N_y$ be the total spatial grid nodes.
The base state vector $\mathbf{\Psi} \in \mathbb{R}^{18 N}$ comprises $9$ hydrodynamic and $9$ phase populations per node.

Under spatial locality (assembling Kronecker monomials per local node rather than globally), the state space dimension scales strictly **linearly with grid nodes $N$**:

| Truncation Order | Included State Monomials | Exact Node Dimension $d_{node}$ | Global Carleman Dimension $D_C(N)$ | Qubits Required $n = \lceil\log_2 D_C\rceil + 1$ |
| :---: | :--- | :---: | :---: | :---: |
| **Order $N_C = 1$ (Linear)** | $\mathbf{\psi}_n$ | $18$ | **$18 N$** | $\lceil\log_2(18N)\rceil + 1$ |
| **Order $N_C = 2$ (Quadratic)** | $\mathbf{\psi}_n, \mathbf{\psi}_n^{\otimes 2}$ | $18 + 18^2 = 342$ | **$342 N$** | $\lceil\log_2(342N)\rceil + 1$ |
| **Order $N_C = 3$ (Cubic)** | $\mathbf{\psi}_n, \mathbf{\psi}_n^{\otimes 2}, \mathbf{\psi}_n^{\otimes 3}$ | $18 + 324 + 5832 = 6174$ | **$6,174 N$** | $\lceil\log_2(6174N)\rceil + 1$ |

---

## 2. Dimensional Accounting across Benchmark Grids

| Grid Domain ($N_x \times N_y$) | Spatial Nodes $N$ | Order 1 Dimension ($18N$) | Order 1 Qubits | Order 2 Dimension ($342N$) | Order 2 Qubits | Order 3 Dimension ($6174N$) | Order 3 Qubits |
| :---: | :---: | :---: | :---: | :---: | :---: | :---: | :---: |
| **$1 \times 1$ (Single Node)** | 1 | 18 | 6 | **342** | **10** | 6,174 | 14 |
| **$2 \times 1$ (Minimal)** | 2 | 36 | 7 | **684** | **11** | 12,348 | 15 |
| **$2 \times 2$ (Coarse)** | 4 | 72 | 8 | **1,368** | **12** | 24,696 | 16 |
| **$4 \times 2$ (Small)** | 8 | 144 | 9 | **2,736** | **13** | 49,392 | 17 |
| **$4 \times 4$ (Medium)** | 16 | 288 | 10 | **5,472** | **14** | 98,784 | 18 |
| **$8 \times 4$ (Test Grid)** | 32 | 576 | 11 | **10,944** | **15** | 197,568 | 19 |
| **$16 \times 8$ (Refined)** | 128 | 2,304 | 13 | **43,776** | **17** | 790,272 | 21 |
| **$32 \times 16$ (Intermediate)**| 512 | 9,216 | 15 | **175,104** | **19** | 3,161,088 | 23 |
| **$64 \times 32$ (Fine)** | 2,048 | 36,864 | 17 | **700,416** | **21** | 12,644,352 | 25 |
| **$300 \times 100$ (Production)**| 30,000 | 540,000 | 21 | **10,260,000** | **25** | 185,220,000 | 29 |

---

## 3. Key Findings on Quantum Register Allocation
1. **Exponential State Compression**: For the full $300 \times 100$ macroscopic fluid domain ($30,000$ spatial sites, $10,260,000$ quadratic Carleman state variables), exactly **25 logical qubits** ($24$ system qubits $+ 1$ block-encoding ancilla) represent the entire system.
2. **Sparsity Scaling**: Because each node interacts only with its nearest lattice neighbors via $\mathbf{S}$, the Carleman matrix $\mathbf{A}_C$ contains $\mathcal{O}(N)$ non-zeros, ensuring that the number of non-zero elements per row is independent of $N$.
