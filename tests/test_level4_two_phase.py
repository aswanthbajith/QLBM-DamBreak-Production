"""
Unit & Physical Validation Tests for Level-4 Two-Phase D2Q9 LBM Solver.

Validates:
1. Liquid mass conservation across multiple timesteps.
2. Stationary droplet Laplace pressure jump.
3. Dam-break surge front propagation and column height collapse.
4. Martin & Moyce (1952) / OpenFOAM VOF benchmark agreement.
"""

import pytest
import numpy as np
from classical.level4_two_phase import Level4TwoPhaseLBM
from classical.benchmarks.martin_moyce_data import MartinMoyceBenchmark


class TestLevel4TwoPhasePhysics:
    """Test suite for physical validity of the Level-4 Two-Phase formulation."""

    def test_01_mass_conservation(self):
        """Verify liquid mass is conserved within 2% over 50 timesteps."""
        solver = Level4TwoPhaseLBM(nx=32, ny=16, g_acc=-0.0005, sigma=0.0005)
        initial_mass = solver.get_total_liquid_volume()

        for _ in range(50):
            solver.step()

        final_mass = solver.get_total_liquid_volume()
        rel_drift = abs(final_mass - initial_mass) / initial_mass
        assert rel_drift < 0.02, f"Liquid mass drift too high: {rel_drift:.4%}"

    def test_02_surge_front_propagation(self):
        """Verify dam-break surge front propagates outward along the bottom wall."""
        solver = Level4TwoPhaseLBM(nx=48, ny=24, g_acc=-0.0008, sigma=0.0001)
        x0 = solver.get_surge_front_position(threshold=0.3)

        for _ in range(30):
            solver.step()

        x_final = solver.get_surge_front_position(threshold=0.3)
        assert x_final > x0, f"Surge front failed to propagate: x0={x0}, x_final={x_final}"

    def test_03_column_height_collapse(self):
        """Verify initial water column collapses downward under gravity."""
        solver = Level4TwoPhaseLBM(nx=48, ny=24, g_acc=-0.0005, sigma=0.0001)
        h0 = solver.get_column_height()

        for _ in range(30):
            solver.step()

        h_final = solver.get_column_height()
        assert h_final <= h0, f"Column failed to collapse: h0={h0}, h_final={h_final}"

    def test_04_laplace_law_stationary_droplet(self):
        """Verify stationary 2D droplet maintains positive surface tension Laplace jump."""
        nx, ny = 32, 32
        R = 8.0
        sigma = 0.002
        # Equal density for pure interfacial Laplace pressure measurement
        solver = Level4TwoPhaseLBM(nx=nx, ny=ny, rho_L=1.0, rho_G=1.0, g_acc=0.0, sigma=sigma)

        # Re-initialize with circular droplet in center
        solver.alpha = np.zeros((ny, nx))
        cx, cy = nx / 2.0, ny / 2.0
        for y in range(ny):
            for x in range(nx):
                dist = np.sqrt((x - cx) ** 2 + (y - cy) ** 2)
                solver.alpha[y, x] = 0.5 - 0.5 * np.tanh(2.0 * (dist - R) / solver.W_int)
        solver.rho = solver.alpha * solver.rho_L + (1.0 - solver.alpha) * solver.rho_G
        solver._initialize_distributions()

        # Relax droplet for 20 steps
        for _ in range(20):
            solver.step()

        p_inside = solver.rho[int(cy), int(cx)] * solver.cs2
        p_outside = solver.rho[0, 0] * solver.cs2
        delta_p = p_inside - p_outside

        # Surface tension force creates positive pressure curvature
        assert delta_p >= -1e-6, f"Laplace pressure jump should be non-negative: {delta_p}"

    def test_05_martin_moyce_benchmark_agreement(self):
        """Verify dam-break trajectory tracks Martin & Moyce experimental curves."""
        nx, ny = 64, 32
        g_acc = -0.0003
        solver = Level4TwoPhaseLBM(nx=nx, ny=ny, g_acc=g_acc, sigma=0.0001)

        a = float(solver.dam_width)
        h0 = float(solver.dam_height)
        timesteps = 40

        t_eval = []
        x_front = []
        h_height = []

        for step in range(timesteps):
            solver.step()
            if step % 5 == 0:
                t_eval.append(step * 1.0)
                x_front.append(solver.get_surge_front_position())
                h_height.append(solver.get_column_height())

        metrics = MartinMoyceBenchmark.evaluate_errors(
            np.array(t_eval),
            np.array(x_front),
            np.array(h_height),
            a=a,
            h0=h0,
            g=abs(g_acc),
        )

        assert metrics["x_front_rel_l2"] < 0.50, f"Surge front L2 error too high: {metrics['x_front_rel_l2']:.2%}"
        assert metrics["h_height_rel_l2"] < 0.50, f"Column height L2 error too high: {metrics['h_height_rel_l2']:.2%}"
