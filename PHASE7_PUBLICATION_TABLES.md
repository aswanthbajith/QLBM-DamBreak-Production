# PHASE 7 PUBLICATION TABLES (STAGE 7.16)

**Status**: Verified Publication-Ready Tables (Tables 1–10)  
**Date**: 2026-08-19  

---

### Table 1: Classical Solver Parameters
| Parameter | Symbol | Value | Physical Units |
| :--- | :--- | :--- | :--- |
| Liquid Density | $\rho_L$ | 1.0 | Lattice Units |
| Gas Density | $\rho_G$ | 0.1 | Lattice Units |
| Kinematic Viscosity | $\nu$ | 0.01 | Lattice Units |
| Surface Tension Coefficient | $\sigma$ | 0.001 | Lattice Units |
| Gravity Acceleration | $g_y$ | $-2.0 \times 10^{-4}$ | Lattice Units |
| Speed of Sound Squared | $c_s^2$ | $1/3$ | Lattice Units |
| Interface Width | $W$ | 4.0 | Lattice Units |
| Phase Mobility | $M_\phi$ | 0.05 | Lattice Units |

---

### Table 2: Classical Multi-Grid Validation Benchmark
| Grid Resolution | Nodes ($N$) | Steps | Step Time (ms) | Peak RAM (MB) | Mass Drift | Max Velocity $u_{\max}$ | Mach Number | Status |
| :--- | :--- | :--- | :--- | :--- | :--- | :--- | :--- | :--- |
| **$4 \times 2$** | 8 | 50 | 5.82 | 0.04 | $4.34 \times 10^{-3}$ | $3.23 \times 10^{-4}$ | $5.60 \times 10^{-4}$ | **PASS** |
| **$8 \times 4$** | 32 | 50 | 5.29 | 0.03 | $1.45 \times 10^{-3}$ | $3.23 \times 10^{-4}$ | $5.60 \times 10^{-4}$ | **PASS** |
| **$16 \times 8$** | 128 | 50 | 5.69 | 0.07 | $7.23 \times 10^{-5}$ | $3.23 \times 10^{-4}$ | $5.60 \times 10^{-4}$ | **PASS** |
| **$32 \times 16$** | 512 | 50 | 5.85 | 0.26 | $6.60 \times 10^{-4}$ | $3.23 \times 10^{-4}$ | $5.60 \times 10^{-4}$ | **PASS** |
| **$64 \times 32$** | 2,048 | 50 | 6.38 | 1.01 | $3.00 \times 10^{-3}$ | $3.23 \times 10^{-4}$ | $5.60 \times 10^{-4}$ | **PASS** |
| **$300 \times 100$** | 30,000 | 50 | 17.46 | 14.65 | $2.00 \times 10^{-3}$ | $3.23 \times 10^{-4}$ | $5.60 \times 10^{-4}$ | **PASS** |

---

### Table 3: Carleman Dimensional Scaling ($D_C = 342 N$)
| Grid Resolution | Nodes ($N$) | Base Dim ($18N$) | Quadratic Dim ($324N$) | Carleman Dim ($D_C$) | Logical Qubits | Sparse Non-Zeros ($NNZ$) |
| :--- | :--- | :--- | :--- | :--- | :--- | :--- |
| **$1 \times 1$** | 1 | 18 | 324 | 342 | 10 | 4,212 |
| **$4 \times 2$** | 8 | 144 | 2,592 | 2,736 | 13 | 33,696 |
| **$8 \times 4$** | 32 | 576 | 10,368 | 10,944 | 15 | 134,784 |
| **$16 \times 8$** | 128 | 2,304 | 41,472 | 43,776 | 17 | 539,136 |
| **$32 \times 16$** | 512 | 9,216 | 165,888 | 175,104 | 19 | 2,156,544 |
| **$64 \times 32$** | 2,048 | 36,864 | 663,552 | 700,416 | 21 | 8,626,176 |
| **$300 \times 100$** | 30,000 | 540,000 | 9,720,000 | 10,260,000 | 25 | 126,360,000 |

---

