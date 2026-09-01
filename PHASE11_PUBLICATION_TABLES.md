# PHASE 11 MASTER PUBLICATION TABLES (STAGE 11.21)

**Status**: Verified Publication Tables (Tables 1–10)  
**Date**: 2026-08-19  

---

### Table 1: Complete Quantum Circuit Inventory
See [`PHASE11_COMPLETE_QUANTUM_INVENTORY.csv`](PHASE11_COMPLETE_QUANTUM_INVENTORY.csv).

### Table 2: Structured Oracle Resources
| Oracle | Qubits | Original Depth | Transpiled Depth (Eagle-127) | CX Gates | Unitarity Error |
| :--- | :--- | :--- | :--- | :--- | :--- |
| **Streaming (2x2)** | 6 | 2 | 3 | 4 | $< 10^{-16}$ |
| **Streaming (4x2)** | 7 | 3 | 5 | 6 | $< 10^{-16}$ |
| **Collision (Local 2Q)** | 2 | 4 | 8 | 2 | $< 10^{-16}$ |
| **Structured QSVT (d=3)** | 3 | 8 | 15 | 4 | $< 10^{-16}$ |
| **E2E Structured LBM (2x2)**| 6 | 6 | 9 | 4 | $< 10^{-16}$ |

### Table 3: Dense vs Structured Resource Comparison on 4x2 Mesh (13 Qubits)
| Metric | Dense CS/Halmos Dilation | Structured LCU Oracle | Improvement Factor |
| :--- | :--- | :--- | :--- |
| **Transpiled CNOT Count** | $\sim 2,500,000$ | **34** | **$\approx 73,500 \times$ Reduction** |
| **Transpiled Depth** | $\sim 1,500,000$ | **42** | **$\approx 35,700 \times$ Reduction** |
| **NISQ Feasibility** | **UNEXECUTABLE** | **CLEAN EXECUTION (Fidelity $> 95\%$)** | **Direct Hardware Access** |

### Table 4: Ideal Quantum Validation Results
See [`PHASE11_IDEAL_VALIDATION.csv`](PHASE11_IDEAL_VALIDATION.csv).

### Table 5: Noisy Simulation Results
See [`PHASE11_NOISY_VALIDATION.csv`](PHASE11_NOISY_VALIDATION.csv).

### Table 6: Real QPU Hardware Comparison
See [`PHASE11_HARDWARE_RESULTS.csv`](PHASE11_HARDWARE_RESULTS.csv).

### Table 7: Hardware Backend Calibration Metadata
See [`PHASE11_HARDWARE_METADATA.json`](PHASE11_HARDWARE_METADATA.json).

### Table 8: Comprehensive Error Budget Decomposition
| Component | Low-Shot ($N_s=100$) | Medium-Shot ($N_s=1000$) | High-Shot ($N_s=10000$) | Noisy | Ideal |
| :--- | :--- | :--- | :--- | :--- | :--- |
| $\epsilon_{\text{streaming}}$ | 0.00 | 0.00 | 0.00 | 0.00 | 0.00 |
| $\epsilon_{\text{collision}}$ | 0.00 | 0.00 | 0.00 | 0.00 | 0.00 |
| $\epsilon_{\text{QSVT}}$ ($d=3$) | $9.60 \times 10^{-4}$ | $9.60 \times 10^{-4}$ | $9.60 \times 10^{-4}$ | $9.60 \times 10^{-4}$ | $9.60 \times 10^{-4}$ |
| $\epsilon_{\text{meas}}$ | $1.00 \times 10^{-1}$ | $3.16 \times 10^{-2}$ | $1.00 \times 10^{-2}$ | $3.16 \times 10^{-2}$ | 0.00 |
| $\epsilon_{\text{noise}}$ | $1.20 \times 10^{-2}$ | $1.20 \times 10^{-2}$ | $1.20 \times 10^{-2}$ | $1.20 \times 10^{-2}$ | 0.00 |
| **Total Error (RSS)** | **$1.01 \times 10^{-1}$** | **$3.38 \times 10^{-2}$** | **$1.56 \times 10^{-2}$** | **$3.38 \times 10^{-2}$** | **$9.60 \times 10^{-4}$** |

### Table 9: Multi-Scale Grid Scaling Projections
See [`PHASE11_SCALING_ANALYSIS.md`](PHASE11_SCALING_ANALYSIS.md).

### Table 10: Final Claim Classification Matrix
See [`PHASE11_FINAL_CLAIM_MATRIX.csv`](PHASE11_FINAL_CLAIM_MATRIX.csv).
