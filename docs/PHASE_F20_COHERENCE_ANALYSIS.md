# PHASE F20: COHERENCE PRESERVATION & SUPERPOSITION ANALYSIS

## 1. Executive Summary
This document presents the definitive density-matrix experiments testing coherence preservation under the three critical superposition classes:
- **Case A**: Superposition of states sharing the same non-equilibrium sector.
- **Case B**: Superposition of states in different non-equilibrium sectors.
- **Case C**: Superposition of states with identical macroscopic hydrodynamics but different kinetic modes.

The experimental data completely falsify the claim that open-system BGK collision must destroy all quantum coherences, while confirming that microscopic kinetic memory is physically dissipated into the environment.

---

## 2. Experimental Data Across the Three Critical Classes

### Case A: Same Non-Equilibrium Sector ($\Delta \mathbf{m}_{\text{neq}}^{(A)} = \Delta \mathbf{m}_{\text{neq}}^{(B)}$)
From [`results/phase_f20/f20_superposition_same_neq.csv`](file:///home/aswa/Research/QLBM-DamBreak-Production/results/phase_f20/f20_superposition_same_neq.csv):
- State pair: $|\Psi_0\rangle = \frac{1}{\sqrt{2}}(|0\rangle + |3\rangle)$ (two distinct local equilibria with $\mathbf{u}_0 \neq \mathbf{u}_3$).
- Input coherence: $C_{l_1}(\rho_{\text{in}}) = 1.0000$.
- Output density matrix: $\rho_{\text{out}} = |\Psi_0^*\rangle\langle \Psi_0^*|$ (pure state, purity $\text{Tr}(\rho^2) = 1.0000$).
- Output coherence: $C_{l_1}(\rho_{\text{out}}) = 1.0000$.
- **Coherence Retention**: $\mathbf{100.0\%}$.
- **Physical Interpretation**: Because both branches share $\Delta \mathbf{m}_{\text{neq}} = \mathbf{0}$, the environment state $|e(\mathbf{0})\rangle_E$ factors out completely:
  $$V_m |\Psi_0\rangle |0\rangle_E = \left( \frac{1}{\sqrt{2}} |0^*\rangle_S + \frac{1}{\sqrt{2}} |3^*\rangle_S \right) \otimes |e(\mathbf{0})\rangle_E$$
  Tracing out the environment leaves the system in a pure coherent macroscopic superposition!

### Case B: Different Non-Equilibrium Sector ($\Delta \mathbf{m}_{\text{neq}}^{(A)} \neq \Delta \mathbf{m}_{\text{neq}}^{(B)}$)
From [`results/phase_f20/f20_superposition_different_neq.csv`](file:///home/aswa/Research/QLBM-DamBreak-Production/results/phase_f20/f20_superposition_different_neq.csv):
- State pair: $|\Psi_0\rangle = \frac{1}{\sqrt{2}}(|0\rangle + |1\rangle)$ where $|0\rangle$ is in equilibrium ($\text{neq}=0$) and $|1\rangle$ has a shear perturbation ($\text{neq}=1$).
- Input coherence: $C_{l_1}(\rho_{\text{in}}) = 1.0000$.
- Since $F(0) = 0$ and $F(1) = 0$, both relax to the equilibrium $|0\rangle$.
- Output state: $\rho_{\text{out}} = |0\rangle\langle 0|$ (purity $1.0000$, coherence $0.0000$).
- **Physical Interpretation**: The environment distinguishes the non-equilibrium deviation ($|e(0)\rangle_E \perp |e(1)\rangle_E$). Tracing over $E$ projects the state onto the pure macroscopic equilibrium target, transferring relative kinetic phase into $E$.

### Case C: Same Hydrodynamic Variables, Different Kinetic Modes
From [`results/phase_f20/f20_same_hydro_different_kinetic.csv`](file:///home/aswa/Research/QLBM-DamBreak-Production/results/phase_f20/f20_same_hydro_different_kinetic.csv):
- State pair: Distinct microscopic distributions having the exact same $(\rho, j_x, j_y)$.
- Result: After collision, both relax to the identical macroscopic state with zero residual coherence between the original kinetic perturbations.
- **Physical Interpretation**: This proves that the quantum channel faithfully reproduces the second law of thermodynamics and Boltzmann's H-theorem: microscopic kinetic differences are erased, while macroscopic flow information is preserved.

---

## 3. Comparison with Phase F18 Full-Copying Baseline
From [`results/phase_f20/f18_control_superposition.csv`](file:///home/aswa/Research/QLBM-DamBreak-Production/results/phase_f20/f18_control_superposition.csv):
- Under F18 full copying ($|x\rangle|0\rangle \to |F(x)\rangle|x\rangle$), the environment copies the entire microstate.
- Even for two local equilibria ($|0\rangle$ and $|3\rangle$), F18 entangles the environment ($|e(0)\rangle = |0\rangle, |e(3)\rangle = |3\rangle$), forcing $\langle e(0)|e(3)\rangle = 0$.
- As a consequence:
  $$\rho_{\text{out}}^{\text{F18}} = \frac{1}{2}|0\rangle\langle 0| + \frac{1}{2}|3\rangle\langle 3| \implies C_{l_1} = 0.0000 \quad (\mathbf{Universal\ Dephasing})$$
- Architecture F20 completely eliminates this universal dephasing for all conserved hydrodynamic superpositions.
