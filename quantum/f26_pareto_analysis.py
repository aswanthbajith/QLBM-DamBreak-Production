"""
Phase F26: Precision/Accuracy Pareto Analysis and Architectural Comparison.

Sweeps:
- Precisions: Q4.8, Q4.10, Q4.12, Q4.14, Q4.16, Q4.18, Q4.20
- Architectures:
    - Architecture A: Fully Parallel 2D Lattice Nodes (Peak parallelism, high qubit count)
    - Architecture B: Shared Execution Unit with Spatial Registers (Time-multiplexed arithmetic)
"""

from typing import Dict, Any, List
import numpy as np

from classical.level4_two_phase import Level4TwoPhaseLBM
from quantum.f21_fixed_point import F21FixedPointCSFMath
from quantum.f26_optimized_bgk import F26OptimizedBGKEngine


class F26ParetoAnalysis:
    """
    Rigorously constructs the Precision/Accuracy and Hardware Resource Pareto Front.
    """

    @staticmethod
    def run_precision_accuracy_sweep(
        nx: int = 4,
        ny: int = 4,
        sigma: float = 0.001,
    ) -> List[Dict[str, Any]]:
        """
        Runs one-step simulation across Q4.8 through Q4.20 and measures point-wise errors.
        """
        c_lbm = Level4TwoPhaseLBM(nx=nx, ny=ny, sigma=sigma, g_acc=-0.0005, dam_width_ratio=0.5, dam_height_ratio=0.5)
        c_lbm.step()
        c_rho_hydro = np.sum(c_lbm.f, axis=0)

        results = []
        for name, frac in [
            ("Q4.8", 8),
            ("Q4.10", 10),
            ("Q4.12", 12),
            ("Q4.14", 14),
            ("Q4.16", 16),
            ("Q4.18", 18),
            ("Q4.20", 20),
        ]:
            math = F21FixedPointCSFMath(frac_bits=frac)
            bgk = F26OptimizedBGKEngine(frac_bits=frac)

            # Initialize initial dam state in fixed-point
            x_grid, y_grid = np.meshgrid(np.arange(nx), np.arange(ny))
            dam_mask = (x_grid < 0.5 * nx) & (y_grid < 0.5 * ny)
            rho_init = np.where(dam_mask, 1.0, 0.1)
            alpha_init = np.where(dam_mask, 1.0, 0.0)

            # Simulate one node BGK step
            f_in = [math.to_fixed(rho_init[0, 0] / 9.0)] * 9
            g_in = [math.to_fixed(alpha_init[0, 0] / 9.0)] * 9

            f_out, g_out, meta = bgk.evaluate_optimized_bgk_map(f_in, g_in)

            f_float = [math.to_float(val) for val in f_out]
            rho_sim = sum(f_float)
            err_rho = abs(rho_sim - rho_init[0, 0])
            lsb = 1.0 / (1 << frac)

            results.append({
                "format": name,
                "frac_bits": frac,
                "lsb_resolution": lsb,
                "rho_error": err_rho,
                "is_mass_conserved": meta["is_mass_conserved"],
                "is_phase_conserved": meta["is_phase_conserved"],
            })
        return results

    @staticmethod
    def get_architectural_comparison(nx: int = 128, ny: int = 64, bit_width: int = 16) -> Dict[str, Any]:
        """
        Compares Architecture A (Parallel 2D Grid) vs Architecture B (Shared Arithmetic Core).
        """
        num_nodes = nx * ny  # 8192
        n = bit_width

        # Architecture A: Every node has full local system + env + workspace registers
        arch_a_qubits = num_nodes * (18 * n + 18 * n + 3 * n)  # 8192 * 624 = 5,111,808

        # Architecture B: Spatial memory holds system populations + shared arithmetic execution core
        # Memory per node = 18 * n = 288 qubits (populations)
        # Shared execution unit = 18 * n (env/scratch) + 3 * n (CSF/arithmetic) = 336 qubits
        arch_b_qubits = (num_nodes * 18 * n) + (18 * n + 3 * n)  # 8192 * 288 + 336 = 2,359,632

        return {
            "domain": f"{nx}x{ny}",
            "num_nodes": num_nodes,
            "architecture_A_parallel_qubits": arch_a_qubits,
            "architecture_B_shared_core_qubits": arch_b_qubits,
            "memory_reduction_factor": float(arch_a_qubits) / arch_b_qubits,
        }
