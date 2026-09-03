# PROFESSOR RESEARCH GUIDE
## Forensic Technical Summary of the Quantum Two-Phase Dam-Break LBM Project

---

### 1. What problem is being solved?
The transient fluid dynamics of a 2D two-phase dam break: the gravitational collapse of a high-density liquid column into an air reservoir bounded by no-slip solid walls, governed by the Navier-Stokes equations with interfacial surface tension (CSF).

### 2. What classical method is used?
The Lattice Boltzmann Method (LBM) on a D2Q9 lattice using a two-distribution approach: $f_i$ for hydrodynamic momentum/density transport and $g_i$ for conservative phase-field interface capturing, combined with BGK collision and Guo body forcing.

### 3. Why LBM?
LBM replaces nonlinear advection PDEs ($\mathbf{u} \cdot \nabla \mathbf{u}$) with linear, exact spatial streaming along discrete lattice vectors $\mathbf{c}_i$, confining nonlinearity strictly to local algebraic collisions.

### 4. Why quantum LBM?
Quantum computers excel at exact spatial permutations (streaming is a unitary SWAP network on quantum wires, $S^\dagger S = I$) and boundary reflections (bounce-back is a Pauli involution, $B^2 = I$).

### 5. What was implemented?
1. Classical high-fidelity Level-4 solver (`classical/level4_two_phase.py`).
2. Hybrid Level-6B local Carleman solver (`quantum/level6b_hybrid_solver.py`, SHA-256 frozen).
3. Gate-level reversible arithmetic QLBM circuits in $Q4.16$ with Stinespring environment registers (`quantum/f29_scalable_circuit.py`, `quantum/f31_reduced_architecture.py`).
4. Condensed 16-qubit NISQ hardware demonstrator transpiled to 127-qubit IBM Heavy-Hex topology (`quantum/f33_hardware_demo.py`, `quantum/f38_qpu_executor.py`).

### 6. What was validated?
- Martin & Moyce (1952) physical dam-break benchmark ($<3.8\%$ surge error).
- Exact gate-level reversibility ($C^{-1} C = I$) across $4\times 4, 8\times 8, 16\times 16$ meshes.
- 127-qubit noisy hardware emulation (`FakeSherbrooke`, SNR $> 15$).

### 7. What failed?
Finite-order Carleman linearization (Level-6A & Phase F15) broke down due to second-order truncation closure failure ($>1400\%$ error accumulation over multiple timesteps) and block-encoding dilation leakage.

### 8. Why did Carleman fail as a complete solution?
Truncating polynomial powers at order 2 neglects higher-order hydrodynamic correlations, causing unphysical energy growth unless artificial classical re-lifting and clipping are applied at every timestep.

### 9. What did F18 reveal about BGK reversibility?
Discrete dissipative BGK collision is strictly non-injective (multiple pre-collision velocities relax to the identical equilibrium state). Therefore, an in-place closed-system unitary $|x\rangle \to |F(x)\rangle$ is mathematically impossible; it fundamentally requires an open-system CPTP Stinespring dilation with an environment register $|x\rangle_S |0\rangle_E \to |F(x)\rangle_S |E(x)\rangle_E$.

### 10. What is the final architecture?
A discrete computational-basis open-system quantum circuit where the full timestep is unitary:
$$U_{\text{step}} = U_{\text{boundary}} \cdot U_{\text{stream}} \cdot U_{\text{collision}} \cdot U_{\text{force}}$$
with non-equilibrium modes absorbed by environment registers, and measurement performed strictly at $t = T$.

### 11. What is genuinely quantum?
- Deterministic Pauli-$X$ state preparation ($U_{\text{prep}}$).
- Entangling 2Q collision ($V$) and cross-node controlled-phase surface tension coupling.
- Unitary SWAP coordinate streaming ($S$).
- Pauli bounce-back wall reflection involutions ($B$).

### 12. What remains hybrid?
- Initial parameter selection and grid sizing.
- Terminal observable readout decoding from sampled bitstrings into macroscopic fields.

### 13. What can run today?
1. Ideal quantum statevector simulation (Mode A).
2. 127-qubit noisy hardware emulation on `FakeSherbrooke` (Mode B).
3. Physical Heavy-Hex ISA transpilation and depth profiling (Mode C).
4. Scalable fault-tolerant reversible circuit validation on $4\times 4 \dots 16\times 16$ meshes.

### 14. What has run on real hardware?
Real QPU cloud execution has NOT occurred because authenticated IBM Quantum cloud credentials are not configured in the local execution environment. The engine is verified and guarded with double opt-in safety checks (`QLBM_ENABLE_REAL_QPU=1`).

### 15. What is the next research step?
Configure a live IBM Quantum cloud API token in the environment and submit the existing, pre-compiled, 19-layer, 16-ECR circuit to `ibm_sherbrooke` for physical quantum processor execution.
