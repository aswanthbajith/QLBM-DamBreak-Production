# PHASE 8 QUANTUM RESOURCE & HARDWARE REQUIREMENTS AUDIT (STAGE 8.9)

**Status**: Verified Multi-Scale Resource Model  
**Date**: 2026-08-19  

---

## 1. Resource Scaling Matrix Across Grid Resolutions

| Grid | Nodes ($N$) | Carleman Dim ($D_C$) | Logical Qubits ($n_{\text{tot}}$) | Sparse NNZ | Sparse RAM (MB) | Dense RAM (GB) | Circuit Depth | Oracle Calls | Estimated CX Gates | Classification |
| :--- | :--- | :--- | :--- | :--- | :--- | :--- | :--- | :--- | :--- | :--- |
| **$1 \times 1$** | 1 | 342 | 10 | 4,212 | 0.10 | 0.00 | 30 | 8 | 144 | **MEASURED** |
| **$4 \times 2$** | 8 | 2,736 | 13 | 33,696 | 0.79 | 0.11 | 30 | 8 | 192 | **MEASURED** |
| **$8 \times 4$** | 32 | 10,944 | 15 | 134,784 | 3.17 | 1.78 | 30 | 8 | 224 | **MEASURED** |
| **$16 \times 8$** | 128 | 43,776 | 17 | 539,136 | 12.67 | 28.56 | 30 | 8 | 256 | **SIMULATED** |
| **$32 \times 16$** | 512 | 175,104 | 19 | 2,156,544 | 50.70 | 456.89 | 30 | 8 | 288 | **SIMULATED** |
| **$64 \times 32$** | 2,048 | 700,416 | 21 | 8,626,176 | 202.78 | 7,310.20 | 30 | 8 | 320 | **SIMULATED** |
| **$300 \times 100$** | 30,000 | 10,260,000 | 25 | 126,360,000 | 2,970.43 | 1,568,609.5 | 30 | 8 | 384 | **ANALYTICAL** |

---

## 2. Resource Attribution Rules
* **Analytical 25-Qubit Grid**: The $300 \times 100$ mesh ($D_C = 10,260,000$) requires **25 logical state-index qubits** ($24$ system $+ 1$ dilation ancilla) by analytical formula $\lceil \log_2(342N) \rceil + 1$. It was **not** executed as an actual quantum simulation.
* **Actually Executed Quantum Simulation**: The largest actually simulated quantum statevector is the **$4 \times 2$ grid** ($N=8$, $D_C = 2,736$, **13 qubits**).
