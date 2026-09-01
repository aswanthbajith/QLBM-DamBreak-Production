#!/usr/bin/env python3
"""
Complete Quantum Two-Phase Dam-Break Solver & Multi-Backend Benchmark Script.
"""
import argparse
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

from classical.two_phase import initialize_two_phase_dambreak, step_two_phase, run_two_phase_dambreak
from quantum.two_phase_step import quantum_two_phase_step

def parse_args():
    parser = argparse.ArgumentParser(description="Run Quantum Two-Phase Dam-Break Simulation")
    parser.add_argument("--nx", type=int, default=4, help="Grid nodes in X (default: 4)")
    parser.add_argument("--ny", type=int, default=4, help="Grid nodes in Y (default: 4)")
    parser.add_argument("--timesteps", type=int, default=1, help="Number of timesteps (default: 1)")
    parser.add_argument("--shots", type=int, default=4096, help="Shot budget for measurement (default: 4096)")
    parser.add_argument("--backend", type=str, default="aer_ideal", choices=["aer_ideal", "aer_noisy", "fake_ibm", "real_ibm"], help="Simulation or hardware backend")
    return parser.parse_args()

def main():
    args = parse_args()
    print("============================================================")
    print("STARTING QUANTUM TWO-PHASE DAM-BREAK SOLVER")
    print(f"Mesh: {args.nx} x {args.ny}")
    print(f"Timesteps: {args.timesteps}")
    print(f"Backend: {args.backend}")
    print(f"Shots: {args.shots}")
    print("============================================================")
    
    # 1. Classical Reference Simulation
    print("--- [1/4] Running Classical Reference Simulation ---")
    c_hist = run_two_phase_dambreak(nx=args.nx, ny=args.ny, timesteps=args.timesteps)
    c_final = c_hist[-1]
    rho_c = c_final["rho"]
    u_c = c_final["u"]
    phi_c = c_final["phi"]
    
    # 2. Quantum Two-Phase Simulation
    print(f"--- [2/4] Executing Quantum Two-Phase Step on Backend ({args.backend}) ---")
    q_res = quantum_two_phase_step(nx=args.nx, ny=args.ny, timesteps=args.timesteps, backend=args.backend, shots=args.shots)
    rho_q = q_res["rho"]
    u_q = q_res["u"]
    phi_q = q_res["phi"]
    
    # 3. Scientific Comparison Metrics
    print("--- [3/4] Computing Classical vs Quantum Comparison Metrics ---")
    def calc_metrics(q_field, c_field):
        diff = q_field - c_field
        l2 = float(la.norm(diff) / (la.norm(c_field) + 1e-14))
        rmse = float(np.sqrt(np.mean(diff**2)))
        mae = float(np.mean(np.abs(diff)))
        return {"relative_l2": l2, "rmse": rmse, "mae": mae}
        
    metrics_rho = calc_metrics(rho_q, rho_c)
    metrics_phi = calc_metrics(phi_q, phi_c)
    metrics_ux = calc_metrics(u_q[0], u_c[0])
    metrics_uy = calc_metrics(u_q[1], u_c[1])
    
    comparison = {
        "mesh": f"{args.nx}x{args.ny}",
        "timesteps": args.timesteps,
        "backend": args.backend,
        "shots": args.shots,
        "density_metrics": metrics_rho,
        "phase_metrics": metrics_phi,
        "velocity_x_metrics": metrics_ux,
        "velocity_y_metrics": metrics_uy
    }
    
    print(f"Density Relative L2 Error: {metrics_rho['relative_l2']*100:.2f}% | RMSE: {metrics_rho['rmse']:.4f}")
    print(f"Phase Field Relative L2:   {metrics_phi['relative_l2']*100:.2f}% | RMSE: {metrics_phi['rmse']:.4f}")
    
    # 4. Save Outputs & Plots
    print("--- [4/4] Saving Results to results/two_phase/ ---")
    out_dir = os.path.join(os.path.dirname(__file__), "..", "results/two_phase")
    os.makedirs(out_dir, exist_ok=True)
    
    np.savez(os.path.join(out_dir, "classical_fields.npz"), rho=rho_c, u=u_c, phi=phi_c)
    np.savez(os.path.join(out_dir, "quantum_fields.npz"), rho=rho_q, u=u_q, phi=phi_q)
    
    with open(os.path.join(out_dir, "comparison.json"), "w") as f:
        json.dump(comparison, f, indent=2)
        
    # Generate 7 Verification Plots
    fig, axes = plt.subplots(2, 3, figsize=(12, 7))
    
    # 1. Initial Phase
    im0 = axes[0, 0].imshow(c_hist[0]["phi"], origin="lower", cmap="Blues", vmin=0, vmax=1)
    axes[0, 0].set_title("1. Initial Phase Field phi(0)")
    plt.colorbar(im0, ax=axes[0, 0])
    
    # 2. Classical Final Phase
    im1 = axes[0, 1].imshow(phi_c, origin="lower", cmap="Blues", vmin=0, vmax=1)
    axes[0, 1].set_title(f"2. Classical Phase phi({args.timesteps})")
    plt.colorbar(im1, ax=axes[0, 1])
    
    # 3. Quantum Final Phase
    im2 = axes[0, 2].imshow(phi_q, origin="lower", cmap="Blues", vmin=0, vmax=1)
    axes[0, 2].set_title(f"3. Quantum Phase ({args.backend})")
    plt.colorbar(im2, ax=axes[0, 2])
    
    # 4. Phase Difference
    diff_phi = np.abs(phi_q - phi_c)
    im3 = axes[1, 0].imshow(diff_phi, origin="lower", cmap="Reds")
    axes[1, 0].set_title("4. |Quantum - Classical| phi")
    plt.colorbar(im3, ax=axes[1, 0])
    
    # 5. Quantum Density
    im4 = axes[1, 1].imshow(rho_q, origin="lower", cmap="viridis")
    axes[1, 1].set_title("5. Quantum Density rho_q")
    plt.colorbar(im4, ax=axes[1, 1])
    
    # 6. Velocity Magnitude
    vel_mag = np.sqrt(u_q[0]**2 + u_q[1]**2)
    im5 = axes[1, 2].imshow(vel_mag, origin="lower", cmap="plasma")
    axes[1, 2].set_title("6. Quantum Velocity |u_q|")
    plt.colorbar(im5, ax=axes[1, 2])
    
    plt.tight_layout()
    plt.savefig(os.path.join(out_dir, "two_phase_dambreak_comparison.png"), dpi=300)
    plt.close()
    
    print("============================================================")
    print("QUANTUM TWO-PHASE DAM-BREAK SIMULATION COMPLETED SUCCESSFULLY")
    print(f"Results saved in: {out_dir}")
    print("============================================================")

if __name__ == "__main__":
    main()
