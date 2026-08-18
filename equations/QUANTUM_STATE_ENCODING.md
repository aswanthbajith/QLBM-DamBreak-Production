# Mathematical Definition of Quantum State Encoding for Two-Phase Carleman QLBM

**Author**: Lead Quantum Fluid Dynamics Specialist  
**Pipeline**: Carleman Linearization $\to$ Block Encoding $\to$ QSVT $\to$ Quantum State Representation  
**State Space**: Hilbert Space $\mathcal{H} = \mathcal{H}_{time} \otimes \mathcal{H}_{space} \otimes \mathcal{H}_{species} \otimes \mathcal{H}_{lattice} \otimes \mathcal{H}_{monomial}$  

---

## 1. Register Decomposition & Qubit Allocation

Let the total spatial lattice have $N = N_x \times N_y$ nodes, $Q = 9$ discrete velocities, $2$ distribution fields (hydrodynamic $g$ and phase-field $h$), Carleman truncation order $N_C = 2$ ($M = 1 + 18 = 19$ monomial subspaces: 1 linear + 18 quadratic pairs), and time horizon $T$.

The quantum register is structured as:
$$
|\Psi_{QLBM}\rangle = \sum_{t=0}^T \sum_{x=0}^{N_x-1} \sum_{y=0}^{N_y-1} \sum_{f \in \{g, h\}} \sum_{q=0}^8 \sum_{m=0}^{18} \mathcal{A}(t, x, y, f, q, m) |t\rangle |x\rangle |y\rangle |f\rangle |q\rangle |m\rangle
$$

### Quantum Register Breakdown
| Register Name | Physical Meaning | Dimension | Qubits Required |
| :--- | :--- | :---: | :---: |
| $|t\rangle$ | Time-step coordinate | $T + 1$ | $n_t = \lceil \log_2(T + 1) \rceil$ |
| $|x\rangle, |y\rangle$ | Spatial node coordinate $\mathbf{x} = (x, y)$ | $N_x \times N_y = N$ | $n_s = \lceil \log_2(N_x) \rceil + \lceil \log_2(N_y) \rceil$ |
| $|f\rangle$ | Physical species (0 for $g$, 1 for $h$) | 2 | $n_f = 1$ |
| $|q\rangle$ | D2Q9 lattice velocity direction $0 \dots 8$ | 9 | $n_q = 4$ |
| $|m\rangle$ | Carleman monomial index ($0 = \text{linear}$, $1 \dots 18 = \text{quadratic monomial}$) | 19 | $n_m = 5$ |
| $|a\rangle$ | Block-encoding ancilla register | 2 | $n_a = 1$ |

**Total Logical Qubit Requirement**:
$$
n_{total} = n_t + n_s + n_f + n_q + n_m + n_a = \lceil \log_2(T+1) \rceil + \lceil \log_2(N) \rceil + 11
$$

---

## 2. Amplitude Normalization & Physical Field Mapping

In quantum mechanics, all physical state vectors must satisfy unit $L_2$ normalization:
$$
\langle \Psi_{QLBM} | \Psi_{QLBM} \rangle = \sum_{t, \mathbf{x}, f, q, m} |\mathcal{A}(t, \mathbf{x}, f, q, m)|^2 = 1.0
$$

Let the classical physical state vector at time $t$ be $\mathbf{Y}(t) \in \mathbb{R}^{342 N}$ with Euclidean norm $\|\mathbf{Y}(t)\|_2$.
The quantum amplitude encodes the normalized classical value:
$$
\mathcal{A}(t, \mathbf{x}, f, q, m) = \frac{Y_{f, q, m}(\mathbf{x}, t)}{\mathcal{N}_{total}}, \quad \mathcal{N}_{total} = \sqrt{\sum_{t=0}^T \|\mathbf{Y}(t)\|_2^2}
$$

### Extraction of Physical Observables from Amplitudes
1. **Order Parameter $\phi(\mathbf{x}, t)$**:
   $$ \phi(\mathbf{x}, t) = \sum_{q=0}^8 h_q(\mathbf{x}, t) = \mathcal{N}_{total} \sum_{q=0}^8 \mathcal{A}(t, \mathbf{x}, f=1, q, m=0) $$
2. **Macroscopic Density $\rho(\mathbf{x}, t)$**:
   $$ \rho(\mathbf{x}, t) = \rho_G + (\rho_L - \rho_G) \phi(\mathbf{x}, t) $$
3. **Macroscopic Hydrodynamic Momentum $\rho \mathbf{u}(\mathbf{x}, t)$**:
   $$ \rho \mathbf{u}(\mathbf{x}, t) = \mathcal{N}_{total} \sum_{q=0}^8 \mathbf{c}_q \mathcal{A}(t, \mathbf{x}, f=0, q, m=0) + \frac{\Delta t}{2} \mathbf{F}(\mathbf{x}, t) $$
4. **Hydrodynamic Pressure $p(\mathbf{x}, t)$**:
   $$ p(\mathbf{x}, t) = \rho(\mathbf{x}, t) c_s^2 \left( \mathcal{N}_{total} \sum_{q=0}^8 \mathcal{A}(t, \mathbf{x}, f=0, q, m=0) \right) $$

---

## 3. Important Quantum Reality: The Output Data Bottleneck

> [!WARNING]
> A quantum state $|\Psi_{QLBM}\rangle$ does **NOT** provide instant simultaneous classical access to all $342 \times N \times T$ discrete variables.
> To reconstruct the entire flow field classically would require $\mathcal{O}(342 N T)$ quantum measurement shots, completely erasing any quantum speedup.
> Quantum advantage is **only** physically realizable when querying **global macroscopic or regional engineering observables** (e.g. surge front position, total fluid mass, average wall impact force) via quantum amplitude estimation / Hadamard test with $\mathcal{O}(1/\epsilon_{stat})$ shots.
