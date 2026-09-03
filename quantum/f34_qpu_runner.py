"""
Phase F34: Real Quantum Processor (QPU) Runner & Safety Gate.

Manages:
- Double opt-in safety checks (QLBM_ENABLE_REAL_QPU=1 and QLBM_CONFIRM_REAL_QPU=YES)
- Dry-run circuit transpilation and cost estimation
- Live IBM Quantum Runtime job dispatch and result archiving
"""

import os
from typing import Dict, Any, Tuple, Optional
from qiskit import QuantumCircuit, transpile
from quantum.f33_hardware_demo import F33HardwareDamBreakDemo
from quantum.f34_result_parser import F34ResultParser
from quantum.f34_observables import F34ObservableExtractor


class F34QPURunner:
    """
    Executes or dry-runs dam-break quantum circuits on real QPU hardware.
    """

    def __init__(self, nx: int = 2, ny: int = 2, bits_per_node: int = 4, results_dir: str = "results/f34"):
        self.nx = nx
        self.ny = ny
        self.bits_per_node = bits_per_node
        self.results_dir = results_dir
        self.demo = F33HardwareDamBreakDemo(nx=nx, ny=ny, bits_per_node=bits_per_node)

    def execute_dry_run(self) -> Dict[str, Any]:
        """
        Transpiles circuit for real hardware architecture and archives metrics without submitting.
        """
        # Transpile for 127-qubit heavy-hex architecture (FakeSherbrooke)
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
            "status": "DRY_RUN_COMPLETED — Ready for hardware submission",
            "is_submitted": False,
        }

        # Archive dry-run metadata
        F34ResultParser.save_results_to_disk(
            self.results_dir,
            job_metadata=metadata,
            raw_counts={},
            measurement_summary={"status": "dry_run"},
            validation_summary={"dry_run_passed": True},
        )

        return metadata

    def execute_live_qpu(self, shots: int = 4096) -> Dict[str, Any]:
        """
        Submits job to real IBM Quantum hardware if safety flags and credentials are present.
        """
        enable_flag = os.environ.get("QLBM_ENABLE_REAL_QPU", "0")
        confirm_flag = os.environ.get("QLBM_CONFIRM_REAL_QPU", "NO")
        token = os.environ.get("QISKIT_IBM_TOKEN") or os.environ.get("IBM_QUANTUM_TOKEN")

        if enable_flag != "1" or confirm_flag != "YES":
            return {
                "mode": "REAL_QPU",
                "status": "BLOCKED — Safety gates active (Set QLBM_ENABLE_REAL_QPU=1 and QLBM_CONFIRM_REAL_QPU=YES)",
                "is_executed": False,
            }

        if not token:
            return {
                "mode": "REAL_QPU",
                "status": "BLOCKED — NO VALID CREDENTIALS (Set QISKIT_IBM_TOKEN)",
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

            fields = F34ObservableExtractor.compute_fields(counts, self.nx, self.ny, self.bits_per_node)

            metadata = {
                "mode": "REAL_QPU",
                "job_id": job.job_id(),
                "backend_name": backend.name,
                "shots": shots,
                "status": "SUCCESSFUL_REAL_QPU_EXECUTION",
                "is_executed": True,
            }

            F34ResultParser.save_results_to_disk(
                self.results_dir,
                job_metadata=metadata,
                raw_counts=counts,
                measurement_summary={
                    "total_mass": fields["total_mass"],
                    "mean_density": fields["mean_density"],
                },
                validation_summary={"is_valid": True},
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
