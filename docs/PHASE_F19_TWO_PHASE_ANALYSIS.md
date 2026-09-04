# PHASE F19: TWO-PHASE HYDRODYNAMIC MOMENT ANALYSIS
## Coupled Moment Decompositions for Hydrodynamic and Order-Parameter Populations

---

## 1. Dual Distribution Framework
The two-phase dam break requires evolving two distinct discrete distribution sets at every lattice node:
1. Hydrodynamic populations $\mathbf{f} = [f_0 \dots f_8]^T \in \mathbb{R}^9$: Transport fluid mass $\rho$ and momentum $\rho \mathbf{u}$.
2. Phase-field populations $\mathbf{g} = [g_0 \dots g_8]^T \in \mathbb{R}^9$: Transport the conservative order parameter $\alpha$ ($1$ for liquid, $0$ for gas).

---

## 2. Dual Moment Spaces

$$\begin{array}{|l|l|l|l|}
\hline
\textbf{Mode} & \textbf{Hydrodynamic Moment } m_k^{(f)} & \textbf{Phase-Field Moment } m_k^{(g)} & \textbf{Physical Role} \\
\hline
k = 0 & \rho = \sum_i f_i & \alpha = \sum_i g_i & \mathbf{Conserved\ Invariants} \\
k = 1 & e^{(f)}\text{ (bulk energy)} & e^{(g)}\text{ (order variance)} & \text{Relaxed non-equilibrium mode} \\
k = 2 & \epsilon^{(f)}\text{ (energy squared)} & \epsilon^{(g)} & \text{Relaxed higher kinetic mode} \\
k = 3 & j_x = \sum_i f_i c_{ix} & j_{\alpha x} = \sum_i g_i c_{ix} & \mathbf{Conserved\ x-Momentum / Flux} \\
k = 4 & q_x^{(f)}\text{ (heat flux x)} & q_x^{(g)} & \text{Relaxed non-equilibrium flux} \\
k = 5 & j_y = \sum_i f_i c_{iy} & j_{\alpha y} = \sum_i g_i c_{iy} & \mathbf{Conserved\ y-Momentum / Flux} \\
k = 6 & q_y^{(f)}\text{ (heat flux y)} & q_y^{(g)} & \text{Relaxed non-equilibrium flux} \\
k = 7 & p_{xx}\text{ (normal stress)} & p_{xx}^{(g)} & \text{Viscous shear relaxation} \\
k = 8 & p_{xy}\text{ (shear stress)} & p_{xy}^{(g)} & \text{Viscous shear relaxation} \\
\hline
\end{array}$$

---

## 3. Separation of Reversible and Dissipative Components

$$\begin{array}{|l|c|l|l|}
\hline
\textbf{Physical Subsystem} & \textbf{Mathematical Form} & \textbf{Quantum Nature} & \textbf{Dissipation Status} \\
\hline
\text{Density Interpolation } \rho(\alpha) & \alpha \rho_L + (1-\alpha)\rho_G & \text{Reversible fixed-point arithmetic} & \mathbf{Zero\ Dissipation\ (Reversible)} \\
\text{Viscosity Interpolation } \nu(\alpha) & \alpha \nu_L + (1-\alpha)\nu_G & \text{Reversible parameter generation} & \mathbf{Zero\ Dissipation\ (Reversible)} \\
\text{Gravitational Body Forcing } \mathbf{F}_g & (\rho - \rho_G) \mathbf{g} & \text{Momentum register shift } (CX) & \mathbf{Zero\ Dissipation\ (Unitary\ Shift)} \\
\text{Spatial Streaming } (S) & \text{Coordinate SWAP network} & \text{Permutation matrix } (S^\dagger S = I) & \mathbf{Zero\ Dissipation\ (Exact\ Unitary)} \\
\text{Wall Reflections } (B) & \text{Bounce-back bit reflection} & \text{Pauli involution } (B^2 = I) & \mathbf{Zero\ Dissipation\ (Exact\ Unitary)} \\
\hline\hline
\mathbf{Hydrodynamic\ BGK\ Collision} & -\frac{1}{\tau_f} (\mathbf{m}^{(f)} - \mathbf{m}^{(f),\text{eq}}) & \text{Open-system Stinespring channel} & \mathbf{Viscous\ Energy\ Dissipation} \\
\mathbf{Phase-Field\ Relaxation} & -\frac{1}{\tau_g} (\mathbf{m}^{(g)} - \mathbf{m}^{(g),\text{eq}}) & \text{Open-system Stinespring channel} & \mathbf{Interfacial\ Mobility\ Dissipation} \\
\hline
\end{array}$$

### Critical Finding:
Only the relaxation of non-equilibrium moments toward their respective equilibrium functions involves entropy production and phase-space contraction. All parameter couplings ($\rho(\alpha), \nu(\alpha)$), body forcing, streaming, and wall boundary reflections are **intrinsically unitary and reversible transformations**.
