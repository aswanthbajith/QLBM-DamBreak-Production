# ASYMPTOTIC COMPLEXITY & SCALING ANALYSIS: TWO-PHASE QLBM

This document presents a rigorous complexity analysis and lattice-size scaling comparison for the Two-Phase D2Q9 Quantum Lattice Boltzmann solver.

---

## 1. Asymptotic Resource Scaling Formulation

Let $N = N_x \times N_y$ denote the total number of spatial lattice nodes.

| Algorithmic Stage | Classical LBM | Hybrid Carleman QLBM | End-to-End Quantum LBM |
| :--- | :---: | :---: | :---: |
| **State Encoding** | $O(N)$ memory | $O(N)$ memory | $O(\log N)$ qubits ($2^n = 32 N$) |
| **Collision Step** | $O(N)$ floating-point ops | $O(N \cdot 2^{10})$ statevector | $O(N \cdot \text{poly}(\log d))$ or multiplexed |
| **Gravitational Forcing** | $O(N)$ floating-point ops | $O(N)$ operations | $O(\text{poly}(\log N))$ |
| **Spatial Streaming** | $O(N)$ array shifts | $O(N)$ permutation | $O(\log N)$ modular additions |
| **Boundary Bounce-Back** | $O(\sqrt{N})$ perimeter ops | $O(\sqrt{N})$ reflections | $O(\log N)$ controlled swaps |
| **Observable Extraction** | $O(N)$ reductions | $O(N)$ reductions | $O(\frac{1}{\epsilon^2})$ shots or $O(\frac{1}{\epsilon})$ QAE |

---

## 2. Lattice Size Scaling ($4 \times 4$, $8 \times 8$, $16 \times 16$)

| Parameter | $4 \times 4$ Lattice | $8 \times 8$ Lattice | $16 \times 16$ Lattice |
| :--- | :---: | :---: | :---: |
| **Total Physical Nodes ($N$)** | 16 | 64 | 256 |
| **Total Physical Distributions ($18 N$)** | 288 | 1,152 | 4,608 |
| **Position Qubits ($n_{qx} + n_{qy}$)** | $2 + 2 = 4$ | $3 + 3 = 6$ | $4 + 4 = 8$ |
| **Velocity Qubits ($n_{qvel}$)** | 4 | 4 | 4 |
| **Selector Qubits ($n_{qsel}$)** | 1 | 1 | 1 |
| **Total Logical System Qubits** | **9 qubits** | **11 qubits** | **13 qubits** |
| **Block-Encoding Ancilla Qubits** | 1 | 1 | 1 |
| **Total Register Size (with Ancilla)** | **10 qubits** | **12 qubits** | **14 qubits** |
| **Full Hilbert Space Dimension** | $2^9 = 512$ | $2^{11} = 2,048$ | $2^{13} = 8,192$ |
| **Postselection Scaling Factor ($\alpha$)** | $\sim 58.75$ | $\sim 58.75$ | $\sim 58.75$ |
| **Success Probability ($P_{\text{succ}} \approx \alpha^{-2}$)** | $\approx 2.1 \times 10^{-3}$ | $\approx 2.1 \times 10^{-3}$ | $\approx 2.1 \times 10^{-3}$ |

---

## 3. Analysis of Bottlenecks and Advantages

1. **Logarithmic State Space Compression**:
   The entire physical fluid state of $18 N$ populations is compressed into $n = \log_2 N + 5$ qubits. For a large $256 \times 256$ grid ($N = 65,536$), the system requires only 21 logical qubits ($16 + 4 + 1$).
2. **Spatial Transport Advantage**:
   Streaming and boundary wall reflections scale as $O(\log N)$ quantum gate operations compared to $O(N)$ classical array indexing.
3. **Block-Encoding Postselection Overhead**:
   Because the local second-order Carleman operator has spectral norm $\|\widetilde{A}\|_2 \approx 58$, the postselection probability is $P_{\text{succ}} \approx 10^{-3}$ per block-encoded step. In asymptotic fault-tolerant architectures, this overhead is suppressed quadratically via Oblivious Amplitude Amplification (OAA) using $\sim \alpha$ rounds of quantum walk reflection.
