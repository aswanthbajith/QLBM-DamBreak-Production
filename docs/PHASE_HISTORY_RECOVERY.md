# COMPLETE PHASE HISTORY RECOVERY
## Chronological Evolution of the Two-Phase Dam-Break QLBM Project

$$\begin{array}{|l|l|l|l|l|}
\hline
\textbf{Phase / Milestone} & \textbf{Branch} & \textbf{Key Commit} & \textbf{Primary Contribution} & \textbf{Scientific Status} \\
\hline
\text{Baseline v0} & \text{main} & \texttt{bfa9eda} & \text{Initial simplified classical \& quantum pipeline} & \text{Archived} \\
\text{Classical Validated} & \text{development} & \texttt{0779537} & \text{Validated D2Q9 classical LBM solver} & \text{Reference} \\
\text{Level 3 Baseline} & \text{development} & \texttt{7b7aad0} & \text{Historical research lineage integration (Phases 1-15)} & \text{Archived} \\
\text{Level 4 Two-Phase} & \text{development} & \texttt{30807c7} & \text{Level-4 solver, Martin-Moyce } (<3.8\%\text{ error}) & \mathbf{ACTIVE\ REF} \\
\text{Level 5 Formulation} & \text{level5} & \texttt{69fc877} & \text{Quantum two-phase mathematical derivation} & \text{Archived} \\
\text{Level 6 Architecture} & \text{level6} & \texttt{d8454e2} & \text{23-dimension architecture decision matrix} & \text{Archived} \\
\text{Level 6A Carleman} & \text{level6a} & \texttt{ef1d9b7} & \text{Lifted Carleman collision \& streaming} & \text{Archived} \\
\text{Level 6A-S Analysis} & \text{level6a} & \texttt{d871f4f} & \text{Isolated spatial lifting \& block leakage} & \text{Forensic Ref} \\
\text{Level 6B Hybrid K=1} & \text{level6b} & \texttt{064e67a} & \text{Stable physical hybrid baseline (SHA-256 frozen)} & \mathbf{FROZEN\ REF} \\
\text{Level 7 Coherent} & \text{level7} & \texttt{50f579c} & \text{Coherent multi-step investigation \& OAA audit} & \text{Experimental} \\
\text{Phase 1-2 Direct} & \text{direct-enc} & \texttt{a854e2c} & \text{Direct spatial/population encoding architecture} & \text{Validated} \\
\text{Phase F8-F12} & \text{direct-enc} & \texttt{2bbd45f} & 2\times 2\text{ end-to-end solver, boundary masks} & \text{Validated} \\
\text{Phase F13-F14} & \text{direct-enc} & \texttt{95bc106} & \text{Fully coherent quantum prototype audit} & \text{Forensic Ref} \\
\text{Phase F15 Carleman} & \text{direct-enc} & \texttt{6feb817} & \text{Carleman autonomous collision attempt} & \mathbf{REJECTED} \\
\text{Phase F17 Reversible} & \text{direct-enc} & \texttt{6bf7d3a} & \text{Reversible arithmetic collision solver} & \text{Experimental} \\
\text{Phase F18 Bijectivity} & \text{direct-enc} & \texttt{c3dbc6c} & \text{Proved BGK non-injectivity requires dilation} & \mathbf{FORENSIC\ REF} \\
\text{Phase F19-F23 CPTP} & \text{direct-enc} & \texttt{b167943} & \text{CPTP Stinespring dilation \& CSF channel} & \mathbf{ACTIVE\ REF} \\
\text{Phase F27-F29 Circuit} & \text{direct-enc} & \texttt{f90e503} & \text{Scalable gate-level reversible circuit } (C^{-1}C=I) & \mathbf{ACTIVE\ VAL} \\
\text{Phase F30 Scaling} & \text{direct-enc} & \texttt{8797c32} & 128\times 64\text{ scaling sweep \& } Q4.16\text{ precision Pareto} & \mathbf{ACTIVE\ VAL} \\
\text{Phase F31 Reduction} & \text{direct-enc} & \texttt{cc3eef3} & -22.2\%\text{ qubits, } -28.0\%\text{ Toffolis architecture} & \mathbf{ACTIVE\ VAL} \\
\text{Phase F33-F38 NISQ} & \text{direct-enc} & \texttt{a42040a} & \text{127Q FakeSherbrooke emulation \& real QPU gate} & \mathbf{ACTIVE\ DEMO} \\
\hline
\end{array}$$
