r"""
Phase F36: Mode A Ideal Simulator Runner.
"""

import os
import sys
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from quantum.f33_hardware_demo import F33HardwareDamBreakDemo


def run_ideal():
    print("=" * 85)
    print("PHASE F36: MODE A — IDEAL SIMULATOR")
    print("=" * 85)

    demo = F33HardwareDamBreakDemo(nx=2, ny=2, bits_per_node=4)
    res = demo.execute_mode(mode="ideal", num_timesteps=1, shots=4096)

    print(f"Backend: {res['backend_name']}")
    print(f"Total Shots: {res['shots']}")
    print("\nReconstructed Ideal Density Field (rho):")
    print(res["extracted_fields"]["rho"])
    print(f"\nTotal Mass: {res['extracted_fields']['total_mass']:.4f}")


if __name__ == "__main__":
    run_ideal()
