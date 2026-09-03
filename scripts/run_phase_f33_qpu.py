r"""
Phase F33: Mode C Real Quantum Hardware Runner (Safety-Guarded).
"""

import os
import sys
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from quantum.f33_hardware_demo import F33HardwareDamBreakDemo


def run_real_qpu_job():
    print("=" * 80)
    print("PHASE F33: MODE C — REAL QUANTUM HARDWARE RUNNER (SAFETY-GUARDED)")
    print("=" * 80)

    demo = F33HardwareDamBreakDemo(nx=2, ny=2, bits_per_node=4)
    res = demo.execute_mode(mode="real_qpu", num_timesteps=1, shots=2048)

    if not res.get("is_executed", False):
        print(f"\nREAL-QPU EXECUTION: {res.get('status', 'BLOCKED')}")
        print("Safety and credential checks operated as intended. No unauthorized jobs submitted.")
    else:
        print(f"Connected Real QPU Backend: {res['backend_name']}")
        print(f"Transpiled Depth: {res['transpilation']['transpiled_depth']}")
        print(f"Native 2Q Gates: {res['transpilation']['2q_gates']}")
        print(f"Observed Density: {res['extracted_fields']['mean_density']:.4f}")


if __name__ == "__main__":
    run_real_qpu_job()
