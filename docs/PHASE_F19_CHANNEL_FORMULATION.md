# PHASE F19: QUANTUM CHANNEL AND STINESPRING FORMULATION
## Complete Mathematical Formulation of Open-System CPTP Collision Channels

---

## 1. The Stinespring Isometry

Let $\mathcal{H}_S$ be the $d_S$-dimensional Hilbert space of system lattice node states. Let $\mathcal{H}_E$ be the environment Hilbert space initialized to $|0\rangle_E$.
The collision is realized as a linear isometry $V: \mathcal{H}_S \to \mathcal{H}_S \otimes \mathcal{H}_E$:
$$V |\psi\rangle_S = U (|\psi\rangle_S \otimes |0\rangle_E)$$
where $U$ is a unitary operator on the joint system-environment space $\mathcal{H}_S \otimes \mathcal{H}_E$.

For computational basis states $|x\rangle_S$:
$$\boxed{V |x\rangle_S = |F(x)\rangle_S \otimes |e(x)\rangle_E}$$

### The Inner Product Condition:
Because $V$ is an isometry ($V^\dagger V = I_S$):
$$\langle V x_1 | V x_2 \rangle = \langle F(x_1) | F(x_2) \rangle_S \cdot \langle e(x_1) | e(x_2) \rangle_E = \langle x_1 | x_2 \rangle = \delta_{x_1, x_2}$$

This imposes a strict mathematical duality:
1. If $F(x_1) = F(x_2)$ (degenerate preimages), then $\langle F(x_1) | F(x_2) \rangle = 1$, which forces:
   $$\langle e(x_1) | e(x_2) \rangle_E = 0 \quad (\text{Environment states MUST be orthogonal})$$
2. If $F(x_1) \neq F(x_2)$ and $\langle e(x_1) | e(x_2) \rangle_E = 1$ (states share the same environment pointer state), then:
   $$\langle F(x_1) | F(x_2) \rangle_S = 0 \quad (\text{Post-collision states MUST be orthogonal})$$

---

## 2. Kraus Representation and Trace Preservation

Tracing out the environment produces the reduced CPTP channel:
$$\mathcal{E}(\rho) = \text{Tr}_E [ V \rho V^\dagger ] = \sum_{e} K_e \rho K_e^\dagger$$
where the Kraus operators are defined by projections onto environment basis states $|e\rangle_E$:
$$K_e = \langle e |_E V = \sum_{x: e(x) = e} |F(x)\rangle \langle x |$$

### Trace Preservation:
$$\sum_e K_e^\dagger K_e = \sum_e \left( \sum_{x: e(x)=e} |x\rangle\langle F(x)| \right) \left( \sum_{y: e(y)=e} |F(y)\rangle\langle y| \right)$$
Using $\langle F(x) | F(y) \rangle = \delta_{x, y}$ for preimages mapped to the same environment bin $e$:
$$\sum_e K_e^\dagger K_e = \sum_e \sum_{x: e(x)=e} |x\rangle\langle x| = \sum_{x} |x\rangle\langle x| = I_S \quad \implies \mathbf{Trace-Preserving\ (TP)}$$

---

## 3. Choi-Jamiołkowski Matrix & Complete Positivity (CP)

The Choi matrix $J(\mathcal{E})$ is constructed via the maximally entangled Bell state $|\Phi^+\rangle = \frac{1}{\sqrt{d_S}} \sum_i |i\rangle \otimes |i\rangle$:
$$J(\mathcal{E}) = (I \otimes \mathcal{E})(|\Phi^+\rangle\langle\Phi^+|) = \frac{1}{d_S} \sum_{i, j} |i\rangle\langle j| \otimes \mathcal{E}(|i\rangle\langle j|)$$

Using the Kraus decomposition:
$$J(\mathcal{E}) = \frac{1}{d_S} \sum_e \left( \sum_i |i\rangle \otimes K_e |i\rangle \right) \left( \sum_j \langle j| \otimes \langle j| K_e^\dagger \right) = \frac{1}{d_S} \sum_e |v_e\rangle\langle v_e|$$
where $|v_e\rangle = \sum_i |i\rangle \otimes K_e |i\rangle$.
Because $J(\mathcal{E})$ is a sum of positive semi-definite rank-1 projectors, all its eigenvalues are non-negative:
$$\lambda_{\min}(J(\mathcal{E})) \ge 0 \quad \implies \mathbf{Completely\ Positive\ (CP)}$$

---

## 4. Entanglement Preservation with a Reference System ($R$)

To verify that the channel is physically consistent when acting on entangled inputs, a reference system $R$ is initialized in a Bell state with $S$:
$$|\Phi\rangle_{RS} = \frac{1}{\sqrt{2}} (|0\rangle_R |0\rangle_S + |1\rangle_R |3\rangle_S)$$
Applying the collision channel strictly to $S$:
$$\rho_{RS}^* = (I_R \otimes \mathcal{E}_S)(|\Phi\rangle\langle\Phi|_{RS})$$
Evaluating eigenvalues (recorded in `results/phase_f19/collision_cptp.csv`):
$$\lambda_{\min}(\rho_{RS}^*) \ge 0, \quad \text{Tr}(\rho_{RS}^*) = 1.000000$$
The joint reference-system state remains a strictly valid quantum density operator without unphysical negative probabilities.
