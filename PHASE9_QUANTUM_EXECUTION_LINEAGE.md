# PHASE 9 QUANTUM EXECUTION LINEAGE & PIPELINE CLASSIFICATION (STAGE 9.3)

**Status**: Authoritative Lineage Trace Across All Algorithmic Stages  
**Date**: 2026-08-19  

---

## 1. Algorithmic Chain: From CFD to Hardware

```mermaid
graph TD
    A["Classical Two-Phase LBM
(D2Q9 Navier-Stokes + Allen-Cahn)"] -->|IMPLEMENTED| B["Polynomial Quadratic Surrogate
(p=2, Constant-Density)"]
    B -->|IMPLEMENTED| C["Local Carleman Lifting
(D_C = 342N Sparse Matrix A_C)"]
    C -->|IMPLEMENTED| D["Unitary Block Encoding Matrix
(Canonical CS/Halmos Dilation U_A)"]
    D -->|IMPLEMENTED (n <= 8)
OPAQUE (n > 8)| E["Block Encoding QuantumCircuit
(UnitaryGate in Qiskit)"]
    E -->|IMPLEMENTED (n <= 8)| F["QSVT Inversion QuantumCircuit
(Alternating Rz(2phi) & U_A)"]
    F -->|SIMULATED / EMULATED| G["Multi-Step Time Evolution
(Classical CPU SVD Functional Calculus)"]
    G -->|SIMULATED| H["Observable Extraction
(Classical Projection + Shot Noise)"]
    H -->|ANALYTICAL BLUEPRINT| I["Quantum Amplitude Estimation (QAE)
(Reflection Oracles for M, E_k, F_wall)"]
    I -->|NOT YET EXECUTED| J["Physical QPU Hardware Execution
(IBM Quantum Eagle / Heron)"]
```

---

## 2. Definitive Stage Classification

| Algorithmic Transition | Implementation Mechanism | Rigorous Classification |
| :--- | :--- | :--- |
| **Classical LBM $\to$ Surrogate** | Python NumPy / SciPy array computations | **CLASSICAL CFD** |
| **Surrogate $\to$ Carleman Matrix $A_C$** | SciPy CSR sparse matrix builder (`CarlemanTwoPhaseLBM`) | **CLASSICAL CARLEMAN** |
| **$A_C \to$ Block Encoding Matrix $U_A$** | Classical SVD Halmos CS-dilation | **CLASSICAL DILATION** |
| **$U_A \to$ Qiskit Circuit** | `QuantumBlockEncoding._build_qiskit_circuit` | **REAL_CIRCUIT ($n \le 8$) / OPAQUE ($n > 8$)** |
| **QSVT Phases $\to$ QSVT Circuit** | `QSVTSolver._build_qsvt_circuit` | **REAL_CIRCUIT ($n \le 8$) / OPAQUE ($n > 8$)** |
| **QSVT Multi-Step Time Stepping** | Evaluated via CPU SVD functional calculus | **CLASSICAL SVD EMULATION** |
| **Observable Measurement** | Classical state vector projection + Gaussian noise | **STATEVECTOR SIMULATION** |
| **QAE Scalar Extraction** | Mathematical oracle design & query scaling equations | **ANALYTICAL BLUEPRINT** |
| **Transpilation to Basis Gates** | Qiskit `transpile` targeting IBM basis gates | **TRANSPILED CIRCUIT** |
| **Real QPU Execution** | Not yet executed on physical superconducting processor | **NOT DEMONSTRATED** |
