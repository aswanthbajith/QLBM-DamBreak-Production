#!/usr/bin/env python3
"""
Collision Operator Validation Script (Part E).

Compares single-node classical BGK collision vs quantum collision operator across
relaxation parameters (omega in [0.5, 0.8, 1.0, 1.2, 1.5, 1.8]) and phase states.
Saves results into results/validation/collision_operator_validation.json.
"""
import os
import sys
import json
import numpy as np
import scipy.linalg as la

# Add root directory
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from classical.d2q9 import C_X, C_Y, W, OPPOSITE
from classical.equilibrium import compute_equilibrium
from quantum.two_phase_collision import build_two_phase_collision_unitary


def main():
    print("============================================================")
    print("PART E: COLLISION OPERATOR VALIDATION & ERROR ANALYSIS")
    print("============================================================")
    
    np.random.seed(42)
    omegas = [0.5, 0.8, 1.0, 1.2, 1.5, 1.8]
    phases = [0.0, 0.5, 1.0] # pure gas, mixture, pure liquid
    
    results = {}
    
    # 5 random valid population sets
    test_cases = []
    for k in range(5):
        rho_val = float(np.random.uniform(0.5, 1.5))
        u_val = np.random.uniform(-0.05, 0.05, 2)
        f_eq = compute_equilibrium(np.array([[rho_val]]), u_val[:, None, None])[:, 0, 0]
        # Add non-equilibrium perturbation
        perturbation = np.random.uniform(-0.02, 0.02, 9)
        # Ensure mass and momentum are conserved by perturbation
        perturbation -= np.sum(perturbation) * W
        perturbation -= (np.sum(perturbation * C_X) / np.sum(W * C_X**2)) * (W * C_X)
        perturbation -= (np.sum(perturbation * C_Y) / np.sum(W * C_Y**2)) * (W * C_Y)
        f_in = np.maximum(f_eq + perturbation, 1e-4)
        test_cases.append((rho_val, u_val, f_in))
        
    for omega in omegas:
        tau_val = 1.0 / omega
        U_coll = build_two_phase_collision_unitary(tau_gas=tau_val, tau_liquid=tau_val)
        
        omega_results = []
        for p_idx, phase_val in enumerate(phases):
            phase_res = []
            for t_idx, (rho_val, u_val, f_in) in enumerate(test_cases):
                # 1. Classical BGK Collision
                rho_in = np.sum(f_in)
                ux_in = np.sum(f_in * C_X) / rho_in
                uy_in = np.sum(f_in * C_Y) / rho_in
                u_in = np.array([ux_in, uy_in])
                f_eq = compute_equilibrium(np.array([[rho_in]]), u_in[:, None, None])[:, 0, 0]
                
                f_classical = f_in - omega * (f_in - f_eq)
                
                # 2. Quantum Unitary Action on 5-qubit subspace (1 phase + 4 vel = 32 dim)
                psi_in = np.zeros(32, dtype=np.complex128)
                # Phase bit 0 = gas, 1 = liquid
                p_bit = 1 if phase_val >= 0.5 else 0
                for i in range(9):
                    idx = (p_bit << 4) | i
                    psi_in[idx] = np.sqrt(f_in[i] / rho_in)
                psi_in /= np.linalg.norm(psi_in)
                
                psi_out = U_coll @ psi_in
                probs_out = np.abs(psi_out)**2
                
                f_quantum = np.zeros(9)
                for i in range(9):
                    idx_g = (0 << 4) | i
                    idx_l = (1 << 4) | i
                    f_quantum[i] = rho_in * (probs_out[idx_g] + probs_out[idx_l])
                    
                # 3. Compare Observables & Errors
                diff_f = f_quantum - f_classical
                rel_l2 = float(la.norm(diff_f) / (la.norm(f_classical) + 1e-14))
                max_ae = float(np.max(np.abs(diff_f)))
                
                mass_err = float(abs(np.sum(f_quantum) - np.sum(f_classical)) / np.sum(f_classical))
                mom_x_c = np.sum(f_classical * C_X)
                mom_y_c = np.sum(f_classical * C_Y)
                mom_x_q = np.sum(f_quantum * C_X)
                mom_y_q = np.sum(f_quantum * C_Y)
                mom_err = float(np.sqrt((mom_x_q - mom_x_c)**2 + (mom_y_q - mom_y_c)**2))
                
                phase_res.append({
                    "case": t_idx,
                    "rel_l2_error": rel_l2,
                    "max_absolute_error": max_ae,
                    "mass_error": mass_err,
                    "momentum_error": mom_err
                })
                
            avg_l2 = np.mean([r["rel_l2_error"] for r in phase_res])
            avg_max_ae = np.mean([r["max_absolute_error"] for r in phase_res])
            avg_mass_err = np.mean([r["mass_error"] for r in phase_res])
            avg_mom_err = np.mean([r["momentum_error"] for r in phase_res])
            
            omega_results.append({
                "phase": phase_val,
                "avg_rel_l2": float(avg_l2),
                "avg_max_ae": float(avg_max_ae),
                "avg_mass_err": float(avg_mass_err),
                "avg_mom_err": float(avg_mom_err),
                "detailed_cases": phase_res
            })
            
            print(f"omega={omega:3.1f} | Phase={phase_val:3.1f} | Rel L2: {avg_l2*100:6.2f}% | Max AE: {avg_max_ae:.4e} | Mass Err: {avg_mass_err:.2e} | Mom Err: {avg_mom_err:.2e}")
            
        results[f"omega_{omega}"] = omega_results

    out_dir = os.path.join(os.path.dirname(__file__), "..", "results/validation")
    os.makedirs(out_dir, exist_ok=True)
    out_file = os.path.join(out_dir, "collision_operator_validation.json")
    with open(out_file, "w") as f:
        json.dump(results, f, indent=2)
        
    print("============================================================")
    print(f"Collision validation saved in: {out_file}")
    print("============================================================")


if __name__ == "__main__":
    main()
