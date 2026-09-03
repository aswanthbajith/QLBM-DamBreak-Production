r"""
Phase F36: Real QPU Dry-Run & Gate Resource Estimator.
"""

import os
import sys
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from quantum.f36_qpu_executor import F36QPUExecutor


def run_dryrun():
    print("=" * 85)
    print("PHASE F36: REAL QPU DRY-RUN & COST ESTIMATOR")
    print("=" * 85)

    executor = F36QPUExecutor(nx=2, ny=2, bits_per_node=4)
    meta = executor.execute_dry_run()

    print(f"Target Backend Architecture: {meta['backend_target']}")
    print(f"Logical Qubits: {meta['logical_qubits']}")
    print(f"Physical Qubits: {meta['physical_qubits']}")
    print(f"Transpiled Depth: {meta['transpiled_depth']}")
    print(f"Native 2Q Hardware Gates (ECR): {meta['native_2q_gates']}")
    print(f"Status: {meta['status']}")
    print("\nDry-run artifacts serialized to results/f36/.")


if __name__ == "__main__":
    run_dryrun()
