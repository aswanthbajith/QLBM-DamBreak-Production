# LEVEL-6B: QUANTUM-CLASSICAL INTERFACE SPECIFICATION

**Document**: Boundary Definition and Data Exchange between Quantum and Classical Layers  
**Repository**: `/home/aswa/Research/QLBM-DamBreak-Production`  
**Date**: September 2026  

---

## 1. Domain Separation

| Layer | Responsibility | Computational Complexity | Precision / Format |
| :--- | :--- | :---: | :---: |
| **Quantum Layer** | Local Carleman collision execution via 10-qubit Sz.-Nagy unitary dilation $U_C \in \mathbb{U}(1024)$ | $\mathcal{O}(\text{poly}(\log N))$ depth per node | Quantum state amplitudes in $\mathcal{H}_{1024}$ |
| **Classical Layer** | Spatial streaming $S$, boundary reflection $B$, macroscopic moments ($\rho, \alpha, \mathbf{u}$), Continuum Surface Force ($\mathbf{F}_s = \sigma\kappa\nabla\alpha$), and local quadratic re-lifting ($\mathbf{z} \otimes \mathbf{z}$) | $\mathcal{O}(N)$ FLOPs per step | Float64 IEEE 754 |

---

## 2. Information Crossing Protocol

1. **Forward Handoff ($C \to Q$)**:
   - Classical linear state $\mathbf{z}(\mathbf{x}) \in \mathbb{R}^{18}$ is locally lifted to $\mathbf{Y}(\mathbf{x}) = [\mathbf{z}(\mathbf{x}); \mathbf{z}(\mathbf{x}) \otimes \mathbf{z}(\mathbf{x})] \in \mathbb{R}^{342}$.
   - Normalized state $|\Psi_{\text{in}}\rangle = \mathbf{Y}/\|\mathbf{Y}\|_2$ is prepared into the 10-qubit register $|v_1\rangle |v_2\rangle |\text{deg}\rangle |\text{anc}\rangle$.

2. **Backward Handoff ($Q \to C$)**:
   - Quantum collision operator $U_C$ is applied.
   - Measurement / projection onto $|\text{anc}=0\rangle$ extracts output amplitudes $\mathbf{z}^*(\mathbf{x}) \in \mathbb{R}^{18}$.
   - Classical layer reconstructs post-collision populations $\mathbf{f}^*(\mathbf{x}), \mathbf{g}^*(\mathbf{x})$ and performs spatial streaming without quantum overhead.
