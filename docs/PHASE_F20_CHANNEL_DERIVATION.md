# PHASE F20: MOMENT-SPACE CPTP CHANNEL DERIVATION

## 1. Stinespring Dilation in Moment Space
To implement dissipative BGK relaxation without destroying macroscopic quantum coherences, the collision channel $\mathcal{E}_C$ is constructed via a Stinespring dilation that couples the environment **strictly to the non-equilibrium moment register**.

Let the local node Hilbert space factorize into conserved and non-equilibrium subspaces:
$$\mathcal{H}_S = \mathcal{H}_{\text{cons}} \otimes \mathcal{H}_{\text{neq}}$$
where:
- $\mathcal{H}_{\text{cons}} = \text{span}\{|\rho\rangle, |j_x\rangle, |j_y\rangle\}$ carries the conserved hydrodynamic modes.
- $\mathcal{H}_{\text{neq}} = \text{span}\{|e\rangle, |\epsilon\rangle, |q_x\rangle, |q_y\rangle, |p_{xx}\rangle, |p_{xy}\rangle\}$ carries the non-equilibrium modes.

The Stinespring isometry $V_m: \mathcal{H}_S \to \mathcal{H}_S \otimes \mathcal{H}_E$ is defined by:
$$V_m |\mathbf{m}_{\text{cons}}\rangle |\mathbf{m}_{\text{neq}}\rangle |0\rangle_E = |\mathbf{m}_{\text{cons}}\rangle |\mathbf{m}_{\text{neq}}^*(\mathbf{m}_{\text{cons}}, \mathbf{m}_{\text{neq}})\rangle_S \otimes |e(\mathbf{m}_{\text{neq}} - \mathbf{m}_{\text{neq}}^{\text{eq}})\rangle_E$$

---

## 2. Environment Coupling Specification
The environment state $|e\rangle_E$ records **only the non-equilibrium deviation**:
$$\Delta \mathbf{m}_{\text{neq}} = \mathbf{m}_{\text{neq}} - \mathbf{m}_{\text{neq}}^{\text{eq}}(\mathbf{m}_{\text{cons}})$$
Crucially:
1. If two states share the same non-equilibrium deviation $\Delta \mathbf{m}_{\text{neq}}$ (for example, if both are in local equilibrium $\Delta \mathbf{m}_{\text{neq}} = \mathbf{0}$), they couple to the **exact same environment state**:
   $$|e(\mathbf{0})\rangle_E = |0\rangle_E$$
2. The environment register does **NOT** copy or entangle with $\mathbf{m}_{\text{cons}} = (\rho, j_x, j_y)$.
3. Consequently, the inner product of the environment states between two local equilibria with distinct macroscopic velocities $\mathbf{u}_1 \neq \mathbf{u}_2$ is:
   $$\langle e(\mathbf{0}) | e(\mathbf{0}) \rangle_E = 1.0$$

---

## 3. Quantum Channel Action
The open-system quantum channel on system density matrix $\rho_S$ is obtained by tracing over the environment:
$$\mathcal{E}_C(\rho_S) = \text{Tr}_E \left[ V_m (\rho_S \otimes |0\rangle\langle 0|_E) V_m^\dagger \right]$$

For a general density matrix element in the moment basis $|\mathbf{m}_{\text{cons}}^{(A)}, \mathbf{m}_{\text{neq}}^{(A)}\rangle \langle \mathbf{m}_{\text{cons}}^{(B)}, \mathbf{m}_{\text{neq}}^{(B)}|$:
$$\mathcal{E}_C\left( |\mathbf{m}_A\rangle \langle \mathbf{m}_B| \right) = \langle e(\Delta \mathbf{m}_{\text{neq}}^{(B)}) | e(\Delta \mathbf{m}_{\text{neq}}^{(A)}) \rangle_E \cdot |\mathbf{m}_A^*\rangle \langle \mathbf{m}_B^*|$$

The off-diagonal coherence is modulated by the environment overlap factor:
$$\gamma(A, B) = \langle e(\Delta \mathbf{m}_{\text{neq}}^{(B)}) | e(\Delta \mathbf{m}_{\text{neq}}^{(A)}) \rangle_E$$

### Fundamental Implications:
- If $\Delta \mathbf{m}_{\text{neq}}^{(A)} = \Delta \mathbf{m}_{\text{neq}}^{(B)}$: $\gamma(A, B) = 1.0 \implies \mathbf{100\%\ Coherence\ Survival}$.
- If $\Delta \mathbf{m}_{\text{neq}}^{(A)} \neq \Delta \mathbf{m}_{\text{neq}}^{(B)}$: $\gamma(A, B) = 0.0 \implies \mathbf{Complete\ Dissipative\ Dephasing}$.

This proves that Architecture F19-A / F20 achieves exact selective dissipation without universal dephasing.
