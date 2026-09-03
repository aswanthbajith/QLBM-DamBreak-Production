r"""
Phase F34: Mode B Noisy Hardware Emulator Runner.
"""

import os
import sys
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from quantum.f33_hardware_demo import F33HardwareDamBreakDemo


def run_noisy():
    print("=" * 80)
    print("PHASE F34: MODE B — NOISY HARDWARE EMULATOR")
    print("=" * 80)

    demo = F33HardwareDamBreakDemo(nx=2, ny=2, bits_per_node=4)
    res = demo.execute_mode(mode="noisy", num_timesteps=1, shots=4096)

    print(f"Backend Emulator: {res['backend_name']}")
    print(f"Transpiled Depth: {res['transpilation']['transpiled_depth']}")
    print(f"Native 2Q Hardware Gates: {res['transpilation']['2q_gates']}")
    print("\nReconstructed Noisy Density Field (rho):")
    print(res["extracted_fields"]["rho"])
    print(f"\nTotal Fluid Mass: {res['extracted_fields']['total_mass']:.4f}")


if __name__ == "__main__":
    run_noisy()
