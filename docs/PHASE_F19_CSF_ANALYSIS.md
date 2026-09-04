# PHASE F19: CONTINUUM SURFACE FORCE (CSF) AUDIT
## Interfacial Surface Tension, Curvature Stencils, and Quantum Circuit Feasibility

---

## 1. Classical Formulation of CSF
Interfacial surface tension is represented via the Continuum Surface Force (CSF) of Brackbill et al. (1992):
$$\mathbf{F}_s(\mathbf{x}) = \sigma \kappa(\mathbf{x}) \nabla \alpha(\mathbf{x})$$
where:
- $\sigma$ is the physical surface tension coefficient ($\sigma > 0$).
- $\nabla \alpha$ is the gradient of the conservative phase field $\alpha$.
- $\kappa$ is the local interface curvature, defined as the divergence of the unit interface normal:
  $$\mathbf{n} = \frac{\nabla \alpha}{|\nabla \alpha| + \epsilon}, \quad \kappa = -\nabla \cdot \mathbf{n} = -\left[ \frac{\partial n_x}{\partial x} + \frac{\partial n_y}{\partial y} \right]$$

---

## 2. Forensic Audit Across Architectural Tiers

$$\begin{array}{|l|c|l|l|}
\hline
\textbf{Implementation Tier} & \sigma\text{ Value} & \text{Curvature Stencil } \kappa & \text{Implementation Classification} \\
\hline
\text{Classical Level-4 Reference} & \sigma = 0.001 & 9\text{-point isotropic finite difference} & \mathbf{VALIDATED\ (Exact\ Classical)} \\
\text{Hybrid Level-6B Baseline} & \sigma = 0.001 & \text{Classical parameter bus / Carleman block} & \mathbf{VALIDATED\ (Hybrid\ Control)} \\
\text{Reversible FTQC (F27/F31)} & \sigma = 0.0 & \text{Excluded from integer arithmetic} & \mathbf{REVERSIBLE\ ARITHMETIC\ (\sigma=0)} \\
\text{NISQ Demonstrator (F38)} & \text{Qualitative} & \text{Cross-node controlled-phase (CZ) gate} & \mathbf{NISQ\ QUALITATIVE\ COUPLING} \\
\text{Proposed F19-A Architecture} & \sigma > 0 & \text{Multi-node quantum stencil circuit} & \mathbf{THEORETICAL\ PROSPECTIVE} \\
\hline
\end{array}$$

---

## 3. Quantum Feasibility of Full CSF Curvature Stencils

To compute $\mathbf{F}_s = \sigma \kappa \nabla \alpha$ autonomously within a quantum circuit without measurement, the circuit must execute:
1. **Gradient Extraction**: 9-point spatial finite-difference stencils coupling neighbor nodes on quantum wires.
2. **Euclidean Normalization**: $|\nabla \alpha| = \sqrt{(\partial_x \alpha)^2 + (\partial_y \alpha)^2}$ via reversible square-root and reciprocal circuits.
3. **Divergence of Normal**: Second-order finite differences across neighboring nodes.
4. **Coupled Momentum Injection**: Adding the resulting vector force $\mathbf{F}_s$ to the conserved momentum registers $j_x, j_y$.

### Stencil Complexity:
Evaluating $\kappa$ on a $Q4.16$ integer register requires at least:
- 16 quantum spatial shifts across adjacent nodes.
- 2 reversible squarers, 1 reversible square root, and 1 reciprocal divider per node.
- Estimated gate overhead: $\approx 18,500$ Toffoli gates per node per timestep.

---

## 4. Truth-in-Advertising Verdict on CSF

$$\boxed{\text{Verdict: FULL AUTONOMOUS QUANTUM CSF IS NOT YET DEMONSTRATED.}}$$
The autonomous NISQ circuit implements qualitative controlled-phase pinning, while the FTQC reversible circuit executed with $\sigma = 0$. Full high-fidelity surface tension remains active exclusively within the validated classical Level-4 and hybrid Level-6B solvers.
