# RESEARCH UPGRADE AUDIT: QUANTUM TWO-PHASE DAM-BREAK IMPLEMENTATION

**Date**: 2026-08-25  
**Author**: Lead Quantum-CFD Implementation Specialist  
**Repository**: `/home/aswa/Research/QLBM-DamBreak/`  

---

## 1. Executive Summary

This forensic audit evaluates the pre-existing QLBM codebase to determine the mathematical completeness, approximation levels, placeholder components, hybrid elements, and genuine quantum operations within the two-phase dam-break solver.

The repository features a functional classical foundation (D2Q9 lattice, BGK collision, half-way bounce-back, Allen-Cahn interface capturing) and a preliminary 9-qubit quantum pipeline ($2_x + 2_y + 4_{\text{vel}} + 1_{\text{phase}}$). However, a deep diagnostic reveals several critical deficiencies that previously led to large relative errors (43–57% in density, 81–96% in phase field):

1. **Amplitude vs. Probability Mismatch**: The original encoding used $A(x,y,i) = \sqrt{\phi} f_i$ instead of normalized square-root population distributions $A(x,y,i) = \sqrt{\phi f_i / Z}$, resulting in probability distributions proportional to $f_i^2$ rather than $f_i$.
2. **Heuristic Collision Circuit**: The collision circuit used a 3-gate heuristic rotation (`Ry(0.6435)`, `Rz(0.45)`, `Rz(0.25)`) instead of an exact unitary derived from the physical BGK collision matrix $M = I - \omega(I - M_{\text{eq}})$ or Local Carleman relaxation.
3. **Streaming Simplification**: The multi-step quantum streaming in `quantum/two_phase_step.py` reduced D2Q9 streaming to 2 global CNOTs instead of using the fully verified $\mathcal{O}(\log N)$ coordinate shift permutation oracles available in `PHASE11_STREAMING_ORACLE.py`.
4. **Boundary Simplification**: The boundary condition applied global velocity-qubit flips rather than spatially conditioned reflections at domain wall coordinates.

---

## 2. Component-by-Component Scientific Audit

| Module / Component | Mathematical Status | Approximation Level | Quantum / Classical Status | Reusability | Action Required |
| :--- | :--- | :--- | :--- | :--- | :--- |
| `classical/d2q9.py` | Complete | Exact lattice vectors & weights | Pure Classical | 100% Reusable | Keep intact as core D2Q9 definition. |
| `classical/equilibrium.py` | Complete | Second-order BGK polynomial | Pure Classical | 100% Reusable | Keep intact. |
| `classical/collision.py` | Complete | Single-relaxation-time (SRT) BGK | Pure Classical | 100% Reusable | Keep intact. |
| `classical/streaming.py` | Complete | Periodic spatial rolls | Pure Classical | 100% Reusable | Keep intact. |
| `classical/boundary.py` | Complete | Half-way bounce-back enclosure | Pure Classical | 100% Reusable | Keep intact. |
| `classical/phase_field.py` | Partially Modular | Conservative Allen-Cahn | Pure Classical | 90% Reusable | Standardize functional API (`compute_phase_gradient`, `compute_phase_laplacian`, `validate_phase_field`). |
| `classical/two_phase.py` | Complete | Coupled BGK + Phase advection | Pure Classical | 95% Reusable | Align with formal reduced model API (`initialize_two_phase_dambreak`, `step`, `run`). |
| `carleman/` | Complete | Global & Local Carleman lifting | Mathematical / Operator | 100% Reusable | Reference for local collision unitary embedding. |
| `quantum/two_phase_encoding.py` | Inconsistent Normalization | Heuristic amplitude scaling | Genuinely Quantum | 60% Reusable | Upgrade to exact square-root amplitude encoding $A = \sqrt{f/Z}$ with $L_2 < 10^{-10}$ reconstruction. |
| `quantum/two_phase_collision.py` | Placeholder / Heuristic | Arbitrary rotation angles | Genuinely Quantum | 20% Reusable | Replace with mathematically derived local collision unitary $U_{\text{coll}} = \exp(-i H \Delta t)$. |
| `quantum/two_phase_boundary.py` | Unconditioned | Global bit flips | Genuinely Quantum | 30% Reusable | Condition reflections on spatial boundary registers. |
| `quantum/streaming.py` | Complete | Reversible $\mathcal{O}(\log N)$ permutations | Genuinely Quantum | 100% Reusable | Directly integrate into the two-phase pipeline. |
| `quantum/two_phase_step.py` | Mixed / Incomplete | Simplified streaming & boundary | Hybrid Quantum-Classical | 70% Reusable | Connect exact collision, streaming, boundary, and unbiased observable reconstruction. |
| `backends/` | Complete | Aer, Noisy, Fake IBM, IBM Runtime | Quantum Infrastructure | 100% Reusable | Ensure `SamplerV2` and ISA pass manager integration. |

---

## 3. Forensic Analysis of Previous Numerical Discrepancies

* **Initial Density Error ($t=0$)**: Was previously $> 25\%$ due to calculating $\rho = \sum P$ where $P \propto f_i^2$, distorting the spatial density gradient across the liquid-gas interface.
* **Phase Error ($t=0$)**: Was previously $> 40\%$ due to measuring $\phi = P(\text{phase}=1) / \rho$ without accounting for the nonlinear square of populations.
* **Evolution Drift ($t > 0$)**: Incoherent rotation angles in `quantum/two_phase_collision.py` rotated populations into unphysical states, causing loss of momentum and artificial phase diffusion.

---

## 4. Hardware Limitations & NISQ Boundaries

1. **Eagle-127 Topology**: Heavy-Hex qubit connectivity requires routing overhead (SWAP insertions) during transpilation.
2. **Coherence Decay**: On unencoded physical qubits ($T_1 \approx 150-300\,\mu\text{s}$, $T_2 \approx 100-200\,\mu\text{s}$), two-qubit gate errors ($5\times 10^{-3}$ per CX/ECR) limit the coherent circuit depth to $\approx 30-50$ two-qubit gates before the output approaches a maximally mixed state.
3. **Safety Interlock**: Cloud execution must remain strictly dual-locked (`QLBM_ENABLE_REAL_QPU=1` and `QLBM_CONFIRM_REAL_QPU=YES`) with explicit credential checking.
