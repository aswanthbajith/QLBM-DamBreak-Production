#!/usr/bin/env python3
"""
Level-6 Comprehensive Resource Scaling Model.

Evaluates:
- Logical, Ancilla, and Total Qubits
- Carleman and Hilbert Space Dimensions
- Circuit Gate Counts and Depths
- Multi-Timestep QSVT Query Complexity
Across mesh resolutions (4x4 to 128x64) and timesteps (Nt = 1, 5, 10, 20).

Outputs: results/level6_resource_estimates.csv
"""

import os
import sys
import csv
import numpy as np

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))


def run_resource_modeling():
    results_dir = os.path.join(os.path.dirname(__file__), "../results")
    os.makedirs(results_dir, exist_ok=True)

    meshes = [
        {"name": "4x4", "nx": 4, "ny": 4},
        {"name": "8x8", "nx": 8, "ny": 8},
        {"name": "16x16", "nx": 16, "ny": 16},
        {"name": "32x16", "nx": 32, "ny": 16},
        {"name": "64x32", "nx": 64, "ny": 32},
        {"name": "128x64", "nx": 128, "ny": 64},
    ]

    timesteps_list = [1, 5, 10, 20]
    alpha_C = 5.319
    alpha_L = 2.92

    resource_records = []

    print("=" * 80)
    print("LEVEL-6 QUANTUM RESOURCE SCALING MODEL")
    print("=" * 80)

    for mesh in meshes:
        nx, ny = mesh["nx"], mesh["ny"]
        nodes = nx * ny
        nqx = int(np.ceil(np.log2(nx)))
        nqy = int(np.ceil(np.log2(ny)))

        # Architecture A (HQC)
        qubits_hqc = nqx + nqy + 4 + 1 + 1  # x + y + v + s + anc
        dim_hqc = 1 << qubits_hqc

        # Architecture B (Local Carleman)
        qubits_local_carleman = nqx + nqy + 5 + 5 + 1 + 1  # x + y + v1 + v2 + deg + anc
        dim_local_carleman = 1 << qubits_local_carleman

        # Decoupled Carleman physical dimension
        carleman_dim = 342 * nodes

        for Nt in timesteps_list:
            # Architecture C (Global QSVT)
            nq_time = int(np.ceil(np.log2(Nt + 1)))
            qubits_qsvt = nq_time + qubits_local_carleman
            dim_qsvt = 1 << qubits_qsvt

            # Condition number & QSVT query estimate
            kappa_L = 2.5 * Nt + 3.0
            qsvt_queries = int(np.ceil(alpha_L * kappa_L * np.log(1000.0) * np.sqrt(Nt)))

            # Gate counts estimates
            gates_hqc = Nt * (nodes * 350 + 200)
            gates_local_b = Nt * (nodes * 1200 + 450)
            gates_qsvt = qsvt_queries * (nodes * 1500 + 600)

            rec = {
                "mesh_name": mesh["name"],
                "nx": nx,
                "ny": ny,
                "nodes": nodes,
                "timesteps_Nt": Nt,
                "qubits_arch_A_hqc": qubits_hqc,
                "qubits_arch_B_local": qubits_local_carleman,
                "qubits_arch_C_qsvt": qubits_qsvt,
                "hilbert_dim_arch_A": dim_hqc,
                "hilbert_dim_arch_B": dim_local_carleman,
                "carleman_physical_dim": carleman_dim,
                "global_spacetime_dim": carleman_dim * (Nt + 1),
                "condition_number_L": round(kappa_L, 2),
                "qsvt_query_count": qsvt_queries,
                "estimated_gates_arch_A": gates_hqc,
                "estimated_gates_arch_B": gates_local_b,
                "estimated_gates_arch_C": gates_qsvt,
            }
            resource_records.append(rec)

    # Save CSV
    csv_path = os.path.join(results_dir, "level6_resource_estimates.csv")
    with open(csv_path, "w", newline="") as f:
        writer = csv.DictWriter(f, fieldnames=list(resource_records[0].keys()))
        writer.writeheader()
        writer.writerows(resource_records)
    print(f"[+] Saved Level-6 Resource Estimates CSV to: {csv_path}")

    # Print summary
    print(f"\n{'Mesh':<8} | {'Nodes':<6} | {'Nt':<4} | {'Qubits (A/B/C)':<16} | {'Carleman Dim':<14} | {'cond(L)':<8} | {'QSVT Queries'}")
    print("-" * 80)
    for r in resource_records:
        if r["timesteps_Nt"] in [1, 10]:
            q_str = f"{r['qubits_arch_A_hqc']}/{r['qubits_arch_B_local']}/{r['qubits_arch_C_qsvt']}"
            print(f"{r['mesh_name']:<8} | {r['nodes']:<6} | {r['timesteps_Nt']:<4} | {q_str:<16} | {r['carleman_physical_dim']:<14} | {r['condition_number_L']:<8.2f} | {r['qsvt_query_count']}")
    print("=" * 80)


if __name__ == "__main__":
    run_resource_modeling()