### Table 4: QSVT Chebyshev Polynomial Degree Sweep
| Degree ($d$) | Max $|P(x)|$ | Parity Error | Inversion Residual | Relative Sol Error | Fidelity | Circuit Depth | Phase Count | Meets $10^{-10}$ |
| :--- | :--- | :--- | :--- | :--- | :--- | :--- | :--- | :--- |
| **3** | 0.9285 | 0.0 | $9.60 \times 10^{-4}$ | $9.65 \times 10^{-4}$ | 0.999999 | 6 | 3 | False |
| **5** | 0.9500 | 0.0 | $9.14 \times 10^{-5}$ | $9.18 \times 10^{-5}$ | 1.000000 | 10 | 5 | False |
| **7** | 0.9500 | 0.0 | $4.52 \times 10^{-6}$ | $4.45 \times 10^{-6}$ | 1.000000 | 14 | 7 | False |
| **9** | 0.9500 | 0.0 | $3.84 \times 10^{-7}$ | $3.85 \times 10^{-7}$ | 1.000000 | 18 | 9 | False |
| **11** | 0.9500 | 0.0 | $1.62 \times 10^{-8}$ | $1.63 \times 10^{-8}$ | 1.000000 | 22 | 11 | False |
| **15** | 0.9500 | 0.0 | $5.03 \times 10^{-11}$ | $5.05 \times 10^{-11}$ | 1.000000 | 30 | 15 | **TRUE** |
| **21** | 0.9500 | 0.0 | $1.58 \times 10^{-14}$ | $1.59 \times 10^{-14}$ | 1.000000 | 42 | 21 | **TRUE** |
| **31** | 0.9500 | 0.0 | $2.76 \times 10^{-15}$ | $2.76 \times 10^{-15}$ | 1.000000 | 62 | 31 | **TRUE** |

---

### Table 5: System Condition Number vs. Time Step
| Time Step ($\Delta t$) | Condition Number $\kappa(I + \Delta t A_C)$ | Inversion Residual | Stability Status |
| :--- | :--- | :--- | :--- |
| **0.0010** | 1.0111 | $2.49 \times 10^{-15}$ | Well-Conditioned ($\kappa < 1.5$) |
| **0.0050** | 1.0567 | $2.16 \times 10^{-13}$ | Well-Conditioned ($\kappa < 1.5$) |
| **0.0100** | 1.1168 | $5.03 \times 10^{-11}$ | Well-Conditioned ($\kappa < 1.5$) |
| **0.0200** | 1.2483 | $1.32 \times 10^{-8}$ | Well-Conditioned ($\kappa < 1.5$) |
| **0.0500** | 1.7457 | $2.90 \times 10^{-5}$ | Ill-Conditioned ($\kappa > 1.5$) |
| **0.1000** | 3.0192 | $2.55 \times 10^{-3}$ | Ill-Conditioned ($\kappa > 1.5$) |

---

### Table 6: Multi-Scale Quantum Resource Scaling
| Mesh Size | Nodes ($N$) | Total Qubits | Sparse RAM | Dense RAM | QSVT Depth | Block Calls | CX Gates |
| :--- | :--- | :--- | :--- | :--- | :--- | :--- | :--- |
| **$1 \times 1$** | 1 | 10 | 0.10 MB | 0.00 GB | 30 | 8 | 144 |
| **$4 \times 2$** | 8 | 13 | 0.79 MB | 0.11 GB | 30 | 8 | 192 |
| **$8 \times 4$** | 32 | 15 | 3.17 MB | 1.78 GB | 30 | 8 | 224 |
| **$16 \times 8$** | 128 | 17 | 12.67 MB | 28.56 GB | 30 | 8 | 256 |
| **$32 \times 16$** | 512 | 19 | 50.70 MB | 456.89 GB | 30 | 8 | 288 |
| **$64 \times 32$** | 2,048 | 21 | 202.78 MB | 7,310.20 GB | 30 | 8 | 320 |
| **$300 \times 100$** | 30,000 | 25 | 2,970.43 MB | 1,568,609.5 GB | 30 | 8 | 384 |

---

