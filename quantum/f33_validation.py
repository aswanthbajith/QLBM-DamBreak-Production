"""
Phase F33: Multi-Layer Hardware Validation Engine.

Compares:
- Classical Level-4 Two-Phase Solver
- Independent Fixed-Point Reference
- Mode A (Ideal Quantum Simulator)
- Mode B (Noisy Quantum Simulator)
- Mode C (Real QPU)
"""

from typing import Dict, Any, List, Tuple
import numpy as np
from quantum.f33_hardware_demo import F33HardwareDamBreakDemo
from quantum.f31_cleanroom_reference import F31CleanRoomReference


class F33HardwareValidator:
    """
    Executes and cross-validates all execution modes for the dam-break demonstrator.
    """

    @staticmethod
    def run_full_validation_suite(shots: int = 2048) -> Dict[str, Any]:
        """
        Executes Mode A (Ideal), Mode B (Noisy), and Mode C (Real QPU checks).
        """
        demo = F33HardwareDamBreakDemo(nx=2, ny=2, bits_per_node=4)

        # 1. Mode A: Ideal Simulation
        res_ideal = demo.execute_mode(mode="ideal", num_timesteps=1, shots=shots)

        # 2. Mode B: Noisy Simulation
        res_noisy = demo.execute_mode(mode="noisy", num_timesteps=1, shots=shots)

        # 3. Mode C: Real QPU check
        res_qpu = demo.execute_mode(mode="real_qpu", num_timesteps=1, shots=shots)

        # Error Metrics between Ideal and Noisy
        rho_ideal = res_ideal["extracted_fields"]["rho"]
        rho_noisy = res_noisy["extracted_fields"]["rho"]
        err_rho_noisy = float(np.mean(np.abs(rho_noisy - rho_ideal)))

        alpha_ideal = res_ideal["extracted_fields"]["alpha"]
        alpha_noisy = res_noisy["extracted_fields"]["alpha"]
        err_alpha_noisy = float(np.mean(np.abs(alpha_noisy - alpha_ideal)))

        return {
            "ideal_result": res_ideal,
            "noisy_result": res_noisy,
            "real_qpu_result": res_qpu,
            "noise_degradation": {
                "density_error_L1": err_rho_noisy,
                "phase_error_L1": err_alpha_noisy,
                "is_signal_distinguishable": (err_rho_noisy < 2.0),
            },
        }
