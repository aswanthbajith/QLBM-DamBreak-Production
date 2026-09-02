# QUANTUM TWO-PHASE DAM-BREAK LBM (QLBM)
## Phase 2: Reversible Quantum Arithmetic Streaming Implementation & Transpilation

**Document**: Gate-Level Arithmetic Streaming Circuits and Hardware Profiling  
**Repository**: `/home/aswa/Research/QLBM-DamBreak-Production`  
**Branch**: `feature/direct-encoding-two-phase-qlbm`  
**Date**: September 2026  

---

## 1. Mathematical Architecture

Reversible arithmetic streaming implements the conditional spatial translation:
$$|x\rangle |y\rangle |i\rangle |p\rangle \mapsto |(x + c_{ix}) \bmod N_x\rangle |(y + c_{iy}) \bmod N_y\rangle |i\rangle |p\rangle$$
using quantum logic gates (MCX, CX, X) without synthesizing arbitrary exponential matrix unitaries.

### Circuit Construction Principles:
1. **Velocity Decoding**: For each discrete velocity $i \in \{0, \dots, 8\}$, the 4-qubit velocity register $|i\rangle$ controls conditional addition/subtraction.
2. **Modular In-Place Coordinate Ripple Carry**:
   - For $n=1$ ($N=2$): Single CX/MCX flip on target coordinate qubit.
   - For $n=2$ ($N=4$): 2-bit ripple increment/decrement using chained multi-controlled X gates.
   - For general $n$: $n$-bit modular ripple-carry adder.
3. **Uncomputing Controls**: Velocity controls are inverted and uncomputed in place, restoring the velocity register with zero auxiliary ancilla footprint.

---

## 2. Experimental Verification & Hardware Profiling

Executing `scripts/run_arithmetic_streaming_validation.py`:

$$\begin{array}{|l|c|c|c|c|c|c|}
\hline
\textbf{Grid} & \textbf{Logical Qubits} & \mathbf{\|S_{\text{arith}} - S_{\text{mat}}\|_2} & \textbf{Transpiled Depth} & \textbf{Two-Qubit Gates} & \textbf{Total Gates} & \textbf{Transpile Time} \\
\hline
2 \times 2 & 7 & \mathbf{3.86 \times 10^{-14}} & \mathbf{604} & \mathbf{214 \text{ (CX)}} & 751 & 0.04\text{s} \\
4 \times 4 & 9 & \mathbf{9.92 \times 10^{-14}} & \mathbf{929} & \mathbf{362 \text{ (CX)}} & 1,291 & 0.10\text{s} \\
\hline
\end{array}$$

### Transpilation Backend:
- Target Backend: **IBM FakeSherbrooke (127Q Heavy-Hex ISA)**
- Basis Gates: `[ecr, id, rz, sx, x, reset]`
- Circuit Validation: Both $2\times 2$ and $4\times 4$ arithmetic circuits reproduce the exact unitary permutation matrix to machine precision ($< 10^{-13}$) while achieving low circuit depth ($< 1,000$).
