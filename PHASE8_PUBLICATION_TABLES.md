# PHASE 8 MASTER PUBLICATION TABLES (STAGE 8.16)

**Status**: Verified Master Tables (Tables 1–10)  
**Date**: 2026-08-19  

---

### Table 1: Classical CFD Validation Across 6 Grid Resolutions
| Grid Resolution | Nodes ($N$) | Total Time (s) | Step Time (ms) | Peak RAM (MB) | Mass Drift | $u_{\max}$ | Mach Number | Status |
| :--- | :--- | :--- | :--- | :--- | :--- | :--- | :--- | :--- |
| **$4 \times 2$** | 8 | 0.285 | 5.70 | 0.04 | $4.34 \times 10^{-3}$ | $3.23 \times 10^{-4}$ | $5.60 \times 10^{-4}$ | **PASS** |
| **$8 \times 4$** | 32 | 0.258 | 5.19 | 0.03 | $1.45 \times 10^{-3}$ | $3.23 \times 10^{-4}$ | $5.60 \times 10^{-4}$ | **PASS** |
| **$16 \times 8$** | 128 | 0.268 | 5.48 | 0.07 | $7.23 \times 10^{-5}$ | $3.23 \times 10^{-4}$ | $5.60 \times 10^{-4}$ | **PASS** |
| **$32 \times 16$** | 512 | 0.287 | 5.84 | 0.26 | $6.60 \times 10^{-4}$ | $3.23 \times 10^{-4}$ | $5.60 \times 10^{-4}$ | **PASS** |
| **$64 \times 32$** | 2,048 | 0.320 | 6.36 | 1.01 | $3.00 \times 10^{-3}$ | $3.23 \times 10^{-4}$ | $5.60 \times 10^{-4}$ | **PASS** |
| **$300 \times 100$** | 30,000 | 0.914 | 16.71 | 14.65 | $2.00 \times 10^{-3}$ | $3.23 \times 10^{-4}$ | $5.60 \times 10^{-4}$ | **PASS** |

---

### Table 2: Carleman Dimensions and Scaling ($D_C = 342N$)
| Grid Resolution | Nodes ($N$) | Base Space ($18N$) | Quadratic Space ($324N$) | Carleman Dim ($D_C$) | Sparse NNZ ($4212N$) |
| :--- | :--- | :--- | :--- | :--- | :--- |
| **$1 \times 1$** | 1 | 18 | 324 | 342 | 4,212 |
| **$4 \times 2$** | 8 | 144 | 2,592 | 2,736 | 33,696 |
| **$8 \times 4$** | 32 | 576 | 10,368 | 10,944 | 134,784 |
| **$16 \times 8$** | 128 | 2,304 | 41,472 | 43,776 | 539,136 |
| **$32 \times 16$** | 512 | 9,216 | 165,888 | 175,104 | 2,156,544 |
| **$64 \times 32$** | 2,048 | 36,864 | 663,552 | 700,416 | 8,626,176 |
| **$300 \times 100$** | 30,000 | 540,000 | 9,720,000 | 10,260,000 | 126,360,000 |

---

### Table 3: Block Encoding Verification
| Grid | Nodes ($N$) | Carleman Dim ($D_C$) | Padded Dim ($2^n$) | Total Qubits | Subnorm $\alpha$ | Unitarity Error | Block Error | Status |
| :--- | :--- | :--- | :--- | :--- | :--- | :--- | :--- | :--- |
| **$1 \times 1$** | 1 | 342 | 512 | 10 | 11.4739 | $4.00 \times 10^{-15}$ | $1.11 \times 10^{-16}$ | **VERIFIED** |
| **$2 \times 1$** | 2 | 684 | 1,024 | 11 | 11.4739 | $4.00 \times 10^{-15}$ | $1.11 \times 10^{-16}$ | **VERIFIED** |
| **$2 \times 2$** | 4 | 1,368 | 2,048 | 12 | 11.4739 | $3.44 \times 10^{-15}$ | $5.55 \times 10^{-17}$ | **VERIFIED** |
| **$4 \times 2$** | 8 | 2,736 | 4,096 | 13 | 11.4739 | $3.22 \times 10^{-15}$ | $1.11 \times 10^{-16}$ | **VERIFIED** |
| **$8 \times 4$** | 32 | 10,944 | 16,384 | 15 | 11.4739 | $3.11 \times 10^{-15}$ | $1.11 \times 10^{-16}$ | **VERIFIED** |

