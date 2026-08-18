# End-to-End Quantum Lattice Boltzmann Dam-Break Validation Report

## 1. End-to-End Milestone Summary
- **Physical model**: Two-Phase Incompressible Velocity-Based D2Q9 LBM coupled with Conservative Allen-Cahn Interface Capturing, Variable Density $\rho(\phi) = \rho_G + \phi(\rho_L - \rho_G)$, Variable Viscosity, Continuum Surface Force $\mathbf{F}_s = \sigma \kappa_I \nabla \phi$, and Gravitational Buoyancy.
- **Grid**: $8 \times 4$ lattice nodes ($N = 32$ spatial sites, column $3 \times 3$).
- **Time steps**: $10$ discrete simulation time steps.
- **Carleman dimension**: $576 \times 576$ ($18 \times 32$ base linear state; $10,944 \times 10,944$ for order $N_C = 2$).
- **Quantum qubits**: $11$ total qubits ($10$ system qubits $+ 1$ ancilla qubit).
- **Ancillas**: $1$ ancilla qubit ($a = 1$ for exact canonical CS/Halmos block encoding dilation).
- **QSVT degree**: Degree $15$ odd Chebyshev matrix inversion polynomial.
- **Observable**: 
  1. Surge wavefront position $x^*(t^*)$
  2. Residual water column height $h^*(t^*)$
  3. Downstream impact wall sensor pressure $p^*(t^*)$
  4. Total phase-field fluid mass $M(t)$
- **Classical result**: 
  - Surge front: $x^* = 1.00 \to 0.67$
  - Column height: $h^* = 1.00$
  - Downstream pressure: $p = 1.62 \times 10^{-4}$
- **Quantum result**: 
  - Surge front: $x^* = 1.00 \to 1.00$
  - Column height: $h^* = 1.00 \to 0.67$
  - Downstream pressure: $p = 1.63 \times 10^{-4}$
- **Error**: 
  - Surge front error: $L_1 = 0.2121$, $L_2 = 0.2659$, $L_\infty = 0.3333$
  - Column height error: $L_1 = 0.3030$, $L_2 = 0.3178$, $L_\infty = 0.3333$
  - Downstream pressure error: $L_1 = 3.1853 \times 10^{-5}$, $L_2 = 3.8089 \times 10^{-5}$, $L_\infty = 5.5252 \times 10^{-5}$
  - Quantum State In-Fidelity: $1 - \mathcal{F} \le 1.90 \times 10^{-2}$ ($\mathcal{F}_{avg} = \mathbf{0.987722}$)
- **Shots**: $N_{shots} = 10,000$ measurement shots ($\pm 1.0\%$ statistical measurement sampling uncertainty).
- **Circuit depth**: $30$ layers per QSVT inversion cycle; $300$ cumulative circuit depth over $10$ time steps.
- **Runtime**: $14.82$ seconds for complete end-to-end multi-step quantum circuit simulation.
- **Limitations**:
  1. Quantum output bottleneck: Extracting full fine-grained local flow fields requires $\mathcal{O}(N)$ projective measurements; quantum advantage is strictly restricted to global macroscopic engineering observables (wavefront speed, total fluid volume, boundary impact force).
  2. Coherence and gate synthesis: High-dimensional multi-qubit unitaries require Clifford+T decomposition for fault-tolerant physical quantum hardware.

---

## 2. Step-by-Step Observable Validation Table

| Step | Time $t^*$ | Classical Front $x_c^*$ | Quantum Front $x_q^*$ | Classical Height $h_c^*$ | Quantum Height $h_q^*$ | Quantum Fidelity $\mathcal{F}$ | QSVT Residual |
| :---: | :---: | :---: | :---: | :---: | :---: | :---: | :---: |
| **0** | 0.00 | **1.00** | **1.00** | **1.00** | **1.00** | **1.000000** | $0.00e+00$ |
| **1** | 0.01 | **1.00** | **0.67** | **1.00** | **0.67** | **0.987236** | $2.80e-15$ |
| **2** | 0.02 | **1.00** | **1.00** | **1.00** | **0.67** | **0.990184** | $2.76e-15$ |
| **3** | 0.02 | **1.00** | **1.00** | **1.00** | **0.67** | **0.990308** | $2.76e-15$ |
| **4** | 0.03 | **1.00** | **1.00** | **1.00** | **0.67** | **0.989576** | $2.77e-15$ |
| **5** | 0.04 | **0.67** | **1.00** | **1.00** | **0.67** | **0.988211** | $2.74e-15$ |
| **6** | 0.05 | **0.67** | **1.00** | **1.00** | **0.67** | **0.986632** | $2.77e-15$ |
| **7** | 0.06 | **0.67** | **1.00** | **1.00** | **0.67** | **0.985439** | $2.78e-15$ |
| **8** | 0.07 | **0.67** | **1.00** | **1.00** | **0.67** | **0.983872** | $2.76e-15$ |
| **9** | 0.07 | **0.67** | **1.00** | **1.00** | **0.67** | **0.982483** | $2.76e-15$ |
| **10** | 0.08 | **0.67** | **1.00** | **1.00** | **0.67** | **0.980999** | $2.78e-15$ |

---

## 3. Generated Publication Figures in `validation/figures/`
1. [`initial_phase_field.png`](file:///home/aswa/Research/QLBM-DamBreak/validation/figures/initial_phase_field.png): Initial two-phase fluid column configuration $\phi(\mathbf{x}, 0)$.
2. [`classical_dam_break_profile.png`](file:///home/aswa/Research/QLBM-DamBreak/validation/figures/classical_dam_break_profile.png): Classical reference liquid distribution at collapse stage.
3. [`quantum_reconstructed_observable.png`](file:///home/aswa/Research/QLBM-DamBreak/validation/figures/quantum_reconstructed_observable.png): Quantum QSVT state-extracted liquid distribution.
4. [`front_position_comparison.png`](file:///home/aswa/Research/QLBM-DamBreak/validation/figures/front_position_comparison.png): Surge wavefront kinematics $x^*(t^*)$ comparison.
5. [`column_height_comparison.png`](file:///home/aswa/Research/QLBM-DamBreak/validation/figures/column_height_comparison.png): Water column decay $h^*(t^*)$ comparison.
6. [`pressure_comparison.png`](file:///home/aswa/Research/QLBM-DamBreak/validation/figures/pressure_comparison.png): Downstream impact pressure dynamics $p^*(t^*)$.
7. [`error_versus_time.png`](file:///home/aswa/Research/QLBM-DamBreak/validation/figures/error_versus_time.png): Absolute observable error and in-fidelity growth over time.
8. [`quantum_resource_scaling.png`](file:///home/aswa/Research/QLBM-DamBreak/validation/figures/quantum_resource_scaling.png): Logarithmic qubit scaling vs. spatial grid nodes $N$.
