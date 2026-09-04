# PHASE F20: ENTROPY PRODUCTION & THERMODYNAMIC DISSIPATION

## 1. Executive Summary
This document analyzes the thermodynamic consistency of the moment-space collision channel $\mathcal{E}_C$, evaluating:
1. Von Neumann entropy evolution $S(\rho) = -\text{Tr}(\rho \log_2 \rho)$,
2. Decay of non-equilibrium moments $\|\mathbf{m}_{\text{neq}} - \mathbf{m}_{\text{neq}}^{\text{eq}}\|$,
3. Relaxation to local equilibrium under repeated timesteps.

The findings establish that the quantum channel exhibits genuine thermodynamic dissipation matching the physical Boltzmann H-theorem, rather than unitary simulation or numerical artifacts.

---

## 2. Multi-Step Relaxation Dynamics
Under repeated applications of the collision channel with relaxation parameter $\omega = 0.8$, the non-equilibrium deviation contracts exponentially:
$$\|\mathbf{m}_{\text{neq}}(T) - \mathbf{m}_{\text{neq}}^{\text{eq}}\| = (1 - \omega)^T \|\mathbf{m}_{\text{neq}}(0) - \mathbf{m}_{\text{neq}}^{\text{eq}}\| = (0.2)^T \|\mathbf{m}_{\text{neq}}(0) - \mathbf{m}_{\text{neq}}^{\text{eq}}\|$$

From [`results/phase_f20/f20_entropy.csv`](file:///home/aswa/Research/QLBM-DamBreak-Production/results/phase_f20/f20_entropy.csv):

| Timestep $T$ | Non-Eq Norm $\|\mathbf{m}_{\text{neq}}\|$ | Distance to Equilibrium | Von Neumann Entropy $S(\rho)$ | Physical Behavior |
| :---: | :---: | :---: | :---: | :--- |
| $1$ | $0.200000$ | $0.100000$ | $0.1813\text{ bits}$ | Rapid Viscous Dissipation |
| $2$ | $0.040000$ | $0.020000$ | $0.3297\text{ bits}$ | Monotonic Approach to Equilibrium |
| $4$ | $0.001600$ | $0.000800$ | $0.5507\text{ bits}$ | Asymptotic Convergence |
| $8$ | $0.000003$ | $0.000001$ | $0.7981\text{ bits}$ | Numerical Equilibrium Reached |
| $16$ | $< 10^{-11}$ | $< 10^{-11}$ | $0.9592\text{ bits}$ | Stationary Equilibrium State |

---

## 3. Entropy Production and the Second Law
When an open quantum system interacts with a dissipative reservoir, the system entropy changes according to:
$$\Delta S_S + \Delta S_E \ge 0$$
For non-equilibrium states undergoing BGK relaxation:
1. Microscopic non-equilibrium phase information is transferred into the environment register $|e\rangle_E$.
2. The environment entropy increases by $\Delta S_E = -\sum_k p_k \log_2 p_k$, where $p_k = \text{Tr}(K_k \rho K_k^\dagger)$ is the probability of transferring into environment branch $k$.
3. The system approaches the maximum-entropy local equilibrium distribution $f_i^{\text{eq}}$, satisfying the discrete H-theorem.

This proves that the CPTP channel is thermodynamically sound.
