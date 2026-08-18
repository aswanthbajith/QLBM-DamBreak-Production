# Quantum Block Encoding & QSVT Algorithm Design for Carleman QLBM

**Author**: Quantum Algorithm & Scientific Computing Specialist  
**Target Linear System**: $\mathbf{A}_C \mathbf{Y} = \mathbf{B}$ and Grand Linear System $\mathbf{A}_{grand} \mathbf{X} = \mathbf{B}$  
**Framework**: Qiskit 2.5.2 / Quantum Singular Value Transformation (QSVT)  

---

## 1. Mathematical Block Encoding Specification

An $(\alpha, a, \epsilon)$-block encoding of a matrix $\mathbf{A} \in \mathbb{C}^{N_s \times N_s}$ (where $N_s = 2^n$) is a unitary operator $\mathcal{U}_A \in \mathcal{U}(2^{a + n})$ acting on $a$ ancilla qubits and $n$ system qubits such that:
$$
\langle 0^a | \mathcal{U}_A | 0^a \rangle = \frac{\mathbf{A}}{\alpha} + \mathcal{E}, \quad \|\mathcal{E}\|_\infty \le \epsilon
$$
Equivalently, the matrix representation of $\mathcal{U}_A$ is partitioned as:
$$
\mathcal{U}_A = \begin{bmatrix}
\mathbf{A} / \alpha & \sqrt{\mathbf{I} - (\mathbf{A}/\alpha)(\mathbf{A}/\alpha)^\dagger} \\
\sqrt{\mathbf{I} - (\mathbf{A}/\alpha)^\dagger(\mathbf{A}/\alpha)} & -\mathbf{A}^\dagger / \alpha
\end{bmatrix}
$$

### Parameter Definitions
- **System Qubits**: $n = \lceil \log_2(\dim(\mathbf{A})) \rceil$
- **Ancilla Qubits**: $a \ge 1$ (for exact single-ancilla dilation, $a = 1$)
- **Subnormalization Factor $\alpha$**:
  $$ \alpha \ge \|\mathbf{A}\|_2 = \sigma_{\max}(\mathbf{A}) $$
  Ensures that $\|\mathbf{A}/\alpha\|_2 \le 1.0$, guaranteeing that the singular values of the dilated matrix lie strictly within $[0, 1]$.
- **Sparsity**: $s = \max_i \|\mathbf{A}_{i, :}\|_0$ (bounded by lattice stencil connectivity).

---

## 2. Theoretical Oracle vs. Implemented Circuit Architecture

| Architecture Level | State Preparation | Matrix Oracle | Dilation Method | Ancilla Overhead | Gate Complexity |
| :--- | :--- | :--- | :--- | :---: | :---: |
| **Theoretical Sparse Oracle** (Gilyén 2019, Childs 2017) | $O_p |0\rangle |j\rangle = \sum \sqrt{\frac{A_{jk}}{s\alpha}} |k\rangle |j\rangle$ | $O_F |j\rangle |l\rangle = |j\rangle |col(j, l)\rangle$ | Linear Combination of Unitaries (LCU) | $a = 2 \lceil \log_2 s \rceil + 2$ | $\mathcal{O}(s \cdot \text{poly}(n))$ |
| **Implemented Exact Dilation Circuit** (Present) | Direct statevector / amplitude encoding | Exact SVD/Cosine-Sine decomposition $\mathbf{U} \mathcal{R}_{\mathbf{\Sigma}} \mathbf{V}^\dagger$ | Canonical unitary embedding | $a = 1$ | Exact unitary gate synthesis |

---

## 3. Quantum Singular Value Transformation (QSVT) Linear Solver

### A. Polynomial Inversion Target
To solve $\mathbf{A} \mathbf{x} = \mathbf{b}$, we construct an odd polynomial $P_{2k+1}(x)$ approximating the inverse function $f(x) = \frac{1}{\kappa x}$ over $x \in [-1, -1/\kappa] \cup [1/\kappa, 1]$.
Using the Remez / Chebyshev polynomial expansion:
$$
P_{2k+1}(x) = 4 \left( \sum_{j=0}^k (-1)^j \frac{T_{2j+1}(x)}{2j + 1} \right) \cdot \frac{1}{\gamma}
$$
where:
- $\kappa = \sigma_{\max} / \sigma_{\min}$ is the effective condition number.
- Degree $d_{poly} = 2k + 1 \sim \mathcal{O}(\kappa \log(1/\epsilon))$.
- Success probability: $P_{succ} = \gamma^2 \approx \frac{1}{\kappa^2}$.

### B. QSVT Circuit Sequence
Given the block encoding $\mathcal{U}_A$ and phase angles $\vec{\Phi} = (\phi_0, \phi_1, \dots, \phi_d)$:
$$
\mathcal{U}_{QSVT}(\vec{\Phi}) = e^{i \phi_0 \Pi_0} \left( \prod_{j=1}^{(d-1)/2} \mathcal{U}_A^\dagger e^{i \phi_{2j-1} \Pi_0} \mathcal{U}_A e^{i \phi_{2j} \Pi_0} \right) \mathcal{U}_A^\dagger e^{i \phi_d \Pi_0}
$$
where $\Pi_0 = (2 |0^a\rangle\langle 0^a| - \mathbf{I}) \otimes \mathbf{I}_{sys}$ is the projector phase shift on the ancilla register.

### C. Solution State Extraction
Applying $\mathcal{U}_{QSVT}$ to $|0^a\rangle |b\rangle$ produces:
$$
\mathcal{U}_{QSVT} |0^a\rangle |b\rangle = |0^a\rangle \otimes \left( \gamma \frac{\mathbf{A}^{-1} |b\rangle}{\alpha} \right) + |\perp\rangle
$$
Measuring the ancilla in $|0^a\rangle$ projects the system register onto the exact normalized solution $|x\rangle = \frac{\mathbf{A}^{-1} |b\rangle}{\|\mathbf{A}^{-1} |b\rangle\|}$.
