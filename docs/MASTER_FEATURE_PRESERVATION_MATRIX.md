# MASTER FEATURE PRESERVATION MATRIX
## Comprehensive Status Across All Research Components

$$\begin{array}{|l|l|l|l|c|l|}
\hline
\textbf{Feature} & \textbf{First Phase} & \textbf{Best Known Implementation} & \textbf{Scientific Status} & \textbf{In Tree?} & \textbf{Preservation Role} \\
\hline
\text{D2Q9 BGK Classical LBM} & \text{Level 4} & \texttt{classical/level4\_two\_phase.py} & \mathbf{ACTIVE\ REF} & \checkmark & \text{Physical ground truth} \\
\text{Martin-Moyce Benchmark} & \text{Level 4} & \texttt{classical/level4\_two\_phase.py} & \mathbf{ACTIVE\ REF} & \checkmark & \text{Experimental comparison} \\
\text{Level-6B Hybrid Baseline} & \text{Level 6B} & \texttt{quantum/level6b\_hybrid\_solver.py} & \mathbf{FROZEN\ REF} & \checkmark & \text{Frozen baseline (SHA-256)} \\
\text{Direct State Preparation} & \text{Phase 1} & \texttt{quantum/f33\_state\_preparation.py} & \mathbf{ACTIVE\ VAL} & \checkmark & 100\%\text{ fidelity Pauli-}X\text{ prep} \\
\text{Reversible Streaming} & \text{Phase 1} & \texttt{quantum/streaming.py} & \mathbf{ACTIVE\ VAL} & \checkmark & \text{Exact SWAP network} \\
\text{Bounce-Back Boundary Mask} & \text{Phase F10} & \texttt{quantum/physical\_boundary\_mask.py} & \mathbf{ACTIVE\ VAL} & \checkmark & \text{Arbitrary wall geometry} \\
\text{Carleman Linearization} & \text{Phase F15} & \texttt{quantum/f15\_carleman\_collision.py} & \mathbf{REJECTED} & \checkmark & \text{Carleman failure proof} \\
\text{Reversible Arithmetic} & \text{Phase F17} & \texttt{quantum/f17\_reversible\_collision.py} & \mathbf{EXPERIMENTAL} & \checkmark & \text{Fixed-point arithmetic} \\
\text{BGK Bijectivity Proof} & \text{Phase F18} & \texttt{docs/F18\_FORENSIC\_VALIDATION.md} & \mathbf{FORENSIC\ REF} & \checkmark & \text{Non-injectivity theorem} \\
\text{CPTP Stinespring Channel} & \text{Phase F22} & \texttt{quantum/f22\_stinespring.py} & \mathbf{ACTIVE\ REF} & \checkmark & \text{Open-system dilation} \\
\text{Reversible CSF Channel} & \text{Phase F21} & \texttt{quantum/f21\_csf.py} & \mathbf{ACTIVE\ REF} & \checkmark & \text{Surface tension channel} \\
\text{Scalable Gate Circuit} & \text{Phase F29} & \texttt{quantum/f29\_scalable\_circuit.py} & \mathbf{ACTIVE\ VAL} & \checkmark & C^{-1}C=I\text{ on } 4\times 4 \dots 16\times 16 \\
\text{Resource-Reduced Arch} & \text{Phase F31} & \texttt{quantum/f31\_reduced\_architecture.py} & \mathbf{ACTIVE\ VAL} & \checkmark & -22.2\%\text{ qubits, } -28.0\%\text{ Toffolis} \\
\text{NISQ Hardware Demo} & \text{Phase F33} & \texttt{quantum/f33\_hardware\_demo.py} & \mathbf{ACTIVE\ DEMO} & \checkmark & 127\text{Q FakeSherbrooke emulation} \\
\text{Live QPU Gateway} & \text{Phase F38} & \texttt{quantum/f38\_qpu\_executor.py} & \mathbf{ACTIVE\ GATE} & \checkmark & \text{Guarded cloud execution} \\
\hline
\end{array}$$
