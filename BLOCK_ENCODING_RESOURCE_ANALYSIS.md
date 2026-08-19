# Comprehensive Quantum Resource Scaling & Complexity Analysis

**Author**: Lead Quantum Algorithm Engineer & Quantum Linear Algebra Specialist  
**Date**: August 19, 2026  
**Repository**: `/home/aswa/Research/QLBM-DamBreak/`  

---

## 1. Resource Scaling Table from $N=1$ to Production $N=30,000$

| Grid Domain | Nodes $N$ | Carleman Dim $D_C$ | Padded Dim $D_{pad}$ | System Qubits $n_{sys}$ | Ancilla Qubits $a$ | Total Qubits | Normalization $\alpha$ | Matrix NNZ | Sparsity | Classical RAM for SVD | Quantum Execution Feasibility | Data Category |
| :---: | :---: | :---: | :---: | :---: | :---: | :---: | :---: | :---: | :---: | :---: | :--- | :---: |
| **$1 \times 1$** | 1 | 342 | 512 | 9 | 1 | **10** | 11.50 | 27,334 | $2.34 \times 10^{-1}$ | $\approx 8 \text{ MB}$ | **Exact Statevector Execution** | **ACTUAL MEASURED** |
| **$2 \times 1$** | 2 | 684 | 1,024 | 10 | 1 | **11** | 11.50 | 54,668 | $1.17 \times 10^{-1}$ | $\approx 32 \text{ MB}$ | **Exact Statevector Execution** | **ACTUAL MEASURED** |
| **$2 \times 2$** | 4 | 1,368 | 2,048 | 11 | 1 | **12** | 11.50 | 109,336 | $5.84 \times 10^{-2}$ | $\approx 128 \text{ MB}$ | **Exact Statevector Execution** | **ACTUAL MEASURED** |
| **$4 \times 2$** | 8 | 2,736 | 4,096 | 12 | 1 | **13** | 11.50 | 218,672 | $2.92 \times 10^{-2}$ | $\approx 512 \text{ MB}$ | **Exact Statevector Execution** | **ACTUAL MEASURED** |
| **$8 \times 4$** | 32 | 10,944 | 16,384 | 14 | 1 | **15** | 11.50 | 874,688 | $7.30 \times 10^{-3}$ | $\approx 8 \text{ GB}$ | **Factorized $\mathbf{S}_C \cdot \mathcal{U}_{C2}$ Circuit**| **ACTUAL MEASURED** |
| **$16 \times 8$** | 128 | 43,776 | 65,536 | 16 | 1 | **17** | 11.50 | 3,498,752 | $1.83 \times 10^{-3}$ | $\approx 128 \text{ GB}$ | Factorized / Sparse Oracle | **ANALYTICAL ESTIMATE** |
| **$32 \times 16$**| 512 | 175,104 | 262,144 | 18 | 1 | **19** | 11.50 | 13,995,008 | $4.56 \times 10^{-4}$ | $\approx 2 \text{ TB}$ | Factorized / Sparse Oracle | **ANALYTICAL ESTIMATE** |
| **$64 \times 32$**| 2,048 | 700,416 | 1,048,576 | 20 | 1 | **21** | 11.50 | 55,980,032 | $1.14 \times 10^{-4}$ | $\approx 32 \text{ TB}$ | Factorized / Sparse Oracle | **ANALYTICAL ESTIMATE** |
| **$300 \times 100$**| 30,000 | 10,260,000 | 16,777,216 | 24 | 1 | **25** | 11.50 | $\approx 8.2 \times 10^8$ | $7.79 \times 10^{-6}$ | $\approx 8 \text{ PB}$ | **Factorized Oracle on QPU** | **ANALYTICAL ESTIMATE** |

---

## 2. Distinction between Direct SVD Synthesis and Factorized Quantum Oracles
1. **Direct Halmos Dense SVD**:
   - Practical up to $N=8$ ($D_{pad} = 4096$, $13$ qubits) in RAM.
   - Provides exact machine-precision baseline ($L_\infty < 10^{-14}$) for mathematical validation.
2. **Factorized Reversible Oracle ($\mathbf{S}_C \cdot (\mathbf{I}_N \otimes \mathcal{U}_{C2, node})$)**:
   - Scales to production $N=30,000$ (25 qubits) by synthesizing only a single 10-qubit local collision block $\mathcal{U}_{C2, node}$ and standard spatial permutation adder gates for streaming.
