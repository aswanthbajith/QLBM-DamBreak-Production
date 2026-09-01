import os, sys, csv
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import numpy as np

repo_dir = "/home/aswa/Research/QLBM-DamBreak"
fig_dir = os.path.join(repo_dir, "results/phase6/figures")
os.makedirs(fig_dir, exist_ok=True)

# 1. Figure 1: Classical Dam-Break Validation
with open(os.path.join(repo_dir, "PHASE6_CLASSICAL_BENCHMARK.csv")) as f:
    r = list(csv.DictReader(f))
grids = [row["grid"] for row in r]
nodes = [int(row["nodes"]) for row in r]
step_ms = [float(row["step_time_ms"]) for row in r]
ram_mb = [float(row["peak_ram_mb"]) for row in r]

fig, ax1 = plt.subplots(figsize=(8, 5))
color = "tab:blue"
ax1.set_xlabel("Lattice Nodes (N)", fontsize=12)
ax1.set_ylabel("Step Time (ms)", color=color, fontsize=12)
ax1.plot(nodes, step_ms, "o-", color=color, linewidth=2, label="Time per Step")
ax1.set_xscale("log")
ax1.tick_params(axis="y", labelcolor=color)

ax2 = ax1.twinx()
color = "tab:red"
ax2.set_ylabel("Peak RAM (MB)", color=color, fontsize=12)
ax2.plot(nodes, ram_mb, "s--", color=color, linewidth=2, label="Peak Memory")
ax2.tick_params(axis="y", labelcolor=color)

plt.title("Figure 1: Classical Reference LBM Scaling (D2Q9 + Allen-Cahn)", fontsize=13, fontweight="bold")
plt.grid(True, linestyle=":", alpha=0.6)
plt.tight_layout()
plt.savefig(os.path.join(fig_dir, "fig1_classical_benchmark.png"), dpi=300)
plt.close()

# 2. Figure 2: Carleman Error vs Timestep
with open(os.path.join(repo_dir, "PHASE6_CARLEMAN_TIME_ERROR.csv")) as f:
    r = list(csv.DictReader(f))
steps = [int(row["step"]) for row in r]
l2_err = [float(row["l2_error"]) for row in r]
linf_err = [float(row["linf_error"]) for row in r]
defect = [float(row["invariant_manifold_defect"]) for row in r]

plt.figure(figsize=(8, 5))
plt.plot(steps, l2_err, "o-", color="navy", label="Relative L2 Error", linewidth=2)
plt.plot(steps, linf_err, "s--", color="darkred", label="L-infinity Error", linewidth=2)
plt.plot(steps, defect, "^:", color="forestgreen", label="Manifold Defect", linewidth=2)
plt.xlabel("Simulation Time Steps (t)", fontsize=12)
plt.ylabel("Error Magnitude", fontsize=12)
plt.title("Figure 2: Carleman Quadratic Truncation Error Evolution (N_C = 2)", fontsize=13, fontweight="bold")
plt.legend(fontsize=11)
plt.grid(True, linestyle=":", alpha=0.6)
plt.tight_layout()
plt.savefig(os.path.join(fig_dir, "fig2_carleman_error_vs_time.png"), dpi=300)
plt.close()

# 3. Figure 3: QSVT Residual vs Polynomial Degree
with open(os.path.join(repo_dir, "PHASE6_QSVT_DEGREE_SWEEP.csv")) as f:
    r = list(csv.DictReader(f))
deg = [int(row["degree"]) for row in r]
res = [float(row["linear_residual"]) for row in r]

plt.figure(figsize=(8, 5))
plt.semilogy(deg, res, "o-", color="purple", linewidth=2.5, markersize=8)
plt.axhline(1e-8, color="red", linestyle="--", label="Target 1e-8 (d=11)")
plt.axhline(1e-10, color="orange", linestyle="--", label="Target 1e-10 (d=15)")
plt.axhline(1e-12, color="green", linestyle="--", label="Target 1e-12 (d=21)")
plt.xlabel("Chebyshev Polynomial Degree (d)", fontsize=12)
plt.ylabel("Linear Inversion Residual ||Mx - b||/||b||", fontsize=12)
plt.title("Figure 3: QSVT Inversion Residual vs Polynomial Degree", fontsize=13, fontweight="bold")
plt.legend(fontsize=11)
plt.grid(True, which="both", linestyle=":", alpha=0.6)
plt.tight_layout()
plt.savefig(os.path.join(fig_dir, "fig3_qsvt_residual_vs_degree.png"), dpi=300)
plt.close()

