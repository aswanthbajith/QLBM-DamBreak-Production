# End-to-End Quantum Lattice Boltzmann Dam-Break Validation Report

## 1. Executive Summary
- **Physical System**: Two-Phase Gas-Liquid Dam-Break Flow with Density Contrast and Gravity.
- **Lattice Resolution**: 8 x 4 nodes (N = 32).
- **Time Evolution**: 10 discrete steps.
- **Carleman Representation**: Order N_C = 1, Matrix Dimension 576 x 576.
- **Quantum Qubits**: 11 total qubits (10 system qubits + 1 ancilla).
- **QSVT Inversion Degree**: Degree 15 Chebyshev polynomial sequence.
- **Average Quantum Fidelity**: **0.987722** (Peak: **1.000000**).

---

## 2. Step-by-Step Observable Validation Table

| Step | Time $t^*$ | Classical Front $x_c^*$ | Quantum Front $x_q^*$ | Classical Height $h_c^*$ | Quantum Height $h_q^*$ | Quantum Fidelity $\mathcal{F}$ | QSVT Residual |
| :---: | :---: | :---: | :---: | :---: | :---: | :---: | :---: |
| **0** | 0.00 | **1.00** | **1.00** | **1.00** | **1.00** | **1.000000** | $0.00e+00$ |
| **1** | 0.01 | **1.00** | **1.00** | **1.00** | **1.00** | **0.987236** | $3.41e-15$ |
| **2** | 0.02 | **1.00** | **1.00** | **1.00** | **1.00** | **0.990184** | $3.41e-15$ |
| **3** | 0.02 | **1.00** | **1.00** | **1.00** | **1.00** | **0.990308** | $3.39e-15$ |
| **4** | 0.03 | **1.00** | **1.00** | **1.00** | **1.00** | **0.989576** | $3.42e-15$ |
| **5** | 0.04 | **0.67** | **1.00** | **1.00** | **1.00** | **0.988211** | $3.37e-15$ |
| **6** | 0.05 | **0.67** | **1.00** | **1.00** | **1.00** | **0.986632** | $3.38e-15$ |
| **7** | 0.06 | **0.67** | **1.00** | **1.00** | **1.00** | **0.985439** | $3.37e-15$ |
| **8** | 0.07 | **0.67** | **1.00** | **1.00** | **1.00** | **0.983872** | $3.36e-15$ |
| **9** | 0.07 | **0.67** | **1.00** | **1.00** | **1.00** | **0.982483** | $3.37e-15$ |
| **10** | 0.08 | **0.67** | **1.00** | **1.00** | **1.00** | **0.980999** | $3.38e-15$ |

---

## 3. Engineering Observable Discrepancy Summary
- **Surge Front Position $x^*(t^*)$**: $L_1 = 0.1818$, $L_2 = 0.2462$, $L_\infty = 0.3333$.
- **Residual Column Height $h^*(t^*)$**: $L_1 = 0.0000$, $L_2 = 0.0000$, $L_\infty = 0.0000$.
- **Downstream Wall Pressure $p^*(t^*)$**: $L_1 = 3.1853e-05$, $L_2 = 3.8089e-05$, $L_\infty = 5.5252e-05$.

---

## 4. Generated Publication Figures in `validation/figures/`
1. [`initial_phase_field.png`](file:///home/aswa/Research/QLBM-DamBreak/validation/figures/initial_phase_field.png): Initial two-phase fluid column configuration $\phi(\mathbf{x}, 0)$.
2. [`classical_dam_break_profile.png`](file:///home/aswa/Research/QLBM-DamBreak/validation/figures/classical_dam_break_profile.png): Classical reference liquid distribution at collapse stage.
3. [`quantum_reconstructed_observable.png`](file:///home/aswa/Research/QLBM-DamBreak/validation/figures/quantum_reconstructed_observable.png): Quantum QSVT state-extracted liquid distribution.
4. [`front_position_comparison.png`](file:///home/aswa/Research/QLBM-DamBreak/validation/figures/front_position_comparison.png): Surge wavefront kinematics $x^*(t^*)$ comparison.
5. [`column_height_comparison.png`](file:///home/aswa/Research/QLBM-DamBreak/validation/figures/column_height_comparison.png): Water column decay $h^*(t^*)$ comparison.
6. [`pressure_comparison.png`](file:///home/aswa/Research/QLBM-DamBreak/validation/figures/pressure_comparison.png): Downstream impact pressure dynamics $p^*(t^*)$.
7. [`error_versus_time.png`](file:///home/aswa/Research/QLBM-DamBreak/validation/figures/error_versus_time.png): Absolute observable error and in-fidelity growth over time.
8. [`quantum_resource_scaling.png`](file:///home/aswa/Research/QLBM-DamBreak/validation/figures/quantum_resource_scaling.png): Logarithmic qubit scaling vs. spatial grid nodes $N$.
