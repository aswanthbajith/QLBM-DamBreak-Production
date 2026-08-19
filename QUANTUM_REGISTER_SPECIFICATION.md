# Mathematical Quantum Register Sizing & Allocation Specification

**Author**: Lead Quantum Algorithm Engineer & Quantum Linear Algebra Specialist  
**Date**: August 19, 2026  
**Repository**: `/home/aswa/Research/QLBM-DamBreak/`  

---

## 1. Register Partitioning & Qubit Layout

The quantum circuit for the block-encoded operator $\mathcal{U}_A$ is partitioned into two distinct physical registers:

```
Qubit Index               Register Name           Qubit Count            Role
──────────────────────────────────────────────────────────────────────────────────────────────────────────
0 .. (n_sys - 1)          |sys> (System)          n_sys = ceil(log2(D_C)) Encodes Carleman state Y in R^(D_pad)
n_sys                     |anc> (Ancilla)         a = 1                  Dilation ancilla (Block projection |0>)
──────────────────────────────────────────────────────────────────────────────────────────────────────────
TOTAL QUBITS:                                     n_sys + 1
```

---

## 2. Complete Dimension & Register Table

| Spatial Grid | Total Nodes $N$ | Physical Carleman Dim $D_C = 342N$ | Padded Hilbert Dim $D_{pad} = 2^{n_{sys}}$ | System Qubits $n_{sys}$ | Block Ancilla Qubits $a$ | Total Circuit Qubits |
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
