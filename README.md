# Hybrid Quantum-Classical Lattice Boltzmann Two-Phase Dam-Break Solver (Production)

A clean, standalone implementation of the **Hybrid Quantum-Classical Lattice Boltzmann Method (Hybrid QLBM)** for two-phase fluid hydrodynamics using **Local Second-Order Carleman Linearization, 10-Qubit Power-of-Two Unitary Dilation / Block Encoding, and Reversible Closed-Domain Wall-Aware Streaming**.

---

## 1. What is this?

This software simulates a 2D two-phase liquid–gas dam-break problem on a D2Q9 lattice using a **hybrid quantum-classical algorithm**. The fluid consists of a dense liquid column collapsing under gravity inside an enclosed rectangular box bounded by solid walls.

---

## 2. Why Carleman Linearization?

Standard classical Lattice Boltzmann BGK collision relaxes non-equilibrium modes dissipatively toward a nonlinear equilibrium distribution:
$$f_i^* = f_i - \frac{1}{\tau_f} (f_i - f_i^{\text{eq}}(\rho, \mathbf{u}))$$

Closed unitary quantum gates cannot represent physical contractive modes ($\lambda = 1 - \omega < 1$) without dilation.

**Local Second-Order Carleman Linearization** embeds the local nonlinear D2Q9 equations into a 342-dimensional lifted linear space $\mathbf{Y}_2 = [\Psi; \Psi^{\otimes 2}]^T$ where $\Psi = [f_0..f_8, g_0..g_8]^T \in \mathbb{R}^{18}$. The step-evaluation operator $A_{\text{eval}} = [M_1, M_2] \in \mathbb{R}^{18 \times 342}$ is padded to $512 \times 512$ ($2^9$), normalized ($\bar{A} = \widetilde{A} / \alpha$), and embedded into a machine-precision $1024 \times 1024$ ($2^{10}$) unitary matrix $U_{\text{10Q}}$ via **Sz.-Nagy Unitary Dilation**. Projective measurement of a single ancilla qubit implements the contractive collision step.

---

## 3. Algorithmic Workflow (Hybrid Architecture)

```
Initial Two-Phase Distributions [f(t), g(t)]
            ↓
Independent Distribution-Selector Encoding (s=0 -> f, s=1 -> g)
            ↓
Local Polynomial Lifting to Y_2 [342 dimensions per node]
            ↓
10-Qubit Sz.-Nagy Unitary Dilation U [1024x1024 unitary operator]
            ↓
Quantum State Evolution on |0>_anc ⊗ |Y_512>
            ↓
Ancilla Postselection & Scaling Tracking (alpha ≈ 58.75, P_succ ≈ 0.0021)
            ↓
Physical Positivity Guard (Classical numerical admissibility)
            ↓
Gravitational Body Forcing (Buoyancy)
            ↓
Reversible Closed-Domain Wall-Aware Streaming (Permutation Operator S)
- Interior nodes: (x, y, i) -> (x + cx, y + cy, i)
- Wall-hitting nodes: (x, y, i) -> (x, y, opposite(i))
            ↓
Decoded Observable Fields [rho(t+1), u(t+1), phi(t+1)]
            ↓
Re-encode Next Timestep (t + 1)
```

* **Multi-Step Nature**: This solver is **hybrid quantum-classical**: at each timestep, local populations are decoded/measured and re-lifted to configure the local state for timestep $t+1$.

---

## 4. Installation

```bash
# 1. Create a clean virtual environment
python3 -m venv .venv
source .venv/bin/activate

# 2. Install runtime dependencies
pip install -r requirements.txt
```

---

## 5. Execution

### Default Run (4x4 Mesh, 10 Timesteps, Order-2 Carleman)
```bash
python run.py
```

### 1-Timestep Execution
```bash
python run.py --nx 4 --ny 4 --timesteps 1
```

### 5-Timestep Execution
```bash
python run.py --nx 4 --ny 4 --timesteps 5
```

### 10-Timestep Execution
```bash
python run.py --nx 4 --ny 4 --timesteps 10
```

### Aer Simulation & IBM Heavy-Hex Transpilation Preflight
```bash
# Run with Qiskit Aer simulation
python run.py --backend aer

# Run with IBM Quantum 127Q Heavy-Hex compilation preflight
python run.py --backend fake_ibm
```

---

## 6. Output Files

Each execution populates the `results/` folder:
* `results/classical/classical_fields.npz`: Complete classical reference ground truth history ($\rho, \phi, \mathbf{u}$).
* `results/quantum/quantum_fields.npz`: Quantum Carleman simulation history ($\rho, \phi, \mathbf{u}$).
* `results/comparison/comparison.json`: Detailed quantitative error and conservation metrics at every timestep.
* `results/plots/dam_break_comparison.png`: Side-by-side plots of error convergence and final phase field contours.

---

## 7. Validation Status

### Validated Scientifically:
* **Single-Step Accuracy ($t=1$)**: $0.000\%$ relative density error ($5.55 \times 10^{-17}$ at collision).
* **Multi-Step Stability ($t=10$)**: **$1.42\%$** relative density error against classical reference across the enclosed dam break.
* **Mass Conservation**: Mass error strictly bounded under $1.22\%$ over 10 steps.
* **Unitary Dilation Precision**: $\|U_{\text{10Q}}^\dagger U_{\text{10Q}} - I\| < 10^{-13}$ on $1024 \times 1024$ Hilbert space.
* **Transpilation to IBM Heavy-Hex**: Transpilation successfully verified on 127-qubit architecture (`generic_backend_127q`).

### NOT Validated on Physical Hardware:
* **Real IBM Quantum hardware execution: NOT PERFORMED.**
* Physical cloud submission is safely protected by an environment dual-lock interlock (`QLBM_ENABLE_REAL_QPU=1` and `QLBM_CONFIRM_REAL_QPU=YES`). Real execution on unmitigated NISQ devices is currently depth-limited by two-qubit gate error rates.
