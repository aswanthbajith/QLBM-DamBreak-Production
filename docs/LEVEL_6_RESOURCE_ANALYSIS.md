# LEVEL-6: QUANTUM RESOURCE SCALING & HARDWARE OVERHEAD ANALYSIS

**Data Reference**: [`results/level6_resource_estimates.csv`](file:///home/aswa/Research/QLBM-DamBreak-Production/results/level6_resource_estimates.csv)  
**Objective**: Comparative resource scaling of Architecture A (HQC), Architecture B (Local Carleman), and Architecture C (Global QSVT) across grid resolutions and timesteps.

---

## 1. Qubit & Space Complexity Comparison

| Mesh Size | Spatial Nodes ($N$) | Physical Carleman State Dim ($342 N$) | Arch A (HQC) Qubits | Arch B (Local Carleman) Qubits | Arch C (Global QSVT, $N_t=10$) Qubits |
| :---: | :---: | :---: | :---: | :---: | :---: |
| **$4 \times 4$** | 16 | 5,472 | 10 | 16 | 20 |
| **$8 \times 8$** | 64 | 21,888 | 12 | 18 | 22 |
| **$16 \times 16$** | 256 | 87,552 | 14 | 20 | 24 |
| **$32 \times 16$** | 512 | 175,104 | 15 | 21 | 25 |
| **$64 \times 32$** | 2,048 | 700,416 | 17 | 23 | 27 |
| **$128 \times 64$** | 8,192 | 2,801,664 | 19 | 25 | 29 |

---

## 2. Dominant Scaling Bottlenecks by Architecture

1. **Architecture A (HQC)**:
   - *Bottleneck*: **Tomographic Measurement & State Preparation Overhead** ($\mathcal{O}(N_t \cdot N)$ classical-quantum handoffs).
   - *Feasibility*: NISQ / Near-Term (runs today on emulators / small QPUs).
2. **Architecture B (Local Carleman Multi-Timestep)**:
   - *Bottleneck*: **Dilation Normalization Compounding** ($\alpha_C^K \approx 5.32^K$). Requires Oblivious Amplitude Amplification (OAA) for $K \ge 3$.
   - *Feasibility*: Early Fault-Tolerant Quantum Computing (FTQC) with $K = 2 \dots 4$.
3. **Architecture C (Global Carleman + QSVT)**:
   - *Bottleneck*: **Total Oracle Query Depth & Non-linear Dynamic Forcing Incompatibility**.
   - *Feasibility*: Mature FTQC with millions of physical qubits and logical surface codes.
