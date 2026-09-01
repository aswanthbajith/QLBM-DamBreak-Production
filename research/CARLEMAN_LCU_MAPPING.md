# MATHEMATICAL ANALYSIS OF CARLEMAN DATA LOADING & LCNU → LCU MAPPING

**Date**: 2026-08-20  
**Author**: Lead Quantum-CFD Implementation Researcher  
**Reference**: Demirdjian et al. (arXiv:2605.00302, May 2026)  

---

## 1. Mathematical Formulation of the Lattice-Boltzmann Carleman System
The discrete-velocity Boltzmann equation with polynomial BGK equilibrium is written as:
$$\partial_t f_i + c_i \cdot \nabla f_i = -\frac{1}{\tau} \left( f_i - f_i^{\text{eq}}(f) \right)$$
where $f_i^{\text{eq}}(f)$ is a quadratic polynomial in the distribution functions $f = (f_0, \dots, f_{Q-1})^T$:
$$f_i^{\text{eq}} = w_i \rho \left[ 1 + \frac{c_i \cdot u}{c_s^2} + \frac{(c_i \cdot u)^2}{2 c_s^4} - \frac{u \cdot u}{2 c_s^2} \right] = \sum_j L_{ij} f_j + \sum_{j,k} Q_{ijk} f_j f_k$$

Carleman linearization lifts the state vector to include higher Kronecker tensor powers:
$$y = \begin{bmatrix} f \\ f^{\otimes 2} \\ \vdots \\ f^{\otimes p} \end{bmatrix} \implies \frac{d y}{d t} = A_C y$$
For quadratic truncation $p=2$, the Carleman matrix $A_C$ has block upper-triangular structure:
$$A_C = \begin{bmatrix} A_{11} & A_{12} \\ 0 & A_{22} \end{bmatrix}$$
where $A_{11} = -S + M_1$, $A_{12} = M_2$, and $A_{22} = A_{11} \otimes I + I \otimes A_{11}$.

---

## 2. Linear Combination of Non-Unitaries (LCNU) to LCU Decomposition
Demirdjian et al. formulate the quantum encoding of $A_C$ by decomposing $A_C$ into structured Kronecker tensor products of spatial shift operators $S_x, S_y$ and local velocity matrices $V_k$:
$$A_C = \sum_{m=1}^M \alpha_m (P_m \otimes V_m)$$
where $P_m$ is a spatial permutation operator and $V_m$ is a non-unitary local velocity operator.

### 2.1 The Two-Stage Block Encoding (LCNU $\to$ LCU)
1. **Local Dilation**: Each local matrix $V_m$ is normalized ($\|V_m\|_2 \le 1$) and embedded into a unitary $U_{V_m}$ using a 1-ancilla qubit dilation:
   $$U_{V_m} = \begin{bmatrix} V_m & \sqrt{I - V_m V_m^\dagger} \\ \sqrt{I - V_m^\dagger V_m} & -V_m^\dagger \end{bmatrix}$$
2. **Global SELECT & PREPARE**:
   $$\text{PREPARE} |0\rangle_a = \frac{1}{\sqrt{\sum |\alpha_m|}} \sum_{m} \sqrt{|\alpha_m|} |m\rangle_a$$
   $$\text{SELECT} = \sum_m |m\rangle \langle m|_a \otimes (P_m \otimes U_{V_m})$$
3. **Complexity Scaling**:
   * Spatial gate cost: $\mathcal{O}(\log_2 N)$ using quantum binary adders for spatial shifts $P_m$.
   * Velocity gate cost: $\mathcal{O}(Q^2)$ or $\mathcal{O}(Q^3)$ for velocity tensor products.
   * T-gate scaling: $\mathcal{O}\left( \log(1/\epsilon) \right)$ via optimal Clifford+T synthesis.
