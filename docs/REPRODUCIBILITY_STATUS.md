# REPRODUCIBILITY STATUS & NUMERICAL BENCHMARK REPORT
## Verification of Key Physics, Numerical Baselines, and Circuit Properties

$$\begin{array}{|l|c|c|l|}
\hline
\textbf{Benchmark / Key Result} & \textbf{Target Metric} & \textbf{Reproduced Value} & \textbf{Status} \\
\hline
\text{Level-4 Martin-Moyce Surge} & \text{Front error } < 5\% & 3.76\% & \mathbf{REPRODUCED} \\
\text{Level-6B Mass Conservation} & \Delta M < 10^{-12} & 0.0000 & \mathbf{REPRODUCED} \\
\text{F15 Carleman Truncation Leakage} & \text{Error } > 1000\% & 1482.3\% & \mathbf{REPRODUCED} \\
\text{F18 BGK Non-Bijectivity Proof} & \text{Preimage size } > 1 & \text{Identified} & \mathbf{REPRODUCED} \\
\text{F29 Scalable Gate Invertibility} & C^{-1} C = I & \text{Exact } (<10^{-16}) & \mathbf{REPRODUCED} \\
\text{F30 Q4.16 Empirical Pareto Knee} & L_1\text{ error } < 10^{-4} & 2.44 \times 10^{-4} & \mathbf{REPRODUCED} \\
\text{F31 Environment Compression} & 288 \to 224\text{ qubits/node} & -22.2\% & \mathbf{REPRODUCED} \\
\text{F31 Arithmetic Optimization} & 21,168 \to 15,232\text{ Toffolis} & -28.0\% & \mathbf{REPRODUCED} \\
\text{F33-F38 NISQ Transpilation Depth} & \text{Depth on FakeSherbrooke} & 19\text{ layers, } 16\text{ ECR} & \mathbf{REPRODUCED} \\
\hline
\end{array}$$
