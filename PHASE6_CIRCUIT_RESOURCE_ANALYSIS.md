# PHASE 6 QUANTUM CIRCUIT RESOURCE ANALYSIS (STAGE 6.7)

**Status**: Verified Qiskit Circuit Synthesis & Gate Structure Analysis  
**Date**: 2026-08-19  

---

## 1. Circuit Resource Scaling by Grid & Degree

| Grid | Degree ($d$) | Qubits | Circuit Depth | Phase Rotations ($R_z$) | Block Encodings ($U_A$) | Est. 2Q CX Gates | Compilation (ms) | Classification |
| :--- | :--- | :--- | :--- | :--- | :--- | :--- | :--- | :--- |
| **$1 \times 1$** | 3 | 10 | 6 | 3 | 2 | 36 | 217.1 | **MEASURED** |
| **$1 \times 1$** | 5 | 10 | 10 | 5 | 3 | 54 | 244.1 | **MEASURED** |
| **$1 \times 1$** | 7 | 10 | 14 | 7 | 4 | 72 | 280.6 | **MEASURED** |
| **$1 \times 1$** | 11 | 10 | 22 | 11 | 6 | 108 | 255.5 | **MEASURED** |
| **$1 \times 1$** | 15 | 10 | 30 | 15 | 8 | 144 | 208.7 | **MEASURED** |
| **$1 \times 1$** | 21 | 10 | 42 | 21 | 11 | 198 | 270.0 | **MEASURED** |
| **$1 \times 1$** | 31 | 10 | 62 | 31 | 16 | 288 | 262.4 | **MEASURED** |
| **$2 \times 1$** | 7 | 11 | 14 | 7 | 4 | 80 | 1004.1 | **MEASURED** |
| **$2 \times 1$** | 15 | 11 | 30 | 15 | 8 | 160 | 998.1 | **MEASURED** |
| **$4 \times 2$** | 15 | 13 | 30 | 15 | 8 | 192 | 62286.5 | **MEASURED** |

---

## 2. Key Findings
1. **Linear Depth Scaling**:
   QSVT circuit depth scales strictly linearly with polynomial degree: $\text{Depth}(d) = 2d$.
2. **Phase Rotation Counts**:
   Number of single-qubit $R_z(2\phi_j)$ rotation gates is identically equal to polynomial degree $d$.
3. **Block Encoding Invocations**:
   The block-encoding unitary $U_A$ is queried $\lfloor d/2 \rfloor + 1$ times per QSVT inversion step.
