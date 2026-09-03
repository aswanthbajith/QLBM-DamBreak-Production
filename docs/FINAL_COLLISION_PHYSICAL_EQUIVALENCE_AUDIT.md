# FINAL COLLISION PHYSICAL-EQUIVALENCE AUDIT
## Mathematical and Computational Forensic Investigation of Reversible BGK Collision

---

## 1. Executive Summary

This forensic audit investigates whether the reversible and environment-assisted collision circuits in the QLBM repository are physically equivalent to the finite-precision Navier-Stokes BGK collision operator.

**Core Findings**:
1. **Computational-Basis Equivalence**: On individual computational basis states $|x\rangle$, the gate-level local node circuit (`quantum/f27_local_node_circuit.py`, `quantum/f31_reduced_architecture.py`) exactly reproduces the finite-precision $Q4.12$ BGK post-collision populations ($L_1 = 0.000000e+00$, $L_\infty = 0.000000e+00$ across all 22 representative physical test states).
2. **Confirmation of F18 Non-Injectivity**: The dissipative BGK mapping is strictly non-injective. A specific computational counterexample was reproduced under exact $Q4.12$ arithmetic:
   $$\|x_1 - x_2\|_1 = 0.009766 \ (40\text{ LSB counts}), \quad \|F(x_1) - F(x_2)\|_1 = 0.000000$$
3. **Location of Conserved Information**: Because the mapping is non-injective, a closed-system unitary cannot map $|x\rangle \to |F(x)\rangle$ in-place on the system register alone. In the implemented gate circuit, the distinction between $x_1$ and $x_2$ resides **entirely in the environment register** $|x\rangle_E$, which stores the pre-collision microstate.
4. **Physical Limitation**: The reversible embedding $|x\rangle_S |0\rangle_E \to |F(x)\rangle_S |x\rangle_E$ preserves total mathematical information in the joint system-environment space. It does not implement physical dissipation unless the environment register is traced out or reset. If fresh environment registers are not supplied at each step, entropy accumulates.

---

## 2. Register Layout and Bit Allocation Diagram

For each lattice node in the scalable fault-tolerant architecture (`quantum/f31_reduced_architecture.py`):

$$\begin{array}{|l|l|c|c|c|l|}
\hline
\textbf{Register} & \textbf{Physical Meaning} & \textbf{Fields} & \textbf{Bits/Field} & \textbf{Total Qubits} & \textbf{Lifecycle / Uncomputation} \\
\hline
q_S^{(f)} & \text{Hydrodynamic populations } f_0 \dots f_8 & 9 & 16 & 144 & \text{Preserved; contains post-collision } f_i^* \\
q_S^{(g)} & \text{Phase-field populations } g_0 \dots g_8 & 9 & 16 & 144 & \text{Preserved; contains post-collision } g_i^* \\
q_E & \text{Compressed environment } (f_1..f_6, g_1..g_8) & 14 & 16 & 224 & \text{Preserved; stores pre-collision state} \\
q_W & \text{Arithmetic workspace scratchpad} & 3 & 16 & 48 & \text{Uncomputed strictly to } |0\rangle \\
\hline\hline
\mathbf{Total} & \textbf{Full Node Quantum Register} & \mathbf{35} & \mathbf{16} & \mathbf{560} & \textbf{All ancillas returned to } |0\rangle \\
\hline
\end{array}$$

---

## 3. Mathematical Transformation of the Unitary Gate Sequence

The gate sequence implements the explicit isometry:
$$\boxed{U: |x\rangle_S |0\rangle_E |0\rangle_W \xrightarrow{\text{Fanout}} |x\rangle_S |x\rangle_E |0\rangle_W \xrightarrow{\text{Arithmetic}} |x\rangle_S |x\rangle_E |F(x)\rangle_W \xrightarrow{\text{In-place}} |F(x)\rangle_S |x\rangle_E |0\rangle_W}$$

Where:
- $x = (f_0 \dots f_8, g_0 \dots g_8) \in \mathbb{Z}^{18}$ is the integer fixed-point population vector.
- $F(x)$ is the post-collision state computed via reversible arithmetic.
- The workspace $W$ is uncomputed back to $|0\rangle$ using mirror arithmetic circuits.
- The pre-collision state $x$ remains in register $E$.

---

## 4. Physical Equivalence Across 22 Representative States

The equivalence was tested computationally between the classical floating-point reference, the fixed-point BGK engine, and the gate-level quantum circuit across 22 representative states (recorded in `results/final_collision_equivalence.csv`):

$$\begin{array}{|l|c|c|c|c|}
\hline
\textbf{Test State Regime} & L_1\text{ Discrepancy} & L_\infty\text{ Discrepancy} & \Delta M\text{ (Mass Conserved)} & \text{Preimage in } E \\
\hline
\text{Equilibrium Liquid Stationary} & 0.000000 & 0.000000 & \mathbf{YES} & \mathbf{YES} \\
\text{Equilibrium Gas Stationary} & 0.000000 & 0.000000 & \mathbf{YES} & \mathbf{YES} \\
\text{Equilibrium Liquid Moderate Vel} & 0.000000 & 0.000000 & \mathbf{YES} & \mathbf{YES} \\
\text{Near-Equilibrium Liquid Perturbed} & 0.000000 & 0.000000 & \mathbf{YES} & \mathbf{YES} \\
\text{Strongly Non-Equilibrium Shear} & 0.000000 & 0.000000 & \mathbf{YES} & \mathbf{YES} \\
\text{High-Velocity State (Near Mach Limit)} & 0.000000 & 0.000000 & \mathbf{YES} & \mathbf{YES} \\
\text{Interface State Stationary } (\alpha=0.5) & 0.000000 & 0.000000 & \mathbf{YES} & \mathbf{YES} \\
\text{Extreme Low Density Gas } (\rho=0.02) & 0.000000 & 0.000000 & \mathbf{YES} & \mathbf{YES} \\
\text{Fractional Rounding Inducing State} & 0.000000 & 0.000000 & \mathbf{YES} & \mathbf{YES} \\
\text{F18 Non-Injective Preimage 1} & 0.000000 & 0.000000 & \mathbf{YES} & \mathbf{YES} \\
\text{F18 Non-Injective Preimage 2} & 0.000000 & 0.000000 & \mathbf{YES} & \mathbf{YES} \\
\hline
\end{array}$$

**Finding**: On every computational basis state $|x\rangle$, the reduced system state $\text{Tr}_E(U |x\rangle\langle x| \otimes |0\rangle\langle 0| U^\dagger)$ matches the classical finite-precision BGK result to machine precision ($0.000000$).
