# Master Quantum Carleman Linear Operator Handoff Specification

**Author**: Lead Quantum Algorithm Engineer & Quantum Linear Algebra Specialist  
**Date**: August 19, 2026  
**Repository**: `/home/aswa/Research/QLBM-DamBreak/`  

---

## 1. Frozen Linear Operator Specification

The quantum linear algebra pipeline operates strictly on the validated second-order Carleman matrix $\mathbf{A}_C$:
$$ \mathbf{Y}(t+1) = \mathbf{A}_C \mathbf{Y}(t) + \mathbf{b}_C $$

### Operator Structural Properties:
- **Mathematical Factorization**: $\mathbf{A}_C = \mathbf{S}_C \cdot \mathbf{C}_2 \in \mathbb{R}^{342 N \times 342 N}$
- **Global Dimension**: $D_C(N) = 342 N$ ($18 N$ linear $+ 324 N$ quadratic state variables).
- **Matrix Non-Zero Count (NNZ)**: $\approx 27,334 N$ non-zeros.
- **Sparse Storage Format**: SciPy Compressed Sparse Row (`csr_matrix`, `float64`).
- **Spectral Norm ($\|A_C\|_2$)**: **$10.9275$** (Invariant across all spatial grid nodes $N \ge 1$ due to local collision and unitary streaming).
- **Max Row-Sum Norm ($\|A_C\|_\infty$)**: **$73.0238$**.
- **Max Column-Sum Norm ($\|A_C\|_1$)**: **$11.4690$**.

---

## 2. Global State-Space Basis Ordering

The $D_C = 342 N$ indices of $\mathbf{Y}$ are partitioned into three contiguous sectors:

```
Index Range                  Dimension      Physical Content
─────────────────────────────────────────────────────────────────────────────
0           ..  9N - 1       9 N            Hydrodynamic populations g_0 .. g_8
9N          .. 18N - 1       9 N            Phase-field populations h_0 .. h_8
18N         .. 342N - 1      324 N          Local quadratic monomials psi_n (x) psi_n
```

### Local Node Monomial Indexing:
For node $n \in \{0, \dots, N-1\}$ and velocity pair $(q_1, q_2) \in \{0, \dots, 17\}^2$:
$$ \text{Quadratic Index} = 18 N + (q_1 \cdot 18 + q_2) N + n $$
where $q_1, q_2 \in 0..8$ correspond to hydrodynamic distributions $\mathbf{g}$, and $q_1, q_2 \in 9..17$ correspond to phase-field distributions $\mathbf{h}$.

---

## 3. Quantum Register Sizing across Standard Grids

| Grid ($N_x \times N_y$) | Nodes $N$ | Carleman Dim $D_C$ | Padded Dim $2^n$ | System Qubits $n_{sys}$ | Ancilla Qubits $n_{anc}$ | Total Qubits |
| :---: | :---: | :---: | :---: | :---: | :---: | :---: |
| **$1 \times 1$** | 1 | 342 | 512 | 9 | 1 | **10** |
| **$2 \times 1$** | 2 | 684 | 1,024 | 10 | 1 | **11** |
| **$2 \times 2$** | 4 | 1,368 | 2,048 | 11 | 1 | **12** |
| **$4 \times 2$** | 8 | 2,736 | 4,096 | 12 | 1 | **13** |
| **$8 \times 4$** | 32 | 10,944 | 16,384 | 14 | 1 | **15** |
| **$16 \times 8$** | 128 | 43,776 | 65,536 | 16 | 1 | **17** |
| **$32 \times 16$**| 512 | 175,104 | 262,144 | 18 | 1 | **19** |
| **$64 \times 32$**| 2,048 | 700,416 | 1,048,576 | 20 | 1 | **21** |
| **$300 \times 100$**| 30,000 | 10,260,000 | 16,777,216 | 24 | 1 | **25** |
