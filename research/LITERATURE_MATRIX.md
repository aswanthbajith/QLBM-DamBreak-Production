# COMPREHENSIVE QUANTUM LATTICE BOLTZMANN LITERATURE MATRIX

**Date**: 2026-08-20  
**Author**: Lead Quantum-CFD Implementation Researcher  

---

## 1. Authoritative Literature Classification

| Paper / Reference | Year | Lattice / Dim | Collision Model | Streaming Model | Boundary Handling | Quantum Encoding & Algorithm | Hardware / Execution Status | Scientific Classification |
| :--- | :--- | :--- | :--- | :--- | :--- | :--- | :--- | :--- |
| **Zamora, Budinski, Lahtinen, Sagaut** (PR E 113, 035307) | 2026 | D2Q9 | Local Carleman Linearization | Reversible Coordinate Shift | Periodic / Bounce-back | Dynamic circuits, $\mathcal{O}(\log^2 N + Q^3)$ scaling | Circuit Simulation / Qiskit Aer | **QUANTUM CIRCUIT SIMULATION** |
| **Demirdjian, Hogancamp, Gnanasekaran, Surana, Gunlycke** (arXiv:2605.00302) | 2026 | D2Q9 / 2D | Carleman Linearization | Spatial Shift | Linear System Constraints | Linear Combination of Non-Unitaries (LCNU) $	o$ LCU | Analytical & Classical Statevector | **THEORY / CLASSICAL SIMULATION** |
| **Ueno, Kanno, Lee (QunaSys & Tokyo Gas)** (arXiv:2606.12770) | 2026 | 1D Boltzmann | Second-Order Carleman | 1D Shift | Periodic / Wall | Taylor ODE Solver via QSVT | Exact Statevector Simulation | **QUANTUM CIRCUIT SIMULATION** |
| **Bastida-Zamora, Budinski, Kerppo, Lahtinen, Niemimäki** (arXiv:2603.02127) | 2026 | D2Q9 / D1Q3 | One-Step Simplified LBM (OSSLBM) | Unified Step Matrix | Linear Acoustics / Wall | Hybrid Variational / Direct Matrix Inversion | IBM Quantum (Small Linear/Hybrid QPU loop) | **HYBRID QUANTUM-CLASSICAL / REAL QPU (Small Linear)** |
| **Lăcătuş & Möller (TU Delft / QCFD-Lab)** (arXiv:2507.12256) | 2025 | D2Q9 | Surrogate Quantum Circuit (SQC) | Classical Reinitialization | Taylor-Green / Cavity | Variational Unitary Learning (724 native Heron gates) | Compiled for IBM Heron (Simulator) | **QUANTUM CIRCUIT SIMULATION** |
| **Nagel & Löwe (DLR)** (arXiv:2510.05965) | 2025 | D1Q2 / D2Q4 | Linear Advection-Diffusion | Shift Permutations | Periodic | Multi-step without reinitialization | Qiskit Aer / Shot Simulation | **QUANTUM CIRCUIT SIMULATION** |
| **Jennings et al. (PsiQuantum & Airbus)** (arXiv:2512.05781) | 2025 | Incompressible LBM | Linearized Collision | Boundary Matrix Embedding | Walls, Inlets, Outlets, Forcing | Fault-Tolerant LCU & QSVT Block Encoding | Classical Complexity Analysis & Numerics | **THEORY / CLASSICAL SIMULATION** |
| **Ueno, Kanno, Lee (QunaSys)** (arXiv:2605.28135) | 2026 | D2Q9 | Carleman Linearization | Index-Value Block Encoding | Inflow, Outflow, No-Slip Obstacle | Block Encoding + QSVT | Statevector Simulation | **QUANTUM CIRCUIT SIMULATION** |
| **Möller et al. (`qlbm` Framework)** | 2024–2026| D2Q9 / D3Q19 | BGK / Linear Collision | Shift Permutation | Bounce-back, Periodic | Python framework for Qiskit/Pytket | Framework / Simulator Interfaces | **HYBRID QUANTUM-CLASSICAL / FRAMEWORK** |

---

## 2. Rigorous Scientific Classifications Defined
* **THEORY**: Analytical complexity derivations, asymptotic bounds, and circuit block diagrams without software execution.
* **CLASSICAL SIMULATION**: Matrix evaluations, sparse SVD/LAPACK solves, and classical CFD evaluations.
* **QUANTUM CIRCUIT SIMULATION**: Execution of explicit `QuantumCircuit` objects on ideal/statevector quantum simulators.
* **NOISY SIMULATION**: Circuit execution with simulated depolarizing, thermal, or readout noise models.
* **FAKE HARDWARE**: Circuit execution on `GenericBackendV2` or transpiled fake topology targets without cloud communication.
* **REAL QUANTUM HARDWARE**: Circuits submitted to a physical quantum device resulting in actual job IDs and raw counts.
* **HYBRID QUANTUM-CLASSICAL**: Quantum circuit used as a subroutine in an iterative classical outer loop.
* **FULLY QUANTUM**: End-to-end multi-step quantum evolution without classical intermediate measurements.
