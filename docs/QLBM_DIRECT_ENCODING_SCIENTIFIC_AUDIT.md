# QUANTUM TWO-PHASE DAM-BREAK LBM (QLBM)
## Scientific Operation Audit & Component Decomposition Report

**Document**: Independent Scientific Operation & Architecture Audit  
**Repository**: `/home/aswa/Research/QLBM-DamBreak-Production`  
**Branch**: `feature/direct-encoding-two-phase-qlbm`  
**Date**: September 2026  

---

## 1. Executive Summary: Truth in Advertising

This independent audit establishes a rigorous distinction between the **genuinely quantum circuit operations** and the **classical numerical operations** in the Direct Spatial/Population Two-Phase QLBM prototype:

$$\mathbf{AUDIT\ VERDICT:\ YELLOW \ (Hybrid\ Quantum-Classical\ Architecture)}$$

1. **What is Genuinely Quantum**:
   - **Unified Quantum State Encoding**: Full lattice distribution embedded in the Hilbert space $\mathcal{H} = \mathcal{H}_x \otimes \mathcal{H}_y \otimes \mathcal{H}_{\text{vel}} \otimes \mathcal{H}_{\text{phase}}$.
   - **Unitary Spatial Streaming ($S$)**: Exact permutation operator and gate-level modular ripple-carry arithmetic circuits satisfying $S^\dagger S = I$ with zero tensor-shift distortion.
   - **Unitary Bounce-Back Involution ($B$)**: Exact reflection on solid wall nodes satisfying $B^\dagger B = I$ and $B^2 = I$.
2. **What Remains Classical**:
   - **Macroscopic Moments & Velocity**: $\rho(x,y) = \sum_i f_i$ and $\mathbf{u}(x,y) = \frac{\sum_i f_i \mathbf{c}_i + 0.5 \mathbf{F}}{\rho}$ are calculated classically on CPU.
   - **Nonlinear Maxwellian Equilibria ($f_i^{\text{eq}}, g_i^{\text{eq}}$)**: Evaluated classically using standard BGK polynomials.
   - **Brackbill CSF Surface Tension**: Curvature $\kappa = -\nabla\cdot\mathbf{n}$ and $\mathbf{F}_s = \sigma \kappa \nabla\alpha$ are evaluated classically using central differences.
   - **Collision Step**: In `direct_two_phase_prototype.py`, collision is executed via classical BGK relaxation on CPU and re-encoded into the statevector.
3. **Scientific Significance of Machine-Precision Agreement**:
   - The reported agreement ($< 10^{-14}$ vs Level 4) is **numerically valid** because streaming and boundary conditions are exact quantum permutations, while collision executes the exact Level 4 formulas.
   - It is a **Hybrid Quantum-Classical (HQC) algorithm**, NOT a fully autonomous measurement-free quantum solver.

---

## 2. Operation-by-Operation Audit Table

| Operation | Implementation | Quantum? | Classical? | Role | Scientific Classification |
| :--- | :--- | :---: | :---: | :--- | :--- |
| **State Preparation & Normalization** | `encode_state()` | Statevector Init | Amplitude Loading | Maps $f_i, g_i \to |\Psi\rangle$ | **Hybrid Initialization** |
| **Spatial Streaming** | `apply_quantum_streaming()` / `build_direct_streaming_circuit()` | **YES ($S^\dagger S = I$)** | NO | Shifts $|x,y\rangle$ by $\mathbf{c}_i$ | **Genuinely Quantum Unitary Permutation** |
| **Bounce-Back Wall Boundary** | `apply_quantum_boundary()` / `build_direct_boundary_circuit()` | **YES ($B^2 = I$)** | NO | Reflects $i \to \text{opp}(i)$ | **Genuinely Quantum Unitary Involution** |
| **Macroscopic Moments** | `decode_state()` $\to \rho, \alpha$ | Contraction | Summation | Decodes $\rho(x,y), \alpha(x,y)$ | **Classical Decoding / Measurement** |
| **Shifted Velocity** | $\mathbf{u} = (\sum f_i \mathbf{c}_i + 0.5 \mathbf{F})/\rho$ | NO | Arithmetic | Momentum division | **Classical Numerical Operation** |
| **Brackbill CSF Surface Tension** | `compute_surface_tension_force()` | NO | Finite Difference | $\mathbf{F}_s = \sigma \kappa \nabla\alpha$ | **Classical Hybrid Feedback** |
| **Gravitational Buoyancy** | `compute_total_force()` | NO | Parameter Eval | $(\rho - \rho_G) \mathbf{g}$ | **Classical Forcing Input** |
| **Equilibria $f^{\text{eq}}, g^{\text{eq}}$** | `compute_equilibrium()` | NO | Maxwellian | Target state | **Classical Numerical Evaluation** |
| **Collision Update** | `execute_collision_step()` | NO | BGK Relaxation | Relaxes populations | **Classical Update in Hybrid Loop** |

---

## 3. Controlled Validation Experiments (Tests A, B, C)

1. **Test A (Full Pipeline vs Level 4)**: Maximum population error $< 3.75 \times 10^{-15}$ across 10 timesteps on $2\times 2$ grid.
2. **Test B (Quantum Streaming Only with Exact Classical Collision)**: Isolating quantum streaming $S$ against classical `stream()` yields error $< 10^{-14}$, proving that quantum streaming is an exact unitary representation of physical D2Q9 advection.
3. **Test C (Subspace Non-Contamination)**: Proves that zero amplitude leaks into idle velocity states $|9\rangle \dots |15\rangle$ ($< 10^{-15}$ leakage probability).
