# Quantum Lattice Boltzmann Method (QLBM) Mathematical Formulations

## 1. Classical Vectorized LBM Operator Form
Let $\mathbf{f}(t) \in \mathbb{R}^{N_{spatial} \times Q}$ be the flattened distribution state vector.
The discrete time step is:
$$
\mathbf{f}(t+1) = \mathbf{S} \left( \mathbf{f}(t) + \mathbf{\Omega}(\mathbf{f}(t)) \right)
$$
where:
- $\mathbf{S} = \bigoplus_{i=0}^{Q-1} \mathbf{S}_i$ is the global linear spatial permutation matrix (unitary for periodic boundary conditions).
- $\mathbf{\Omega}(\mathbf{f}) = -\frac{1}{\tau} (\mathbf{f} - \mathbf{f}^{eq}(\mathbf{f})) + \Delta t \mathbf{F}(\mathbf{f})$ is the local collision operator.

## 2. Polynomial Decomposition of the Collision Operator
The equilibrium distribution $\mathbf{f}^{eq}$ contains polynomial terms in $\mathbf{f}$ (linear, quadratic, and optionally cubic/quartic depending on expansion order):
$$
\mathbf{f}(t+1) = \mathbf{A}_1 \mathbf{f}(t) + \mathbf{A}_2 (\mathbf{f}(t) \otimes \mathbf{f}(t)) + \mathbf{A}_3 (\mathbf{f}(t) \otimes \mathbf{f}(t) \otimes \mathbf{f}(t)) + \dots
$$
where:
- $\mathbf{A}_1 = \mathbf{S} (\mathbf{I} - \frac{1}{\tau} \mathbf{I} + \frac{1}{\tau} \mathbf{E}_1)$ is the linear streaming-relaxation operator.
- $\mathbf{A}_2 = \frac{1}{\tau} \mathbf{S} \mathbf{E}_2$ is the quadratic advective kinetic flux coefficient tensor.
- $\mathbf{A}_3 = \frac{1}{\tau} \mathbf{S} \mathbf{E}_3$ captures cubic interactions (e.g. chemical potential or higher-order compressibility).

## 3. Two-Phase Coupled State Vector
For two-phase flow with hydrodynamic distribution $\mathbf{g}$ and phase distribution $\mathbf{h}$:
$$
\mathbf{\Psi}(t) = \begin{bmatrix} \mathbf{g}(t) \\ \mathbf{h}(t) \end{bmatrix} \in \mathbb{R}^{2 N_{spatial} Q}
$$
Coupled non-linear discrete evolution:
$$
\mathbf{\Psi}(t+1) = \mathbf{\mathcal{S}} \left( \mathbf{\Psi}(t) + \mathbf{\Omega}_{coupled}(\mathbf{\Psi}(t)) \right)
$$
