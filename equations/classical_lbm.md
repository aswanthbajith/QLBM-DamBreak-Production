# Canonical Single-Phase Lattice Boltzmann Formulation (D2Q9 / D3Q27)

## 1. Discrete Velocity Sets ($D_d Q_q$)
For standard 2D 9-velocity (D2Q9) lattice with lattice speed $c = \Delta x / \Delta t$:
$$
\mathbf{c}_i = \begin{cases}
(0, 0) & i = 0 \\
(\pm 1, 0)c, (0, \pm 1)c & i = 1, 2, 3, 4 \\
(\pm 1, \pm 1)c & i = 5, 6, 7, 8
\end{cases}
$$
Lattice weights $w_i$:
$$
w_0 = \frac{4}{9}, \quad w_{1..4} = \frac{1}{9}, \quad w_{5..8} = \frac{1}{36}, \quad c_s^2 = \frac{c^2}{3}
$$

## 2. Discrete Boltzmann Equation (LBGK / Single Relaxation Time)
$$
f_i(\mathbf{x} + \mathbf{c}_i \Delta t, t + \Delta t) - f_i(\mathbf{x}, t) = -\frac{1}{\tau} \left[ f_i(\mathbf{x}, t) - f_i^{eq}(\mathbf{x}, t) \right] + \Delta t \, F_i(\mathbf{x}, t)
$$

## 3. Equilibrium Distribution Function $f_i^{eq}$
$$
f_i^{eq}(\rho, \mathbf{u}) = w_i \rho \left[ 1 + \frac{\mathbf{c}_i \cdot \mathbf{u}}{c_s^2} + \frac{(\mathbf{c}_i \cdot \mathbf{u})^2}{2 c_s^4} - \frac{\mathbf{u} \cdot \mathbf{u}}{2 c_s^2} \right]
$$

## 4. Macroscopic Hydrodynamic Moments
- Density:
$$ \rho(\mathbf{x}, t) = \sum_{i=0}^{Q-1} f_i(\mathbf{x}, t) $$
- Momentum:
$$ \rho \mathbf{u}(\mathbf{x}, t) = \sum_{i=0}^{Q-1} f_i(\mathbf{x}, t) \mathbf{c}_i + \frac{\Delta t}{2} \mathbf{F}(\mathbf{x}, t) $$

## 5. Hydrodynamic Viscosity Relation
$$ \nu = c_s^2 \left( \tau - \frac{\Delta t}{2} \right) $$

## 6. Matrix Separation (Collision vs. Streaming)
Let state vector $\mathbf{f}(t) \in \mathbb{R}^{N_{nodes} \times Q}$:
$$ \mathbf{f}(t + \Delta t) = \mathbf{S} \left[ (\mathbf{I} - \mathbf{M}^{-1} \mathbf{S}_{rel} \mathbf{M}) \mathbf{f}(t) + \mathbf{M}^{-1} \mathbf{S}_{rel} \mathbf{m}^{eq}(\mathbf{f}(t)) + \Delta t \, \mathbf{F} \right] $$
where:
- $\mathbf{S}$: Linear spatial shift permutation operator (exact, unitary on periodic lattices).
- $\mathbf{M}$: Moment transformation matrix ($\mathbf{m} = \mathbf{M} \mathbf{f}$).
- $\mathbf{S}_{rel}$: Diagonal relaxation rate matrix $\text{diag}(s_0, s_1, \dots, s_{Q-1})$.
