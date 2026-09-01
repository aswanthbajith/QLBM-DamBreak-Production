# STAGE 7: FORENSIC ADVERSARIAL FAILURES & LIMITATIONS REPORT

**Auditor Role**: Independent Adversarial Scientific Auditor  
**Date**: 2026-08-19  
**Repository**: `/home/aswa/Research/QLBM-DamBreak/`  

---

## Executive Summary of Adversarial Findings

This report documents all **mathematical impossibilities, algorithmic bottlenecks, physical simplifications, and validation circularities** identified during the clean-room Stage 7 adversarial audit of the Quantum Lattice Boltzmann Method (QLBM) two-phase dam-break solver pipeline.

While the core quantum linear algebra pipeline (CS/Halmos block encoding, QSVT Chebyshev polynomial inversion, Carleman $342N$ dimension scaling, and $1/\sqrt{N_s}$ shot-noise scaling) is computationally and numerically robust on constant-density models, several key theoretical and physical claims in earlier stages fail adversarial falsification or require strict scientific boundaries.

---

## 1. Mathematical Failure: Non-Polynomiality of Variable-Density Two-Phase LBM (Claim CLM-006)
* **Status**: **FAIL**
* **Claimed**: "Exact cubic polynomial closure ($p=3$) for two-phase variable-density Lattice Boltzmann fluid dynamics."
* **Forensic Reality**:
  1. **Counter-Gradient Interface Flux Normal**:
     $$\mathbf{n} = \frac{\nabla \phi}{|\nabla \phi| + \epsilon} = \frac{\nabla \phi}{\sqrt{(\partial_x \phi)^2 + (\partial_y \phi)^2 + \epsilon}}$$
     The Euclidean normalization contains a non-polynomial square root and division. No finite-degree polynomialization ($p=2$ or $p=3$) can represent this term exactly without truncation or an infinite Taylor series.
  2. **Chemical Potential & Surface Tension**:
     $$\mu_\phi = 4 \beta \phi (1 - \phi)(\phi - 0.5) - \kappa_c \nabla^2 \phi$$
     The surface tension force $\mathbf{F}_s = \mu_\phi \nabla \phi$ involves cubic terms $\phi^3 \nabla \phi$, which produces degree-4 monomials when expanded into momentum transport.
  3. **Implemented Code Truth**:
     The implemented quantum matrix model in `quantum/carleman_lbm.py` deliberately bypasses these terms by setting $\rho_0 = 1.0$, $\tau_v = \text{const}$, and discarding counter-gradient normal division. The matrix pipeline represents a *constant-density single-relaxation-time surrogate*, not the full variable-density Navier-Stokes + Allen-Cahn system.

---

## 2. Algorithmic Failure: Divergence of Static Newton-Raphson Reciprocal Closure (Claim CLM-007)
* **Status**: **NEEDS CORRECTION / FAIL AT HIGH DENSITY RATIOS**
* **Claimed**: "Reciprocal density $\xi = 1/\rho$ is dynamically closed via Newton-Raphson iterations $\xi_{k+1} = \xi_k(2 - \rho \xi_k)$."
* **Forensic Reality**:
  * The basin of attraction for $f(\xi) = 1/\xi - \rho = 0$ requires:
    $$0 < \xi_0 < \frac{2}{\rho}$$
  * For water-air ($\rho_L/\rho_G = 1000$), $\xi_0$ must satisfy $\xi_0 < 0.002$.
  * If initialized with static $\xi_0 = 1.0$:
    * At $\rho = 10$: Iteration 1 relative error is $8.1 \times 10^1$; Iteration 3 relative error is $4.3 \times 10^7$ (divergent).
    * At $\rho = 1000$: Iteration 3 relative error reaches $9.92 \times 10^{23}$ (catastrophic divergence).
  * **Correction Required**: Reciprocal density lifting cannot use static initialization; it requires dynamic multi-scale scaling $\xi_0 = 1 / \rho_{\text{local}}$ or log-density coordinate transformation.

---

## 3. Physical Failure: Quadratic Streaming Shear Truncation (Claim CLM-009)
* **Status**: **PARTIALLY VERIFIED**
* **Claimed**: "Streaming permutation $S_{\text{kron2}}$ exactly shifts quadratic state $\Psi \otimes \Psi$ across lattice nodes."
* **Forensic Reality**:
  * Exact two-point streaming for $g_{q1}(\mathbf{x} + \mathbf{c}_{q1}) g_{q2}(\mathbf{x} + \mathbf{c}_{q2})$ requires shifting indices to two distinct spatial locations when $\mathbf{c}_{q1} \ne \mathbf{c}_{q2}$, exploding the state dimension to $(18N)^2 = 324 N^2$.
  * To preserve the local dimension $342N$, `carleman_lbm.py` applies streaming using only the primary directional velocity $\mathbf{c}_{q1}$:
    $$S_{\text{kron2}}(k, \mathbf{x}) \to k(\text{target}), \mathbf{x} + \mathbf{c}_{q1}$$
  * This is an advective shear approximation that discards cross-directional momentum advection, introducing an invariant manifold defect of $\sim 10-13\%$ over 200 steps.

---

## 4. Execution Failure: Circuit Synthesis vs. Numerical Solver Separation (Claim CLM-014)
* **Status**: **PARTIALLY VERIFIED**
* **Claimed**: "Multi-step end-to-end dam-break simulation executed on quantum circuits."
* **Forensic Reality**:
  * The repository correctly synthesizes Qiskit `QuantumCircuit` objects (depth 30, 31 gates) for gate count, ancilla, and depth metrics.
  * However, the actual multi-step numerical time evolution in `dam_break_qlbm_sim.py` executes via classical SVD functional calculus (`A_inv_approx @ rhs`).
  * Simulating 13+ qubits with full multi-step circuit statevectors on classical hardware would be exponentially prohibitive ($2^{13} = 8192$ states per step). The solver is therefore a *verified hybrid classical-quantum emulator*.

---

## 5. Complexity Failure: Fallacy of Exponential Flow-Field Speedup (Claim CLM-018)
* **Status**: **FAIL**
* **Claimed**: "Quantum algorithm achieves exponential computational speedup over classical Navier-Stokes solvers."
* **Forensic Reality**:
  1. **Quantum Readout Bottleneck (Holevo / Tomography Bound)**:
     Extracting the full $N$-point velocity field $\mathbf{u}(\mathbf{x})$ and phase field $\phi(\mathbf{x})$ requires quantum state tomography with $\mathcal{O}(N \log N / \epsilon^2)$ measurements, completely destroying any quantum speedup for dense flow fields.
  2. **Surviving Quantum Advantage**:
     Quantum speedup is strictly limited to **global scalar observables** (e.g., total kinetic energy, total liquid mass, average wall impact force) extractable via Quantum Amplitude Estimation in $\mathcal{O}(1/\epsilon)$ queries versus $\mathcal{O}(1/\epsilon^2)$ classical Monte Carlo sampling.
