"""
Phase F36: Quantum Processor Discovery & Topology Catalog.

Discovers accessible IBM Quantum hardware backends and inspects coupling
maps, native gate sets, and operational status without printing secrets.
"""

import os
from typing import Dict, Any, List


class F36BackendDiscovery:
    """
    Discovers accessible quantum hardware backends with non-sensitive reporting.
    """

    @staticmethod
    def audit_credentials() -> Dict[str, Any]:
        """Audits credential availability without exposing secrets."""
        has_env_token = bool(os.environ.get("QISKIT_IBM_TOKEN") or os.environ.get("IBM_QUANTUM_TOKEN"))
        has_saved = False
        try:
            from qiskit_ibm_runtime import QiskitRuntimeService
            has_saved = len(QiskitRuntimeService.saved_accounts()) > 0
        except Exception:
            has_saved = False

        is_authenticated = has_env_token or has_saved

        return {
            "authenticated": is_authenticated,
            "provider_accessible": is_authenticated,
            "has_env_token": has_env_token,
            "has_saved_account": has_saved,
            "status": "AUTHENTICATED" if is_authenticated else "BLOCKED — No live credentials found in environment",
        }

    @staticmethod
    def discover_backends() -> List[Dict[str, Any]]:
        """Queries accessible hardware backends."""
        cred_status = F36BackendDiscovery.audit_credentials()
        backends_info = []

        if cred_status["authenticated"]:
            try:
                from qiskit_ibm_runtime import QiskitRuntimeService
                service = QiskitRuntimeService()
                real_backends = service.backends(simulator=False)
                for b in real_backends:
                    backends_info.append({
                        "name": b.name,
                        "is_real_qpu": True,
                        "num_qubits": b.num_qubits,
                        "status": "ONLINE" if b.status().operational else "OFFLINE",
                        "basis_gates": getattr(b.configuration(), "basis_gates", []),
                    })
            except Exception as e:
                backends_info.append({
                    "name": "ibm_cloud_query_error",
                    "error": str(e),
                    "is_real_qpu": False,
                })
        else:
            # Fallback catalog of superconducting architectures
            backends_info.append({
                "name": "ibm_sherbrooke (FakeSherbrooke)",
                "is_real_qpu": False,
                "num_qubits": 127,
                "status": "LOCAL_EMULATOR",
                "basis_gates": ["ecr", "id", "rz", "sx", "x"],
            })
            backends_info.append({
                "name": "ibm_manila (FakeManilaV2)",
                "is_real_qpu": False,
                "num_qubits": 5,
                "status": "LOCAL_EMULATOR",
                "basis_gates": ["cx", "id", "rz", "sx", "x"],
            })

        return backends_info
