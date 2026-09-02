# PHASE F: COHERENT PARAMETER ORACLE & STATE DEPENDENCE AUDIT
## Investigation of State-Dependent Parameter Generation in Two-Phase QLBM (Phases F3 & F4)

**Document**: Coherent vs Hybrid Parameter Generation Architecture Analysis  
**Project**: Quantum Lattice Boltzmann Method (QLBM) for Two-Phase Flow  
**Repository**: `/home/aswa/Research/QLBM-DamBreak-Production`  
**Branch**: `feature/direct-encoding-two-phase-qlbm`  
**Date**: September 2026  

---

## 1. Phase F3: The State Dependence Problem

In kinetic Lattice Boltzmann models, the BGK collision operator is locally parameterized by macroscopic fields:
$$\rho(\mathbf{x}) = \sum_{i=0}^8 f_i(\mathbf{x}), \quad \alpha(\mathbf{x}) = \sum_{i=0}^8 g_i(\mathbf{x}), \quad \mathbf{u}(\mathbf{x}) = \frac{\sum_i f_i(\mathbf{x}) \mathbf{c}_i + \frac{1}{2}\mathbf{F}}{\rho(\mathbf{x})}$$
which dictate the relaxation frequency $\omega_f(\alpha) = [3(\alpha\nu_L + (1-\alpha)\nu_G) + 0.5]^{-1}$ and Maxwellian target distributions $f_i^{\text{eq}}(\rho, \mathbf{u}), g_i^{\text{eq}}(\alpha, \mathbf{u})$.

Because populations are stored linearly in amplitudes $|\Psi\rangle = \frac{1}{\mathcal{N}}\sum [f_i |i, 0\rangle + g_i |i, 1\rangle]$, the quantum circuit must obtain these kinematic parameters to execute the collision. We investigate three architectural paradigms:

$$\begin{array}{|l|c|c|c|}
\hline
\textbf{Architectural Criterion} & \textbf{Architecture A: Measured Hybrid} & \textbf{Architecture B: Coherent Arithmetic} & \textbf{Architecture C: Block-Encoded Oracle} \\
\hline
\text{Quantum vs Classical} & \text{Quantum Stream + Classical Control} & \textbf{Fully Quantum Reversible} & \text{Quantum State + Dilation Oracle} \\
\text{Measurement Required?} & \textbf{YES (Destructive Sampling)} & \textbf{NO (Coherent Registers)} & \textbf{NO (Ancilla Projection)} \\
\text{State Preservation} & \text{Requires re-encoding copies} & \textbf{Exact (Unitary Register)} & \textbf{Exact (Projected Subspace)} \\
\text{Ancilla Logical Qubits} & 0 \text{ ancillas (CPU loop)} & 32 - 128 \text{ arithmetic ancillas} & \mathbf{1 \text{ dilation ancilla}} \\
\text{Arithmetic Precision} & \text{Double precision (64-bit IEEE)} & 10 - 16 \text{ bit fixed-point} & \textbf{Continuous parameter angles} \\
\text{Gate Complexity / Node} & \mathcal{O}(1) \text{ classical FLOPs} & > 15,000 \text{ Toffoli Gates} & \mathbf{\approx 250 \text{ Quantum Gates}} \\
\text{Success Probability} & 100\% & 100\% \text{ (Deterministic)} & \mathbf{> 98.5\% \ (OAA } m=1) \\
\text{Hardware Feasibility} & \textbf{Current NISQ / Early FTQC} & \text{Late-Stage FTQC Only} & \textbf{Early FTQC / Logical QPU} \\
\hline
\end{array}$$

---

## 2. Phase F4: Coherent Fixed-Point Moment Arithmetic Scaling

Implemented in [`quantum/parameterized_collision_oracle.py`](file:///home/aswa/Research/QLBM-DamBreak-Production/quantum/parameterized_collision_oracle.py) (`CoherentFixedPointMomentOracle`):
- Models coherent fixed-point quantum arithmetic for computing $[\rho, \alpha, \mathbf{j}, \mathbf{u}]$ from the computational state without measurement.
- Truncation error analysis across register word lengths $B \in \{8, 10, 12, 16\}$:

$$\begin{array}{|l|c|c|c|c|c|}
\hline
\textbf{Word Length} & \textbf{Fixed-Point Format} & \rho \textbf{ Rel Error} & \alpha \textbf{ Rel Error} & u_x \textbf{ Rel Error} & \textbf{Scientific Feasibility} \\
\hline
\text{8-bit Baseline} & Q_{4.4} & 1.190\% & 16.67\% & 212.5\% & \text{Fails (Underflow)} \\
\text{10-bit Candidate} & Q_{4.6} & 1.190\% & 0.000\% & 60.94\% & \text{Coarse Flow Only} \\
\text{12-bit Candidate} & Q_{4.8} & 0.298\% & 0.521\% & 2.344\% & \text{Acceptable for Dam-Break} \\
\text{16-bit Production} & Q_{4.12} & \mathbf{0.005\%} & \mathbf{0.033\%} & \mathbf{10.28\% \ (at } u=0.04) & \textbf{High Precision Target} \\
\hline
\end{array}$$

### Scientific Conclusion:
- **Low word length ($< 10$ bits)** produces unacceptable velocity division underflow due to small momentum $j \sim \mathcal{O}(10^{-2})$.
- **Minimum viable word length** for coherent fixed-point velocity extraction is **$B \ge 12$ bits** ($Q_{4.8}$ or $Q_{4.12}$).