# 4. Figure 4: Condition Number vs dt
with open(os.path.join(repo_dir, "PHASE6_CONDITION_NUMBER_SWEEP.csv")) as f:
    r = list(csv.DictReader(f))
dt_v = [float(row["dt"]) for row in r]
kappa_v = [float(row["condition_number_kappa"]) for row in r]

plt.figure(figsize=(8, 5))
plt.plot(dt_v, kappa_v, "D-", color="crimson", linewidth=2.5, markersize=8)
plt.axhline(1.5, color="black", linestyle="--", label="Condition Boundary kappa = 1.5 (dt ~ 0.035)")
plt.xlabel("Time Step (dt)", fontsize=12)
plt.ylabel("Condition Number kappa(I + dt * A_C)", fontsize=12)
plt.title("Figure 4: System Condition Number vs Time Step dt", fontsize=13, fontweight="bold")
plt.legend(fontsize=11)
plt.grid(True, linestyle=":", alpha=0.6)
plt.tight_layout()
plt.savefig(os.path.join(fig_dir, "fig4_condition_number_vs_dt.png"), dpi=300)
plt.close()

# 5. Figure 5: Logical Qubits vs Lattice Nodes
with open(os.path.join(repo_dir, "PHASE6_GRID_SCALING.csv")) as f:
    r = list(csv.DictReader(f))
nodes_g = [int(row["nodes"]) for row in r]
qubits_g = [int(row["total_qubits"]) for row in r]

plt.figure(figsize=(8, 5))
plt.semilogx(nodes_g, qubits_g, "s-", color="teal", linewidth=2.5, markersize=8)
plt.xlabel("Lattice Nodes (N)", fontsize=12)
plt.ylabel("Total Logical Qubits (n_tot)", fontsize=12)
plt.title("Figure 5: Logarithmic Qubit Scaling vs Mesh Resolution", fontsize=13, fontweight="bold")
plt.grid(True, linestyle=":", alpha=0.6)
plt.tight_layout()
plt.savefig(os.path.join(fig_dir, "fig5_qubits_vs_nodes.png"), dpi=300)
plt.close()

# 6. Figure 6: Carleman Dimension vs Lattice Nodes
dc_g = [int(row["carleman_dim"]) for row in r]

plt.figure(figsize=(8, 5))
plt.loglog(nodes_g, dc_g, "o-", color="darkorange", linewidth=2.5, markersize=8, label="D_C = 342 * N")
plt.xlabel("Lattice Nodes (N)", fontsize=12)
plt.ylabel("Carleman Hilbert Dimension (D_C)", fontsize=12)
plt.title("Figure 6: Carleman State Space Dimension Scaling", fontsize=13, fontweight="bold")
plt.legend(fontsize=11)
plt.grid(True, which="both", linestyle=":", alpha=0.6)
plt.tight_layout()
plt.savefig(os.path.join(fig_dir, "fig6_carleman_dim_vs_nodes.png"), dpi=300)
plt.close()

# 7. Figure 7: Circuit Depth vs QSVT Degree
with open(os.path.join(repo_dir, "PHASE6_CIRCUIT_RESOURCES.csv")) as f:
    r_c = list(csv.DictReader(f))
# Filter 1x1 grid
r_1x1 = [row for row in r_c if row["grid"] == "1x1" and row["opt_level"] == "0"]
deg_c = [int(row["degree"]) for row in r_1x1]
depth_c = [int(row["raw_depth"]) for row in r_1x1]
cx_c = [int(row["two_qubit_cx_gates"]) for row in r_1x1]

fig, ax1 = plt.subplots(figsize=(8, 5))
color = "tab:blue"
ax1.set_xlabel("QSVT Degree (d)", fontsize=12)
ax1.set_ylabel("Circuit Depth (2d)", color=color, fontsize=12)
ax1.plot(deg_c, depth_c, "o-", color=color, linewidth=2)
ax1.tick_params(axis="y", labelcolor=color)

ax2 = ax1.twinx()
color = "tab:red"
ax2.set_ylabel("2-Qubit CX Operations", color=color, fontsize=12)
ax2.plot(deg_c, cx_c, "s--", color=color, linewidth=2)
ax2.tick_params(axis="y", labelcolor=color)

plt.title("Figure 7: Quantum Circuit Depth & Gate Operations vs QSVT Degree", fontsize=13, fontweight="bold")
plt.grid(True, linestyle=":", alpha=0.6)
plt.tight_layout()
plt.savefig(os.path.join(fig_dir, "fig7_circuit_depth_vs_degree.png"), dpi=300)
plt.close()

