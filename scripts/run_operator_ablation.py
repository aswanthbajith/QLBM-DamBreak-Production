#!/usr/bin/env python3
"""
Operator Ablation Experiment Script (Part K).

Runs systematic operator ablation experiments:
- Experiment A: Collision Only
- Experiment B: Streaming Only
- Experiment C: Boundary Only
- Experiment D: Collision + Streaming
- Experiment E: Collision + Boundary
- Experiment F: Streaming + Boundary
- Experiment G: Complete Step (Collision + Streaming + Boundary)

Compares quantum statevector evolution vs classical operator counterpart across t=1..10.
Saves:
- results/validation/operator_ablation.json
- results/validation/operator_ablation.png
"""
import os
import sys
import json
import numpy as np
import scipy.linalg as la
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt

# Add root directory
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from classical.two_phase import (
    initialize_two_phase_dambreak,
    collision_two_phase,
    stream_two_phase,
    apply_two_phase_boundary,
    compute_density,
    compute_velocity,
    compute_phase_field
)
from quantum.two_phase_encoding import (
    get_two_phase_register_layout,
    encode_distribution,
    decode_distribution
)
from quantum.two_phase_collision import build_two_phase_collision_unitary
from quantum.streaming import build_two_phase_streaming_unitary
from quantum.two_phase_boundary import build_two_phase_boundary_unitary