---

### Table 4: QSVT Chebyshev Degree Sweep
| Degree ($d$) | Max $|P(x)|$ | Parity Error | Inversion Residual | Relative Sol Error | Fidelity | Circuit Depth | Block Calls | Target Met |
| :--- | :--- | :--- | :--- | :--- | :--- | :--- | :--- | :--- |
| **3** | 0.9285 | 0.0 | $9.60 \times 10^{-4}$ | $9.65 \times 10^{-4}$ | 0.999999 | 6 | 2 | None |
| **5** | 0.9500 | 0.0 | $9.14 \times 10^{-5}$ | $9.18 \times 10^{-5}$ | 1.000000 | 10 | 3 | None |
| **7** | 0.9500 | 0.0 | $4.52 \times 10^{-6}$ | $4.45 \times 10^{-6}$ | 1.000000 | 14 | 4 | None |
| **9** | 0.9500 | 0.0 | $3.84 \times 10^{-7}$ | $3.85 \times 10^{-7}$ | 1.000000 | 18 | 5 | None |
| **11** | 0.9500 | 0.0 | $1.62 \times 10^{-8}$ | $1.63 \times 10^{-8}$ | 1.000000 | 22 | 6 | $< 10^{-8}$ |
| **15** | 0.9500 | 0.0 | $5.03 \times 10^{-11}$ | $5.05 \times 10^{-11}$ | 1.000000 | 30 | 8 | $< 10^{-10}$ |
| **21** | 0.9500 | 0.0 | $1.58 \times 10^{-14}$ | $1.59 \times 10^{-14}$ | 1.000000 | 42 | 11 | $< 10^{-12}$ |
| **31** | 0.9500 | 0.0 | $2.76 \times 10^{-15}$ | $2.76 \times 10^{-15}$ | 1.000000 | 62 | 16 | Machine Prec. |

---

### Table 5: Condition Number Boundary
| $\Delta t$ | $\sigma_{\max}$ | $\sigma_{\min}$ | Condition Number $\kappa$ | Residual ($d=15$) | Operating Zone |
| :--- | :--- | :--- | :--- | :--- | :--- |
| **0.0010** | 1.0109 | 0.9998 | 1.0111 | $2.49 \times 10^{-15}$ | Safe Zone |
| **0.0050** | 1.0546 | 0.9980 | 1.0567 | $2.16 \times 10^{-13}$ | Safe Zone |
| **0.0100** | 1.1093 | 0.9933 | 1.1168 | $5.03 \times 10^{-11}$ | Safe Zone |
| **0.0200** | 1.2185 | 0.9761 | 1.2483 | $1.32 \times 10^{-8}$ | Safe Zone |
| **0.0300** | 1.3278 | 0.9472 | 1.3958 | $4.19 \times 10^{-7}$ | Safe Zone |
| **0.0350** | 1.3824 | 0.9290 | 1.4761 | $1.57 \times 10^{-6}$ | **Boundary ($\kappa \approx 1.5$)** |
| **0.0400** | 1.4371 | 0.9082 | 1.5610 | $4.84 \times 10^{-6}$ | Ill-Conditioned |
| **0.0500** | 1.5463 | 0.8858 | 1.7457 | $2.90 \times 10^{-5}$ | Ill-Conditioned |
| **0.0750** | 1.8195 | 0.7937 | 2.3030 | $4.25 \times 10^{-4}$ | Ill-Conditioned |
| **0.1000** | 2.0927 | 0.6931 | 3.0192 | $2.55 \times 10^{-3}$ | Ill-Conditioned |

---

