# PHASE 10 COMPREHENSIVE QUANTUM CIRCUIT INVENTORY (STAGE 10.1)

**Status**: Verified Repository-Wide Quantum Circuit Registry (7 Circuits)  
**Date**: 2026-08-19  

---

## 1. Inventory Summary

| Circuit ID | File | Name | Qubits | Clbits | Transpiled Depth | CX Gates | Real-QPU Readiness | Scientific Purpose |
| :--- | :--- | :--- | :--- | :--- | :--- | :--- | :--- | :--- |
| **`QC_01_U_A`** | `quantum/block_encoding.py` | `U_A` | $1+\lceil\log_2 D_C\rceil$ | 0 | 12 (2Q) / $\sim 1.5\text{M}$ (13Q) | 2 to $2.5\times 10^6$ | **HARDWARE_READY (2Q) / FTQC (13Q)** | Carleman dilation matrix $U_A$ |
| **`QC_02_QSVT`** | `quantum/qsvt_solver.py` | `QSVT_Inversion` | $1+\lceil\log_2 D_C\rceil$ | 0 | 15 (2Q) / $\sim 5\text{M}$ (13Q) | 2 to $10\times 10^6$ | **HARDWARE_READY (2Q) / FTQC (13Q)** | Odd Chebyshev matrix inversion |
| **`QC_03_BE_DEMO`** | `quantum_hardware/01_block_encoding_demo.py` | `Block_Enc_2Q` | 2 | 0 | 12 | 2 | **HARDWARE_READY** | $2\times 2$ LBM relaxation primitive |
| **`QC_04_QSVT_DEMO`**| `quantum_hardware/02_qsvt_demo.py` | `QSVT_2Q_deg3` | 2 | 0 | 15 | 2 | **HARDWARE_READY** | $2\times 2$ QSVT matrix inversion ($d=3$) |
| **`QC_05_MEAS_DEMO`**| `quantum_hardware/03_measurement_demo.py` | `Measured_QSVT` | 2 | 2 | 7 | 2 | **HARDWARE_READY** | Ancilla readout protocol |
| **`QC_06_STATE_4Q`** | `quantum_hardware/04_small_qlbm_state.py` | `Small_QLBM_State` | 4 | 0 | 35 | 14 | **HARDWARE_READY** | 2-node sub-volume density state |
| **`QC_07_QAE_DEMO`** | `quantum_hardware/05_qae_scalar_demo.py` | `QAE_Mass_Scalar` | 3 | 1 | 12 | 4 | **HARDWARE_READY** | Mass scalar reflection oracle |

See [`PHASE10_QUANTUM_CIRCUIT_INVENTORY.csv`](PHASE10_QUANTUM_CIRCUIT_INVENTORY.csv) for full gate-level parameters.
