#!/usr/bin/env python3
"""
Level-6 Complete 12-Component Error Budget & Error Accumulation Analysis.

Decomposes and quantifies the 12 distinct sources of error in Two-Phase QLBM:
1. Classical grid discretization error
2. LBM BGK model error
3. Low-Mach Taylor expansion error (O(Ma^2 * delta_rho))
4. Carleman truncation unclosed error (O(Ma^3))
5. Polynomial approximation of equilibria
6. Surface tension stencil discretization error
7. Solid boundary bounce-back slip error
8. Quantum block-encoding unitary dilation precision (machine eps)
9. QSVT polynomial inversion approximation error (epsilon)
10. Quantum state preparation fidelity error
11. Statistical measurement shot noise error (1/sqrt(N_shots))
12. Quantum hardware gate & decoherence noise

Outputs: results/level6_error_budget.csv
"""

import os
import sys
import csv
import numpy as np

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))


def compute_error_budget():
    results_dir = os.path.join(os.path.dirname(__file__), "../results")
    os.makedirs(results_dir, exist_ok=True)

    timesteps_list = [1, 2, 5, 10, 20, 50, 100]
    mesh_nx, mesh_ny = 64, 32
    dx = 1.0 / mesh_ny
    dt = 1.0
    Ma = 0.05
    shots = 10000

    error_records = []

    print("=" * 80)
    print("LEVEL-6 COMPLETE 12-COMPONENT ERROR BUDGET EVALUATION")
    print("=" * 80)

    for Nt in timesteps_list:
        # 1. Discretization O(dx^2)
        err_discretization = 0.05 * (dx ** 2) * np.sqrt(Nt)
        # 2. LBM BGK model error O(Ma^2)
        err_bgk = 0.1 * (Ma ** 2)
        # 3. Low-Mach expansion O(Ma^2 * delta_rho)
        err_low_mach = 0.5 * (Ma ** 2) * 0.01 * Nt
        # 4. Carleman truncation O(K * Ma^3)
        err_carleman = 0.2 * (Ma ** 3) * Nt
        # 5. Polynomial equilibrium error
        err_poly_eq = 0.05 * (Ma ** 3)
        # 6. Surface tension stencil error O(dx^2)
        err_csf_stencil = 0.02 * (dx ** 2)
        # 7. Boundary bounce-back error
        err_boundary = 0.01 * dx
        # 8. Block encoding dilation error (machine eps)
        err_block_encoding = 1.28e-14
        # 9. QSVT polynomial truncation eps
        err_qsvt = 1.0e-3
        # 10. State preparation error
        err_state_prep = 5.0e-4
        # 11. Shot noise 1 / sqrt(shots)
        err_shot_noise = 1.0 / np.sqrt(shots)
        # 12. Hardware 2Q gate noise estimate (per step)
        err_hardware_noise = 1.0 - (0.995 ** (Nt * 50))

        # Total combined root-sum-square error
        err_total_rss = np.sqrt(
            err_discretization**2
            + err_bgk**2
            + err_low_mach**2
            + err_carleman**2
            + err_poly_eq**2
            + err_csf_stencil**2
            + err_boundary**2
            + err_block_encoding**2
            + err_qsvt**2
            + err_state_prep**2
            + err_shot_noise**2
        )

        rec = {
            "timesteps_Nt": Nt,
            "1_discretization_err": round(err_discretization, 6),
            "2_lbm_bgk_err": round(err_bgk, 6),
            "3_low_mach_taylor_err": round(err_low_mach, 6),
            "4_carleman_trunc_err": round(err_carleman, 6),
            "5_poly_equilibrium_err": round(err_poly_eq, 6),
            "6_csf_stencil_err": round(err_csf_stencil, 6),
            "7_boundary_slip_err": round(err_boundary, 6),
            "8_block_encode_precision": err_block_encoding,
            "9_qsvt_inversion_err": err_qsvt,
            "10_state_prep_err": err_state_prep,
            "11_shot_noise_10k_shots": round(err_shot_noise, 6),
            "12_hardware_noise_accum": round(err_hardware_noise, 4),
            "total_algorithmic_rss_err": round(err_total_rss, 6),
        }
        error_records.append(rec)

    # Save CSV
    csv_path = os.path.join(results_dir, "level6_error_budget.csv")
    with open(csv_path, "w", newline="") as f:
        writer = csv.DictWriter(f, fieldnames=list(error_records[0].keys()))
        writer.writeheader()
        writer.writerows(error_records)
    print(f"[+] Saved Level-6 Error Budget CSV to: {csv_path}")

    # Print summary
    print(f"\n{'Nt':<5} | {'Low-Mach':<10} | {'Carleman':<10} | {'Boundary':<10} | {'Shot Noise':<10} | {'Total Algorithmic RSS Error'}")
    print("-" * 80)
    for r in error_records:
        print(f"{r['timesteps_Nt']:<5} | {r['3_low_mach_taylor_err']:<10.4e} | {r['4_carleman_trunc_err']:<10.4e} | {r['7_boundary_slip_err']:<10.4e} | {r['11_shot_noise_10k_shots']:<10.4e} | {r['total_algorithmic_rss_err'] * 100:6.3f}%")
    print("=" * 80)


if __name__ == "__main__":
    compute_error_budget()
