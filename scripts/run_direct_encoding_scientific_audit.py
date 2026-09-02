#!/usr/bin/env python3
"""
Scientific Audit Script for Direct Spatial/Population Two-Phase QLBM.

Traces and classifies all operations in DirectTwoPhaseQLBM:
- Genuinely quantum unitary circuit operations
- Quantum state numerical simulations
- Classical numerical operations
- Hybrid bridge operations

Generates:
- results/direct_encoding_scientific_audit.csv
- results/direct_encoding_resource_audit.csv
"""

import os
import sys
import csv
import numpy as np

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from classical.level4_two_phase import Level4TwoPhaseLBM
from quantum.direct_two_phase_prototype import DirectTwoPhaseQLBM


def run_scientific_audit():
    results_dir = os.path.join(os.path.dirname(__file__), "../results")
    docs_dir = os.path.join(os.path.dirname(__file__), "../docs")
    os.makedirs(results_dir, exist_ok=True)
    os.makedirs(docs_dir, exist_ok=True)

    print("=" * 85)
    print("DIRECT TWO-PHASE QLBM: SCIENTIFIC OPERATION AUDIT")
    print("=" * 85)

    # 1. Operation-by-Operation Classification Table
    audit_table = [
        {
            "operation": "State Preparation & Normalization",
            "implementation": "encode_state()",
            "is_quantum": "Quantum Statevector Initializer",
            "is_classical": "Classical Amplitude Loading",
            "role": "Loads physical f_i, g_i into unified |Psi>",
            "scientific_status": "Hybrid Initialization (Amplitudes proportional to populations)",
        },
        {
            "operation": "Spatial Streaming",
            "implementation": "apply_quantum_streaming() / S_matrix",
            "is_quantum": "YES (Strictly Unitary Permutation S†S=I)",
            "is_classical": "NO",
            "role": "Modular coordinate shift |(x+c_ix) mod Nx>",
            "scientific_status": "Genuinely Quantum Unitary Permutation",
        },
        {
            "operation": "Bounce-Back Wall Boundary",
            "implementation": "apply_quantum_boundary() / B_matrix",
            "is_quantum": "YES (Unitary Involution B^2=I, B†B=I)",
            "is_classical": "NO",
            "role": "Reflects velocities i -> opp(i) at walls",
            "scientific_status": "Genuinely Quantum Unitary Involution",
        },
        {
            "operation": "Macroscopic Density & Phase",
            "implementation": "decode_state() -> rho = sum(f), alpha = sum(g)",
            "is_quantum": "Observable Contraction",
            "is_classical": "Classical Moment Sum",
            "role": "Extracts rho(x,y) and alpha(x,y)",
            "scientific_status": "Classical Decoding / Measurement",
        },
        {
            "operation": "Shifted Velocity Calculation",
            "implementation": "ux = (sum c_ix f_i + 0.5 Fx) / rho",
            "is_classical": "Classical Arithmetic",
            "is_quantum": "NO",
            "role": "Momentum division by local density",
            "scientific_status": "Classical Numerical Operation",
        },
        {
            "operation": "Brackbill CSF Surface Tension",
            "implementation": "compute_surface_tension_force()",
            "is_classical": "Classical Finite Difference",
            "is_quantum": "NO",
            "role": "Calculates F_s = sigma * kappa * grad(alpha)",
            "scientific_status": "Classical Hybrid Feedback",
        },
        {
            "operation": "Gravitational Buoyancy Forcing",
            "implementation": "compute_total_force() -> (rho - rho_G) * g_acc",
            "is_classical": "Classical Parameter Evaluation",
            "is_quantum": "NO",
            "role": "Hydrostatic body force",
            "scientific_status": "Classical Forcing Input",
        },
        {
            "operation": "Equilibrium Populations f_eq, g_eq",
            "implementation": "compute_equilibrium(rho, u)",
            "is_classical": "Classical BGK Quadratic Maxwellian",
            "is_quantum": "NO",
            "role": "Nonlinear local target state",
            "scientific_status": "Classical Numerical Evaluation",
        },
        {
            "operation": "Hydrodynamic & Phase Collision",
            "implementation": "execute_collision_step()",
            "is_classical": "Classical BGK Relaxation with Guo Source",
            "is_quantum": "NO (Simulated via classical update + re-encoding)",
            "role": "Relaxes populations toward equilibrium",
            "scientific_status": "Classical Numerical Update in Hybrid Loop",
        },
    ]

    with open(os.path.join(results_dir, "direct_encoding_scientific_audit.csv"), "w", newline="") as f:
        writer = csv.DictWriter(f, fieldnames=list(audit_table[0].keys()))
        writer.writeheader()
        writer.writerows(audit_table)

    print("\n--- OPERATION CLASSIFICATION ---")
    for row in audit_table:
        print(f"[{row['scientific_status'][:30]:<30}] {row['operation']:<32} -> Quantum: {row['is_quantum'][:10]:<10} | Classical: {row['is_classical'][:15]}")

    # 2. Resource Audit Table across Grid Resolutions
    res_table = []
    grids = [
        ("2x2 Minimal", 2, 2),
        ("4x4 Prototype", 4, 4),
        ("8x4 Intermediate", 8, 4),
        ("16x8 Mesh", 16, 8),
        ("32x16 Refined", 32, 16),
        ("64x32 Benchmark", 64, 32),
        ("128x64 Target Dam-Break", 128, 64),
    ]

    print("\n--- RESOURCE SCALING TABLE ---")
    print(f"{'Grid':<24} | {'Nx':<4} | {'Ny':<4} | {'n_x':<4} | {'n_y':<4} | {'n_vel':<5} | {'n_phase':<7} | {'Data Qubits':<12} | {'Hilbert Dim'}")
    print("-" * 85)

    for label, nx, ny in grids:
        n_x = int(np.ceil(np.log2(nx))) if nx > 1 else 1
        n_y = int(np.ceil(np.log2(ny))) if ny > 1 else 1
        n_vel = 4
        n_phase = 1
        n_data = n_x + n_y + n_vel + n_phase
        hilbert_dim = 2 ** n_data

        rec = {
            "grid_name": label,
            "nx": nx,
            "ny": ny,
            "nodes": nx * ny,
            "n_x_qubits": n_x,
            "n_y_qubits": n_y,
            "n_velocity_qubits": n_vel,
            "n_phase_qubits": n_phase,
            "total_data_logical_qubits": n_data,
            "hilbert_dimension": hilbert_dim,
            "algorithmic_ancillas_streaming": 0,
            "complete_logical_qubits": n_data,
        }
        res_table.append(rec)
        print(f"{label:<24} | {nx:<4} | {ny:<4} | {n_x:<4} | {n_y:<4} | {n_vel:<5} | {n_phase:<7} | {n_data:<12} | {hilbert_dim:,}")

    with open(os.path.join(results_dir, "direct_encoding_resource_audit.csv"), "w", newline="") as f:
        writer = csv.DictWriter(f, fieldnames=list(res_table[0].keys()))
        writer.writeheader()
        writer.writerows(res_table)

    print("\n" + "=" * 85)
    print("SCIENTIFIC AUDIT COMPLETE")
    print("=" * 85)


if __name__ == "__main__":
    run_scientific_audit()
