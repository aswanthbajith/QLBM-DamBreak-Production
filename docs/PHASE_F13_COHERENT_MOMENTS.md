# PHASE F13: COHERENT QUANTUM MOMENTS ARCHITECTURE
## Reversible Quantum Accumulators, Directional Projections, and Fixed-Point Moment Registers

**Document**: Reversible Moment Accumulator & Register Formulation  
**Project**: Quantum Lattice Boltzmann Method (QLBM) for Two-Phase Flow  
**Repository**: `/home/aswa/Research/QLBM-DamBreak-Production`  
**Branch**: `feature/direct-encoding-two-phase-qlbm`  
**Date**: September 2026  

---

## 1. Coherent Moment Registers ($Q4.12$)

In direct population encoding:
$$|\Psi\rangle = \frac{1}{\mathcal{N}} \sum_{x,y} \left( \sum_{i=0}^8 f_i(x,y)|x,y,i,0\rangle + \sum_{i=0}^8 g_i(x,y)|x,y,i,1\rangle \right)$$

The coherent moment generator transforms the state amplitudes into localized fixed-point registers:
$$U_{\text{moments}} |\Psi\rangle |0\rangle_{\rho} |0\rangle_{\alpha} |0\rangle_{jx} |0\rangle_{jy} = |\Psi\rangle |\rho(x,y)\rangle |\alpha(x,y)\rangle |j_x(x,y)\rangle |j_y(x,y)\rangle$$

$$\begin{array}{|l|c|c|c|}
\hline
\textbf{Moment Quantity} & \textbf{Mathematical Definition} & \textbf{Register Type} & \textbf{Bit Precision} \\
\hline
\text{Hydrodynamic Density } \rho(x,y) & \sum_{i=0}^8 f_i(x,y) & Q4.12 & 16 \text{ qubits} \\
\text{Phase-Field Fraction } \alpha(x,y) & \sum_{i=0}^8 g_i(x,y) & Q4.12 & 16 \text{ qubits} \\
\text{Momentum X } j_x(x,y) & \sum_{i=0}^8 f_i(x,y) c_{ix} & Q4.12 & 16 \text{ qubits} \\
\text{Momentum Y } j_y(x,y) & \sum_{i=0}^8 f_i(x,y) c_{iy} & Q4.12 & 16 \text{ qubits} \\
\hline
\end{array}$$

---

## 2. Reversible Arithmetic Accumulator Gate Cost

- **Toffoli Cost per node**: $18 \times (n_{\text{bits}} + n_{\text{bits}}^2) = 4,896$ Toffoli gates.
- **T-gate Estimate per node**: $4 \times 4,896 = 19,584$ T-gates.
- **Ancilla Footprint**: $64$ logical qubits per active accumulator block.
