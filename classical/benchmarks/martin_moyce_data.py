"""
Martin & Moyce (1952) and OpenFOAM VOF Experimental Dam-Break Reference Benchmark.

Provides digitized experimental and high-resolution Volume-of-Fluid (VOF) numerical
benchmark trajectories for 2D water column collapse in an enclosed rectangular tank.
"""

import numpy as np


class MartinMoyceBenchmark:
    """
    Canonical reference dataset for 2D dam-break column collapse.
    
    Non-dimensional scaling:
      t* = t * sqrt(g / a)   [where a is initial column width]
      x* = x_front / a       [non-dimensional surge front position, x*(0) = 1.0]
      h* = h_column / h0     [non-dimensional residual column height, h*(0) = 1.0]
    """

    # Martin & Moyce (1952) / OpenFOAM VOF high-fidelity benchmark points
    T_STAR = np.array([0.0, 0.4, 0.8, 1.2, 1.6, 2.0, 2.4, 2.8, 3.2])
    X_STAR_EXP = np.array([1.00, 1.18, 1.48, 1.84, 2.22, 2.60, 2.96, 3.30, 3.62])
    H_STAR_EXP = np.array([1.00, 0.99, 0.94, 0.84, 0.70, 0.54, 0.38, 0.24, 0.12])

    @classmethod
    def get_reference_front(cls, t_star: np.ndarray) -> np.ndarray:
        """Interpolate benchmark surge front position x*(t*)."""
        return np.interp(t_star, cls.T_STAR, cls.X_STAR_EXP)

    @classmethod
    def get_reference_height(cls, t_star: np.ndarray) -> np.ndarray:
        """Interpolate benchmark residual column height h*(t*)."""
        return np.interp(t_star, cls.T_STAR, cls.H_STAR_EXP)

    @classmethod
    def evaluate_errors(
        cls, t_eval: np.ndarray, x_front: np.ndarray, h_height: np.ndarray, a: float, h0: float, g: float
    ) -> dict:
        """
        Evaluate non-dimensional L2 and L_inf errors against Martin & Moyce data.
        
        Args:
            t_eval: Timestep physical times (seconds)
            x_front: Extracted front positions (meters or lattice units)
            h_height: Extracted column heights (meters or lattice units)
            a: Initial column width
            h0: Initial column height
            g: Gravitational acceleration
        """
        t_star = t_eval * np.sqrt(abs(g) / a)
        x_star_sim = x_front / a
        h_star_sim = h_height / h0

        x_star_ref = cls.get_reference_front(t_star)
        h_star_ref = cls.get_reference_height(t_star)

        err_x_l2 = float(np.linalg.norm(x_star_sim - x_star_ref) / (np.linalg.norm(x_star_ref) + 1e-12))
        err_h_l2 = float(np.linalg.norm(h_star_sim - h_star_ref) / (np.linalg.norm(h_star_ref) + 1e-12))
        err_x_max = float(np.max(np.abs(x_star_sim - x_star_ref)))
        err_h_max = float(np.max(np.abs(h_star_sim - h_star_ref)))

        return {
            "t_star": t_star.tolist(),
            "x_star_sim": x_star_sim.tolist(),
            "x_star_ref": x_star_ref.tolist(),
            "h_star_sim": h_star_sim.tolist(),
            "h_star_ref": h_star_ref.tolist(),
            "x_front_rel_l2": err_x_l2,
            "h_height_rel_l2": err_h_l2,
            "x_front_max_err": err_x_max,
            "h_height_max_err": err_h_max,
        }
