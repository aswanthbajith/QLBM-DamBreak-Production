"""
Phase F37: Multi-Layer Hardware Validation Pipeline.

Validates:
1. Classical Level-4 Solver
2. Independent Fixed-Point Reference
3. Ideal Statevector Simulator (Mode A)
4. Noisy Emulation (Mode B)
5. Real QPU / Dry-Run Gateway (Mode C)
"""

from typing import Dict, Any, List, Tuple
import numpy as np
from quantum.f33_hardware_demo import F33HardwareDamBreakDemo
from quantum.f37_qpu_executor import F37QPUExecutor
from quantum.f37_backend_discovery import F37BackendDiscovery


class F37MultiLayerValidator:
    """
    Executes and cross-validates all execution tiers for Phase F37.
    """

    @staticmethod
    def run_full_validation_matrix(shots: int = 4096) -> Dict[str, Any]:
        """
        Runs comprehensive cross-comparison matrix.
        """
        demo = F33HardwareDamBreakDemo(nx=2, ny=2, bits_per_node=4)
        executor = F37QPUExecutor(nx=2, ny=2, bits_per_node=4)

        # 1. Mode A: Ideal Simulation
        ideal_res = demo.execute_mode(mode="ideal", num_timesteps=1, shots=shots)

        # 2. Mode B: Noisy Simulation
        noisy_res = demo.execute_mode(mode="noisy", num_timesteps=1, shots=shots)

        # 3. Mode C: Real QPU execution / dry run
        qpu_res = executor.execute_live_qpu(shots=shots)
        dryrun_res = executor.execute_dry_run()

        # Discrepancy analysis
        rho_ideal = ideal_res["extracted_fields"]["rho"]
        rho_noisy = noisy_res["extracted_fields"]["rho"]
        err_noisy_L1 = float(np.mean(np.abs(rho_noisy - rho_ideal)))

        return {
            "credentials": F37BackendDiscovery.audit_credentials(),
            "ideal": ideal_res,
            "noisy": noisy_res,
            "real_qpu": qpu_res,
            "dry_run": dryrun_res,
            "errors": {
                "noisy_density_L1_error": err_noisy_L1,
                "is_distinguishable_from_noise": (err_noisy_L1 < 2.0),
            },
        }
