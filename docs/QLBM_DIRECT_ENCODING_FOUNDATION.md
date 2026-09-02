# QUANTUM LATTICE BOLTZMANN METHOD (QLBM)
## Direct Spatial/Population Quantum State Encoding: Mathematical Foundations & Architecture

**Document**: Definitive Mathematical Formulation and Register Specification  
**Project**: Quantum Two-Phase Dam-Break Lattice Boltzmann Method  
**Repository**: `/home/aswa/Research/QLBM-DamBreak-Production`  
**Branch**: `feature/direct-encoding-two-phase-qlbm`  
**Date**: September 2026  

---

## 1. Executive Summary & Core Theoretical Breakthrough

In Level 6A of this research project, an attempt to evolve lifted Carleman tensors $\mathbf{Y}(\mathbf{x}) = [\mathbf{z}(\mathbf{x}); \mathbf{z}(\mathbf{x}) \otimes \mathbf{z}(\mathbf{x})] \in \mathbb{R}^{342}$ autonomously failed because spatial advection on decoupled tensor products ($S \otimes S$) shifted quadratic cross-terms by $\mathbf{c}_a + \mathbf{c}_b$ (as if from a single node) rather than assembling distinct physical node products $z_a(\mathbf{x}-\mathbf{c}_a) z_b(\mathbf{x}-\mathbf{c}_b)$, producing a **$419.5\%$ invariant manifold error**.

**The Direct Spatial/Population Quantum State Encoding** fundamentally eliminates this breakdown:
1. The global lattice state $|\Psi\rangle$ encodes individual kinetic distribution functions $f_i(x,y)$ and $g_i(x,y)$ directly into the computational basis amplitudes $|x\rangle|y\rangle|i\rangle|p\rangle$.
2. Because different velocity directions reside in orthogonal basis states rather than tensor products, spatial streaming $S$ acts as an **exact unitary permutation matrix** on the coordinate basis ($S^\dagger S = I$).
3. The spatial streaming operator operates with zero approximation error, zero defect leakage, and exact preservation of the physical discrete velocity Boltzmann advection equation.

---

## 2. Hilbert Space Decomposition & Register Architecture

For an $N_x \times N_y$ lattice grid with D2Q9 velocities ($Q=9$) and two fluid phases ($P=2$: hydrodynamic $f$ and phase-field $g$):

$$\mathcal{H}_{\text{lattice}} = \mathcal{H}_x \otimes \mathcal{H}_y \otimes \mathcal{H}_{\text{vel}} \otimes \mathcal{H}_{\text{phase}}$$

### Complete Register Layout:
$$\begin{array}{|l|c|c|c|l|}
\hline
\textbf{Quantum Register} & \textbf{Symbol} & \textbf{Bit Sizing} & \textbf{Dimension} & \textbf{Physical Meaning} \\
\hline
\text{X-Coordinate} & |x\rangle & n_x = \lceil\log_2 N_x\rceil & 2^{n_x} \ge N_x & \text{Lattice column position } x \in \{0, \dots, N_x-1\} \\
\text{Y-Coordinate} & |y\rangle & n_y = \lceil\log_2 N_y\rceil & 2^{n_y} \ge N_y & \text{Lattice row position } y \in \{0, \dots, N_y-1\} \\
\text{Discrete Velocity} & |i\rangle & n_{\text{vel}} = 4 & 16 \ge 9 & \text{D2Q9 velocity direction } i \in \{0, \dots, 8\} \\
\text{Phase / Species} & |p\rangle & n_{\text{phase}} = 1 & 2 & \text{Species identifier: } |0\rangle \equiv f \text{ (fluid)}, |1\rangle \equiv g \text{ (phase)} \\
\hline
\textbf{Total Data Register} & |\Psi\rangle & \mathbf{n_{\text{data}} = n_x + n_y + 5} & \mathbf{2^{n_{\text{data}}}} & \textbf{Complete Unified Lattice State} \\
\hline
\end{array}$$

### Scaling Examples:
- **Minimal Prototype ($2 \times 2$)**: $n_x = 1, n_y = 1, n_{\text{vel}} = 4, n_{\text{phase}} = 1 \implies \mathbf{7 \text{ logical data qubits}}$ ($\dim = 128$).
- **Intermediate Lattice ($4 \times 4$)**: $n_x = 2, n_y = 2, n_{\text{vel}} = 4, n_{\text{phase}} = 1 \implies \mathbf{9 \text{ logical data qubits}}$ ($\dim = 512$).
- **Standard Benchmark ($64 \times 32$)**: $n_x = 6, n_y = 5, n_{\text{vel}} = 4, n_{\text{phase}} = 1 \implies \mathbf{16 \text{ logical data qubits}}$ ($\dim = 65,536$).
- **Target Dam-Break Grid ($128 \times 64$)**: $n_x = 7, n_y = 6, n_{\text{vel}} = 4, n_{\text{phase}} = 1 \implies \mathbf{18 \text{ logical data qubits}}$ ($\dim = 262,144$).