### Table 7: Multi-Scale Simulation Error Budget Decomposition
| Shots ($N_s$) | $\epsilon_{\text{disc}}$ | $\epsilon_{\text{Carle}}$ | $\epsilon_{\text{QSVT}}$ | $\epsilon_{\text{meas}}$ | Total Additive Bound | Total RSS Empirical | Dominant Error |
| :--- | :--- | :--- | :--- | :--- | :--- | :--- | :--- |
| **100** | $2.00 \times 10^{-3}$ | $9.52 \times 10^{-3}$ | $5.03 \times 10^{-11}$ | $3.73 \times 10^{-2}$ | $4.96 \times 10^{-2}$ | $3.86 \times 10^{-2}$ | Shot Noise |
| **1,000** | $2.00 \times 10^{-3}$ | $9.52 \times 10^{-3}$ | $5.03 \times 10^{-11}$ | $1.18 \times 10^{-2}$ | $2.41 \times 10^{-2}$ | $1.53 \times 10^{-2}$ | Shot Noise |
| **10,000** | $2.00 \times 10^{-3}$ | $9.52 \times 10^{-3}$ | $5.03 \times 10^{-11}$ | $3.73 \times 10^{-3}$ | $1.60 \times 10^{-2}$ | $1.04 \times 10^{-2}$ | Carleman Truncation |
| **100,000** | $2.00 \times 10^{-3}$ | $9.52 \times 10^{-3}$ | $5.03 \times 10^{-11}$ | $1.18 \times 10^{-3}$ | $1.35 \times 10^{-2}$ | $9.81 \times 10^{-3}$ | Carleman Truncation |
| **1,000,000** | $2.00 \times 10^{-3}$ | $9.52 \times 10^{-3}$ | $5.03 \times 10^{-11}$ | $3.73 \times 10^{-4}$ | $1.27 \times 10^{-2}$ | $9.74 \times 10^{-3}$ | Carleman Truncation |

---

### Table 8: Adversarial Failure Boundary Matrix
| Parameter | Safe Operating Zone | Critical Boundary | Failure Zone | Failure Type |
| :--- | :--- | :--- | :--- | :--- |
| Time Step $\Delta t$ | $\Delta t \le 0.020$ | $\Delta t = 0.035$ | $\Delta t \ge 0.050$ | Spectral Conditioning |
| Density Ratio $\rho_L/\rho_G$ | $\rho_L/\rho_G = 1.0$ | $\rho_L/\rho_G = 2.0$ | $\rho_L/\rho_G \ge 10.0$ | Mathematical Closure |
| Mach Number $u_{\max}/c_s$ | $u < 0.05 c_s$ | $u = 0.10 c_s$ | $u \ge 0.20 c_s$ | Hydrodynamic Asymptotic |
| QSVT Degree $d$ | $d \in [11, 21]$ | $d = 7$ | $d \le 5$ | Algorithmic Approximation |
| Noise Rate $\lambda$ | $\lambda \le 0.001$ | $\lambda = 0.010$ | $\lambda \ge 0.050$ | Quantum Decoherence |
| Shot Count $N_s$ | $N_s \ge 10,000$ | $N_s = 1,000$ | $N_s \le 100$ | Statistical Sampling |

---

### Table 9: Quantum Execution Authenticity Classification
| Subsystem / Operation | Implementation Mechanism | Scientific Classification |
| :--- | :--- | :--- |
| Carleman Sparse Matrix | SciPy Sparse CSR | Classical Numerical |
| Block Encoding Matrix | Canonical CS/Halmos Dilation | Classical SVD Matrix |
| Block Encoding Circuit | Qiskit `QuantumCircuit` IR | Quantum Circuit Synthesis |
| QSVT Phase Angles | Classical Remez Optimization | Classical Algebraic |
| QSVT Circuit | Qiskit `QuantumCircuit` IR | Quantum Circuit Synthesis |
| Multi-Step Dynamics | SVD Functional Calculus | Hybrid Classical SVD Emulation |
| Shot-Noise Sampling | Multinomial Monte Carlo | Statevector Simulation |
| Noise Channel Emulation | Statevector Mixed State | Statevector Simulation |
| Physical Hardware Run | Not Executed | Not Demonstrated |

---

### Table 10: Authoritative Scientific Claim Summary
See [`PHASE7_FINAL_CLAIM_MATRIX.csv`](PHASE7_FINAL_CLAIM_MATRIX.csv) for the full 30-claim matrix.
