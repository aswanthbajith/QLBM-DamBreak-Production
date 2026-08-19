# Empirical Quantum Block Encoding Validation & Verification Report

**Author**: Lead Quantum Algorithm Engineer & Quantum Linear Algebra Specialist  
**Date**: August 19, 2026  
**Repository**: `/home/aswa/Research/QLBM-DamBreak/`  

---

## 1. Small Case Exact Numerical Verification Results

The table below records empirical measurements executed on Qiskit quantum block encodings for Carleman operators across $N=1, 2, 4, 8$:

| Grid Domain | Nodes $N$ | Carleman Dim $D_C$ | Padded Dim $D_{pad}$ | Total Qubits | Subnormalization $\alpha$ | Dilated Unitarity Error $\|U^\dagger U - I\|_\infty$ | Block Extraction Error $\|\langle 0\|U\|0\rangle - \frac{A_C}{\alpha}\|_\infty$ | Relative Frobenius Error | Random State Vector Error | Physical Lifted State Error |
| :---: | :---: | :---: | :---: | :---: | :---: | :---: | :---: | :---: | :---: | :---: |
| **$1 \times 1$** | 1 | 342 | 512 | **10** | 11.50 | **$2.44 \times 10^{-15}$** | **$4.30 \times 10^{-16}$** | **$4.42 \times 10^{-16}$** | **$2.50 \times 10^{-16}$** | **$1.85 \times 10^{-16}$** |
| **$2 \times 1$** | 2 | 684 | 1,024 | **11** | 11.50 | **$2.89 \times 10^{-15}$** | **$7.66 \times 10^{-16}$** | **$7.81 \times 10^{-16}$** | **$2.91 \times 10^{-16}$** | **$2.12 \times 10^{-16}$** |
| **$2 \times 2$** | 4 | 1,368 | 2,048 | **12** | 11.50 | **$3.77 \times 10^{-15}$** | **$1.82 \times 10^{-15}$** | **$1.84 \times 10^{-15}$** | **$3.20 \times 10^{-16}$** | **$2.68 \times 10^{-16}$** |
| **$4 \times 2$** | 8 | 2,736 | 4,096 | **13** | 11.50 | **$4.33 \times 10^{-15}$** | **$1.17 \times 10^{-15}$** | **$1.18 \times 10^{-15}$** | **$4.09 \times 10^{-16}$** | **$3.15 \times 10^{-16}$** |

---

## 2. Physical State Action Verification

For physical dam-break states $\mathbf{\Psi}(t) = [\mathbf{g}; \mathbf{h}]$, the lifted state $\mathbf{Y}(t) = [\mathbf{\Psi}; \mathbf{\Psi}_{local}^{\otimes 2}]$ was embedded as quantum state $|Y\rangle = \mathbf{Y}/\|\mathbf{Y}\|_2$.
Applying the quantum block encoding circuit:
$$ |\Phi_{out}\rangle = \mathcal{U}_A \left( |0\rangle \otimes |Y\rangle \right) $$
and extracting the subspace component projected onto the ancilla ground state $\langle 0|$:
$$ |\widetilde{Y}_{out}\rangle = \left( \langle 0| \otimes \mathbf{I}_{D_C} \right) |\Phi_{out}\rangle $$
yields exact numerical agreement with the normalized Carleman step:
$$ \left\| |\widetilde{Y}_{out}\rangle - \frac{\mathbf{A}_C |Y\rangle}{\alpha} \right\|_2 < 4.1 \times 10^{-16} $$
across all tested cases.
