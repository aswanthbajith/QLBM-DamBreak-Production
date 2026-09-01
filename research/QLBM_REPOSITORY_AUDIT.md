# QLBM OPEN-SOURCE SOFTWARE & REPOSITORY AUDIT

**Date**: 2026-08-20  
**Author**: Lead Quantum-CFD Implementation Researcher  
**Target Framework**: `QCFD-Lab/qlbm` (Matthias Möller et al., TU Delft)  

---

## 1. Architectural Audit of `QCFD-Lab/qlbm`
The `qlbm` Python package provides an end-to-end modular framework for quantum CFD:
* **Lattice Discretization**: Supports D1Q3, D2Q4, D2Q9, D3Q19 lattices with structured spatial bitstring indexing.
* **Velocity / Channel Encoding**: Maps discrete velocity directions to quantum register bitstrings $|q\rangle = |q_0 q_1 \dots q_{k-1}\rangle$.
* **Streaming Operators**: Implements quantum binary incrementers/decrementers for spatial coordinate shifts $x \mapsto (x + c_{ix}) \pmod{N_x}$.
* **Collision Implementations**:
  1. *Linearized Collision*: Single-qubit Pauli-X/Y/Z and controlled rotation gates for acoustic/diffusion models.
  2. *Surrogate Quantum Circuits (SQC)*: Parameterized unitary circuits trained via classical gradient descent to approximate non-unitary BGK dynamics.
  3. *Carleman Block Encoding*: Interfaces for loading Carleman linearized operators.
* **Boundary Handling**: Direct ancilla-assisted bounce-back reflections and periodic wrap-around boundary circuits.

---

## 2. Reusable vs. Missing Components for QLBM-DamBreak

| Component | Status in Literature / `qlbm` | Usability in Our Project | Action Required |
| :--- | :--- | :--- | :--- |
| **D2Q9 Spatial Streaming** | Standard quantum incrementer $\mathcal{O}(\log N)$ | **Directly Reusable** | Verified in `PHASE11_STREAMING_ORACLE.py` |
| **Local Collision Oracle** | Variational SQC / Local Carleman | **Directly Reusable** | Verified in `PHASE11_STRUCTURED_QSVT.py` |
| **Two-Phase Allen-Cahn** | Classical LBM only; absent in quantum literature | **Original Research Contribution** | Keep classical ground truth and local quadratic surrogate |
| **Dam-Break Hydrodynamics**| Classical benchmarks only; absent on real QPU | **Original Research Contribution** | Build small verified proof-of-concept pipeline |
