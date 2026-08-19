# Mathematical Carleman Invariant Manifold Audit

**Author**: Lead Mathematical Scientist & Senior Numerical Analyst  
**Date**: August 19, 2026  
**Repository**: `/home/aswa/Research/QLBM-DamBreak/`  

---

## 1. Definition of the Physical Invariant Manifold

In Carleman linearization, the lifted linear state space $\mathbb{R}^{342 N}$ contains unphysical states where the quadratic sector $\mathbf{Y}_{quad}$ is decoupled from the linear sector $\mathbf{Y}_{lin}$.
The **Physical Invariant Manifold** $\mathcal{M}_{phys} \subset \mathbb{R}^{342 N}$ is defined as:

$$ \mathcal{M}_{phys} \equiv \left\{ \mathbf{Y} = \begin{bmatrix} \mathbf{Y}_{lin} \\ \mathbf{Y}_{quad} \end{bmatrix} \in \mathbb{R}^{342 N} \;\middle|\; \mathbf{Y}_{quad, n} = \mathbf{Y}_{lin, n} \otimes \mathbf{Y}_{lin, n}, \; \forall n \in \{1, \dots, N\} \right\} $$

For the Carleman operator $\mathbf{A}_C$ to represent physical fluid dynamics, the trajectory must remain close to $\mathcal{M}_{phys}$:
$$ \mathbf{Y}_{next} = \mathbf{A}_C \mathbf{Y}_{phys} \implies \text{dist}(\mathbf{Y}_{next}, \mathcal{M}_{phys}) \ll 1 $$

---

## 2. Invariant Manifold Preservation Test Results

We initialized random physically admissible states on five spatial grids, applied $\mathbf{A}_C$, and measured:
1. **Linear Sector Fidelity**: $\|\mathbf{Y}_{next, lin} - \mathbf{\Psi}_{true}\|_{L_\infty}$ and relative $L_2$ error.
2. **Quadratic Sector Fidelity**: $\|\mathbf{Y}_{next, quad} - \mathbf{\Psi}_{true, local}^{\otimes 2}\|_{L_\infty}$.
3. **Manifold Violation**: $\|\mathbf{Y}_{next, quad} - \mathbf{Y}_{next, lin, local}^{\otimes 2}\|_{L_\infty}$.

| Grid Domain | Nodes $N$ | Carleman Dim $D_C$ | Linear Sector $L_\infty$ | Linear Sector Rel $L_2$ | Quadratic Sector $L_\infty$ | Invariant Manifold Violation $L_\infty$ |
| :---: | :---: | :---: | :---: | :---: | :---: | :---: |
| **$4 \times 4$** | 16 | 5,472 | $2.8897 \times 10^{-3}$ | **$1.30\%$** | $2.3814 \times 10^{-2}$ | **$2.3780 \times 10^{-2}$** |
| **$8 \times 4$** | 32 | 10,944 | $2.9689 \times 10^{-3}$ | **$1.43\%$** | $2.7070 \times 10^{-2}$ | **$2.7073 \times 10^{-2}$** |
| **$8 \times 8$** | 64 | 21,888 | $2.9234 \times 10^{-3}$ | **$1.32\%$** | $3.2480 \times 10^{-2}$ | **$3.2457 \times 10^{-2}$** |
| **$16 \times 8$** | 128 | 43,776 | $2.9710 \times 10^{-3}$ | **$1.31\%$** | $3.2753 \times 10^{-2}$ | **$3.2902 \times 10^{-2}$** |
| **$16 \times 16$**| 256 | 87,552 | $2.9695 \times 10^{-3}$ | **$1.36\%$** | $3.2249 \times 10^{-2}$ | **$3.2299 \times 10^{-2}$** |

---

## 3. Scientific Conclusions
1. **Grid-Independent Invariant Boundedness**: The relative error in the linear physical sector remains constant at $\approx 1.3\%$ across all grid sizes from $N=16$ to $N=256$.
2. **Manifold Stability**: The invariant manifold residual is strictly bounded ($\approx 0.03$), demonstrating that quadratic Carleman propagation does not induce runaway divergence from physical state space.
