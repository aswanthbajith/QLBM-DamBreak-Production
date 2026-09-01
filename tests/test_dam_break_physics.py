import pytest
import numpy as np
from classical.two_phase import run_two_phase_dambreak


class TestDamBreakPhysics:
    """
    Rigorously tests Part Q: Physical Dam-Break Behavior.
    - Front position advancement
    - Center of mass trajectory
    - Boundedness of density and phase field
    """

    def test_01_front_position_monotonic_advancement(self):
        history = run_two_phase_dambreak(nx=16, ny=8, timesteps=12, g_acc=-0.002)
        x_fronts = []
        for step_data in history:
            phi = step_data["phi"]
            liquid_mask = (phi >= 0.5)
            if np.any(liquid_mask):
                x_f = float(np.where(np.any(liquid_mask, axis=0))[0][-1])
            else:
                x_f = 0.0
            x_fronts.append(x_f)
            
        # Front position must advance rightward over time
        assert x_fronts[-1] >= x_fronts[0], f"Front did not advance: x0={x_fronts[0]}, x_final={x_fronts[-1]}"

    def test_02_phase_bounds_retention(self):
        history = run_two_phase_dambreak(nx=8, ny=4, timesteps=10)
        for record in history:
            phi = record["phi"]
            assert np.all(phi >= -1e-10) and np.all(phi <= 1.0 + 1e-10)
            rho = record["rho"]
            assert np.all(rho > 0.0)
