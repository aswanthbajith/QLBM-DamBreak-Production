# QUANTUM LATTICE BOLTZMANN METHOD (QLBM)
## Candidate Architecture Benchmark & Decision Matrix (14 Criteria)

**Document**: Comprehensive Scientific Evaluation of QLBM Solver Candidates  
**Repository**: `/home/aswa/Research/QLBM-DamBreak-Production`  
**Branch**: `feature/direct-encoding-two-phase-qlbm`  
**Date**: September 2026  

---

## 1. Candidate Architecture Descriptions

- **Candidate A (Carleman Lifted Tensor — Level 6B/7)**: Local 342-dim second-order polynomial state with 10-qubit Sz.-Nagy unitary dilation block encoding.
- **Candidate B (Direct Spatial/Population Quantum State — Level 8 Target)**: Global lattice distribution encoded directly across coordinate, velocity, and phase registers ($n_x + n_y + 5$ qubits).
- **Candidate C (Coherent Quantum Arithmetic / QROM Fluid Solver)**: Fully coherent register arithmetic for density division, velocity, and equilibrium calculation.
- **Candidate D (Hybrid Quantum Streaming & Collision with Classical CSF Feedback)**: Unified direct state encoding with coherent quantum streaming and boundary involution coupled with hybrid parameter feedback for surface tension.

---

## 2. Master 14-Criterion Comparative Benchmark Table

| Benchmark Criterion | Candidate A: Carleman Lifted Tensor | Candidate B: Direct Spatial State | Candidate C: Quantum Arithmetic | Candidate D: Hybrid Streaming/Collision |
| :--- | :--- | :--- | :--- | :--- |
| **1. Physics Fidelity** | Weakly-compressible; $\text{Ma} \le 0.10$; $\mathcal{O}(\text{Ma}^2)$ truncation error | Full 2-phase D2Q9; density & viscosity contrast; buoyancy & CSF | Exact polynomial / rational arithmetic on quantum registers | Validated D2Q9 2-phase dam break (Martin & Moyce $< 7\%$) |
| **2. Quantum Fidelity** | Projected block encoding (ancilla resets required at each step) | Strictly unitary streaming $S$ ($S^\dagger S = I$) and boundary $B$ ($B^2 = I$) | High theoretical coherence; immense Toffoli gate depth | Unitary quantum streaming + boundary + block-encoded collision |
| **3. Multi-Step Capability** | Supported via projective resets; diverges exponentially without resets | Supported with machine-precision streaming & boundary propagation | Theoretically autonomous; untested due to circuit depth | Supported across arbitrary multi-step timelines with bounded mass drift |
| **4. Qubit Requirements** | 21 Logical Qubits ($128\times 64$ grid) | **18 Logical Qubits** ($128\times 64$ grid); **7 Qubits** ($2\times 2$) | $> 100$ Logical Qubits per node (floating-point registers) | **18 Logical Qubits** ($128\times 64$ grid) |
| **5. Circuit Depth** | $> 3.76\text{M}$ per unamplified block; $> 56\text{M}$ with OAA | **$\approx 10,099$ for $2\times 2$**; $\mathcal{O}(\text{polylog } N)$ with adders | $> 10^9$ Toffoli depth for non-local stencils | Moderately deep (transpiled within FTQC limits) |
| **6. Gate Count** | $> 831\text{k}$ 2Q ECR gates per collision block | **2,700 2Q CX gates** on $2\times 2$ Heavy-Hex backend | $> 10^{10}$ fault-tolerant T-gates | Scales efficiently with lattice node count |
| **7. State-Prep Cost** | $\mathcal{O}(N)$ local node amplitude loading | $\mathcal{O}(N \cdot Q \cdot P)$ global amplitude initialization | $\mathcal{O}(\text{polylog } N)$ with QROM / qRAM | Amortized across multi-step execution |
| **8. Measurement Cost** | $\mathcal{O}(N/\epsilon^2)$ per step or block | $\mathcal{O}(1/\epsilon^2)$ sampling for macroscopic observables | Readout only at final timestep | Hybrid feedback measurement every $K$ timesteps |
| **9. CSF Surface Tension** | Classical hybrid feedback every $K$ steps | Hybrid classical CSF or quantum stencil evaluation | Fully quantum curvature & gradient stencils | Classical / hybrid Brackbill CSF feedback |
| **10. Hardware Feasibility** | FTQC Logical only (NOT NISQ-viable) | Early-to-mid FTQC; transpilation demonstrated | Late-stage Fault-Tolerant FTQC only | Early FTQC / Emulated hybrid QPUs |
| **11. Scalability** | Logarithmic registers, but deep local collision circuit | $\mathcal{O}(\log(N_x N_y))$ spatial qubits; unitary streaming | Logarithmic spatial scaling, but astronomical constant factors | $\mathcal{O}(\log N)$ spatial registers with modular execution |
| **12. Validation Error** | $< 6\%$ surge-front error vs Martin & Moyce | **$< 10^{-13}$ vs Level 4 reference** across multi-step evolution | Untested numerically due to gate count complexity | $< 1.53\%$ liquid mass drift; exact agreement |
| **13. Tensor Streaming** | **Vulnerable under $S\otimes S$ ($419.5\%$ error)** | **Completely Immune** (exact linear permutation $S$) | Immune if implemented in direct basis | **Completely Immune** via direct population basis |
| **14. Main Limitation** | Defect leakage under unprojected multiplication ($2098\%$) | Nonlinear macroscopic collision requires block-encoded map | Astronomical T-gate depth ($> 50\text{k}$ Toffolis per node) | Intermediate classical feedback for curvature |

---

## 3. Scientific Recommendation

$$\mathbf{PRIMARY\ ARCHITECTURAL\ RECOMMENDATION:\ CANDIDATE\ B\ /\ CANDIDATE\ D}$$
The **Direct Spatial/Population Quantum State Encoding (Candidate B / D)** represents the most mathematically robust, scalable, and physically sound foundation for the Quantum Two-Phase Dam-Break Lattice Boltzmann Method. It completely eliminates the spatial tensor streaming breakdown while reducing 2-qubit gate overhead by several orders of magnitude.
