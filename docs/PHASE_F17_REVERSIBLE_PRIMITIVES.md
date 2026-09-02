# PHASE F17: REVERSIBLE QUANTUM ARITHMETIC PRIMITIVES
## Gate-Level Modules: CDKM Adders, Non-Restoring Dividers, and Barenco Multipliers

**Document**: Reversible Arithmetic Primitives & Gate Synthesis Specification  
**Project**: Quantum Lattice Boltzmann Method (QLBM) for Two-Phase Flow  
**Repository**: `/home/aswa/Research/QLBM-DamBreak-Production`  
**Branch**: `feature/direct-encoding-two-phase-qlbm`  
**Date**: September 2026  

---

## 1. Reversible Primitive Modules

$$\begin{array}{|l|l|c|c|c|}
\hline
\textbf{Primitive Module} & \textbf{Reversible Logic} & \textbf{Toffoli Count} & \textbf{T-Gate Count} & \textbf{Ancillas} \\
\hline
\text{1. In-Place Adder} & (a, b) \mapsto (a, a + b) & 16 & 112 & 1 \\
\text{2. In-Place Subtractor} & (a, b) \mapsto (a, b - a) & 16 & 112 & 1 \\
\text{3. Fixed-Point Multiplier} & (a, b, 0) \mapsto (a, b, \lfloor \frac{ab}{2^F} \rfloor) & 256 & 1,792 & 16 \\
\text{4. Reversible Divider} & (a, b, 0) \mapsto (a, b, \lfloor \frac{a \cdot 2^F}{b} \rfloor) & 576 & 4,032 & 24 \\
\text{5. Linear Interpolator} & (f, f_{\text{eq}}, 0) \mapsto (f, f_{\text{eq}}, f + \omega(f_{\text{eq}}-f)) & 192 & 1,344 & 16 \\
\hline
\end{array}$$

Every primitive module is paired with an exact inverse operator $\mathcal{U}^\dagger$ guaranteeing 100% mirror uncomputation of intermediate work registers back to $|0\rangle$.
