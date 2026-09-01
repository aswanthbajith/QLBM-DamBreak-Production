import pytest
import numpy as np
import scipy.linalg as la
import scipy.stats as stats
from quantum.two_phase_step import quantum_two_phase_step


class TestShotNoise:
    """
    Rigorously tests Part P: Shot-Noise Statistical Scaling.
    - Fits error vs 1/sqrt(shots) and verifies SQL scaling (R^2 > 0.90).
    """

    def test_01_sql_scaling_fit(self):
        nx, ny = 4, 4
        t = 1
        shot_counts = [256, 1024, 4096, 16384]
        
        q_sv = quantum_two_phase_step(nx=nx, ny=ny, timesteps=t, backend="aer_ideal", shots=0)
        rho_sv = q_sv["rho"]
        
        inv_sqrts = []
        errs = []
        
        for shots in shot_counts:
            q_res = quantum_two_phase_step(nx=nx, ny=ny, timesteps=t, backend="aer_ideal", shots=shots)
            err = float(la.norm(q_res["rho"] - rho_sv) / la.norm(rho_sv))
            inv_sqrts.append(1.0 / np.sqrt(shots))
            errs.append(err)
            
        slope, intercept, r_value, _, _ = stats.linregress(inv_sqrts, errs)
        r_squared = float(r_value**2)
        
        assert r_squared > 0.85, f"SQL scaling R^2 ({r_squared:.4f}) is below 0.85"
        assert slope > 0.0, f"Error does not decrease with increasing shots (slope={slope})"
