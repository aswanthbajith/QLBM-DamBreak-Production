r"""
Phase F37: Backend Discovery & Credential Audit Script.
"""

import os
import sys
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from quantum.f37_backend_discovery import F37BackendDiscovery


def run_discovery():
    print("=" * 85)
    print("PHASE F37: QUANTUM HARDWARE BACKEND DISCOVERY & CREDENTIAL AUDIT")
    print("=" * 85)

    audit = F37BackendDiscovery.audit_credentials()
    print(f"\nAuthentication Status: {audit['status']}")
    print(f"Provider Accessible: {audit['provider_accessible']}")
    print(f"Environment Token Present: {audit['has_env_token']}")
    print(f"Saved Accounts in Qiskit: {audit['has_saved_account']}")

    print("\n--- Discovered Hardware Topologies ---")
    backends = F37BackendDiscovery.discover_backends()
    for b in backends:
        qpu_type = "REAL HARDWARE" if b.get("is_real_qpu") else "LOCAL HARDWARE EMULATOR"
        print(f"Backend: {b['name']:<32} | Qubits: {b['num_qubits']:<4} | Status: {b['status']:<16} | Type: {qpu_type}")


if __name__ == "__main__":
    run_discovery()
