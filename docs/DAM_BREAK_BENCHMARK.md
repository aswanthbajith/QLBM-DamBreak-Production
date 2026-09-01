# BENCHMARK SPECIFICATION: REDUCED TWO-PHASE DAM-BREAK HYDRODYNAMICS

**Date**: 2026-08-25  
**Author**: Lead Quantum-CFD Algorithm Engineer & Verification Specialist  
**Repository**: `/home/aswa/Research/QLBM-DamBreak/`  

---

## 1. Physical Benchmark Definition

The two-phase dam-break problem models the gravitational collapse and horizontal surge of a column of dense fluid (liquid) in a lighter ambient fluid (gas) within an enclosed rectangular tank.

```
+------------------------------------------------------+
|                     SOLID TOP WALL                   |
|  (x=0..Nx-1, y=Ny-1)                                 |
|                                                      |
|  +--------------------+                              |
|  |                    |                              |
|  |   LIQUID COLUMN    |        AMBIENT GAS           |
|  |   phi = 1.0        |        phi = 0.0             |
|  |   rho = 1.0        |        rho = 0.1             |
|  |   u = (0, 0)       |        u = (0, 0)            |
|  |   x in [0, dam_x)  |                              |
|  |   y in [0, dam_y)  |                              |
|  +--------------------+                              |
|                                                      |
|                     SOLID BOTTOM WALL                |
|  (x=0..Nx-1, y=0)                                    |
+------------------------------------------------------+
```

---

## 2. Parameter Table

| Parameter | Symbol | Benchmark Value | Lattice Units | Description |
| :--- | :--- | :--- | :--- | :--- |
| **Grid Resolutions** | $N_x \times N_y$ | $4\times 4, 8\times 4, 8\times 8, 16\times 8$ | Nodes | Discrete computational lattice |
| **Dam Width** | $L_{\text{dam}}$ | $\lfloor N_x / 2 \rfloor$ | $\Delta x$ | Initial width of liquid column |
| **Dam Height** | $H_{\text{dam}}$ | $\lfloor N_y / 2 \rfloor$ | $\Delta y$ | Initial height of liquid column |
| **Liquid Density** | $\rho_l$ | $1.0$ | $\text{mu} \cdot \Delta x^{-2}$ | Primary liquid density |
| **Gas Density** | $\rho_g$ | $0.1$ | $\text{mu} \cdot \Delta x^{-2}$ | Ambient gas density ($\rho_l/\rho_g = 10$) |
| **Liquid Kinematic Viscosity** | $\nu_l$ | $0.10$ | $\Delta x^2 \Delta t^{-1}$ | Liquid viscosity |
| **Gas Kinematic Viscosity** | $\nu_g$ | $0.05$ | $\Delta x^2 \Delta t^{-1}$ | Gas viscosity |
| **Liquid Relaxation Time** | $\tau_l$ | $0.80$ | $\Delta t$ | $\tau_l = 3\nu_l + 0.5$ |
| **Gas Relaxation Time** | $\tau_g$ | $0.65$ | $\Delta t$ | $\tau_g = 3\nu_g + 0.5$ |
| **Order Parameter Relaxation** | $\tau_\phi$ | $0.70$ | $\Delta t$ | Phase field relaxation time |
| **Gravitational Acceleration** | $g$ | $-0.001$ | $\Delta x \Delta t^{-2}$ | Vertical body force ($F_y = g(\rho - \rho_g)$) |
| **Initial Velocity** | $u_0(x, y)$ | $(0.0, 0.0)$ | $\Delta x \Delta t^{-1}$ | Quiescent initial condition |
| **Boundary Conditions** | $\partial \Omega$ | No-Slip Solid Wall | N/A | Half-way bounce-back on all 4 perimeter walls |

---

## 3. Initial Kinetic Populations

At $t = 0$:
1. **Macroscopic Fields**:
   $$\phi(x, y, 0) = \begin{cases} 1.0 & \text{if } x < L_{\text{dam}} \text{ and } y < H_{\text{dam}} \\ 0.0 & \text{otherwise} \end{cases}$$
   $$\rho(x, y, 0) = \phi(x, y, 0) \rho_l + (1 - \phi(x, y, 0)) \rho_g$$
   $$u(x, y, 0) = (0, 0)$$

2. **Equilibrium Populations**:
   $$f_i(x, y, 0) = f_i^{\text{eq}}(\rho(x, y, 0), u(x, y, 0)) = w_i \rho(x, y, 0)$$
   $$g_i(x, y, 0) = g_i^{\text{eq}}(\phi(x, y, 0), u(x, y, 0)) = w_i \phi(x, y, 0)$$

3. **Total Invariant Mass**:
   $$M_{\text{total}} = \sum_{x=0}^{N_x-1} \sum_{y=0}^{N_y-1} \rho(x, y, 0) = L_{\text{dam}} H_{\text{dam}} \rho_l + (N_x N_y - L_{\text{dam}} H_{\text{dam}}) \rho_g$$

---

## 4. Multi-Grid Scalability Evaluation

| Mesh Size | $L_{\text{dam}} \times H_{\text{dam}}$ | Total Nodes | Initial Mass $M_0$ | Liquid Mass $M_{\text{liq}}$ |
| :--- | :--- | :--- | :--- | :--- |
| **$4\times 4$** | $2\times 2$ | 16 | $5.20$ | $4.00$ |
| **$8\times 4$** | $4\times 2$ | 32 | $10.40$ | $8.00$ |
| **$8\times 8$** | $4\times 4$ | 64 | $20.80$ | $16.00$ |
| **$16\times 8$** | $8\times 4$ | 128 | $41.60$ | $32.00$ |
