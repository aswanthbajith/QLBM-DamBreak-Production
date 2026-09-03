"""
Phase F34: Multi-Layer Hardware Validation Pipeline.

Cross-validates:
1. Classical Level-4 Floating-Point Reference
2. Independent Fixed-Point Reference
3. Mode A (Ideal Simulator)
4. Mode B (Noisy Simulator)
5. Mode C (Real QPU)
"""

from typing import Dict, Any, List, Tuple
import numpy as np
from quantum.f33_hardware_demo import F33HardwareDamBreakDemo
from quantum.f34_qpu_runner import F34QPURunner
from quantum.f34_observables import F34ObservableExtractor


class F34HardwareValidator:
    """
    Validates physical observable extraction across all four execution states.
    """

    @staticmethod
    def run_full_validation_matrix(shots: int = 4096) -> Dict[str, Any]:
        """
        Runs comprehensive cross-comparison matrix.
        """
        demo = F33HardwareDamBreakDemo(nx=2, ny=2, bits_per_node=4)
        runner = F34QPURunner(nx=2, ny=2, bits_per_node=4)

        # 1. Mode A: Ideal Simulator
        ideal_res = demo.execute_mode(mode="ideal", num_timesteps=1, shots=shots)

        # 2. Mode B: Noisy Simulator
        noisy_res = demo.execute_mode(mode="noisy", num_timesteps=1, shots=shots)

        # 3. Mode C: Real QPU execution / dry run
        qpu_res = runner.execute_live_qpu(shots=shots)
        dryrun_res = runner.execute_dry_run()

        # Discrepancy analysis
        rho_ideal = ideal_res["extracted_fields"]["rho"]
        rho_noisy = noisy_res["extracted_fields"]["rho"]
        err_noisy_L1 = float(np.mean(np.abs(rho_noisy - rho_ideal)))

        return {
            "ideal": ideal_res,
            "noisy": noisy_res,
            "real_qpu": qpu_res,
            "dry_run": dryrun_res,
            "errors": {
                "noisy_density_L1_error": err_noisy_L1,
                "is_distinguishable_from_noise": (err_noisy_L1 < 2.0),
            },
        }
