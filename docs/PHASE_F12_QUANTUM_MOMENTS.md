# PHASE F12: QUANTUM MOMENT EXTRACTION ARCHITECTURE
## Observables, Ancilla-Assisted Probes, and Coherent Amplitude Accumulation

**Document**: Quantum Observable Estimation & Moment Extraction Formulation  
**Project**: Quantum Lattice Boltzmann Method (QLBM) for Two-Phase Flow  
**Repository**: `/home/aswa/Research/QLBM-DamBreak-Production`  
**Branch**: `feature/direct-encoding-two-phase-qlbm`  
**Date**: September 2026  

---

## 1. Direct Amplitude State Encoding & Observable Operators

In the direct population encoding:
$$|\Psi\rangle = \frac{1}{\mathcal{N}} \sum_{x,y} \left( \sum_{i=0}^8 f_i(x,y)|x,y,i,0\rangle + \sum_{i=0}^8 g_i(x,y)|x,y,i,1\rangle \right)$$

Macroscopic moments are extracted via projection and observable operators:

1. **Hydrodynamic Density Operator ($\hat{O}_\rho$)**:
   $$\hat{O}_\rho(x, y) = |x, y\rangle\langle x, y| \otimes \left( \sum_{i=0}^8 |i\rangle\langle i| \right) \otimes |0\rangle\langle 0|$$
   $$\langle\Psi | \hat{O}_\rho(x, y) | \Psi\rangle = \frac{1}{\mathcal{N}^2} \sum_{i=0}^8 f_i(x, y)^2$$
2. **Phase Fraction Operator ($\hat{O}_\alpha$)**:
   $$\hat{O}_\alpha(x, y) = |x, y\rangle\langle x, y| \otimes \left( \sum_{i=0}^8 |i\rangle\langle i| \right) \otimes |1\rangle\langle 1|$$
   $$\langle\Psi | \hat{O}_\alpha(x, y) | \Psi\rangle = \frac{1}{\mathcal{N}^2} \sum_{i=0}^8 g_i(x, y)^2$$
3. **Discrete Velocity Momentum Operators ($\hat{O}_{jx}, \hat{O}_{jy}$)**:
   $$\hat{O}_{jx}(x, y) = |x, y\rangle\langle x, y| \otimes \left( \sum_{i=0}^8 c_{ix} |i\rangle\langle i| \right) \otimes |0\rangle\langle 0|$$
   $$\hat{O}_{jy}(x, y) = |x, y\rangle\langle x, y| \otimes \left( \sum_{i=0}^8 c_{iy} |i\rangle\langle i| \right) \otimes |0\rangle\langle 0|$$

---

## 2. Ancilla-Assisted Moment Probe Circuit

To measure linear sums $\sum_i f_i(x, y)$ without destructive collapse of orthogonal spatial sectors:
1. Spatial coordinate qubits $|x\rangle|y\rangle$ and phase qubit $|p\rangle$ serve as control conditions.
2. A single Hadamard-test ancilla qubit $|a\rangle$ is coupled via multi-controlled target rotations.
3. Measurement of the ancilla yields $\langle Z_a \rangle = \frac{1}{3\mathcal{N}} \sum_i f_i(x, y)$, reconstructing local density with gate depth $O(n_x + n_y + 4)$.