def run_ablation_experiments(nx=4, ny=4, timesteps_list=[1, 2, 3, 5, 10]):
    print("============================================================")
    print("PART K: OPERATOR ABLATION EXPERIMENTS & ERROR LOCALIZATION")
    print("============================================================")
    
    layout = get_two_phase_register_layout(nx, ny)
    U_coll = np.eye(1 << layout["total_qubits"], dtype=np.complex128)
    # Embed 5q collision unitary on all spatial nodes
    U_coll_5q = build_two_phase_collision_unitary(tau_liquid=0.8, tau_gas=0.65)
    
    # Broadcast single-cell 5q collision across (ny, nx) spatial lattice
    n_qx = layout["n_qx"]
    n_qy = layout["n_qy"]
    n_qvel = layout["n_qvel"]
    
    dim = 1 << layout["total_qubits"]
    U_coll_full = np.zeros((dim, dim), dtype=np.complex128)
    for y in range(ny):
        for x in range(nx):
            spatial_mask = (y << n_qx) | x
            for p in range(2):
                for v in range(16):
                    src_5q = (p << 4) | v
                    src_full = (p << (n_qx + n_qy + n_qvel)) | (v << (n_qx + n_qy)) | spatial_mask
                    for p_out in range(2):
                        for v_out in range(16):
                            dst_5q = (p_out << 4) | v_out
                            dst_full = (p_out << (n_qx + n_qy + n_qvel)) | (v_out << (n_qx + n_qy)) | spatial_mask
                            U_coll_full[dst_full, src_full] = U_coll_5q[dst_5q, src_5q]
                            
    U_stream_full = build_two_phase_streaming_unitary(layout)
    U_bnd_full = build_two_phase_boundary_unitary(layout)
    
    experiments = {
        "A_collision_only": {"coll": True, "stream": False, "bnd": False},
        "B_streaming_only": {"coll": False, "stream": True, "bnd": False},
        "C_boundary_only": {"coll": False, "stream": False, "bnd": True},
        "D_collision_streaming": {"coll": True, "stream": True, "bnd": False},
        "E_collision_boundary": {"coll": True, "stream": False, "bnd": True},
        "F_streaming_boundary": {"coll": False, "stream": True, "bnd": True},
        "G_complete_step": {"coll": True, "stream": True, "bnd": True}
    }
    
    ablation_results = {}
    
    for exp_name, flags in experiments.items():
        print(f"\n--- Running Ablation Experiment: {exp_name} ---")
        
        # Build composite quantum operator U_op
        U_op = np.eye(dim, dtype=np.complex128)
        if flags["coll"]:
            U_op = U_coll_full @ U_op
        if flags["stream"]:
            U_op = U_stream_full @ U_op
        if flags["bnd"]:
            U_op = U_bnd_full @ U_op
            
        phi_0, rho_0, u_0, f_0, g_0 = initialize_two_phase_dambreak(nx, ny)
        state_0, total_mass, _ = encode_distribution(f_0, phi_0, layout)
        
        f_c, g_c = np.copy(f_0), np.copy(g_0)
        phi_c = np.copy(phi_0)
        rho_c = np.copy(rho_0)
        u_c = np.copy(u_0)
        
        state_q = np.copy(state_0)
        
        exp_time_data = {}
        
        for t in range(1, max(timesteps_list) + 1):
            # 1. Classical operator update
            if flags["coll"]:
                f_c, g_c = collision_two_phase(f_c, g_c, phi_c, rho_c, u_c, tau_f=0.8, tau_g=0.7, g_acc=-0.001)
            if flags["stream"]:
                f_c, g_c = stream_two_phase(f_c, g_c)
            if flags["bnd"]:
                f_c, g_c = apply_two_phase_boundary(f_c, g_c, f_c, g_c)
                
            phi_c = compute_phase_field(g_c)
            rho_c = compute_density(f_c)
            u_c = compute_velocity(f_c, rho_c)
            
            # 2. Quantum operator update
            state_q = U_op @ state_q
            probs_q = np.abs(state_q)**2
            rho_q, u_q, phi_q = decode_distribution(probs_q, layout, total_mass=total_mass)
            
            if t in timesteps_list:
                diff_rho = rho_q - rho_c
                diff_phi = phi_q - phi_c
                rel_l2_rho = float(la.norm(diff_rho) / (la.norm(rho_c) + 1e-14))
                rel_l2_phi = float(la.norm(diff_phi) / (la.norm(phi_c) + 1e-14))
                
                exp_time_data[f"t_{t}"] = {
                    "step": t,
                    "density_rel_l2": rel_l2_rho,
                    "phase_rel_l2": rel_l2_phi
                }
                print(f"t={t:2d} | Density Rel L2: {rel_l2_rho*100:6.2f}% | Phase Rel L2: {rel_l2_phi*100:6.2f}%")
                
        ablation_results[exp_name] = exp_time_data
        
    out_dir = os.path.join(os.path.dirname(__file__), "..", "results/validation")
    os.makedirs(out_dir, exist_ok=True)
    
    with open(os.path.join(out_dir, "operator_ablation.json"), "w") as f:
        json.dump(ablation_results, f, indent=2)
        
    # Plot Ablation Error Curves
    fig, axes = plt.subplots(1, 2, figsize=(14, 6))
    
    colors = {
        "A_collision_only": "red",
        "B_streaming_only": "blue",
        "C_boundary_only": "green",
        "D_collision_streaming": "orange",
        "E_collision_boundary": "magenta",
        "F_streaming_boundary": "cyan",
        "G_complete_step": "black"
    }
    
    for exp_name, data in ablation_results.items():
        t_vals = [d["step"] for d in data.values()]
        rho_errs = [d["density_rel_l2"] * 100 for d in data.values()]
        phi_errs = [d["phase_rel_l2"] * 100 for d in data.values()]
        
        axes[0].plot(t_vals, rho_errs, "o-", color=colors.get(exp_name, "gray"), lw=2, label=exp_name)
        axes[1].plot(t_vals, phi_errs, "s-", color=colors.get(exp_name, "gray"), lw=2, label=exp_name)
        
    axes[0].set_title("Ablation: Density Relative L2 Error (%)")
    axes[0].set_xlabel("Timestep t")
    axes[0].set_ylabel("Error (%)")
    axes[0].grid(True, alpha=0.3)
    axes[0].legend(fontsize=8)
    
    axes[1].set_title("Ablation: Phase Field Relative L2 Error (%)")
    axes[1].set_xlabel("Timestep t")
    axes[1].set_ylabel("Error (%)")
    axes[1].grid(True, alpha=0.3)
    axes[1].legend(fontsize=8)
    
    plt.tight_layout()
    plt.savefig(os.path.join(out_dir, "operator_ablation.png"), dpi=300)
    plt.close()
    
    print("============================================================")
    print("Operator ablation complete. Artifacts saved in results/validation/")
    print("============================================================")


if __name__ == "__main__":
    run_ablation_experiments()
