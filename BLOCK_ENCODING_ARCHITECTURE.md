# Master Quantum Block Encoding Architectural Design

**Author**: Lead Quantum Algorithm Engineer & Quantum Linear Algebra Specialist  
**Date**: August 19, 2026  
**Repository**: `/home/aswa/Research/QLBM-DamBreak/`  

---

## 1. Comparative Architecture Evaluation

| Architecture Option | Ancilla Overhead | Circuit Depth | Normalization $\alpha$ | Scalability | Verification Simplicity | Recommended Use |
| :--- | :---: | :---: | :---: | :---: | :---: | :--- |
| **Option A: Canonical Halmos CS-Dilation** | **$a=1$ qubit** | $\mathcal{O}(1)$ unitary gate | **$\alpha = 11.5$ (Optimal)** | Exact for $N \le 32$ | **Machine precision ($10^{-15}$)** | **PRIMARY VERIFICATION ORACLE** |
| **Option B: Factorized $\mathbf{S}_C \cdot \mathcal{U}_{C2}$** | $a=1$ qubit | Reversible Permutation $+ \mathcal{U}_{C2}$ | $\alpha = 11.5$ | High (Scalable) | Clean separation of streaming/collision | **SCALABLE HARDWARE TARGET** |
| **Option C: Node-Local Block Encodings** | $\mathcal{O}(\log N)$ | Parallel local unitaries | $\alpha = 11.5$ | Highest | High modularity | Future distributed QPU clusters |
| **Option D: Sparse-Access Oracles ($O_A, O_F$)** | $a \approx 2n$ | $\mathcal{O}(\text{poly}(n))$ | $\alpha = d_{max} \|A\|_{\max}$ | High | Indirect (Sampling-based) | Fault-tolerant asymptotics |
| **Option E: Linear Combination of Unitaries (LCU)** | $a = \lceil\log_2 L\rceil$ | $\mathcal{O}(L)$ gates | $\alpha = \sum |c_k|$ | Moderate | Combinatorial overhead | Sub-optimal for large $L$ |

---

## 2. Mathematical Foundation of Canonical Halmos CS-Dilation

Given matrix $\mathbf{B} = \mathbf{A}_{pad} / \alpha \in \mathbb{C}^{d \times d}$ with $\|\mathbf{B}\|_2 \le 1$:
The singular value decomposition is:
$$ \mathbf{B} = \mathbf{U} \boldsymbol{\Sigma} \mathbf{V}^\dagger, \quad \boldsymbol{\Sigma} = \text{diag}(\sigma_1, \dots, \sigma_d), \quad \sigma_k \in [0, 1] $$
The complementary cosine singular value matrix is:
$$ \mathbf{C} = \text{diag}(c_1, \dots, c_d), \quad c_k = \sqrt{1 - \sigma_k^2} $$
The canonical 1-ancilla unitary dilation $\mathcal{U}_A \in \mathbb{C}^{2d \times 2d}$ is constructed as:
$$ \mathcal{U}_A = \begin{bmatrix} \mathbf{U} & \mathbf{0} \\ \mathbf{0} & \mathbf{I}_d \end{bmatrix} \begin{bmatrix} \boldsymbol{\Sigma} & \mathbf{C} \\ \mathbf{C} & -\boldsymbol{\Sigma} \end{bmatrix} \begin{bmatrix} \mathbf{V}^\dagger & \mathbf{0} \\ \mathbf{0} & \mathbf{I}_d \end{bmatrix} $$

### Unitarity Proof:
$$ \mathcal{U}_A^\dagger \mathcal{U}_A = \begin{bmatrix} \mathbf{V} & \mathbf{0} \\ \mathbf{0} & \mathbf{I} \end{bmatrix} \begin{bmatrix} \boldsymbol{\Sigma} & \mathbf{C} \\ \mathbf{C} & -\boldsymbol{\Sigma} \end{bmatrix} \begin{bmatrix} \mathbf{U}^\dagger \mathbf{U} & \mathbf{0} \\ \mathbf{0} & \mathbf{I} \end{bmatrix} \begin{bmatrix} \boldsymbol{\Sigma} & \mathbf{C} \\ \mathbf{C} & -\boldsymbol{\Sigma} \end{bmatrix} \begin{bmatrix} \mathbf{V}^\dagger & \mathbf{0} \\ \mathbf{0} & \mathbf{I} \end{bmatrix} $$
$$ = \begin{bmatrix} \mathbf{V} & \mathbf{0} \\ \mathbf{0} & \mathbf{I} \end{bmatrix} \begin{bmatrix} \boldsymbol{\Sigma}^2 + \mathbf{C}^2 & \boldsymbol{\Sigma}\mathbf{C} - \mathbf{C}\boldsymbol{\Sigma} \\ \mathbf{C}\boldsymbol{\Sigma} - \boldsymbol{\Sigma}\mathbf{C} & \mathbf{C}^2 + \boldsymbol{\Sigma}^2 \end{bmatrix} \begin{bmatrix} \mathbf{V}^\dagger & \mathbf{0} \\ \mathbf{0} & \mathbf{I} \end{bmatrix} = \begin{bmatrix} \mathbf{V} \mathbf{I} \mathbf{V}^\dagger & \mathbf{0} \\ \mathbf{0} & \mathbf{I} \end{bmatrix} = \mathbf{I}_{2d} $$
$\mathcal{U}_A$ is **strictly and unconditionally unitary**.
