# LEVEL-6B: MATHEMATICAL FORMULATION
## Hybrid K=1 Local-Carleman Two-Phase Quantum Lattice Boltzmann Method

**Document**: Mathematical Specification of the Level-6B Production Solver  
**Repository**: `/home/aswa/Research/QLBM-DamBreak-Production`  
**Date**: September 2026  

---

## 1. Classical D2Q9 Physical Reference (Level 4)

Let $\mathbf{x} = (x, y) \in \Omega$ be a node on a two-dimensional lattice. The state is governed by two sets of 9 discrete velocity distribution functions:
- $\mathbf{f}(\mathbf{x}, t) = [f_0, \dots, f_8]^T \in \mathbb{R}^9$: Hydrodynamic momentum distributions.
- $\mathbf{g}(\mathbf{x}, t) = [g_0, \dots, g_8]^T \in \mathbb{R}^9$: Conservative phase-field distributions.

### Macroscopic Quantities:
$$\rho(\mathbf{x}, t) = \sum_{i=0}^8 f_i(\mathbf{x}, t), \quad \alpha(\mathbf{x}, t) = \text{clip}\left(\sum_{i=0}^8 g_i(\mathbf{x}, t), 0, 1\right)$$
$$\mathbf{u}(\mathbf{x}, t) = \frac{1}{\rho(\mathbf{x}, t)} \left( \sum_{i=0}^8 \mathbf{c}_i f_i(\mathbf{x}, t) + \frac{1}{2} \mathbf{F}(\mathbf{x}, t) \right)$$
where $\mathbf{F} = \mathbf{F}_g + \mathbf{F}_s$ combines gravitational buoyancy $\mathbf{F}_g = (\rho - \rho_G)\mathbf{g}_{\text{acc}}$ and Brackbill Continuum Surface Force $\mathbf{F}_s = \sigma \kappa \nabla \alpha$.

---

## 2. Local State Vector & Quadratic Kronecker Lifting

At each node $\mathbf{x}$, the coupled physical state vector is:
$$\mathbf{z}(\mathbf{x}, t) = \begin{bmatrix} \mathbf{f}(\mathbf{x}, t) \\ \mathbf{g}(\mathbf{x}, t) \end{bmatrix} \in \mathbb{R}^{18}$$

The local state is lifted to second-order Carleman space:
$$\mathbf{Y}(\mathbf{x}, t) = \begin{bmatrix} \mathbf{z}(\mathbf{x}, t) \\ \mathbf{z}(\mathbf{x}, t) \otimes \mathbf{z}(\mathbf{x}, t) \end{bmatrix} \in \mathbb{R}^{18 + 324 = 342}$$

---

## 3. Quantum Carleman Collision Block

The local nonlinear BGK collision is represented through the second-order Carleman operator:
$$\mathbf{z}^*(\mathbf{x}, t) = M_1 \mathbf{z}(\mathbf{x}, t) + M_2 (\mathbf{z}(\mathbf{x}, t) \otimes \mathbf{z}(\mathbf{x}, t)) + S_{\text{forcing}}(\mathbf{F}_s)$$

where $M_1 \in \mathbb{R}^{18 \times 18}$, $M_2 \in \mathbb{R}^{18 \times 324}$, and $A_{\text{eval}} = [M_1, M_2] \in \mathbb{R}^{18 \times 342}$.

### Unitary Block-Encoding:
$A_{\text{eval}}$ is block-encoded into a 10-qubit Sz.-Nagy unitary dilation $U_C \in \mathbb{U}(1024)$:
$$\langle 0_{\text{anc}}| U_C |0_{\text{anc}}\rangle = \frac{C_{2,\text{padded}}}{\alpha_C}, \quad \alpha_C \approx 7.9004$$
Projection onto $|0_{\text{anc}}\rangle$ yields:
$$\mathbf{z}^*(\mathbf{x}, t) = P (\alpha_C U_C) P^T \mathbf{Y}(\mathbf{x}, t)$$

---

## 4. Exact Spatial Transport & Hybrid Boundary Update

1. **Reversible Spatial Streaming**:
   Streaming is applied strictly to linear populations:
   $$f_i^*(\mathbf{x} + \mathbf{c}_i, t+1) = f_i^*(\mathbf{x}, t), \quad g_i^*(\mathbf{x} + \mathbf{c}_i, t+1) = g_i^*(\mathbf{x}, t)$$
2. **Direction-Selective Bounce-Back**:
   On solid boundary nodes $\mathbf{x}_{\text{wall}}$:
   $$f_{\text{opp}(i)}(\mathbf{x}_{\text{wall}}, t+1) = f_i^*(\mathbf{x}_{\text{wall}}, t)$$
3. **Local Re-Lifting**:
   At timestep $t+1$, the next quadratic tensor is assembled locally:
   $$\mathbf{Y}(\mathbf{x}, t+1) = \begin{bmatrix} \mathbf{z}(\mathbf{x}, t+1) \\ \mathbf{z}(\mathbf{x}, t+1) \otimes \mathbf{z}(\mathbf{x}, t+1) \end{bmatrix}$$
