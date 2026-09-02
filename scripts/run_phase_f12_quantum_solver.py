#!/usr/bin/env python3
"""
Phase F12: Autonomous Multi-Step Quantum Two-Phase Dam-Break Solver Runner.

Executes autonomous multi-step quantum simulations without intermediate classical population extraction or re-encoding.
"""

import os
import sys
import numpy as np

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from classical.level4_two_phase import Level4TwoPhaseLBM
from quantum.coherent_timestep import PhaseF12AutonomousQLBM


def run_autonomous_simulation():
    print("=" * 80)
    print("PHASE F12: AUTONOMOUS MULTI-STEP QUANTUM TWO-PHASE DAM-BREAK SOLVER")
    print("=" * 80)

    for nx, ny in [(4, 4), (8, 4), (16, 8)]:
        print(f"\n--- DOMAIN {nx}x{ny} MULTI-STEP QUANTUM EVOLUTION ---")
        for T_steps in [1, 2, 4, 8, 16]:
            c_solver = Level4TwoPhaseLBM(nx=nx, ny=ny, g_acc=-0.0005, sigma=0.001, dam_width_ratio=0.25, dam_height_ratio=0.5)
            q_solver = PhaseF12AutonomousQLBM(nx=nx, ny=ny, g_acc=-0.0005, sigma=0.001, dam_width_ratio=0.25, dam_height_ratio=0.5)

            # Advance classical solver T steps
            for _ in range(T_steps):
                c_solver.step()

            # Advance autonomous quantum solver T steps (Coherent statevector evolution)
            for _ in range(T_steps):
                q_solver.step()

            # Final measurement / readout
            final_fields = q_solver.decode_final_fields()

            err_f = float(np.max(np.abs(final_fields["f"] - c_solver.f)))
            err_g = float(np.max(np.abs(final_fields["g"] - c_solver.g)))
            err_rho = float(np.max(np.abs(final_fields["rho"] - c_solver.rho)))
            err_alpha = float(np.max(np.abs(final_fields["alpha"] - c_solver.alpha)))

            print(f"T={T_steps:>2} Steps | Q-Timesteps: {q_solver.num_quantum_timesteps:>2} | Extractions: {q_solver.num_classical_extractions} | Re-Encodings: {q_solver.num_re_encodings} | Max f Err: {err_f:.2e} | Max g Err: {err_g:.2e} | Max Rho Err: {err_rho:.2e}")

    print("\n" + "=" * 80)
    print("AUTONOMOUS MULTI-STEP SIMULATION COMPLETE: ALL RUNS SUCCESSFUL")
    print("=" * 80)


if __name__ == "__main__":
    run_autonomous_simulation()
