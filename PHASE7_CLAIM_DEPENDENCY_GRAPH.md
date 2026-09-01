# PHASE 7 SCIENTIFIC CLAIM DEPENDENCY GRAPH (STAGE 7.2)

**Status**: Verified Verification & Evidence Dependency Structure  
**Date**: 2026-08-19  

---

## 1. Hierarchical Scientific Claim Dependency Architecture

```mermaid
graph TD
    classDef verified fill:#d4edda,stroke:#28a745,stroke-width:2px;
    classDef disproven fill:#f8d7da,stroke:#dc3545,stroke-width:2px;
    classDef analytical fill:#cce5ff,stroke:#007bff,stroke-width:2px;
    classDef emulated fill:#fff3cd,stroke:#ffc107,stroke-width:2px;

    PHY01["PHY-01: Classical 2-Phase LBM Ground Truth<br/>(D2Q9 Navier-Stokes + Allen-Cahn)"]:::verified
    PHY02["PHY-02: Martin & Moyce (1952) Dam Break<br/>(300x100 Grid Validation)"]:::verified
    
    MAT01["MAT-01: Quadratic Surrogate Model (p=2)<br/>(Constant-Density Regime)"]:::verified
    MAT02["MAT-02: Local Carleman Lifting D_C = 342N<br/>(Node-wise Kronecker Square)"]:::verified
    MAT03["MAT-03: Variable-Density Cubic Closure (p=3)<br/>(DISPROVEN: Sqrt normal & Quartic force)"]:::disproven
    MAT04["MAT-04: Static Reciprocal Density xi=1/rho<br/>(DISPROVEN: Diverges for rho >= 10)"]:::disproven

    NUM01["NUM-01: Bounded Carleman Multi-Step Error<br/>(Saturates at ~1.05% at t=200)"]:::verified
    NUM02["NUM-02: Linear O(N) Classical Scaling<br/>(5.14 ms on N=32 to 17.0 ms on N=30k)"]:::verified

    QAL01["QAL-01: CS/Halmos Unitary Block Encoding<br/>(Unitary Err < 4e-15)"]:::verified
    QAL02["QAL-02: Grid-Invariant Subnormalization<br/>(alpha = 11.4739 Invariant)"]:::verified
    QAL03["QAL-03: QSVT Chebyshev Matrix Inversion<br/>(Residual 5.03e-11 at d=15)"]:::verified
    QAL04["QAL-04: Step Condition Number Bound<br/>(kappa < 1.5 for dt <= 0.035)"]:::verified
    QAL05["QAL-05: Qiskit Circuit Synthesis<br/>(Depth = 2d, Phase Rotations = d)"]:::verified
    QAL06["QAL-06: Hybrid Multi-Step SVD Emulation<br/>(448.8x Classical CPU Overhead)"]:::emulated
    QAL07["QAL-07: Depolarizing Noise Robustness<br/>(Usable up to lambda <= 0.05)"]:::verified

    CMP01["CMP-01: Logarithmic Qubit Register Scaling<br/>(n_tot = ceil(log2(342N)) + 1)"]:::analytical
    CMP02["CMP-02: Production 300x100 Extrapolation<br/>(25 Qubits, 1.54 GB Sparse RAM)"]:::analytical
    CMP03["CMP-03: Quantum Amplitude Estimation Advantage<br/>(Quadratic O(1/eps) for Scalar Integrals)"]:::analytical
    CMP04["CMP-04: Exponential Full-Field Speedup<br/>(DISPROVEN: Omega(N log N / eps^2) Tomography)"]:::disproven
    CMP05["CMP-05: Physical Fault-Tolerant Hardware<br/>(NOT DEMONSTRATED)"]:::emulated

    PHY01 --> PHY02
    PHY01 --> MAT01
    PHY01 --> NUM02
    PHY01 -.-> MAT03
    MAT03 -.-> MAT04
    MAT01 --> MAT02
    MAT02 --> NUM01
    MAT02 --> QAL01
    MAT02 --> QAL04
    MAT02 --> CMP01
    QAL01 --> QAL02
    QAL01 --> QAL03
    QAL02 --> QAL03
    QAL03 --> QAL05
    QAL03 --> QAL06
    QAL03 --> QAL07
    QAL03 --> CMP03
    CMP01 --> CMP02
```

---

## 2. Complete Verification Evidence Chain
Every surviving claim in the graph is anchored by deterministic unit tests in `tests/` and clean-room empirical datasets in `results/phase6/` and `validation/`.
