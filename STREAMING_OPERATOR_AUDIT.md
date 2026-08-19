# Mathematical & Algorithmic Audit of the LBM Streaming Operator

**Author**: Lead Mathematical Scientist & Senior Numerical Analyst  
**Date**: August 19, 2026  
**Repository**: `/home/aswa/Research/QLBM-DamBreak/`  

---

## 1. Mathematical Structure of the Streaming Matrix $\mathbf{S}$

The global spatial streaming operator $\mathbf{S} \in \{0, 1\}^{18N \times 18N}$ maps the post-collision state vector $\mathbf{\Psi}^{post}$ to the streamed state at time $t+1$:
$$ \mathbf{\Psi}(t+1) = \mathbf{S} \mathbf{\Psi}^{post}(t) $$

### Block Structure:
$$ \mathbf{S} = \begin{bmatrix} \mathbf{S}_g & \mathbf{0} \\ \mathbf{0} & \mathbf{S}_h \end{bmatrix} $$
where:
- $\mathbf{S}_g \in \{0, 1\}^{9N \times 9N}$: Streaming operator for 9 hydrodynamic distribution functions.
- $\mathbf{S}_h \in \{0, 1\}^{9N \times 9N}$: Streaming operator for 9 phase-field distribution functions.

---

## 2. Boundary Condition Permutation Mapping

1. **Interior Nodes**: For any node $(x, y)$ such that $(x + c_x, y + c_y)$ is inside the domain:
   $$ \text{Destination}: (x + c_x, y + c_y), \quad \text{Direction}: q $$
2. **Top, Left, Right Solid Walls (No-Slip Bounce-Back)**:
   $$ \text{Destination}: (x, y), \quad \text{Direction}: \text{opp}[q] = [0, 3, 4, 1, 2, 7, 8, 5, 6][q] $$
3. **Bottom Floor (Free-Slip Specular Reflection)**:
   $$ \text{Destination}: (x, 0), \quad \text{Direction}: \text{refl\_floor}[q] = [0, 1, 4, 3, 2, 8, 7, 6, 5][q] $$

Because both bounce-back and specular reflection are involutive bijections on the discrete velocity set $\mathcal{Q} = \{0, \dots, 8\}$, every population leaving a boundary node is mapped to exactly one reflected population.

---

## 3. Unitarity & Machine-Precision Verification

| Grid Domain | Nodes $N$ | Matrix Dimension | Non-Zero Count (NNZ) | Row Sums | Col Sums | $\|\mathbf{S}^T \mathbf{S} - \mathbf{I}\|_\infty$ | Status |
| :---: | :---: | :---: | :---: | :---: | :---: | :---: | :---: |
| **$4 \times 4$** | 16 | $288 \times 288$ | 288 | Exactly 1.0 | Exactly 1.0 | **$0.0000 \times 10^0$** | **STRICTLY UNITARY** |
| **$8 \times 4$** | 32 | $576 \times 576$ | 576 | Exactly 1.0 | Exactly 1.0 | **$0.0000 \times 10^0$** | **STRICTLY UNITARY** |
| **$16 \times 8$** | 128 | $2,304 \times 2,304$ | 2,304 | Exactly 1.0 | Exactly 1.0 | **$0.0000 \times 10^0$** | **STRICTLY UNITARY** |

### Verified Theorem:
The spatial streaming and boundary reflection matrix $\mathbf{S}$ is a **pure permutation matrix** satisfying:
$$ \mathbf{S}^T \mathbf{S} = \mathbf{S} \mathbf{S}^T = \mathbf{I}_{18N} $$
to exact floating-point machine precision.
