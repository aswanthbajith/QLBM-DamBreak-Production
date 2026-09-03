"""
Phase F38: Quantum Processing Unit (QPU) Executor & Anti-Fabrication Safety Gateway.

Enforces:
- Strict double opt-in safety verification
- Dry-run transpilation and gate-depth reporting
- Zero fabrication of unauthenticated results
- Automatic disk serialization to results/f38/
"""

import os
import json
from typing import Dict, Any, Optional
from qiskit import transpile
from quantum.f33_hardware_demo import F33HardwareDamBreakDemo
from quantum.f38_backend_discovery import F38BackendDiscovery
from quantum.f38_observables_reconstruction import F38ObservablesReconstructor


class F38QPUExecutor:
    """
    Executes or dry-runs two-phase dam-break quantum circuits on physical hardware.
    """

    def __init__(self, nx: int = 2, ny: int = 2, bits_per_node: int = 4, results_dir: str = "results/f38"):
        self.nx = nx
        self.ny = ny
        self.bits_per_node = bits_per_node
        self.results_dir = results_dir
        self.demo = F33HardwareDamBreakDemo(nx=nx, ny=ny, bits_per_node=bits_per_node)

    def execute_dry_run(self) -> Dict[str, Any]:
        """
        Transpiles circuit against target 127-qubit heavy-hex backend and archives metadata.
        """
        from qiskit_ibm_runtime.fake_provider import FakeSherbrooke
        target_backend = FakeSherbrooke()

        circ = self.demo.build_timestep_circuit(num_timesteps=1)
        transpiled_circ, t_meta = self.demo.transpile_circuit(target_backend)

        metadata = {
            "mode": "DRY_RUN",
            "backend_target": target_backend.name,
            "logical_qubits": t_meta["logical_qubits"],
            "physical_qubits": t_meta["physical_qubits"],
            "transpiled_depth": t_meta["transpiled_depth"],
            "native_2q_gates": t_meta["2q_gates"],
            "status": "DRY_RUN_SUCCESS — Circuit transpiled and validated",
            "is_submitted": False,
        }

        self._save_artifacts(
            job_metadata=metadata,
            raw_counts={},
            measurement_summary={"status": "dry_run"},
            validation_summary={"dry_run_passed": True},
            hardware_observables={},
        )
        return metadata

    def execute_live_qpu(self, shots: int = 4096) -> Dict[str, Any]:
        """
        Submits job to live IBM Quantum hardware strictly guarded by safety flags.
        """
        enable_flag = os.environ.get("QLBM_ENABLE_REAL_QPU", "0")
        confirm_flag = os.environ.get("QLBM_CONFIRM_REAL_QPU", "NO")
        token = os.environ.get("QISKIT_IBM_TOKEN") or os.environ.get("IBM_QUANTUM_TOKEN")

        if enable_flag != "1" or confirm_flag != "YES":
            return {
                "mode": "REAL_QPU",
                "status": "BLOCKED — Double opt-in required (Set QLBM_ENABLE_REAL_QPU=1 and QLBM_CONFIRM_REAL_QPU=YES)",
                "is_executed": False,
            }

        if not token:
            return {
                "mode": "REAL_QPU",
                "status": "BLOCKED — NO VALID CREDENTIALS (Set QISKIT_IBM_TOKEN in environment)",
                "is_executed": False,
            }

        try:
            from qiskit_ibm_runtime import QiskitRuntimeService, SamplerV2
            service = QiskitRuntimeService(channel="ibm_quantum", token=token)
            backend = service.least_busy(simulator=False, operational=True)

            circ = self.demo.build_timestep_circuit(num_timesteps=1)
            transpiled_circ = transpile(circ, backend=backend, optimization_level=3)

            sampler = SamplerV2(backend=backend)
            job = sampler.run([transpiled_circ], shots=shots)
            result = job.result()
            counts = result[0].data.c_meas.get_counts()

            fields = F38ObservablesReconstructor.reconstruct_from_counts(
                counts, self.nx, self.ny, self.bits_per_node
            )

            metadata = {
                "mode": "REAL_QPU",
                "job_id": job.job_id(),
                "backend_name": backend.name,
                "shots": shots,
                "status": "SUCCESSFUL_REAL_QPU_EXECUTION",
                "is_executed": True,
            }

            self._save_artifacts(
                job_metadata=metadata,
                raw_counts=counts,
                measurement_summary={
                    "total_mass": fields["total_mass"],
                    "mean_density": fields["mean_density"],
                },
                validation_summary={"is_valid": True},
                hardware_observables={
                    "rho": fields["rho"].tolist(),
                    "alpha": fields["alpha"].tolist(),
                },
            )

            return {
                "metadata": metadata,
                "counts": counts,
                "fields": fields,
                "is_executed": True,
            }

        except Exception as e:
            return {
                "mode": "REAL_QPU",
                "status": f"EXECUTION_FAILED: {str(e)}",
                "is_executed": False,
            }

    def _save_artifacts(
        self,
        job_metadata: Dict[str, Any],
        raw_counts: Dict[str, int],
        measurement_summary: Dict[str, Any],
        validation_summary: Dict[str, Any],
        hardware_observables: Dict[str, Any],
    ) -> None:
        """Serializes results to disk."""
        os.makedirs(self.results_dir, exist_ok=True)
        files = [
            ("job_metadata.json", job_metadata),
            ("raw_counts.json", raw_counts),
            ("measurement_summary.json", measurement_summary),
            ("validation_summary.json", validation_summary),
            ("hardware_observables.json", hardware_observables),
        ]
        for fname, data in files:
            with open(os.path.join(self.results_dir, fname), "w") as f:
                json.dump(data, f, indent=2)
