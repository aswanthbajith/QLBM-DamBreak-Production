# LEVEL-6A: MATHEMATICAL DERIVATION OF LIFTED LOCAL CARLEMAN DYNAMICS

**Document**: Mathematical Re-derivation and Operator Closure for Level 6A  
**Target Reference**: [`classical/level4_two_phase.py`](file:///home/aswa/Research/QLBM-DamBreak-Production/classical/level4_two_phase.py)  

---

## 1. Local State Vector & Lifted Tensor Space

For a single lattice site $\mathbf{x} = (x, y)$, the coupled two-phase physical state vector $\mathbf{z}(\mathbf{x}, t)$ contains 9 hydrodynamic velocity populations and 9 phase-field populations:

$$\mathbf{z}(\mathbf{x}, t) = \begin{bmatrix} f_0(\mathbf{x}, t) \\ \vdots \\ f_8(\mathbf{x}, t) \\ g_0(\mathbf{x}, t) \\ \vdots \\ g_8(\mathbf{x}, t) \end{bmatrix} \in \mathbb{R}^{18}$$

The **second-order Carleman lifted state vector** is constructed via the Kronecker product:

$$\mathbf{Y}(\mathbf{x}, t) = \begin{bmatrix} \mathbf{z}(\mathbf{x}, t) \\ \mathbf{z}(\mathbf{x}, t) \otimes \mathbf{z}(\mathbf{x}, t) \end{bmatrix} \in \mathbb{R}^{18 + 324 = 342}$$

where the quadratic subspace $\mathbf{z} \otimes \mathbf{z}$ contains all $18 \times 18 = 324$ pairwise population cross-products:
$$\left( \mathbf{z} \otimes \mathbf{z} \right)_{18 a + b} = z_a \cdot z_b, \quad a, b \in \{0, \dots, 17\}$$

---

## 2. Re-Derivation of Linear ($M_1$) and Quadratic ($M_2$) Collision Tensors

### A. Linear Hydrodynamic & Buoyancy Block ($M_1 \in \mathbb{R}^{18 \times 18}$)
For hydrodynamic populations $i \in \{0\dots 8\}$ and input $k \in \{0\dots 8\}$:
$$M_{1, ik}^{(f)} = (1 - \omega_f) \delta_{ik} + \omega_f w_i \left[ 1 + 3(\mathbf{c}_i \cdot \mathbf{c}_k) \right] + \left(1 - \frac{\omega_f}{2}\right) 3 w_i c_{iy} g_{\text{acc}}$$
For phase populations $i \in \{0\dots 8\}$ (mapped to rows $9+i$) and input $k \in \{0\dots 8\}$ (mapped to cols $9+k$):
$$M_{1, (9+i)(9+k)}^{(g)} = (1 - \omega_g) \delta_{ik} + \omega_g w_i$$

### B. Quadratic Convective & Bilinear Phase Tensors ($M_2 \in \mathbb{R}^{18 \times 324}$)
1. **Hydrodynamic Convective Cross-Coupling ($f_j \cdot f_k$)**:
   For row $i \in \{0\dots 8\}$ and column $\text{idx} = j \times 18 + k$ ($j, k \in \{0\dots 8\}$):
   $$M_{2, i, (18 j + k)}^{(f)} = \frac{\omega_f w_i}{\rho_0} \left[ \frac{9}{2} (\mathbf{c}_i \cdot \mathbf{c}_j)(\mathbf{c}_i \cdot \mathbf{c}_k) - \frac{3}{2} (\mathbf{c}_j \cdot \mathbf{c}_k) \right]$$
2. **Phase-Velocity Advection Cross-Coupling ($g_j \cdot f_k$)**:
   For row $9+i$ ($i \in \{0\dots 8\}$) and column $\text{idx} = (9+j) \times 18 + k$ ($j \in \{0\dots 8\}, k \in \{0\dots 8\}$):
   $$M_{2, (9+i), (18(9+j) + k)}^{(g)} = \frac{3 \omega_g w_i}{\rho_0} (\mathbf{c}_i \cdot \mathbf{c}_k)$$

---

## 3. Autonomous Second-Order Carleman Evolution Operator ($C_2$)

Advancing the full 342-dimensional lifted state $\mathbf{Y}_t$:

$$\mathbf{Y}_{t+1}^* = C_2 \mathbf{Y}_t$$

$$C_2 = \begin{bmatrix}
M_1 & M_2 \\
0 & M_1 \otimes M_1
\end{bmatrix} \in \mathbb{R}^{342 \times 342}$$

### Exact Unclosed Truncation Residual:
Let $\mathbf{z}_{t+1}^* = M_1 \mathbf{z}_t + M_2 (\mathbf{z}_t \otimes \mathbf{z}_t)$. The true quadratic tensor at $t+1$ is:
$$\mathbf{z}_{t+1}^* \otimes \mathbf{z}_{t+1}^* = (M_1 \mathbf{z}_t) \otimes (M_1 \mathbf{z}_t) + \underbrace{(M_1 \mathbf{z}_t) \otimes (M_2 \mathbf{z}_t^{\otimes 2}) + (M_2 \mathbf{z}_t^{\otimes 2}) \otimes (M_1 \mathbf{z}_t)}_{\text{Degree 3 Residual: } \mathcal{O}(\text{Ma}^3)} + \underbrace{(M_2 \mathbf{z}_t^{\otimes 2}) \otimes (M_2 \mathbf{z}_t^{\otimes 2})}_{\text{Degree 4 Residual: } \mathcal{O}(\text{Ma}^4)}$$
Because $C_2$ advances the quadratic sector via $(M_1 \otimes M_1) \mathbf{z}_t^{\otimes 2}$, it precisely omits the degree-3 and degree-4 terms. For weakly-compressible low-Mach flows ($\text{Ma} \le 0.05$), the truncation error is bounded by:
$$\| \mathbf{z}_{t+1}^* \otimes \mathbf{z}_{t+1}^* - (M_1 \otimes M_1)\mathbf{z}_t^{\otimes 2} \|_2 \le 2 \|M_1\|_2 \|M_2\|_2 \|\mathbf{z}_t\|_2^3 \sim \mathcal{O}(\text{Ma}^3) \le 2.5 \times 10^{-4}$$
