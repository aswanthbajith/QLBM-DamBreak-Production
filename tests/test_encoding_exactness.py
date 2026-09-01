import pytest
import numpy as np
from classical.two_phase import initialize_two_phase_dambreak, compute_density, compute_velocity, compute_phase_field
from classical.equilibrium import compute_equilibrium
from quantum.two_phase_encoding import (
    get_two_phase_register_layout,
    encode_distribution,
    decode_distribution,
    validate_normalization
)


class TestEncodingExactness:
    """
    Rigorously tests Part C Quantum Encoding audit:
    - Normalization, positivity, reconstructability, mass consistency, phase consistency, velocity consistency
    - Tests random valid states, equilibrium states, dam-break initial states, non-equilibrium states, multiple phase distributions
    - Verifies encode -> decode -> encode idempotence and reconstruction error < 1e-12
    """

    def _verify_state_reconstruction(self, f_orig, phi_orig, nx, ny, desc=""):
        # 1. Encode
        state, total_mass, layout = encode_distribution(f_orig, phi_orig)
        
        # 2. Check normalization & positivity
        is_norm, norm = validate_normalization(state)
        assert is_norm, f"{desc}: State normalization failed, norm={norm}"
        assert np.isclose(norm, 1.0, atol=1e-12)
        
        # 3. Decode
        probs = np.abs(state)**2
        rho_rec, u_rec, phi_rec = decode_distribution(probs, layout, total_mass=total_mass)
        
        # Original macroscopic fields
        rho_orig = compute_density(f_orig)
        u_orig = compute_velocity(f_orig, rho_orig)
        
        # Reconstructed populations f_rec
        n_qx = layout["n_qx"]
        n_qy = layout["n_qy"]
        n_qvel = layout["n_qvel"]
        
        f_rec = np.zeros_like(f_orig)
        for i in range(9):
            for y in range(ny):
                for x in range(nx):
                    idx_gas = (0 << (n_qx + n_qy + n_qvel)) | (i << (n_qx + n_qy)) | (y << n_qx) | x
                    idx_liq = (1 << (n_qx + n_qy + n_qvel)) | (i << (n_qx + n_qy)) | (y << n_qx) | x
                    f_rec[i, y, x] = total_mass * (probs[idx_gas] + probs[idx_liq])
                    
        # Check errors
        err_f = float(np.linalg.norm(f_rec - f_orig) / (np.linalg.norm(f_orig) + 1e-14))
        err_rho = float(np.linalg.norm(rho_rec - rho_orig) / (np.linalg.norm(rho_orig) + 1e-14))
        err_phi = float(np.linalg.norm(phi_rec - phi_orig) / (np.linalg.norm(phi_orig) + 1e-14))
        err_u = float(np.linalg.norm(u_rec - u_orig))
        
        assert err_f < 1e-12, f"{desc}: Population reconstruction error {err_f:.2e} >= 1e-12"
        assert err_rho < 1e-12, f"{desc}: Density reconstruction error {err_rho:.2e} >= 1e-12"
        assert err_phi < 1e-12, f"{desc}: Phase reconstruction error {err_phi:.2e} >= 1e-12"
        assert err_u < 1e-12, f"{desc}: Velocity reconstruction error {err_u:.2e} >= 1e-12"
        
        # 4. Re-encode (idempotence)
        state2, mass2, _ = encode_distribution(f_rec, phi_rec)
        err_state = float(np.linalg.norm(state2 - state))
        assert err_state < 1e-12, f"{desc}: Roundtrip state idempotence error {err_state:.2e} >= 1e-12"

    def test_01_dam_break_initial_state(self):
        for nx, ny in [(4, 4), (8, 4), (8, 8)]:
            phi, rho, u, f, g = initialize_two_phase_dambreak(nx, ny)
            self._verify_state_reconstruction(f, phi, nx, ny, desc=f"Dam-Break {nx}x{ny}")

    def test_02_random_valid_states(self):
        np.random.seed(42)
        for nx, ny in [(4, 4), (8, 4)]:
            for _ in range(5):
                f_rand = np.random.uniform(0.01, 1.0, (9, ny, nx))
                phi_rand = np.random.uniform(0.0, 1.0, (ny, nx))
                self._verify_state_reconstruction(f_rand, phi_rand, nx, ny, desc=f"Random {nx}x{ny}")

    def test_03_equilibrium_states(self):
        for nx, ny in [(4, 4), (8, 4)]:
            rho = np.random.uniform(0.5, 1.5, (ny, nx))
            u = np.random.uniform(-0.05, 0.05, (2, ny, nx))
            phi = np.random.uniform(0.0, 1.0, (ny, nx))
            f_eq = compute_equilibrium(rho, u)
            self._verify_state_reconstruction(f_eq, phi, nx, ny, desc=f"Equilibrium {nx}x{ny}")

    def test_04_non_equilibrium_perturbed_states(self):
        nx, ny = 4, 4
        rho = np.ones((ny, nx))
        u = np.zeros((2, ny, nx))
        f_eq = compute_equilibrium(rho, u)
        # Perturb with shear non-equilibrium
        f_neq = f_eq + 0.05 * np.sin(np.linspace(0, np.pi, 9))[:, None, None]
        f_neq = np.maximum(f_neq, 1e-4) # ensure positivity
        phi = np.array([[1.0 if x < 2 else 0.0 for x in range(nx)] for _ in range(ny)])
        self._verify_state_reconstruction(f_neq, phi, nx, ny, desc="Non-Equilibrium Perturbed")

    def test_05_extreme_phase_distributions(self):
        nx, ny = 4, 4
        f = np.ones((9, ny, nx)) / 9.0
        for desc, phi in [
            ("All Gas", np.zeros((ny, nx))),
            ("All Liquid", np.ones((ny, nx))),
            ("Checkerboard", np.indices((ny, nx)).sum(axis=0) % 2)
        ]:
            self._verify_state_reconstruction(f, phi, nx, ny, desc=desc)
