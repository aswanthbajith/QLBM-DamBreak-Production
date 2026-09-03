r"""
Phase F38: Mode C Live QPU Execution Script (Anti-Fabrication & Safety Guarded).
"""

import os
import sys
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from quantum.f38_qpu_executor import F38QPUExecutor


def run_live_qpu():
    print("=" * 85)
    print("PHASE F38: REAL QUANTUM HARDWARE (QPU) DISPATCH")
    print("=" * 85)

    executor = F38QPUExecutor(nx=2, ny=2, bits_per_node=4)
    res = executor.execute_live_qpu(shots=4096)

    if not res.get("is_executed", False):
        print(f"\nREAL QPU EXECUTION STATUS: {res.get('status')}")
        print("Live QPU submission safely blocked. No unauthorized cloud credits consumed.")
    else:
        print(f"Connected QPU Backend: {res['metadata']['backend_name']}")
        print(f"Job ID: {res['metadata']['job_id']}")
        print(f"Total Shots: {res['metadata']['shots']}")
        print(f"Status: {res['metadata']['status']}")


if __name__ == "__main__":
    run_live_qpu()
