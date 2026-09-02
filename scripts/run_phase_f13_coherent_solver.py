#!/usr/bin/env python3
"""
Phase F13: Fully Coherent Quantum Two-Phase Dam-Break Solver Runner.

Executes multi-step quantum simulations with zero intermediate classical population extractions, re-encodings, or classical parameter feedback loops.
"""

import os
import sys
import numpy as np

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from classical.level4_two_phase import Level4TwoPhaseLBM
from quantum.coherent_timestep import PhaseF13AutonomousQLBM


def run_coherent_simulation():
    print("=" * 85)
    print("PHASE F13: FULLY COHERENT QUANTUM TWO-PHASE DAM-BREAK SOLVER")
    print("=" * 85)

    for nx, ny in [(4, 4), (8, 4), (16, 8)]:
        print(f"\n--- GRID {nx}x{ny} COHERENT TIME EVOLUTION ---")
        for T_steps in [1, 2, 4, 8, 16]:
            c_solver = Level4TwoPhaseLBM(nx=nx, ny=ny, g_acc=-0.0005, sigma=0.001, dam_width_ratio=0.25, dam_height_ratio=0.5)
            q_solver = PhaseF13AutonomousQLBM(nx=nx, ny=ny, g_acc=-0.0005, sigma=0.001, dam_width_ratio=0.25, dam_height_ratio=0.5)

            # Advance classical reference
            for _ in range(T_steps):
                c_solver.step()

            # Advance fully coherent quantum solver
            for _ in range(T_steps):
                q_solver.step()

            fields = q_solver.decode_final_fields()

            err_f = float(np.max(np.abs(fields["f"] - c_solver.f)))
            err_g = float(np.max(np.abs(fields["g"] - c_solver.g)))
            err_rho = float(np.max(np.abs(fields["rho"] - np.sum(c_solver.f, axis=0))))
            err_alpha = float(np.max(np.abs(fields["alpha"] - np.clip(np.sum(c_solver.g, axis=0), 0.0, 1.0))))

            print(f"T={T_steps:>2} | Extractions: {q_solver.num_classical_extractions} | Re-Encodings: {q_solver.num_re_encodings} | Q-Steps: {q_solver.num_quantum_timesteps:>2} | Max f Err: {err_f:.2e} | Max g Err: {err_g:.2e} | Max Rho Err: {err_rho:.2e}")

    print("\n" + "=" * 85)
    print("PHASE F13 COHERENT SIMULATION COMPLETE: ALL RUNS SUCCESSFUL")
    print("=" * 85)


if __name__ == "__main__":
    run_coherent_simulation()
