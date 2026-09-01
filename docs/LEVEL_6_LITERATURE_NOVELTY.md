# LEVEL-6: LITERATURE POSITIONING & SCIENTIFIC NOVELTY ANALYSIS

This document establishes the exact boundary between existing peer-reviewed literature and the novel contributions of the Level-6 Two-Phase QLBM architecture.

---

## 1. Direct Comparison Against Prior Art

| Prior Work / Reference | Scope & Fluid Physics | Methodological Approach | Key Limitations in Prior Art | Level-6 Advancement |
| :--- | :--- | :--- | :--- | :--- |
| **arXiv 2605.28135** (May 2026) | Single-Phase Obstacle Flow | Global Carleman + QSVT | Restricted to single-phase weakly-compressible flow; no phase boundary; no surface tension. | **Coupled Two-Phase Extension**: Formulates coupled hydrodynamic $f_i$ + phase-field $g_i$ state with density and viscosity contrast. |
| **PRE 113, 035307 / arXiv 2511.13072** (Nov 2025 / 2026) | Single-Phase Nonlinear Fluid | Local Carleman Linearization | Single-component fluid; no interface capturing; no multiphase body forces. | **Multi-Species Carleman Tensor**: Constructs coupled $18\times 324$ bilinear interaction tensor $E_2^{(g)}$ for phase advection. |
| **CPC 321, 110040** (2026) | Linear Advection-Diffusion | Measurement-Free QLBM | Strictly linear PDEs; no non-linear Navier-Stokes convective terms. | **Non-Linear Convective Extension**: Handles non-linear momentum convection $\rho u_a u_b$ and phase dynamics via second-order Carleman. |
| **Lăcătuş & Möller (2025/2026)** | Single-Phase LBM Collision | Surrogate Quantum Circuits | Heuristic neural/polynomial surrogate circuits without formal Carleman convergence bounds. | **Rigorously Derived Carleman Matrices**: Fully traceable, deterministic Sz.-Nagy block-encoding with machine-precision dilation. |

---

## 2. Summary of Genuinely Novel Scientific Contributions

1. **First Coupled Two-Phase Carleman Linearization**: Derivation of the exact second-order Carleman interaction matrices ($M_1 \in \mathbb{R}^{18\times 18}, M_2 \in \mathbb{R}^{18\times 324}$) coupling Navier-Stokes momentum to conservative phase-field interface capturing.
2. **First Multi-Timestep Local Carleman Operator for Multi-Phase Flow**: Formulation of lifted streaming ($S \otimes S$) and boundary reflection ($B \otimes B$) acting coherently on coupled hydrodynamic-phase tensor states.
3. **First Comprehensive Dam-Break Physical Benchmark Comparison**: Grounding the quantum Carleman error budget against the Martin & Moyce (1952) experimental surge front and column collapse dataset.
