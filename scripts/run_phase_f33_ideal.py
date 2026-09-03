r"""
Phase F33: Mode A Ideal Quantum Simulator Runner.
"""

import os
import sys
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from quantum.f33_hardware_demo import F33HardwareDamBreakDemo


def run_ideal_simulation():
    print("=" * 80)
    print("PHASE F33: MODE A — IDEAL QUANTUM SIMULATION RUNNER")
    print("=" * 80)

    demo = F33HardwareDamBreakDemo(nx=2, ny=2, bits_per_node=4)
    res = demo.execute_mode(mode="ideal", num_timesteps=1, shots=2048)

    print(f"Backend: {res['backend_name']}")
    print(f"Logical Qubits: {res['transpilation']['logical_qubits']}")
    print(f"Transpiled Depth: {res['transpilation']['transpiled_depth']}")
    print(f"2Q Gates: {res['transpilation']['2q_gates']}")
    print(f"Total Shots: {res['shots']}")
    print("\nReconstructed Density Field (rho):")
    print(res["extracted_fields"]["rho"])
    print("\nReconstructed Phase Field (alpha):")
    print(res["extracted_fields"]["alpha"])
    print(f"\nMean Density: {res['extracted_fields']['mean_density']:.4f}")
    print(f"Total Mass: {res['extracted_fields']['total_mass']:.4f}")


if __name__ == "__main__":
    run_ideal_simulation()
