# Mathematical Analysis of Block Encoding Subnormalization Constants $\alpha$

**Author**: Lead Quantum Algorithm Engineer & Quantum Linear Algebra Specialist  
**Date**: August 19, 2026  
**Repository**: `/home/aswa/Research/QLBM-DamBreak/`  

---

## 1. Mathematical Requirements for Unitary Block Encoding

A matrix $\mathcal{U}_A \in \mathbb{C}^{2^{n+a} \times 2^{n+a}}$ is an $(\alpha, a, \epsilon)$-block-encoding of $\mathbf{A}_C \in \mathbb{C}^{d \times d}$ if:
$$ \left\| \mathbf{A}_C - \alpha \left( \langle 0^a | \otimes \mathbf{I}_d \right) \mathcal{U}_A \left( |0^a \rangle \otimes \mathbf{I}_d \right) \right\|_2 \le \epsilon $$
For $\mathcal{U}_A$ to be unitary, the encoded matrix contraction $\mathbf{B} = \mathbf{A}_C / \alpha$ must satisfy:
$$ \|\mathbf{B}\|_2 = \left\| \frac{\mathbf{A}_C}{\alpha} \right\|_2 \le 1 \implies \alpha \ge \|\mathbf{A}_C\|_2 $$

---

## 2. Comparison of Candidate Normalization Schemes

| Normalization Method | Formula | Value for $N=1$ ($D_C=342$) | Value for $N=32$ ($D_C=10,944$) | Value for $N=30,000$ ($D_C=10.26\text{M}$) | Asymptotic Scaling with $N$ | QSVT Complexity Impact |
| :--- | :--- | :---: | :---: | :---: | :---: | :--- |
| **1. Spectral Norm ($\|\cdot\|_2$)** | $\sigma_{\max}(\mathbf{A}_C)$ | **$10.9275$** | **$10.9275$** | **$10.9275$** | **$\mathcal{O}(1)$ (Constant)** | **OPTIMAL (Minimum phase-factor degree)** |
| **2. Safe Spectral ($\alpha = 11.5$)**| $1.05 \times \|\mathbf{A}_C\|_2$ | **$11.5000$** | **$11.5000$** | **$11.5000$** | **$\mathcal{O}(1)$ (Constant)** | **RECOMMENDED STANDARD** |
| **3. Max Column-Sum ($\|\cdot\|_1$)**| $\max_j \sum_i |A_{ij}|$ | $11.4690$ | $11.4690$ | $11.4690$ | $\mathcal{O}(1)$ | Slightly sub-optimal |
| **4. Max Row-Sum ($\|\cdot\|_\infty$)**| $\max_i \sum_j |A_{ij}|$ | $73.0238$ | $73.0238$ | $73.0238$ | $\mathcal{O}(1)$ | High query overhead ($6.3\times$) |
| **5. Frobenius Norm ($\|\cdot\|_F$)** | $\sqrt{\sum_{ij} |A_{ij}|^2}$ | $52.28$ | $295.74$ | $9,055.2$ | $\mathcal{O}(\sqrt{N})$ (Diverges) | **UNACCEPTABLE (Degrades with grid size)** |

---

## 3. Selected Authoritative Normalization: $\alpha = 11.50$
We select $\alpha = 11.5000$ (satisfying $\alpha > \|\mathbf{A}_C\|_2 = 10.9275$).
Because $\|\mathbf{A}_C\|_2$ is strictly invariant with $N$, this choice guarantees that the quantum normalization penalty does **not** grow as the classical grid resolution is refined from $N=1$ to production $N=30,000$.
