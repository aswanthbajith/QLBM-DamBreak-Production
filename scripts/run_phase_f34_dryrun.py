r"""
Phase F34: Dry-Run QPU Transpilation & Cost Estimation Script.
"""

import os
import sys
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from quantum.f34_qpu_runner import F34QPURunner


def run_dry_run():
    print("=" * 80)
    print("PHASE F34: REAL QPU DRY-RUN & COST ESTIMATOR")
    print("=" * 80)

    runner = F34QPURunner(nx=2, ny=2, bits_per_node=4)
    meta = runner.execute_dry_run()

    print(f"Backend Target Architecture: {meta['backend_target']}")
    print(f"Logical Qubits: {meta['logical_qubits']}")
    print(f"Physical Qubits: {meta['physical_qubits']}")
    print(f"Transpiled Depth: {meta['transpiled_depth']}")
    print(f"Native 2Q Hardware Gates (ECR): {meta['native_2q_gates']}")
    print(f"Status: {meta['status']}")
    print("\nArtifacts successfully archived to results/f34/.")


if __name__ == "__main__":
    run_dry_run()
