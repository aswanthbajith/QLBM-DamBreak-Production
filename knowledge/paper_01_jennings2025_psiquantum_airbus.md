# Knowledge Base Dossier: Jennings et al. (PsiQuantum & Airbus, 2025)

## 1. Citation & Metadata
- **Title**: Simulating non-trivial incompressible flows with a quantum lattice Boltzmann algorithm
- **Authors**: David Jennings, Kamil Korzekwa, Matteo Lostaglio, Paul Mannix (PsiQuantum); Richard Ashworth, Emanuele Marsili, Stephen Rolston (Airbus Operations Ltd)
- **Year**: Dec 5, 2025 (arXiv:2512.05781v1 [physics.flu-dyn])
- **Affiliations**: PsiQuantum (Palo Alto, CA, USA) & Airbus Operations Ltd (Filton, Bristol, UK)
- **DOI / URL**: [arXiv:2512.05781](https://arxiv.org/abs/2512.05781)

---

## 2. Research Objective & Core Contribution
- **Objective**: Extend quantum LBM from toy periodic domains to non-trivial incompressible flow configurations with physical boundary conditions (solid no-slip walls, velocity inlets, pressure outlets) and external body forcing, without degrading the asymptotic quantum advantage.
- **Core Contribution**: Formulates wall boundaries (half-way bounce-back), inlet/outlet conditions (Zou-He / non-equilibrium bounce-back), and external forcing (Guo forcing) as sparse matrix operators that embed cleanly into Carleman linearization. Proves that condition number scaling and quantum linear system algorithm (QLSA) complexity are preserved ($\widetilde{\mathcal{O}}(\kappa \text{polylog}(1/\epsilon))$).

---

## 3. Physical Model & Governing PDEs
- **Continuum PDE**: Incompressible Navier-Stokes Equations:
  $$ \nabla \cdot \mathbf{u} = 0 $$
  $$ \frac{\partial \mathbf{u}}{\partial t} + (\mathbf{u} \cdot \nabla) \mathbf{u} = -\frac{1}{\rho_0} \nabla p + \nu \nabla^2 \mathbf{u} + \mathbf{F}_{ext} $$
- **Thermodynamic Limit**: Weakly compressible approximation where $\nabla \cdot \mathbf{u} = \frac{1}{c_s^2} \frac{\partial p}{\partial t} \sim \mathcal{O}(\text{Ma}^2)$.
- **Speed of Sound**: $c_s = \frac{1}{\sqrt{3}} \frac{\Delta x}{\Delta t}$.

---

## 4. Lattice Model & Discrete Velocity Set
- **Lattice**: D2Q9 (2D 9-velocity) and D3Q19 / D3Q27.
- **Velocity Vectors** $\mathbf{e}_m = [e_{mx}, e_{my}]^T$:
  - $m=1$: $(0,0)$
  - $m=2..5$: $(\pm 1, 0), (0, \pm 1)$
  - $m=6..9$: $(\pm 1, \pm 1)$
- **Lattice Weights** $w_m$:
  - $w_1 = 4/9$
  - $w_{2..5} = 1/9$
  - $w_{6..9} = 1/36$

---

## 5. Equilibrium Distribution Function ($g_m^{eq}$)
- **Kinematic Incompressible Equilibrium** (Eq. 3):
  $$ g_m^{eq}(\mathbf{r}, t) = \frac{p}{\rho_0 c_s^2} w_m + \left[ \frac{\mathbf{e}_m \cdot \mathbf{u}}{c_s^2} + \frac{(\mathbf{e}_m \cdot \mathbf{u})^2}{2 c_s^4} - \frac{|\mathbf{u}|^2}{2 c_s^2} \right] w_m + \mathcal{O}(\text{Ma}^3) $$
- **Macroscopic Moments** (Eq. 4):
  - Pressure: $p(\mathbf{r}, t) = c_s^2 \sum_{m=1}^Q g_m(\mathbf{r}, t)$
  - Velocity: $\mathbf{u}(\mathbf{r}, t) = \frac{1}{\rho_0} \sum_{m=1}^Q g_m(\mathbf{r}, t) \mathbf{e}_m$

---

## 6. Collision Operator & Relaxation Mechanics
- **BGK Collision Operator** (Eq. 2 & 5):
  $$ g_m(\mathbf{r} + \mathbf{e}_m \Delta t, t + \Delta t) = g_m(\mathbf{r}, t) - \frac{\Delta t}{\tau + \Delta t / 2} [g_m(\mathbf{r}, t) - g_m^{eq}(\mathbf{r}, t)] + \Delta t \, F_m(\mathbf{r}, t) $$
- **Kinematic Viscosity**: $\nu = c_s^2 (\tau - \Delta t / 2)$.

---

## 7. Streaming & Spatial Transport
- **Shift Matrix Form** (Eq. 9b):
  $$ \mathbf{g}(t+1) = \mathbf{S} \mathbf{g}^C(t) $$
  where $\mathbf{S} \in \mathbb{R}^{NQ \times NQ}$ is a permutation matrix ($\mathbf{S}^T \mathbf{S} = \mathbf{I}$).

---

## 8. Multiphase / Interface Capturing Scheme
- Single-phase in paper; however, external forcing $\mathbf{F}_{ext}$ and spatial variations in body forces are formulated in a manner directly adaptable to surface tension force $\mathbf{F}_s = \mu_\phi \nabla \phi$ and gravitational acceleration $\mathbf{g}$.

---

## 9. Forcing & Body Force Coupling
- **Guo Forcing Scheme**:
  $$ F_m = w_m \left( 1 - \frac{\Delta t}{2\tau} \right) \left[ \frac{\mathbf{e}_m - \mathbf{u}}{c_s^2} + \frac{(\mathbf{e}_m \cdot \mathbf{u})\mathbf{e}_m}{c_s^4} \right] \cdot \mathbf{F}_{ext} $$
- **Linearization**: Since external force can be state-dependent, Guo forcing is decomposed into linear matrix contributions $\mathbf{F}_1^{(ext)}$ and quadratic contributions $\mathbf{F}_2^{(ext)}$.

---

## 10. Boundary Conditions (Matrix Form)
1. **Half-Way Bounce-Back (No-Slip Walls)**:
   $$ g_{\bar{m}}(\mathbf{r}_f, t+1) = g_m^C(\mathbf{r}_f, t) + 2 w_m \rho_0 \frac{\mathbf{e}_m \cdot \mathbf{u}_w}{c_s^2} $$
   Represented as a sparse local reflection matrix $\mathbf{R}_{wall}$ replacing the streaming shift at solid boundary nodes.
2. **Velocity Inlets / Pressure Outlets**:
   Formulated as affine linear projections $\mathbf{B}_{in} \mathbf{g} + \mathbf{b}_{in}$.

---

## 11. Dam-Break Benchmark Setup & Geometry
- While this paper focuses on Taylor-Green vortex, lid-driven cavity, and cylinder flow ($Re \in [10, 1000]$), its wall and gravity forcing formulations provide the exact building blocks required for rectangular dam-break tanks and obstacles.

---

## 12. Validation Metrics & Targets
- Streamwise and spanwise velocity profiles $u_x(y), u_y(x)$.
- Kinetic energy decay rate $E_k(t) = \frac{1}{2} \int |\mathbf{u}|^2 d\mathbf{r}$.
- Vorticity fields $\omega = \nabla \times \mathbf{u}$.
- Drag and lift coefficients $C_D, C_L$ for obstacle flow.

---

## 13. Numerical Parameters & Stability Bounds
- Lattice Mach number $\text{Ma} \le 0.1$ to enforce incompressibility.
- Dimensionless relaxation parameter $\tau^* \in (0.5, 2.0)$ for numerical stability.

---

## 14. Linear vs. Nonlinear Term Catalog
| Term | Expression | Mathematical Type | Carleman Block |
| :--- | :--- | :--- | :--- |
| Equilibrium Pressure | $\frac{p}{\rho_0 c_s^2} w_m = w_m \sum_k g_k$ | Linear | $\mathbf{F}_1$ |
| Velocity Linear Term | $w_m \frac{\mathbf{e}_m \cdot \mathbf{u}}{c_s^2} = \frac{w_m}{\rho_0 c_s^2} \sum_k (\mathbf{e}_m \cdot \mathbf{e}_k) g_k$ | Linear | $\mathbf{F}_1$ |
| Convective Flux | $w_m \frac{(\mathbf{e}_m \cdot \mathbf{u})^2}{2 c_s^4}$ | Quadratic Polynomial | $\mathbf{F}_2$ |
| Kinetic Energy Trace | $-w_m \frac{|\mathbf{u}|^2}{2 c_s^2}$ | Quadratic Polynomial | $\mathbf{F}_2$ |
| Spatial Streaming | $\mathbf{g}(\mathbf{r} + \mathbf{e}_m) \leftarrow \mathbf{g}(\mathbf{r})$ | Linear Permutation | $\mathbf{S}$ |
| Bounce-Back Reflection | $\mathbf{g}_{\bar{m}} \leftarrow \mathbf{g}_m$ | Linear Permutation | $\mathbf{R}_{wall}$ |

---

## 15. Carleman Linearization Suitability & Tensor Mapping
- **Exact Quadratic Structure**: Incompressible LBM is strictly degree-2 polynomial in $\mathbf{g}$.
- **Carleman Truncation Order**: $N_C \ge 2$.
- **Lifted State Vector**:
  $$ \mathbf{y}(t) = [\mathbf{g}(t), \mathbf{g}^{\otimes 2}(t), \dots, \mathbf{g}^{\otimes N_C}(t)]^T \in \mathbb{R}^{d_C}, \quad d_C = \sum_{k=1}^{N_C} (NQ)^k $$
- **Carleman Collision Matrix $\mathbf{C}$**: Block upper-triangular matrix formed by Kronecker expansions:
  $$ \mathbf{C}_{j, k} = \sum_{l=0}^{j} \binom{j}{l} (\mathbf{I} + \mathbf{F}_1)^{\otimes (j-l)} \otimes \mathbf{F}_2^{\otimes l} $$
- **Carleman Streaming Matrix $\mathbf{S}_C$**: $\mathbf{S}_C = \bigoplus_{k=1}^{N_C} \mathbf{S}^{\otimes k}$.

---

## 16. Quantum Encoding / QSVT Algorithmic Relevance
- **Grand Lower-Triangular System**: $A \mathbf{Y} = \mathbf{b}$ across $N_t$ time steps (dimension $d_C (N_t + 1)$).
- **Asymptotic Complexity**: $\widetilde{\mathcal{O}}\left( s \cdot \kappa(A) \cdot \text{polylog}\left(\frac{1}{\epsilon}\right) \right)$.
- **Quantum Advantage Condition**: When spatial resolution $N \gg 1$, qubit count scales as $\mathcal{O}(N_C \log_2(NQ))$, offering exponential reduction in state memory.
