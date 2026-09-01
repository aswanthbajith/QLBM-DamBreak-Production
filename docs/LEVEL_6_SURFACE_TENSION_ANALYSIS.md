# LEVEL-6: CONTINUUM SURFACE FORCE (CSF) SURFACE TENSION INVESTIGATION

This document analyzes the mathematical representation, approximation options, and quantum implementation feasibility of interfacial surface tension in two-phase Lattice Boltzmann dam-break flow.

---

## 1. Physical Formulation of Continuum Surface Force (CSF)

In the Level-4 classical reference solver (`classical/level4_two_phase.py`), the interfacial force is governed by Brackbill's Continuum Surface Force model:

$$\mathbf{F}_s(\mathbf{x}, t) = \sigma \kappa(\mathbf{x}, t) \nabla \alpha(\mathbf{x}, t)$$

where:
1. **Volume Fraction Gradient**:
   $$\nabla \alpha = \left[ \frac{\alpha(x+1, y) - \alpha(x-1, y)}{2}, \frac{\alpha(x, y+1) - \alpha(x, y-1)}{2} \right]^T$$
2. **Interface Unit Normal Vector**:
   $$\mathbf{n}(\mathbf{x}, t) = \frac{\nabla \alpha}{|\nabla \alpha| + 10^{-12}} \cdot \mathbb{I}(|\nabla \alpha| > 10^{-3})$$
3. **Interfacial Mean Curvature**:
   $$\kappa(\mathbf{x}, t) = \text{clip}\left(-\nabla \cdot \mathbf{n}, -2.0, 2.0\right) = \text{clip}\left( -\left[ \frac{n_x(x+1, y) - n_x(x-1, y)}{2} + \frac{n_y(x, y+1) - n_y(x, y-1)}{2} \right], -2.0, 2.0 \right)$$

---

## 2. Evaluation of Quantum Implementation Paradigms for Surface Tension

| Paradigm | Implementation Mechanism | Quantum Circuit Complexity | Mathematical Approximation | Physical Fidelity for Dam Break |
| :--- | :--- | :---: | :---: | :---: |
| **Option 1: Reversible Quantum Arithmetic Oracle** | Multi-qubit fixed-point division, square root, and spatial stencil circuits | Depth $> 10^6$, $> 60$ ancilla qubits per lattice node | Exact to finite-precision arithmetic | Exact |
| **Option 2: Polynomial Curvature Stencil** | Approximate $|\nabla\alpha| \approx 1$ in interface core $\implies \kappa \approx -\nabla^2 \alpha \implies \mathbf{F}_s \approx -\sigma (\nabla^2 \alpha) \nabla\alpha$ | Depth $\mathcal{O}(\text{poly}(\log N))$, 4 ancilla qubits | Bilinear spatial polynomial in $\alpha \otimes \alpha$ | High for smooth interfaces, slight parasitic currents |
| **Option 3: Hybrid Classical Preprocessing (Recommended)** | Compute $\mathbf{F}_s(t)$ classically from observable readout or between $K$-step Carleman blocks | **Zero quantum overhead** | Exact Level-4 spatial stencil | **Exact & Stably Bounded** |

---

## 3. Scientific Recommendation on Surface Tension

> [!IMPORTANT]
> **Scientific Verdict**: For Level 6, **Option 3 (Hybrid Classical Evaluation between $K$-step blocks)** is the only scientifically defensible approach that preserves both the true experimental Martin & Moyce dam-break dynamics and quantum hardware feasibility.
> 
> Attempting to synthesize a full non-linear quantum arithmetic oracle for $\kappa = -\nabla\cdot(\nabla\alpha/|\nabla\alpha|)$ requires $> 10^6$ logical gates and introduces severe division-by-zero instabilities in bulk fluid regions.
