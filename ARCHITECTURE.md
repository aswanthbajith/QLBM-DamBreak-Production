# SYSTEM ARCHITECTURE: HYBRID QUANTUM-CLASSICAL CARLEMAN QLBM

**Architecture Type**: Hybrid Quantum-Classical Carleman Lattice Boltzmann Method  
**Target Flow**: 2D Two-Phase Liquid-Gas Dam-Break Hydrodynamics (D2Q9 Lattice)  
**Primary Modules**: `classical/`, `quantum/`, `backends/`, `hardware/`  

---

## 1. Complete Hybrid Quantum-Classical Multi-Step Pipeline

```text
                         ┌──────────────────────┐
                         │ Classical Dam-Break  │
                         │ Initial Fields       │
                         │ f_i(x,y), g_i(x,y)   │
                         └──────────┬───────────┘
                                    │
                                    ▼
             ┌─────────────────────────────────────────┐
             │ Independent Distribution-Selector       │
             │ Amplitude Encoding                      │
             │  |x,y,i,s=0⟩ -> sqrt(f_i / M)           │
             │  |x,y,i,s=1⟩ -> sqrt(g_i / M)           │
             │  M = sum [f_i + g_i]                    │
             └────────────────────┬────────────────────┘
                                  │
                                  ▼
             ┌─────────────────────────────────────────┐
             │ Local Physical State: Ψ ∈ ℝ^18          │
             │ Quadratic Lift:       Y₂ = [Ψ; Ψ⊗Ψ]     │
             │ (342 components per node)               │
             └────────────────────┬────────────────────┘
                                  │
                                  ▼
             ┌─────────────────────────────────────────┐
             │ 10-Qubit Power-of-Two Block Encoding    │
             │  A_eval = [M₁, M₂] ∈ ℝ^(18×342)        │
             │  Padded to 512×512 (2^9 state space)   │
             │  Sz.-Nagy Unitary Dilation:             │
             │  U_C ∈ 𝕌(1024 = 2^10)                   │
             │  Ancilla |0⟩ Postselection -> Ψ* ∈ ℝ^18 │
             └────────────────────┬────────────────────┘
                                  │
                                  ▼
             ┌─────────────────────────────────────────┐
             │ Physical Positivity Guard               │
             │ (Classical numerical admissibility)     │
             └────────────────────┬────────────────────┘
                                  │
                                  ▼
             ┌─────────────────────────────────────────┐
             │ Body Force Update                       │
             │ Δf_i = 3 w_i (ρ - ρ_gas) g_y c_iy       │
             └────────────────────┬────────────────────┘
                                  │
                                  ▼
             ┌─────────────────────────────────────────┐
             │ Reversible Spatial Streaming S          │
             │ |x,y,i,s⟩ -> |(x+cx) mod Nx, (y+cy) mod Ny, i, s⟩
             │ (Exact 512-dim permutation: S† S = I)   │
             └────────────────────┬────────────────────┘
                                  │
                                  ▼
             ┌─────────────────────────────────────────┐
             │ Boundary Bounce-Back Involution B       │
             │ |x_b,y_b,i,s⟩ <-> |x_b,y_b,opposite(i),s⟩
             │ (Direction-selective: B² = I, B† B = I) │
             └────────────────────┬────────────────────┘
                                  │
                                  ▼
             ┌─────────────────────────────────────────┐
             │ Observable Decoding & Moment Reduction  │
             │  ρ(x,y) = sum f_i                       │
             │  φ(x,y) = sum g_i                       │
             │  u(x,y) = (1/ρ) sum c_i f_i             │
             └────────────────────┬────────────────────┘
                                  │
                                  ▼
             ┌─────────────────────────────────────────┐
             │ Re-encode Next Timestep (t + 1)         │
             │ (Reconstruct Ψ and Y₂ from observables) │
             └─────────────────────────────────────────┘
```

---

## 2. Rigorous Operator Unitarity on the Full 512-Qubit Hilbert Space

On the 9-qubit Hilbert space ($\dim \mathcal{H} = 2^9 = 512$), the 288 physical fluid states ($4 \times 4 \times 9 \times 2$) and 224 padding states are evolved by strictly unitary operators:

### A. Streaming Permutation Operator $S$ on $\mathcal{H}_{512}$
* **Physical subspace**: $S |x, y, v, s\rangle = |(x + c_{vx}) \bmod N_x, (y + c_{vy}) \bmod N_y, v, s\rangle$
* **Padding subspace ($v \ge 9$)**: $S |x, y, v, s\rangle = |x, y, v, s\rangle$
* **Unitarity**: Machine-precision unitary:
  $$\|S^\dagger S - I_{512}\|_2 = 0.000000$$

### B. Boundary Bounce-Back Involution $B$ on $\mathcal{H}_{512}$
* **Wall-hitting boundary subspace**: $B |x_b, y_b, v, s\rangle = |x_b, y_b, \bar{v}, s\rangle$ for all $(x_b, y_b, v)$ where $\mathbf{c}_v$ points into a solid wall.
* **Interior and non-hitting subspace**: $B |x, y, v, s\rangle = |x, y, v, s\rangle$
* **Involution Property**:
  $$B = B^\dagger, \quad B^2 = I_{512}, \quad \|B^\dagger B - I_{512}\|_2 = 0.000000, \quad \|B^2 - I_{512}\|_2 = 0.000000$$

### C. Spatial Composition $U_{\text{spatial}} = B \cdot S$
* The composition of separate streaming and wall reflection is strictly unitary:
  $$U_{\text{spatial}}^\dagger U_{\text{spatial}} = S^\dagger B^\dagger B S = S^\dagger I S = S^\dagger S = I_{512}$$
  $$\|U_{\text{spatial}}^\dagger U_{\text{spatial}} - I_{512}\|_2 = 0.000000$$

### D. Local Carleman Block Encoding $U_C$ on $\mathcal{H}_{1024}$
* Step-evaluation operator $A_{\text{eval}} = [M_1, M_2] \in \mathbb{R}^{18 \times 342}$ is padded to $512 \times 512$ ($2^9$) and normalized ($\bar{A} = \widetilde{A} / \alpha$).
* Sz.-Nagy unitary dilation constructs $U_C \in \mathbb{U}(1024 = 2^{10})$:
  $$\|U_C^\dagger U_C - I_{1024}\|_2 = 3.50 \times 10^{-14}$$
* Unscaled postselection $\alpha \langle 0_{\text{anc}}| U_C |0_{\text{anc}}, Y_{512}\rangle_{[:18]}$ reproduces the exact second-order polynomial map $A_{\text{eval}} \mathbf{Y}_2$ to machine precision ($4.16 \times 10^{-17}$).

---

## 3. Hardware Execution & Transpilation Status (`hardware/`)
* **Target Architecture**: IBM Quantum 127Q Heavy-Hex (`generic_backend_127q`).
* **Circuit Parameters**: 10 logical qubits, transpiled depth: 76,459 gates, 2-qubit CX/ECR gates: 21,133.
* **Dual-Lock Safety Interlock**: Requires `QLBM_ENABLE_REAL_QPU=1` and `QLBM_CONFIRM_REAL_QPU=YES`.
* **Hardware Execution Verdict**: **PREPARED / TRANSPILED; NOT EXECUTED ON REAL QPU.**
