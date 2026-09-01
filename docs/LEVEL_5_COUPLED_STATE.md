# LEVEL-5: COUPLED TWO-PHASE STATE VECTOR REPRESENTATION

This document defines the mathematical representations, dimensions, and register mappings of the coupled two-phase fluid state.

---

## 1. Classical Vector Representation ($\mathbf{z}_t$)

Let $N = N_x \times N_y$ be the total number of lattice sites.

$$\mathbf{z}_t = \begin{bmatrix} \mathbf{f}_t \\ \mathbf{g}_t \end{bmatrix} \in \mathbb{R}^{18 N}$$

where:
$$\mathbf{f}_t = \left[ f_0(\mathbf{x}_1), \dots, f_8(\mathbf{x}_1), f_0(\mathbf{x}_2), \dots, f_8(\mathbf{x}_N) \right]^T \in \mathbb{R}^{9 N}$$
$$\mathbf{g}_t = \left[ g_0(\mathbf{x}_1), \dots, g_8(\mathbf{x}_1), g_0(\mathbf{x}_2), \dots, g_8(\mathbf{x}_N) \right]^T \in \mathbb{R}^{9 N}$$

---

## 2. Carleman State Space Dimensions

### A. Global Naive Tensor Product vs. Local Kronecker Decoupling

1. **Global Monolithic Carleman Lifting**:
   $$\mathbf{Y}_{\text{global}} = \begin{bmatrix} \mathbf{z}_t \\ \mathbf{z}_t \otimes \mathbf{z}_t \end{bmatrix} \in \mathbb{R}^{18 N + 324 N^2}$$
   *Scaling Issue*: For $N = 64$ ($8\times 8$), $\dim \mathbf{Y}_{\text{global}} = 1,152 + 1,327,104 = 1,328,256$ dimensions (computationally intractable).

2. **Local Kronecker Decoupled Carleman Lifting**:
   Because the Lattice Boltzmann collision operator acts **locally node-by-node**, the Carleman lift can be constructed on the local $18$-dimensional state at each lattice node:
   $$\mathbf{z}_{\text{node}}(\mathbf{x}) = \begin{bmatrix} \mathbf{f}(\mathbf{x}) \\ \mathbf{g}(\mathbf{x}) \end{bmatrix} \in \mathbb{R}^{18}$$
   $$\mathbf{Y}_{\text{local}}(\mathbf{x}) = \begin{bmatrix} \mathbf{z}_{\text{node}}(\mathbf{x}) \\ \mathbf{z}_{\text{node}}(\mathbf{x}) \otimes \mathbf{z}_{\text{node}}(\mathbf{x}) \end{bmatrix} \in \mathbb{R}^{18 + 324 = 342}$$
   *Decoupled Global Dimension*: $\dim \mathbf{Y}_{\text{decoupled}} = 342 N$.
   For $N = 64$ ($8\times 8$), $\dim \mathbf{Y}_{\text{decoupled}} = 342 \times 64 = 21,888$ dimensions (fully tractable and scalable).

---

## 3. Quantum Hilbert Space & Register Allocation

| Lattice Grid | Physical Nodes ($N$) | Physical State ($18 N$) | Local Lifted ($342 N$) | System Qubits ($n_{\text{sys}}$) | Hilbert Space ($\dim \mathcal{H}$) | Total Qubits with Ancilla | Dilated Dimension ($2^{n+1}$) |
| :---: | :---: | :---: | :---: | :---: | :---: | :---: | :---: |
| **$4 \times 4$** | 16 | 288 | 5,472 | 9 | 512 | 10 | 1,024 |
| **$8 \times 8$** | 64 | 1,152 | 21,888 | 11 | 2,048 | 12 | 4,096 |
| **$16 \times 16$** | 256 | 4,608 | 87,552 | 13 | 8,192 | 14 | 16,384 |
| **$32 \times 32$** | 1,024 | 18,432 | 350,208 | 15 | 32,768 | 16 | 65,536 |
| **$64 \times 64$** | 4,096 | 73,728 | 1,400,832 | 17 | 131,072 | 18 | 262,144 |

### Quantum State Mapping:
$$|\Psi(t)\rangle = \sum_{x=0}^{N_x-1} \sum_{y=0}^{N_y-1} \sum_{i=0}^8 \left[ \sqrt{\frac{f_i(x,y,t)}{M}} |x, y, i, s=0\rangle + \sqrt{\frac{g_i(x,y,t)}{M}} |x, y, i, s=1\rangle \right] \in \mathcal{H}_{2^{n_{\text{sys}}}}$$
where $M = \sum_{x,y,i} [f_i(x,y,t) + g_i(x,y,t)]$ is the global mass normalization scalar.
