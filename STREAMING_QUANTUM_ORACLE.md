# Mathematical Design of the Quantum Spatial Streaming Oracle

**Author**: Lead Quantum Algorithm Engineer & Quantum Linear Algebra Specialist  
**Date**: August 19, 2026  
**Repository**: `/home/aswa/Research/QLBM-DamBreak/`  

---

## 1. Reversible Permutation Representation

Because the spatial streaming operator $\mathbf{S}_C \in \{0, 1\}^{342N \times 342N}$ is a pure classical permutation ($\mathbf{S}_C^T \mathbf{S}_C = \mathbf{I}$), it maps basis states reversibly:
$$ \mathcal{U}_{\text{stream}} |k\rangle |q\rangle |x\rangle |y\rangle = |k\rangle |q'\rangle |x'\rangle |y'\rangle $$

where:
- $|k\rangle$: Monomial sector register ($k=0$ for linear populations $\mathbf{\psi}_n \in \mathbb{R}^{18}$, $k=1$ for quadratic pairs $(q_1, q_2) \in \mathbb{R}^{324}$).
- $|q\rangle$: Lattice velocity register ($q \in \{0, \dots, 8\}$ for hydro or phase distributions).
- $|x\rangle, |y\rangle$: Spatial node coordinate registers ($x \in \{0, \dots, N_x-1\}, y \in \{0, \dots, N_y-1\}$).

---

## 2. Gate Decomposition for Scalable Hardware Implementation
1. **Spatial Shift**: Controlled Draper quantum adders or quantum Fourier transform (QFT) modular addition:
   $$ |x\rangle \to |(x + c_x) \bmod N_x\rangle, \quad |y\rangle \to |(y + c_y) \bmod N_y\rangle $$
2. **Boundary Reflection Involutions**:
   - For lateral solid walls ($x=0, x=N_x-1$): Multi-controlled CNOT / SWAP gates executing $\text{opp}[q]$.
   - For specular floor ($y=0$): Controlled reflection executing $\text{refl\_floor}[q]$.

### Key Architectural Advantage:
The streaming oracle requires **zero dilation ancilla qubits** ($a=0$) and has **strictly unit norm** ($\|\mathcal{U}_{\text{stream}}\|_2 = 1.0$).
