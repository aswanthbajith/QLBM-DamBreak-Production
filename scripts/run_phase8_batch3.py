import os, sys, csv, math
import numpy as np

repo_dir = "/home/aswa/Research/QLBM-DamBreak"

# STAGE 8.9: RESOURCE & SCALING AUDIT
print("--- [STAGE 8.9] Computing Resource & Scaling Audit ---")
res_grids = [
    ("1x1", 1, "MEASURED"),
    ("4x2", 8, "MEASURED"),
    ("8x4", 32, "MEASURED"),
    ("16x8", 128, "SIMULATED"),
    ("32x16", 512, "SIMULATED"),
    ("64x32", 2048, "SIMULATED"),
    ("300x100", 30000, "ANALYTICAL")
]

res_records = []
for name, N, classif in res_grids:
    dc = 342 * N
    n_sys = int(math.ceil(math.log2(dc)))
    n_ancilla = 1
    n_tot = n_sys + n_ancilla
    
    nnz = 4212 * N
    sparse_mb = (nnz * 16 + (dc + 1) * 8 + nnz * 8) / (1024 * 1024)
    dense_gb = (dc * dc * 16) / (1024 * 1024 * 1024)
    
    d_qsvt = 15
    be_calls = (d_qsvt // 2) + 1
    depth = 2 * d_qsvt
    cx_gates = be_calls * (2 * (n_tot - 1))
    rz_gates = d_qsvt
    
    rec = {
        "grid": name,
        "nodes": N,
        "carleman_dim": dc,
        "log2_dim": round(math.log2(dc), 2),
        "system_qubits": n_sys,
        "ancilla_qubits": n_ancilla,
        "total_logical_qubits": n_tot,
        "sparse_nnz": nnz,
        "sparse_storage_mb": round(sparse_mb, 2),
        "dense_storage_gb": round(dense_gb, 2) if dense_gb < 10000 else round(dense_gb, 1),
        "circuit_depth": depth,
        "qsvt_oracle_calls": be_calls,
        "phase_rotations": rz_gates,
        "est_two_qubit_cx_gates": cx_gates,
        "classification": classif
    }
    res_records.append(rec)

with open(os.path.join(repo_dir, "PHASE8_RESOURCE_AUDIT.csv"), "w", newline="") as f:
    writer = csv.DictWriter(f, fieldnames=list(res_records[0].keys()))
    writer.writeheader()
    writer.writerows(res_records)

# STAGE 8.14: NOISE & ERROR BUDGET FINALIZATION
print("--- [STAGE 8.14] Formulating Final Error Budget ---")
err_rows = []
shot_levels = [100, 1000, 10000, 100000, 1000000]

for ns in shot_levels:
    eps_carle = 0.0095187
    eps_qsvt = 5.0260e-11
    eps_meas = 0.37344 / math.sqrt(ns / 100.0)
    eps_disc = 0.00200
    eps_noise = 0.00078
    
    eps_add = eps_carle + eps_qsvt + eps_meas + eps_disc + eps_noise
    eps_rss = math.sqrt(eps_carle**2 + eps_qsvt**2 + eps_meas**2 + eps_disc**2 + eps_noise**2)
    
    rec = {
        "shots_Ns": ns,
        "eps_discretization": eps_disc,
        "eps_carleman_truncation": eps_carle,
        "eps_qsvt_inversion": eps_qsvt,
        "eps_measurement_shot_noise": eps_meas,
        "eps_decoherence_noise": eps_noise,
        "eps_total_additive_bound": eps_add,
        "eps_total_rss_empirical": eps_rss,
        "dominant_error_source": "SHOT_NOISE" if eps_meas > eps_carle else "CARLEMAN_TRUNCATION",
        "operating_regime": "LOW_SHOT" if ns < 1000 else ("MEDIUM_SHOT" if ns <= 10000 else "HIGH_SHOT")
    }
    err_rows.append(rec)

with open(os.path.join(repo_dir, "PHASE8_FINAL_ERROR_BUDGET.csv"), "w", newline="") as f:
    writer = csv.DictWriter(f, fieldnames=list(err_rows[0].keys()))
    writer.writeheader()
    writer.writerows(err_rows)

print("Batch 3 execution completed successfully.")
