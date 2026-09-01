# LEVEL-5: GLOBAL TIME-LINEAR SYSTEM & QSVT FORMULATION

This document derives the all-at-once global time-linear system $L \mathbf{Y}_{\text{global}} = \mathbf{b}_{\text{global}}$ for quantum linear system algorithms (QLSA / QSVT).

---

## 1. Global Time-Stepping Linear Formulation

For $N_t$ timesteps governed by the second-order Carleman affine update $\mathbf{Y}_{t+1} = A_C \mathbf{Y}_t + \mathbf{b}_C$, the complete multi-timestep history is assembled into a single block-bidiagonal linear system:

$$\begin{bmatrix}
I & 0 & 0 & \dots & 0 \\
-A_C & I & 0 & \dots & 0 \\
0 & -A_C & I & \dots & 0 \\
\vdots & \ddots & \ddots & \ddots & \vdots \\
0 & \dots & 0 & -A_C & I
\end{bmatrix}
\begin{bmatrix}
\mathbf{Y}_0 \\
\mathbf{Y}_1 \\
\mathbf{Y}_2 \\
\vdots \\
\mathbf{Y}_{N_t}
\end{bmatrix}
=
\begin{bmatrix}
\mathbf{Y}_{\text{init}} \\
\mathbf{b}_C \\
\mathbf{b}_C \\
\vdots \\
\mathbf{b}_C
\end{bmatrix}$$

---

## 2. Matrix Dimensions & Resource Scaling

Let $d_C = 342 N$ be the local decoupled Carleman dimension for an $N$-node lattice.

| Lattice Grid | Nodes ($N$) | Local $d_C$ | $N_t = 1$ Global Dim | $N_t = 5$ Global Dim | $N_t = 10$ Global Dim | Global Sparsity |
| :---: | :---: | :---: | :---: | :---: | :---: | :---: |
| **$4 \times 4$** | 16 | 5,472 | 10,944 | 32,832 | 60,192 | $> 99.9\%$ |
| **$8 \times 8$** | 64 | 21,888 | 43,776 | 131,328 | 240,768 | $> 99.9\%$ |
| **$16 \times 16$** | 256 | 87,552 | 175,104 | 525,312 | 963,072 | $> 99.9\%$ |
| **$32 \times 32$** | 1,024 | 350,208 | 700,416 | 2,101,248 | 3,852,288 | $> 99.9\%$ |

---

## 3. Condition Number & QSVT Inversion Complexity

1. **Spectral Condition Number**:
   Because $L$ is a block lower-bidiagonal matrix with identity on the diagonal and $\|A_C\|_2 \approx 1.0$ for stable fluid dynamics:
   $$\kappa(L) = \|L\|_2 \|L^{-1}\|_2 \le 1 + N_t \|A_C\|_2 \sim \mathcal{O}(N_t)$$
2. **QSVT Inversion Polynomial Degree ($d_{\text{poly}}$)**:
   To approximate $x^{-1}$ to precision $\epsilon$ over the spectrum $[\kappa^{-1}, 1]$:
   $$d_{\text{poly}} = \mathcal{O}\left( \kappa(L) \log\left(\frac{1}{\epsilon}\right) \right) \sim \mathcal{O}\left( N_t \log\left(\frac{1}{\epsilon}\right) \right)$$
3. **Total Quantum Query Complexity**:
   Using block encoding $U_L \in \mathbb{U}(2^n)$, the QSVT statevector preparation requires:
   $$Q = \mathcal{O}\left( \alpha_L \cdot \kappa(L) \cdot \log(1/\epsilon) \right)$$
   quantum oracle queries, providing an optimal logarithmic spatial scaling $\mathcal{O}(\text{poly}(\log N))$ for fixed physical time.
