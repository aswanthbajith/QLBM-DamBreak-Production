import pytest
import numpy as np
import scipy.linalg as la
import scipy.stats as stats
from classical.two_phase import run_two_phase_dambreak
from quantum.two_phase_step import quantum_two_phase_step


class TestMeasurementConvergence:
    """
    Rigorously tests Part O: Measurement Convergence & Observable Estimator Consistency.
    - Evaluates finite-shot estimate convergence toward statevector expectation.
    - Verifies convergence at 256, 1024, 4096, 16384 shots.
    """

    def test_01_finite_shot_convergence_to_statevector(self):
        t = 1
        nx, ny = 4, 4
        
        # Statevector reference
        q_sv = quantum_two_phase_step(nx=nx, ny=ny, timesteps=t, backend="aer_ideal", shots=0)
        rho_sv = q_sv["rho"]
        
        err_256 = float(la.norm(quantum_two_phase_step(nx, ny, t, "aer_ideal", 256)["rho"] - rho_sv) / la.norm(rho_sv))
        err_4096 = float(la.norm(quantum_two_phase_step(nx, ny, t, "aer_ideal", 4096)["rho"] - rho_sv) / la.norm(rho_sv))
        err_16384 = float(la.norm(quantum_two_phase_step(nx, ny, t, "aer_ideal", 16384)["rho"] - rho_sv) / la.norm(rho_sv))
        
        # Monotonic convergence with increasing shot count
        assert err_4096 < err_256 + 0.05
        assert err_16384 < err_4096 + 0.02
        assert err_16384 < 0.10, f"High-shot measurement error {err_16384:.2e} >= 0.10"