### Table 6: Multi-Step Carleman Accuracy (t=1..200)
| Step ($t$) | Relative $L_1$ Error | Relative $L_2$ Error | $L_\infty$ Error | Relative Mass Error | Manifold Defect |
| :--- | :--- | :--- | :--- | :--- | :--- |
| **1** | $6.97 \times 10^{-4}$ | $7.86 \times 10^{-4}$ | $2.32 \times 10^{-4}$ | $1.44 \times 10^{-5}$ | 0.1071 |
| **5** | $4.59 \times 10^{-3}$ | $4.95 \times 10^{-3}$ | $2.85 \times 10^{-3}$ | $1.82 \times 10^{-3}$ | 0.0744 |
| **10** | $5.36 \times 10^{-3}$ | $5.64 \times 10^{-3}$ | $2.84 \times 10^{-3}$ | $3.09 \times 10^{-3}$ | 0.0864 |
| **20** | $9.38 \times 10^{-3}$ | $9.52 \times 10^{-3}$ | $4.13 \times 10^{-3}$ | $4.55 \times 10^{-3}$ | 0.1069 |
| **50** | $3.55 \times 10^{-2}$ | $3.58 \times 10^{-2}$ | $1.31 \times 10^{-2}$ | $4.35 \times 10^{-3}$ | 0.1327 |
| **100** | $1.41 \times 10^{-2}$ | $1.45 \times 10^{-2}$ | $6.30 \times 10^{-3}$ | $3.39 \times 10^{-3}$ | 0.1372 |
| **200** | $1.04 \times 10^{-2}$ | $1.05 \times 10^{-2}$ | $3.44 \times 10^{-3}$ | $3.39 \times 10^{-3}$ | 0.1373 |

---

### Table 7: Quantum Noise Robustness
| Noise Rate ($\lambda$) | Output State Fidelity | Relative Mass Error | Linear Residual | Usability Status |
| :--- | :--- | :--- | :--- | :--- |
| **0.0000** | 1.000000 | $0.0000$ | $5.03 \times 10^{-11}$ | **TRUE** |
| **0.0001** | 0.999900 | $7.80 \times 10^{-4}$ | $1.20 \times 10^{-5}$ | **TRUE** |
| **0.0010** | 0.999009 | $3.05 \times 10^{-3}$ | $1.20 \times 10^{-4}$ | **TRUE** |
| **0.0100** | 0.990097 | $1.11 \times 10^{-2}$ | $1.20 \times 10^{-3}$ | **TRUE** |
| **0.0500** | 0.949866 | $2.65 \times 10^{-2}$ | $6.00 \times 10^{-3}$ | **TRUE** |
| **0.1000** | 0.900832 | $6.46 \times 10^{-2}$ | $1.20 \times 10^{-2}$ | **FALSE** |

---

### Table 8: Resource Scaling Across Grid Resolutions
| Grid | Nodes ($N$) | Logical Qubits | Sparse RAM (MB) | Dense RAM (GB) | Circuit Depth | Oracle Calls | CX Gates |
| :--- | :--- | :--- | :--- | :--- | :--- | :--- | :--- |
| **$1 \times 1$** | 1 | 10 | 0.10 | 0.00 | 30 | 8 | 144 |
| **$4 \times 2$** | 8 | 13 | 0.79 | 0.11 | 30 | 8 | 192 |
| **$8 \times 4$** | 32 | 15 | 3.17 | 1.78 | 30 | 8 | 224 |
| **$16 \times 8$** | 128 | 17 | 12.67 | 28.56 | 30 | 8 | 256 |
| **$32 \times 16$** | 512 | 19 | 50.70 | 456.89 | 30 | 8 | 288 |
| **$64 \times 32$** | 2,048 | 21 | 202.78 | 7,310.20 | 30 | 8 | 320 |
| **$300 \times 100$** | 30,000 | 25 | 2,970.43 | 1,568,609.5 | 30 | 8 | 384 |

---

### Table 9: Claim Classification Summary
See [`PHASE8_MASTER_CLAIM_MATRIX.csv`](PHASE8_MASTER_CLAIM_MATRIX.csv) for full 30-claim database.

---

### Table 10: Quantum Execution Lineage & Authenticity
| Subsystem | Underlying Solver | Classification |
| :--- | :--- | :--- |
| Carleman Matrix | SciPy Sparse CSR | Classical Numerical |
| Block Encoding Matrix | Canonical CS/Halmos Dilation | Classical SVD Matrix |
| Block Encoding Circuit | Qiskit IR `QuantumCircuit` | Quantum Circuit Synthesis |
| QSVT Phase Angles | Remez Optimization | Classical Algebraic |
| QSVT Circuit | Qiskit IR `QuantumCircuit` | Quantum Circuit Synthesis |
| Dynamical Step | SVD Functional Calculus | Hybrid Classical SVD Emulation |
| Shot Sampling | Multinomial Distribution | Statevector Simulation |
| Noise Channel | Statevector Density Matrix | Statevector Simulation |
| Physical Hardware | Not Executed | Not Demonstrated |
