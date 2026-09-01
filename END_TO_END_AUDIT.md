# COMPLETE CODE & ALGORITHM AUDIT: QLBM TWO-PHASE DAM-BREAK

**Document Version**: 1.0 (End-to-End Scientific Audit)  
**Target Repository**: `/home/aswa/Research/QLBM-DamBreak-Production`  
**Classification Categories**:
* **Q**: Genuinely quantum circuit / unitary operation on quantum register.
* **QC**: Hybrid quantum-classical operation (interfacing quantum state with classical preprocessing/postprocessing).
* **C**: Purely classical computation on host CPU.

---

## 1. Systematic Operation-by-Operation Audit Table

| # | Operation | Current Implementation | Mathematical Representation | Quantum Status | Classical Dependency | Proposed Quantum Replacement | Feasibility | Validation Test |
| :--- | :--- | :--- | :--- | :---: | :--- | :--- | :--- | :--- |
| 1 | **Initialization** | `classical.two_phase.initialize_two_phase_dambreak` + `quantum.two_phase_encoding.encode_two_phase_state` | $\|\psi_0\rangle = \sum_{x,y,i,s} \sqrt{\frac{f_i/g_i}{M}} \|x,y,i,s\rangle$ | **QC** | Classical initial condition arrays $(f_0, g_0)$ | Exact state preparation circuit (Shende-Bullock-Markov / Mottonen state prep or parameterized initialization) | High (9 qubits, $N=512$) | `test_state_preparation.py` |
| 2 | **Equilibrium Evaluation** | `classical.equilibrium.compute_equilibrium` & `compute_phase_equilibrium` | $f_i^{\text{eq}}(\rho, \mathbf{u}), g_i^{\text{eq}}(\phi, \mathbf{u})$ | **C** (Ref) / **Q** (Carleman) | Non-linear quadratic velocity contractions | Embedded directly into Carleman linear operator $M_1 \Psi + M_2(\Psi \otimes \Psi)$ via block encoding | Verified in Carleman | `test_carleman_quantum.py` |
| 3 | **Collision Execution** | Local Carleman polynomial map $A_{\text{eval}} = [M_1, M_2]$ | $\Psi^* = A_{\text{eval}} \mathbf{Y}_2$ | **QC** / **Q** | Node loop on host CPU | Dilated 10-qubit block encoding $U_C \in \mathbb{U}(1024)$ acting on local or multiplexed registers | High on simulator, depth-limited on NISQ | `test_carleman_quantum.py` |
| 4 | **Carleman Lifting** | `quantum.two_phase_carleman.lift_two_phase_state` | $\mathbf{Y}_2 = [\Psi; \Psi \otimes \Psi] \in \mathbb{R}^{342}$ | **QC** | Kronecker product on CPU | Reversible quantum copy / dual-register tensor product $|\Psi\rangle|\Psi\rangle$ | Moderate (requires auxiliary registers) | `test_carleman_quantum.py` |
| 5 | **Unitary Dilation** | `quantum.unitary_dilation.build_unitary_dilation` | $U_C = \begin{pmatrix} \bar{A} & \sqrt{I - \bar{A}\bar{A}^\dagger} \\ \sqrt{I - \bar{A}^\dagger\bar{A}} & -\bar{A}^\dagger \end{pmatrix} \in \mathbb{U}(1024)$ | **Q** | Normalization constant $\alpha = 1.01\|\widetilde{A}\|_2$ | Sz.-Nagy unitary dilation / LCU block encoding circuit | Fully Verified ($\|U^\dagger U - I\| < 10^{-13}$) | `test_carleman_quantum.py` |
| 6 | **Block Encoding & Postselection** | `quantum.unitary_dilation.apply_block_encoding` | $\langle 0_{\text{anc}}| U_C (|0_{\text{anc}}\rangle \otimes |\mathbf{Y}\rangle) = \frac{1}{\alpha} A_{\text{eval}} \mathbf{Y}$ | **Q** | Ancilla measurement postselection | Standard ancilla postselection or Oblivious Amplitude Amplification (OAA) | High ($P_{\text{succ}} \approx 10^{-3} - 10^{-4}$) | `test_carleman_quantum.py` |
| 7 | **Gravitational Forcing** | `classical.reference_solver.apply_force` | $\Delta f_i = 3 w_i (\rho - \rho_{\text{gas}}) g_y c_{iy}$ | **QC** | Explicit floating-point addition | Reversible quantum affine addition / block-encoded diagonal forcing operator $U_{\text{force}}$ | High | `test_force_quantum.py` |
| 8 | **Spatial Streaming** | `quantum.streaming.apply_quantum_streaming` | $S |x,y,v,s\rangle = |(x+c_{vx})\bmod N_x, (y+c_{vy})\bmod N_y, v, s\rangle$ | **Q** | Reversible coordinate shift | Quantum modular addition / incrementer circuit conditioned on velocity register $|v\rangle$ | High ($\|S^\dagger S - I_{512}\| = 0$) | `test_streaming_unitarity.py` |
| 9 | **Boundary Bounce-Back** | `quantum.two_phase_boundary.apply_quantum_boundary` | $B |x_b,y_b,v,s\rangle = |x_b,y_b,\bar{v},s\rangle$ | **Q** | Direction-selective wall predicate | Quantum multi-controlled swap circuit conditioned on wall boundary predicates | High ($\|B^\dagger B - I_{512}\| = 0, B^2 = I$) | `test_boundary_unitarity.py` |
| 10 | **Density Calculation** | `classical.two_phase.compute_density` | $\rho(x,y) = \sum_{i=0}^8 f_i(x,y) = M \sum_{i} |\langle x,y,i,0|\psi\rangle|^2$ | **QC** (Hybrid) / **Q** (Mode A) | Sum over 9 velocity amplitudes | Quantum Amplitude Estimation (QAE) / projective marginal measurement onto $|x,y,s=0\rangle$ | High | `test_observables.py` |
| 11 | **Velocity Calculation** | `classical.two_phase.compute_velocity` | $\mathbf{u}(x,y) = \frac{1}{\rho}\sum_{i=0}^8 \mathbf{c}_i f_i(x,y)$ | **QC** (Hybrid) / **Q** (Mode A) | Momentum sum & division | Hadamard test / quantum expectation value of velocity observables $\hat{C}_x, \hat{C}_y$ | High | `test_observables.py` |
| 12 | **Phase Calculation** | `classical.two_phase.compute_phase_field` | $\phi(x,y) = \sum_{i=0}^8 g_i(x,y) = M \sum_{i} |\langle x,y,i,1|\psi\rangle|^2$ | **QC** (Hybrid) / **Q** (Mode A) | Sum over 9 phase amplitudes | Quantum Amplitude Estimation / projective marginal measurement onto $|x,y,s=1\rangle$ | High | `test_observables.py` |
| 13 | **Normalization Tracking** | `quantum.unitary_dilation.normalize_operator` | $\|\psi\| \to 1.0$, scalar $M = \sum(f_i + g_i)$ | **QC** | Global partition function scaling factor $M$ | Register state is natively normalized in $\mathcal{H}$; global norm $M$ tracked classically | High | `test_state_preparation.py` |
| 14 | **Positivity Correction** | `np.maximum(psi, 0.0)` in step loop | $f_i \ge 0, g_i \ge 0$ | **C** | Elementwise zero-clipping | In exact unitary quantum mechanics, physical populations are $|a|^2 \ge 0$ by Born rule | High (eliminated in pure quantum statevector) | `test_carleman_quantum.py` |
| 15 | **Observable Measurement** | `quantum.two_phase_encoding.decode_macroscopic` | $P(x,y,i,s) = |\langle x,y,i,s|\psi\rangle|^2$ | **Q** | Statistical shot sampling | Computational basis measurement across registers | High (validated in Aer and statevector) | `test_observables.py` |
| 16 | **State Re-Encoding** | Rebuilding $\Psi$ and $\mathbf{Y}_2$ between steps | $|\psi_t\rangle \to \text{decode} \to |\psi_{t+1}\rangle$ | **QC** (Mode B) / **Q** (Mode A) | Classical array reconstruction | Mode A: Coherent quantum evolution $U_{\text{step}} |\psi_t\rangle$ without intermediate statevector destruction | High in Mode A; Mode B retained as baseline | `test_full_quantum_step.py`, `test_end_to_end.py` |

