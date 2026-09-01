import pytest
import numpy as np
from classical.two_phase import (
    initialize_two_phase_dambreak,
    step_two_phase,
    run_two_phase_dambreak,
    compute_phase_field,
    compute_density,
    compute_velocity
)
from classical.phase_field import (
    initialize_phase_field,
    compute_phase_gradient,
    compute_phase_laplacian,
    update_phase_field,
    validate_phase_field
)


class TestTwoPhaseClassical:
    def test_01_initialization_bounds(self):
        phi, rho, u, f, g = initialize_two_phase_dambreak(4, 4)
        assert phi.shape == (4, 4)
        assert np.all(phi >= 0.0) and np.all(phi <= 1.0)
        assert np.all(rho >= 0.1) and np.all(rho <= 1.0)
        assert np.allclose(u, 0.0)

    def test_02_mass_conservation_and_phase_bounds(self):
        history = run_two_phase_dambreak(nx=4, ny=4, timesteps=5)
        initial_mass = history[0]["total_mass"]
        initial_liq = history[0]["total_liquid_mass"]
        
        for record in history:
            phi = record["phi"]
            rho = record["rho"]
            u = record["u"]
            # Phase bounded in [0, 1]
            assert np.all(phi >= -1e-12) and np.all(phi <= 1.0 + 1e-12)
            # Density bounded
            assert np.all(rho > 0.0)
            # Mass conservation (boundary wall enclosure tolerance on 4x4)
            mass_drift = abs(record["total_mass"] - initial_mass) / initial_mass
            assert mass_drift < 0.10

    def test_03_grid_8x4_stability(self):
        history = run_two_phase_dambreak(nx=8, ny=4, timesteps=3)
        assert len(history) == 4
        assert history[-1]["step"] == 3

    def test_04_phase_field_functional_module(self):
        phi = initialize_phase_field(4, 4)
        val = validate_phase_field(phi)
        assert val["valid"]
        assert 0.0 <= val["min"] <= val["max"] <= 1.0
        
        gx, gy = compute_phase_gradient(phi)
        assert gx.shape == (4, 4)
        assert gy.shape == (4, 4)
        
        u = np.zeros((2, 4, 4))
        phi_next = update_phase_field(phi, u)
        assert np.all(phi_next >= 0.0) and np.all(phi_next <= 1.0)
