# LEVEL-6A: QUANTUM REGISTER & RESOURCE DERIVATION

This document provides the mathematical derivation of the exact logical register requirements for the Level-6A Local Carleman Multi-Timestep architecture.

---

## 1. Explicit Derivation of Logical Register Layout

For a lattice of size $N = N_x \times N_y$, the composite quantum state $|\mathbf{Y}\rangle$ is mapped onto 6 distinct quantum registers:

$$|\mathbf{Y}\rangle = \sum_{x=0}^{N_x-1} \sum_{y=0}^{N_y-1} \left( \sum_{a=0}^{17} z_a(x, y) |x, y, a, 0, 0, 0\rangle + \sum_{a=0}^{17} \sum_{b=0}^{17} z_a(x,y) z_b(x,y) |x, y, a, b, 1, 0\rangle \right)$$

### Breakdown of the $+12$ Qubits:

| Register | Name | Dimension | Qubit Count | Justification |
| :--- | :--- | :---: | :---: | :--- |
| $|x\rangle$ | Spatial $X$-Coordinate | $N_x$ | $n_{qx} = \lceil\log_2 N_x\rceil$ | Binary spatial coordinate indexing along the horizontal axis. |
| $|y\rangle$ | Spatial $Y$-Coordinate | $N_y$ | $n_{qy} = \lceil\log_2 N_y\rceil$ | Binary spatial coordinate indexing along the vertical axis. |
| $|v_1\rangle$ | Primary Velocity & Species | 18 | **5 qubits** | $2^4 = 16 < 18 \le 32 = 2^5$. Indexes 9 hydrodynamic ($f_0..f_8$) and 9 phase ($g_0..g_8$) populations. |
| $|v_2\rangle$ | Secondary Velocity & Species | 18 | **5 qubits** | Indexes the secondary factor in the quadratic Kronecker product $(\mathbf{z}\otimes\mathbf{z})_{18a+b}$. |
| $|\text{deg}\rangle$ | Carleman Sector Selector | 2 | **1 qubit** | Selects between linear sector ($|0\rangle \to \mathbf{z} \in \mathbb{R}^{18}$) and quadratic sector ($|1\rangle \to \mathbf{z}\otimes\mathbf{z} \in \mathbb{R}^{324}$). |
| $|\text{anc}\rangle$ | Sz.-Nagy Dilation Ancilla | 2 | **1 qubit** | Ancilla qubit for the 2-block Sz.-Nagy unitary dilation $\mathcal{U}_{\text{Carleman}} \in \mathbb{U}(2 \times 512 = 1024)$. |
| **Total** | **Full System Qubits** | $1024 N$ | **$n = \log_2 N + 12$** | Exact sum: $\lceil\log_2 N_x\rceil + \lceil\log_2 N_y\rceil + 5 + 5 + 1 + 1$. |

---

## 2. Multi-Grid Qubit & Hilbert Space Dimensions

| Mesh Size | Lattice Nodes ($N$) | Spatial Qubits ($\log_2 N$) | Local + Ancilla Qubits | Total Logical Qubits ($n$) | Total Hilbert Space Dimension ($2^n$) |
| :---: | :---: | :---: | :---: | :---: | :---: |
| **$4 \times 4$** | 16 | 4 | 12 | **16 qubits** | 65,536 |
| **$8 \times 8$** | 64 | 6 | 12 | **18 qubits** | 262,144 |
| **$16 \times 16$** | 256 | 8 | 12 | **20 qubits** | 1,048,576 |
| **$32 \times 16$** | 512 | 9 | 12 | **21 qubits** | 2,097,152 |
| **$64 \times 32$** | 2,048 | 11 | 12 | **23 qubits** | 8,388,608 |
| **$128 \times 64$** | 8,192 | 13 | 12 | **25 qubits** | 33,554,432 |
