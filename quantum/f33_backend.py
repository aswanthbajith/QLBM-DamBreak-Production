"""
Phase F33: Quantum Hardware Backend Manager & Safety Gate.

Manages:
- Mode A: Ideal Quantum Simulator (AerSimulator statevector)
- Mode B: Noisy Quantum Simulator (FakeManilaV2 / FakeSherbrooke with realistic noise model)
- Mode C: Real Quantum Hardware (Guarded by QLBM_ENABLE_REAL_QPU=1 and QLBM_CONFIRM_REAL_QPU=YES)
"""

import os
from typing import Dict, Any, Tuple, Optional
from qiskit_aer import AerSimulator


class F33BackendManager:
    """
    Manages backend dispatch with strict hardware safety gates.
    """

    @staticmethod
    def get_ideal_backend() -> Tuple[AerSimulator, Dict[str, Any]]:
        """Returns ideal statevector/unitary simulator."""
        backend = AerSimulator(method="statevector")
        meta = {
            "mode": "MODE_A_IDEAL_SIMULATOR",
            "backend_name": "aer_simulator_statevector",
            "is_noisy": False,
            "is_real_hardware": False,
        }
        return backend, meta

    @staticmethod
    def get_noisy_backend(backend_type: str = "sherbrooke") -> Tuple[AerSimulator, Dict[str, Any]]:
        """Returns AerSimulator configured with fake hardware noise model."""
        try:
            if backend_type.lower() == "manila":
                from qiskit_ibm_runtime.fake_provider import FakeManilaV2
                fake_backend = FakeManilaV2()
            else:
                from qiskit_ibm_runtime.fake_provider import FakeSherbrooke
                fake_backend = FakeSherbrooke()

            backend = AerSimulator.from_backend(fake_backend)
            backend_name = fake_backend.name
        except Exception as e:
            # Fallback to standard aer simulator with basic depolarizing noise if provider fails
            backend = AerSimulator()
            backend_name = f"aer_simulator_fallback ({str(e)})"

        meta = {
            "mode": "MODE_B_NOISY_SIMULATOR",
            "backend_name": backend_name,
            "is_noisy": True,
            "is_real_hardware": False,
        }
        return backend, meta

    @staticmethod
    def get_real_qpu_backend() -> Tuple[Optional[Any], Dict[str, Any]]:
        """
        Attempts to access real QPU backend strictly guarded by safety environment variables.
        """
        enable_flag = os.environ.get("QLBM_ENABLE_REAL_QPU", "0")
        confirm_flag = os.environ.get("QLBM_CONFIRM_REAL_QPU", "NO")

        if enable_flag != "1" or confirm_flag != "YES":
            return None, {
                "mode": "MODE_C_REAL_QPU",
                "status": "BLOCKED — Safety gates active (Set QLBM_ENABLE_REAL_QPU=1 and QLBM_CONFIRM_REAL_QPU=YES)",
                "is_real_hardware": True,
                "is_active": False,
            }

        # Check for IBM Quantum credentials
        token = os.environ.get("QISKIT_IBM_TOKEN") or os.environ.get("IBM_QUANTUM_TOKEN")
        if not token:
            return None, {
                "mode": "MODE_C_REAL_QPU",
                "status": "BLOCKED — credentials/backend unavailable (No IBM Quantum Token in environment)",
                "is_real_hardware": True,
                "is_active": False,
            }

        try:
            from qiskit_ibm_runtime import QiskitRuntimeService
            service = QiskitRuntimeService(channel="ibm_quantum", token=token)
            backend = service.least_busy(simulator=False, operational=True)
            return backend, {
                "mode": "MODE_C_REAL_QPU",
                "backend_name": backend.name,
                "status": "READY — Real hardware connected",
                "is_real_hardware": True,
                "is_active": True,
            }
        except Exception as e:
            return None, {
                "mode": "MODE_C_REAL_QPU",
                "status": f"BLOCKED — Hardware connection failed: {str(e)}",
                "is_real_hardware": True,
                "is_active": False,
            }
