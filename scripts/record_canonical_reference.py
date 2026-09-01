#!/usr/bin/env python3
"""
Records canonical reference simulation data for nx=4, ny=4 and nx=8, ny=8 for t=0..10.
Saves exact ground truth snapshots to results/validation/canonical_reference_snapshots.json.
"""
import os
import sys
import json
import numpy as np

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from classical.reference_solver import run_two_phase_dambreak


def main():
    out_dir = os.path.join(os.path.dirname(__file__), "..", "results/validation")
    os.makedirs(out_dir, exist_ok=True)
    
    reference_data = {}
    
    for nx, ny in [(4, 4), (8, 8)]:
        grid_key = f"{nx}x{ny}"
        print(f"Recording canonical reference for {grid_key} over 10 timesteps...")
        hist = run_two_phase_dambreak(nx=nx, ny=ny, timesteps=10)
        
        steps_data = []
        for h in hist:
            steps_data.append({
                "step": h["step"],
                "total_mass": h["total_mass"],
                "total_liquid_mass": h["total_liquid_mass"],
                "mean_density": float(np.mean(h["rho"])),
                "max_velocity": float(np.max(np.sqrt(h["u"][0]**2 + h["u"][1]**2))),
                "f_checksum": float(np.sum(np.abs(h["f"]))),
                "g_checksum": float(np.sum(np.abs(h["g"]))),
                "rho": h["rho"].tolist(),
                "phi": h["phi"].tolist(),
                "ux": h["u"][0].tolist(),
                "uy": h["u"][1].tolist()
            })
        reference_data[grid_key] = steps_data
        
    out_path = os.path.join(out_dir, "canonical_reference_snapshots.json")
    with open(out_path, "w") as f:
        json.dump(reference_data, f, indent=2)
        
    print(f"Saved canonical reference snapshots to {out_path}")


if __name__ == "__main__":
    main()