---

## 3. Global Quantum State Vector

The normalized quantum state vector $|\Psi\rangle \in \mathcal{H}_{\text{lattice}}$ is defined as:

$$|\Psi\rangle = \frac{1}{\mathcal{N}} \left( \sum_{x=0}^{N_x-1} \sum_{y=0}^{N_y-1} \sum_{i=0}^8 f_i(x,y) |x\rangle|y\rangle|i\rangle|0\rangle + \sum_{x=0}^{N_x-1} \sum_{y=0}^{N_y-1} \sum_{i=0}^8 g_i(x,y) |x\rangle|y\rangle|i\rangle|1\rangle \right)$$

where the Euclidean normalization constant is:
$$\mathcal{N} = \sqrt{\sum_{x=0}^{N_x-1}\sum_{y=0}^{N_y-1}\sum_{i=0}^8 \left( |f_i(x,y)|^2 + |g_i(x,y)|^2 \right)}$$

---

## 4. Quantum Streaming Operator ($S$)

### Mathematical Definition:
Streaming shifts each population along its discrete velocity vector $\mathbf{c}_i = (c_{ix}, c_{iy})$:

$$S |x\rangle |y\rangle |i\rangle |p\rangle = |(x + c_{ix}) \bmod N_x\rangle |(y + c_{iy}) \bmod N_y\rangle |i\rangle |p\rangle$$

where standard D2Q9 lattice velocities are:
$$c_x = [0, 1, 0, -1, 0, 1, -1, -1, 1], \quad c_y = [0, 0, 1, 0, -1, 1, 1, -1, -1]$$

### Unitarity Proof:
Because the modular shift mapping $(x, y) \mapsto ((x + c_{ix}) \bmod N_x, (y + c_{iy}) \bmod N_y)$ is a bijective bijection on the finite discrete torus $\mathbb{Z}_{N_x} \times \mathbb{Z}_{N_y}$ for every fixed $i$, the matrix representation of $S$ in the computational basis is a **permutation matrix** (one entry equal to $1$ per row and column, zeros elsewhere).
Therefore:
$$S^\dagger S = S S^\dagger = I, \quad \|S^\dagger S - I\| = 0.000000 \times 10^0$$

---

## 5. Quantum Bounce-Back Boundary Operator ($B$)

### Mathematical Definition:
At solid boundary nodes $(x, y) \in \partial\Omega$, non-equilibrium populations reflect to their opposite discrete velocity direction:

$$B |x\rangle |y\rangle |i\rangle |p\rangle = \begin{cases} |x\rangle |y\rangle |\text{opp}(i)\rangle |p\rangle & \text{if } (x,y) \in \partial\Omega \\ |x\rangle |y\rangle |i\rangle |p\rangle & \text{if } (x,y) \notin \partial\Omega \end{cases}$$

where the D2Q9 opposite direction map is:
$$\text{opp} = [0, 3, 4, 1, 2, 7, 8, 5, 6]$$

### Involution Proof:
Because $\text{opp}(\text{opp}(i)) = i$ for all $i \in \{0, \dots, 8\}$, applying $B$ twice yields:
$$B^2 |x, y, i, p\rangle = B |x, y, \text{opp}(i), p\rangle = |x, y, \text{opp}(\text{opp}(i)), p\rangle = |x, y, i, p\rangle \implies B^2 = I$$
Because $B$ is a real symmetric permutation matrix ($B = B^T = B^\dagger$), it is simultaneously **unitary** and a **self-inverse involution**:
$$B = B^\dagger, \quad B^2 = I, \quad B^\dagger B = I$$

---

## 6. Two-Phase Coupling & Continuum Surface Force (CSF)

Macroscopic density $\rho(x,y)$ and phase fraction $\alpha(x,y)$ are obtained by contracting over the velocity register:
$$\rho(x,y) = \mathcal{N} \sum_{i=0}^8 \langle x, y, i, 0 | \Psi\rangle, \quad \alpha(x,y) = \text{clip}\left( \mathcal{N} \sum_{i=0}^8 \langle x, y, i, 1 | \Psi\rangle, 0, 1 \right)$$

Physical fluid parameters dynamically interpolate across the diffuse interface:
$$\rho(\alpha) = \alpha \rho_L + (1-\alpha) \rho_G, \quad \nu(\alpha) = \alpha \nu_L + (1-\alpha) \nu_G, \quad \tau_f(\alpha) = 3\nu(\alpha) + 0.5$$

Interfacial surface tension is evaluated via Brackbill Continuum Surface Force:
$$\mathbf{F}_s = \sigma \kappa \nabla\alpha, \quad \mathbf{n} = \frac{\nabla\alpha}{|\nabla\alpha|}, \quad \kappa = -\nabla\cdot\mathbf{n}$$
and coupled to momentum as hybrid feedback.
