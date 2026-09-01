#!/usr/bin/env python3
"""
Shot Noise Convergence & Error Decomposition Script (Parts O & P).

1. Evaluates finite-shot convergence across shot counts: [256, 1024, 4096, 16384, 65536]
2. Computes regression against 1/sqrt(shots) (Standard Quantum Limit SQL)
3. Separates Algorithmic Error, Sampling Error, and Hardware Noise across backends.
4. Saves:
   - results/validation/error_decomposition.json
   - results/validation/shot_noise_convergence.png
"""
import os
import sys
import json
import numpy as np
import scipy.linalg as la
import scipy.stats as stats
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt

# Add root directory
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from classical.two_phase import run_two_phase_dambreak
from quantum.two_phase_step import quantum_two_phase_step


def main():
    print("============================================================")
    print("PARTS O & P: SHOT NOISE CONVERGENCE & ERROR DECOMPOSITION")
    print("============================================================")
    
    nx, ny = 4, 4
    t = 1
    shot_counts = [256, 1024, 4096, 16384, 65536]
    
    # 1. Classical Reference
    c_hist = run_two_phase_dambreak(nx=nx, ny=ny, timesteps=t)
    rho_c = c_hist[-1]["rho"]
    phi_c = c_hist[-1]["phi"]
    u_c = c_hist[-1]["u"]
    
    # 2. Statevector (Algorithmic Reference)
    q_sv = quantum_two_phase_step(nx=nx, ny=ny, timesteps=t, backend="aer_ideal", shots=0)
    rho_sv = q_sv["rho"]
    phi_sv = q_sv["phi"]
    u_sv = q_sv["u"]
    
    algo_err_rho = float(la.norm(rho_sv - rho_c) / la.norm(rho_c))
    algo_err_phi = float(la.norm(phi_sv - phi_c) / (la.norm(phi_c) + 1e-14))
    
    print(f"Algorithmic Error (Statevector vs Classical): Density = {algo_err_rho*100:.2f}%, Phase = {algo_err_phi*100:.2f}%")
    
    # 3. Finite Shot Sampling Error
    sampling_results = []
    
    for shots in shot_counts:
        errs_rho_sample = []
        errs_phi_sample = []
        
        # 5 repetitions to get mean and standard deviation
        for rep in range(5):
            q_res = quantum_two_phase_step(nx=nx, ny=ny, timesteps=t, backend="aer_ideal", shots=shots)
            # Compare vs exact statevector to isolate pure sampling error
            err_rho_samp = float(la.norm(q_res["rho"] - rho_sv) / la.norm(rho_sv))
            err_phi_samp = float(la.norm(q_res["phi"] - phi_sv) / (la.norm(phi_sv) + 1e-14))
            errs_rho_sample.append(err_rho_samp)
            errs_phi_sample.append(err_phi_samp)
            
        mean_err_rho = float(np.mean(errs_rho_sample))
        mean_err_phi = float(np.mean(errs_phi_sample))
        
        sampling_results.append({
            "shots": shots,
            "inv_sqrt_shots": float(1.0 / np.sqrt(shots)),
            "density_sampling_error": mean_err_rho,
            "phase_sampling_error": mean_err_phi
        })
        print(f"Shots={shots:6d} (1/sqrt(N)={1.0/np.sqrt(shots):.4f}) | Sampling Density Err: {mean_err_rho*100:5.2f}% | Phase Err: {mean_err_phi*100:5.2f}%")
        
    # Fit linear regression: Error vs 1/sqrt(N)
    inv_sqrts = [s["inv_sqrt_shots"] for s in sampling_results]
    rho_samp_errs = [s["density_sampling_error"] for s in sampling_results]
    slope, intercept, r_value, _, _ = stats.linregress(inv_sqrts, rho_samp_errs)
    r_squared = float(r_value**2)
    print(f"\nSQL Convergence Fit R^2: {r_squared:.4f} (Slope: {slope:.4f})")
    
    # 4. Multi-Backend Error Decomposition (at N=4096)
    ref_shots = 4096
    
    q_ideal = quantum_two_phase_step(nx=nx, ny=ny, timesteps=t, backend="aer_ideal", shots=ref_shots)
    q_noisy = quantum_two_phase_step(nx=nx, ny=ny, timesteps=t, backend="aer_noisy", shots=ref_shots)
    q_fake = quantum_two_phase_step(nx=nx, ny=ny, timesteps=t, backend="fake_ibm", shots=ref_shots)
    
    tot_err_ideal = float(la.norm(q_ideal["rho"] - rho_c) / la.norm(rho_c))
    tot_err_noisy = float(la.norm(q_noisy["rho"] - rho_c) / la.norm(rho_c))
    tot_err_fake = float(la.norm(q_fake["rho"] - rho_c) / la.norm(rho_c))
    
    sampling_err_4k = float(la.norm(q_ideal["rho"] - rho_sv) / la.norm(rho_sv))
    noise_err_aer = float(la.norm(q_noisy["rho"] - q_ideal["rho"]) / la.norm(q_ideal["rho"]))
    noise_err_ibm = float(la.norm(q_fake["rho"] - q_ideal["rho"]) / la.norm(q_ideal["rho"]))
    
    decomposition = {
        "problem": f"Two-Phase Dam-Break {nx}x{ny}, t={t}",
        "reference_shots": ref_shots,
        "algorithmic_error": {
            "density_rel_l2": algo_err_rho,
            "phase_rel_l2": algo_err_phi
        },
        "sampling_error_at_4096": {
            "density_rel_l2": sampling_err_4k
        },
        "hardware_noise_error": {
            "aer_noisy_rel_l2": noise_err_aer,
            "fake_ibm_rel_l2": noise_err_ibm
        },
        "total_errors_by_backend": {
            "aer_ideal_sampled": tot_err_ideal,
            "aer_noisy_sampled": tot_err_noisy,
            "fake_ibm_sampled": tot_err_fake
        },
        "sql_convergence": {
            "r_squared": r_squared,
            "slope": float(slope),
            "intercept": float(intercept),
            "data_points": sampling_results
        }
    }
    
    out_dir = os.path.join(os.path.dirname(__file__), "..", "results/validation")
    os.makedirs(out_dir, exist_ok=True)
    
    with open(os.path.join(out_dir, "error_decomposition.json"), "w") as f:
        json.dump(decomposition, f, indent=2)
        
    # 5. Plot Convergence Curve
    fig, ax = plt.subplots(figsize=(8, 6))
    ax.plot(inv_sqrts, rho_samp_errs, "o", color="blue", label="Measured Density Sampling Error")
    fit_line = [slope * x + intercept for x in inv_sqrts]
    ax.plot(inv_sqrts, fit_line, "--", color="red", label=f"SQL Fit: y = {slope:.2f} x (R² = {r_squared:.3f})")
    ax.set_title("Shot Noise Convergence vs $1/\\sqrt{N_{\\mathrm{shots}}}$")
    ax.set_xlabel("$1/\\sqrt{N_{\\mathrm{shots}}}$")
    ax.set_ylabel("Relative $L_2$ Sampling Error")
    ax.grid(True, alpha=0.3)
    ax.legend()
    
    plt.tight_layout()
    plt.savefig(os.path.join(out_dir, "shot_noise_convergence.png"), dpi=300)
    plt.close()
    
    print("============================================================")
    print("Error decomposition & SQL convergence saved in results/validation/")
    print("============================================================")


if __name__ == "__main__":
    main()
