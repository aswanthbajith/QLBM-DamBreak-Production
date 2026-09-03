# PHASE F31: PRE-IMPLEMENTATION AUDIT & RESOURCE-REDUCTION RESEARCH FRAMEWORK
## Systematic Optimization of Gate-Level Reversible Two-Phase QLBM Architecture

**Document**: Pre-Implementation Resource Reduction Audit  
**Project**: Quantum Lattice Boltzmann Method (QLBM) for Two-Phase Flow  
**Repository**: `/home/aswa/Research/QLBM-DamBreak-Production`  
**Development Branch**: `feature/direct-encoding-two-phase-qlbm`  
**Checkpoint Commit**: `8797c32`  
**Baseline Level-6B SHA-256**: `2a306f5a413945adc1acd10f3f63340c3d3617e4ef1c94981a92e8ebad8742c8` (**100% Intact**)  
**Audit Date**: September 2026  

---

## 1. Baseline State & Safety Verification

- **Active Development Branch**: `feature/direct-encoding-two-phase-qlbm`
- **Current Milestone**: `8797c32` (*"QLBM: scaling and resource validation"*)
- **Baseline Test Suite**: **292 / 292 Tests Passing (100%)** in $394.80\text{s}$.
- **Read-Only Archive**: `/home/aswa/Research/QLBM-DamBreak` (**Untouched on `master`**).
- **Professor Release Branch**: `professor/final-research-code` (**Frozen**).

---

## 2. Baseline Resource Model (F30 $Q4.12$ Reference)

$$\begin{array}{|l|c|l|}
\hline
\textbf{Resource Metric} & \textbf{Baseline Value} & \textbf{Physical / Algorithmic Role} \\
\hline
\text{System Population Qubits } (Q_{\text{sys}}) & 288\text{ qubits/node} & 18\text{ populations } (9 f_i + 9 g_i) \times 16\text{ bits} \\
\text{Environment Preimage Qubits } (Q_{\text{env}}) & 288\text{ qubits/node} & 18\text{ pre-collision fields } \times 16\text{ bits (Stinespring dilation)} \\
\text{Shared Sequential Workspace } (Q_{\text{work}}) & 48\text{ qubits/core} & 3\text{ words } \times 16\text{ bits (sequential scratchpad)} \\
\textbf{Total Peak Logical Qubits / Node} & \mathbf{624\text{ qubits/node}} & \mathbf{Baseline\ per-node\ memory\ footprint} \\
\hline
\text{Moment Accumulation} & 256\text{ Toffolis} & \text{Summation of density and momentum} \\
\text{Velocity Division (Reciprocal)} & 3,584\text{ Toffolis} & \text{Newton-Raphson reciprocal + momentum multiply} \\
\text{Reversible CSF Stencils} & 4,864\text{ Toffolis} & \text{Gradient norms, curvature, and surface force} \\
\text{Symmetric Equilibrium} & 3,584\text{ Toffolis} & \text{D2Q9 velocity invariants and quadratic bracket} \\
\text{BGK Relaxation \& Guard} & 8,880\text{ Toffolis} & \text{Linear interpolation and } f_0 \text{ mass guard} \\
\textbf{Total Toffoli Count / Node / Step} & \mathbf{21,168\text{ Toffolis}} & \mathbf{Baseline\ arithmetic\ cost\ per\ step} \\
\hline
\end{array}$$

---

## 3. Phase F31 Research Hypotheses & Targets

1. **Environment Compression**: Can $Q_{\text{env}}$ be reduced below $288\text{ qubits/node}$ by encoding non-equilibrium deviations $\delta f_i = f_i - f_i^{\text{eq}}$ or collision-class preimages?
2. **BGK & Equilibrium Arithmetic Optimization**: Can common factor elimination, shift-fused additions, and symmetric grouping reduce BGK Toffolis by $>20\%$?
3. **Workspace Reduction**: Can the peak workspace be compressed from $48\text{ qubits} \to 32\text{ qubits}$ via tighter uncomputation schedules?
4. **Combined Architecture Reduction**: What is the overall percentage reduction in qubits and gates for $4\times 4, 8\times 8$, and $128\times 64$ meshes?
