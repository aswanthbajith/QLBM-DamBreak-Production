# FINAL INTEGRATED ARCHITECTURE
## Formal Mathematical and Circuit Architecture for Two-Phase Dam-Break QLBM

---

## 1. Problem Definition
The problem models a liquid column of initial height $H$ and width $L$ collapsing under gravitational acceleration $\mathbf{g} = (0, -g)$ inside an enclosed rectangular solid box $\Omega = [0, N_x] \times [0, N_y]$ filled with air, developing an interfacial surge front and wall impact.

---

## 2. Classical LBM Formulation
The lattice velocity set is D2Q9 with discrete velocities $\mathbf{c}_i$ ($i = 0 \dots 8$) and weights $w_i$.
Two distribution functions are evolved:
1. $f_i(\mathbf{x}, t)$: Hydrodynamic population representing fluid density $\rho = \sum_i f_i$ and momentum $\rho \mathbf{u} = \sum_i \mathbf{c}_i f_i + \frac{1}{2} \mathbf{F}$.
2. $g_i(\mathbf{x}, t)$: Conservative phase field representing order parameter $\alpha = \sum_i g_i$ ($\alpha \approx 1$ liquid, $\alpha \approx 0$ gas).

---

## 3. Two-Phase Coupling & CSF Surface Tension
Interfacial surface tension is modeled via the Continuum Surface Force (CSF):
$$\mathbf{F}_s = \sigma \kappa \nabla \alpha, \quad \kappa = -\nabla \cdot \left( \frac{\nabla \alpha}{|\nabla \alpha|} \right)$$
Total force $\mathbf{F} = \mathbf{F}_g + \mathbf{F}_s$ is incorporated via Guo forcing.

---

## 4. Quantum State Representation
On a discrete $N_x \times N_y$ lattice, the register is allocated as:
$$\mathcal{H}_{\text{total}} = \bigotimes_{x=0}^{N_x-1} \bigotimes_{y=0}^{N_y-1} \mathcal{H}_{\text{node}}(x,y)$$
- In the **NISQ Demonstrator**, each node uses $k=4$ qubits (16 logical qubits for $2\times 2$).
- In the **FTQC Scalable Architecture**, each node uses $560$ qubits ($Q4.16$ arithmetic + 14 environment fields).

---

## 5. Quantum Operators

### A. State Preparation ($U_{\text{prep}}$)
Synthesizes the computational basis state corresponding to the liquid column geometry:
$$|\Psi_0\rangle = U_{\text{prep}} |0\rangle^{\otimes n} = |\mathbf{x}_{\text{col}}\rangle \otimes |\text{liquid}\rangle \otimes |\mathbf{x}_{\text{gas}}\rangle \otimes |\text{gas}\rangle$$

### B. Unitary Timestep Operator ($U_{\text{step}}$)
$$\boxed{U_{\text{step}} = U_{\text{boundary}} \cdot U_{\text{stream}} \cdot U_{\text{collision}} \cdot U_{\text{force}}}$$
- **Nonlinear Collision ($U_{\text{collision}}$)**: Reversible mapping $V$ dilated with environment registers $|0\rangle_E$ to satisfy the F18 non-injectivity constraint.
- **Coordinate Streaming ($U_{\text{stream}}$)**: Exact spatial SWAP network permuting node populations along velocity directions $\mathbf{c}_i$ ($S^\dagger S = I$).
- **Boundary Reflections ($U_{\text{boundary}}$)**: Pauli reflection involutions on solid boundary nodes ($B^2 = I, B^\dagger B = I$).

### C. Multi-Step State Evolution
$$|\Psi_T\rangle = \left( U_{\text{step}} \right)^T |\Psi_0\rangle$$
Evolution between $t = 0$ and $t = T$ is completely unitary and measurement-free.

---

## 6. Terminal Measurement & Observable Readout
Measurement is strictly separated from unitary evolution:
$$\hat{\mathcal{M}} = \text{ProjectiveReadout}(|\Psi_T\rangle)$$
Sampling produces bitstring frequencies $N(b)$, which are decoded classically into:
$$\hat{\rho}(x,y) = \sum_b w_\rho(b) \frac{N(b)}{N_{\text{shots}}}, \quad \hat{\alpha}(x,y) = \sum_b w_\alpha(b) \frac{N(b)}{N_{\text{shots}}}$$