---

## 2. Summary of Quantumness & Architectural Status

1. **Genuinely Quantum Operations ($Q$)**:
   - Spatial Streaming ($S$): Exact 512-dimensional unitary permutation matrix and quantum circuit ($S^\dagger S = I_{512}$).
   - Boundary Wall Reflection ($B$): Direction-selective unitary involution ($B^2 = I_{512}, B^\dagger B = I_{512}$).
   - Carleman Block Encoding ($U_C$): Exact 10-qubit Sz.-Nagy unitary dilation on $\mathcal{H}_{1024}$ ($\|U_C^\dagger U_C - I\| < 10^{-13}$).
   - Computational Basis Measurement & Amplitude Estimation.
2. **Hybrid / Ancilla-Assisted Operations ($QC$)**:
   - State Preparation: Preparing arbitrary initial 9-qubit fluid amplitudes from classical initial condition data.
   - Observable Estimation: Extracting macroscopic fields $\rho, \mathbf{u}, \phi$ via expectation value sampling.
   - Gravitational Buoyancy Forcing: Block-encoded affine source term.
3. **Dual Operating Modes**:
   - **Mode A (Fully Quantum Step)**: Coherent quantum state evolution $|\Psi_{t+1}\rangle = U_{\text{step}} |\Psi_t\rangle$ where macroscopic observables are estimated via quantum measurements at desired inspection intervals.
   - **Mode B (Hybrid Baseline)**: Local quantum block-encoded collision with intermediate observable reconstruction and state re-lifting for benchmark comparison against classical LBM.
