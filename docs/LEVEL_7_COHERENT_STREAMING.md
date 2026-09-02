# LEVEL-7: COHERENT SPATIAL STREAMING & BOUNDARY INVOLUTIONS

**Document**: Reversible Permutation Circuit Formulation for Spatial Advection  
**Repository**: `/home/aswa/Research/QLBM-DamBreak-Production`  
**Date**: September 2026  

---

## 1. Unitary Permutation Operator on Linear Populations

Let $|x\rangle |y\rangle |a\rangle$ represent the spatial coordinate $(x, y) \in [0, N_x-1] \times [0, N_y-1]$ and discrete velocity population $a \in [0, 17]$ ($9$ hydrodynamic $f_i$ + $9$ phase $g_i$).

The coherent spatial streaming operator $S$ is a unitary permutation:

$$S |x\rangle |y\rangle |a\rangle = |(x + c_{x, a}) \bmod N_x\rangle |(y + c_{y, a}) \bmod N_y\rangle |a\rangle$$

### Circuit Implementation:
- Conditioned on velocity register $|a\rangle$, spatial coordinates $|x\rangle$ and $|y\rangle$ are incremented by discrete shifts $c_{x, a}, c_{y, a} \in \{-1, 0, +1\}$ using Quantum Adder / Shift circuits (controlled $\text{QFT}$ or reversible ripple-carry adders).
- **Circuit Depth**: $\mathcal{O}(\log N_x + \log N_y)$ 2-qubit gates.
- **Unitarity & Norm Conservation**: $\|S^\dagger S - I\| = 0.00 \times 10^0$ (exact permutation matrix).

---

## 2. Coherent Solid Wall Bounce-Back Boundary Operator

On solid boundary perimeter nodes $\mathbf{x}_{\text{wall}}$, the boundary involution operator $B$ applies velocity reflection:

$$B |x_{\text{wall}}\rangle |y_{\text{wall}}\rangle |a\rangle = |x_{\text{wall}}\rangle |y_{\text{wall}}\rangle |\text{opp}(a)\rangle$$

where $\text{opp} = [0, 3, 4, 1, 2, 7, 8, 5, 6]$ for both $f$ and $g$ species.
- **Involution Property**: $B^2 = I$.
- **Circuit Depth**: $\mathcal{O}(1)$ single-qubit / CNOT swaps on velocity register $|a\rangle$ controlled by boundary node flags.
