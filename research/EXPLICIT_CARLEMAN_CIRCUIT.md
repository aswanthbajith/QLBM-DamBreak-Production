# EXPLICIT GATE-LEVEL CARLEMAN QUANTUM CIRCUIT ANALYSIS

**Date**: 2026-08-20  
**Author**: Lead Quantum-CFD Implementation Researcher  
**Reference**: Ueno et al. (QunaSys & Tokyo Gas, arXiv:2606.12770, June 2026)  

---

## 1. Algorithm Structure: Second-Order Carleman + Taylor ODE Solver
Ueno et al. construct an explicit quantum circuit for the 1D Boltzmann equation:
$$\partial_t f + v \partial_x f = -\frac{1}{\tau}(f - f^{\text{eq}})$$
1. **Second-Order Carleman Lifting**:
   * Linear state: $f(x, v)$ on $N$ grid points and 3 discrete velocities ($Q=3$).
   * Quadratic state: $f^{\otimes 2}(x, v)$.
   * Total state dimension: $D_C = N Q + N^2 Q^2$ (or local tensor $N Q(1 + Q)$).
2. **Taylor-Expansion ODE Solver via QSVT**:
   * Time evolution operator $e^{A_C \Delta t}$ is expanded via truncated Taylor polynomial:
     $$\mathcal{T}_K(A_C \Delta t) = \sum_{k=0}^K \frac{(A_C \Delta t)^k}{k!}$$
   * Implemented on quantum hardware using QSVT with odd/even polynomial phase sequences.
3. **Circuit Resource Scaling**:
   * Qubit Complexity: $\mathcal{O}(\log N)$ logical qubits.
   * Two-qubit Gate Complexity: $\mathcal{O}(K \cdot \text{polylog}(N))$.
4. **Key Scientific Demarcation**:
   * This work represents an **EXPLICIT CIRCUIT SIMULATION** conducted via statevector emulators. It was **NOT** executed on physical IBM QPUs.
