"""
Phase F23: Comprehensive Two-Phase LBM Equivalence Engine.

Compares classical Level-4 two-phase solver against the quantum CPTP channel solver
across all physical and macroscopic observables.
"""

from typing import Dict, Any, List, Tuple
import numpy as np

from classical.level4_two_phase import Level4TwoPhaseLBM
from quantum.f22_channel_solver import PhaseF22CPTPChannelSolver


class F23TwoPhaseEquivalenceEngine:
    """
    Rigorously benchmarks physical equivalence between classical Level-4 and quantum CPTP channel.
    """

    @staticmethod
    def run_one_step_lattice_comparison(
        nx: int = 4,
        ny: int = 4,
        sigma: float = 0.001,
        g_acc: float = -0.0005,
    ) -> Dict[str, Any]:
        """
        Runs exactly 1 timestep on both solvers and compares all fields cell-by-cell.
        """
        c_solver = Level4TwoPhaseLBM(nx=nx, ny=ny, sigma=sigma, g_acc=g_acc, dam_width_ratio=0.5, dam_height_ratio=0.5)
        q_solver = PhaseF22CPTPChannelSolver(nx=nx, ny=ny, sigma=sigma, g_acc=g_acc, dam_width_ratio=0.5, dam_height_ratio=0.5)

        c_solver.step()
        q_solver.step()

        q_fields = q_solver.decode_final_fields()
        c_rho_hydro = np.sum(c_solver.f, axis=0)
        err_f_inf = float(np.max(np.abs(q_fields["f"] - c_solver.f)))
        err_g_inf = float(np.max(np.abs(q_fields["g"] - c_solver.g)))
        err_rho_inf = float(np.max(np.abs(q_fields["rho"] - c_rho_hydro)))
        err_alpha_inf = float(np.max(np.abs(q_fields["alpha"] - c_solver.alpha)))
        err_u_inf = float(np.max(np.abs(q_fields["ux"] - c_solver.u[0])))

        rel_f_l2 = float(np.linalg.norm(q_fields["f"] - c_solver.f) / np.linalg.norm(c_solver.f))
        rel_g_l2 = float(np.linalg.norm(q_fields["g"] - c_solver.g) / (np.linalg.norm(c_solver.g) + 1e-14))

        return {
            "nx": nx,
            "ny": ny,
            "sigma": sigma,
            "err_f_Linf": err_f_inf,
            "err_g_Linf": err_g_inf,
            "err_rho_Linf": err_rho_inf,
            "err_alpha_Linf": err_alpha_inf,
            "err_u_Linf": err_u_inf,
            "rel_f_L2": rel_f_l2,
            "rel_g_L2": rel_g_l2,
            "is_equivalent_within_q412": (err_f_inf < 0.01),
        }

    @staticmethod
    def run_multistep_comparison_trajectory(
        nx: int = 4,
        ny: int = 4,
        sigma: float = 0.001,
        timesteps: List[int] = [1, 2, 4, 8, 16, 32],
    ) -> List[Dict[str, Any]]:
        """
        Runs multi-step trajectory comparing at discrete checkpoint steps T.
        """
        c_solver = Level4TwoPhaseLBM(nx=nx, ny=ny, sigma=sigma, g_acc=-0.0005, dam_width_ratio=0.5, dam_height_ratio=0.5)
        q_solver = PhaseF22CPTPChannelSolver(nx=nx, ny=ny, sigma=sigma, g_acc=-0.0005, dam_width_ratio=0.5, dam_height_ratio=0.5)

        initial_fields = q_solver.decode_final_fields()
        initial_mass = initial_fields["total_mass"]

        results = []
        for t in timesteps:
            steps_needed = t - q_solver.num_quantum_timesteps
            for _ in range(steps_needed):
                c_solver.step()
                q_solver.step()

            q_fields = q_solver.decode_final_fields()
            err_f = float(np.max(np.abs(q_fields["f"] - c_solver.f)))
            err_g = float(np.max(np.abs(q_fields["g"] - c_solver.g)))
            err_rho = float(np.max(np.abs(q_fields["rho"] - c_solver.rho)))
            err_alpha = float(np.max(np.abs(q_fields["alpha"] - c_solver.alpha)))
            mass_drift = abs(q_fields["total_mass"] - initial_mass)

            results.append({
                "T": t,
                "f_Linf": err_f,
                "g_Linf": err_g,
                "rho_Linf": err_rho,
                "alpha_Linf": err_alpha,
                "total_mass": q_fields["total_mass"],
                "mass_drift": mass_drift,
                "is_conserved": (mass_drift == 0.0),
            })
        return results