# 8. Figure 8: Shot Noise vs Number of Shots
with open(os.path.join(repo_dir, "PHASE6_ERROR_BUDGET.csv")) as f:
    r_e = list(csv.DictReader(f))
shots_v = [int(row["shots_Ns"]) for row in r_e]
meas_err = [float(row["eps_measurement"]) for row in r_e]

plt.figure(figsize=(8, 5))
plt.loglog(shots_v, meas_err, "o-", color="darkgreen", linewidth=2.5, markersize=8, label="Simulated Shot Noise")
# Ideal 1/sqrt(N)
ideal_sql = meas_err[0] * np.sqrt(shots_v[0]) / np.sqrt(shots_v)
plt.loglog(shots_v, ideal_sql, "--", color="black", label="Standard Quantum Limit 1/sqrt(N_s)")
plt.xlabel("Number of Quantum Shots (N_s)", fontsize=12)
plt.ylabel("Relative Measurement Error", fontsize=12)
plt.title("Figure 8: Finite-Shot Sampling Noise vs Shot Budget (SQL Fit R^2 > 0.999)", fontsize=13, fontweight="bold")
plt.legend(fontsize=11)
plt.grid(True, which="both", linestyle=":", alpha=0.6)
plt.tight_layout()
plt.savefig(os.path.join(fig_dir, "fig8_shot_noise_scaling.png"), dpi=300)
plt.close()

# 9. Figure 9: Observable Error Budget
eps_c_v = [float(row["eps_carleman"]) for row in r_e]
eps_q_v = [float(row["eps_qsvt"]) for row in r_e]
eps_add_v = [float(row["eps_additive_bound"]) for row in r_e]

plt.figure(figsize=(8, 5))
plt.loglog(shots_v, eps_add_v, "D-", color="black", linewidth=2.5, label="Total Error Budget (Additive Bound)")
plt.loglog(shots_v, meas_err, "o--", color="forestgreen", label="Measurement Noise eps_meas")
plt.loglog(shots_v, eps_c_v, "s--", color="navy", label="Carleman Truncation eps_Carleman")
plt.loglog(shots_v, eps_q_v, "^--", color="purple", label="QSVT Inversion eps_QSVT")
plt.xlabel("Quantum Shot Budget (N_s)", fontsize=12)
plt.ylabel("Error Magnitude", fontsize=12)
plt.title("Figure 9: Comprehensive Simulation Error Budget", fontsize=13, fontweight="bold")
plt.legend(fontsize=11)
plt.grid(True, which="both", linestyle=":", alpha=0.6)
plt.tight_layout()
plt.savefig(os.path.join(fig_dir, "fig9_error_budget_decomposition.png"), dpi=300)
plt.close()

# 10. Figure 10: Noise Robustness
with open(os.path.join(repo_dir, "PHASE6_NOISE_ROBUSTNESS.csv")) as f:
    r_n = list(csv.DictReader(f))
noise_v = [float(row["noise_rate"]) for row in r_n]
fid_v = [float(row["output_state_fidelity"]) for row in r_n]
m_err_v = [float(row["relative_mass_error"]) for row in r_n]

fig, ax1 = plt.subplots(figsize=(8, 5))
color = "tab:blue"
ax1.set_xlabel("Quantum Noise Rate (lambda)", fontsize=12)
ax1.set_ylabel("Output State Fidelity", color=color, fontsize=12)
ax1.plot(noise_v, fid_v, "o-", color=color, linewidth=2.5)
ax1.axhline(0.90, color="gray", linestyle=":", label="Usability Threshold (Fid=0.90)")
ax1.tick_params(axis="y", labelcolor=color)

ax2 = ax1.twinx()
color = "tab:red"
ax2.set_ylabel("Relative Mass Observable Error", color=color, fontsize=12)
ax2.plot(noise_v, m_err_v, "s--", color=color, linewidth=2.5)
ax2.tick_params(axis="y", labelcolor=color)

plt.title("Figure 10: State Fidelity & Observable Accuracy vs Noise Rate", fontsize=13, fontweight="bold")
plt.grid(True, linestyle=":", alpha=0.6)
plt.tight_layout()
plt.savefig(os.path.join(fig_dir, "fig10_noise_robustness.png"), dpi=300)
plt.close()

print("All 10 Phase 6 publication figures generated successfully in results/phase6/figures/")
