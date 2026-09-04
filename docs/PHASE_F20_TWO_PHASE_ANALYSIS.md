# PHASE F20: TWO-PHASE QUANTUM COUPLING ANALYSIS

## 1. Dual Distribution Representation
The complete two-phase dam-break Lattice Boltzmann formulation tracks two discrete sets of distribution functions at every lattice node $\mathbf{x}$:
1. **Hydrodynamic Distributions $f_i(\mathbf{x}, t)$**: Govern momentum transport, fluid pressure, and Navier-Stokes dynamics.
2. **Phase-Field Distributions $g_i(\mathbf{x}, t)$**: Govern conservative interface advection and track the liquid volume fraction $\alpha(\mathbf{x}, t) = \sum_i g_i(\mathbf{x}, t)$.

---

## 2. Decoupling of Reversible Couplings from Dissipative Relaxations
A central achievement of Phase F20 is proving which two-phase operations are strictly reversible (unitary) and which require environment-assisted open quantum channels:

From [`results/phase_f20/f20_two_phase.csv`](file:///home/aswa/Research/QLBM-DamBreak-Production/results/phase_f20/f20_two_phase.csv):

| Subsystem / Operation | Mathematical Definition | Quantum Representation | Type |
| :--- | :--- | :--- | :--- |
| **Phase Order Parameter** | $\alpha = \sum_i g_i$ | Quantum Adder Tree on $g$ register | **Unitary / Reversible** |
| **Density Interpolation** | $\rho(\alpha) = \alpha \rho_L + (1 - \alpha)\rho_G$ | Reversible Linear Arithmetic | **Unitary / Reversible** |
| **Viscosity Interpolation** | $\nu(\alpha) = \alpha \nu_L + (1 - \alpha)\nu_G$ | Reversible Linear Arithmetic | **Unitary / Reversible** |
| **Relaxation Times** | $\tau_f = 3\nu + 0.5, \omega_f = 1/\tau_f$ | In-place Arithmetic LUT | **Unitary / Reversible** |
| **Buoyancy Forcing** | $\mathbf{F}_g = (0, (\rho - \rho_G)g_{\text{acc}})^T$ | Linear Shift on $j_y$ register | **Unitary / Reversible** |
| **Phase-Field Mobility** | $g_i^* = g_i - \omega_g(g_i - g_i^{\text{eq}})$ | Open Channel on non-eq $g$ modes | **CPTP Quantum Channel** |
| **Hydrodynamic Viscosity** | $f_i^* = f_i - \omega_f(f_i - f_i^{\text{eq}}) + S_i$ | Open Channel on non-eq $f$ modes | **CPTP Quantum Channel** |
| **Spatial Streaming** | $f_i(\mathbf{x} + \mathbf{c}_i) = f_i^*(\mathbf{x})$ | Inter-node Permutation / SWAP | **Unitary / Reversible** |
| **Solid Bounce-Back** | $f_{\bar{i}} = f_i$ on walls | Directional Inversion / Pauli-X | **Unitary / Reversible** |

### Critical Finding:
Only the viscous relaxation in $f$ and mobility relaxation in $g$ require environment coupling.
All other two-phase couplings—including phase-dependent density $\rho(\alpha)$, viscosity $\nu(\alpha)$, gravitational body forcing, spatial streaming, and wall boundary conditions—are **100% reversible unitary transformations**.
