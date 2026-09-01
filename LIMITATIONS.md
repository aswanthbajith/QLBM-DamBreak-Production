# THEORETICAL & COMPUTATIONAL LIMITATIONS: TWO-PHASE QLBM

This document provides a scientifically rigorous and transparent audit of the physical approximations, quantum overheads, and hardware limitations of the current Two-Phase D2Q9 Carleman Quantum Lattice Boltzmann implementation.

---

## 1. Carleman Linearization Truncation Error

* **Approximation**: The non-linear equilibrium distribution $f_i^{\text{eq}}(\rho, \mathbf{u})$ and phase equilibrium $g_i^{\text{eq}}(\phi, \mathbf{u})$ contain quadratic convective terms $\frac{\mathbf{u}\mathbf{u}}{\rho_0}$ and cross-terms $\frac{\phi \mathbf{u}}{\rho_0}$.
* **Second-Order Cutoff**: Cubic and higher-order velocity terms $O(\|\mathbf{u}\|^3)$ and compressibility corrections $O(\delta\rho^2)$ are truncated.
* **Closed-Carleman Truncation**: In autonomous closed Carleman evolution ($Y_{t+1} = C_2 Y_t$), the quadratic layer evolution truncates higher-order powers $\Psi^{\otimes 3}$ and $\Psi^{\otimes 4}$. Consequently, hybrid re-lifting (rebuilding $\mathbf{Y}_2 = [\Psi; \Psi \otimes \Psi]$ from physical populations) is required for multi-step stability.

---

## 2. Block-Encoding Postselection Overhead ($P_{\text{succ}}$)

* **Normalization Scalar**: The padded Carleman matrix $\widetilde{A} \in \mathbb{R}^{512 \times 512}$ has spectral norm $\|\widetilde{A}\|_2 \approx 58$.
* **Spectral Factor $\alpha$**: To ensure $\|\bar{A}\|_2 \le 1$ for Sz.-Nagy dilation, $\alpha \approx 58.75$ is required.
* **Success Probability**: Postselection onto ancilla $|0\rangle_{\text{anc}}$ succeeds with probability:
  $$P_{\text{succ}} = \frac{\|A_{\text{eval}} \mathbf{Y}_2\|_2^2}{\alpha^2 \|\mathbf{Y}_2\|_2^2} \approx 2.1 \times 10^{-3} \quad (t=1)$$
  $$P_{\text{succ}} \approx 1.0 \times 10^{-4} \quad (t=10)$$
* **Fault-Tolerant Resolution**: In asymptotic fault-tolerant architectures, this overhead is suppressed quadratically via Oblivious Amplitude Amplification (OAA), requiring $O(\alpha) \approx 58$ Grover-like reflection queries.

---

## 3. NISQ Hardware Bottlenecks & Gate Depths

* **Transpiled Depth on IBM 127Q Heavy-Hex**:
  * Logical depth: 6 gates.
  * Transpiled physical depth: **76,459 gates**.
  * Two-qubit CX/ECR gates: **21,133**.
* **Coherence Time Limit**: On current superconducting transmon QPUs (average $T_1, T_2 \approx 100-300\,\mu\text{s}$ and 2-qubit gate error rates $\sim 0.5\% - 1.0\%$), a circuit with $>20,000$ CX gates will decohere into statistical noise without quantum error correction.
* **Status**: Hardware execution has been **transpiled and simulated on fake backends, but not executed on physical cloud QPUs**.

---

## 4. Claim Audit Matrix

| Phrasing / Claim | Scientific Validity | Approved Thesis Statement |
| :--- | :---: | :--- |
| *"Closed Unitary Evolution of Global Lattice"* | ❌ False | **"Hybrid Quantum-Classical Carleman LBM with Observable Re-Encoding"** |
| *"Exponential Quantum Speedup on NISQ"* | ❌ False | **"Logarithmic state compression ($O(\log N)$ qubits) with polynomial collision circuit depth"** |
| *"Real IBM Hardware Demonstrator"* | ❌ False | **"Circuits compiled and transpiled to IBM 127Q Heavy-Hex ISA; verified in noise-free and noisy simulation"** |
| *"Strict Unitarity of Spatial Transport"* | ✅ True | **"Streaming permutation $S$ and boundary involution $B$ strictly satisfy $S^\dagger S = I_{512}$ and $B^2 = I_{512}$ on $\mathcal{H}_{512}$"** |
| *"Machine-Precision Single-Step Collision"* | ✅ True | **"Unitary dilation reproduces second-order Carleman map to $3.45 \times 10^{-16}$"** |

---

## 5. Final Implementation Level Classification

According to the 6-tier classification framework:

> **LEVEL 3: Quantum Subroutines Validated Inside LBM (Hybrid Carleman with Circuit Transpilation)**  
> *Reasoning*: The algorithm implements strictly unitary quantum subroutines (10-qubit block-encoded Carleman collision $U_C \in \mathbb{U}(1024)$, exact 512-dim streaming permutation $S$, exact 512-dim boundary involution $B$, and quantum observable estimation) within an authenticated simulation and heavy-hex transpilation pipeline.
