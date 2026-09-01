import pytest
import numpy as np
from classical.two_phase import initialize_two_phase_dambreak
from quantum.two_phase_encoding import (
    get_two_phase_register_layout,
    quantum_initialize_two_phase_dambreak,
    encode_distribution,
    decode_distribution,
    validate_normalization
)


class TestTwoPhaseEncoding:
    def test_01_register_layout_4x4(self):
        layout = get_two_phase_register_layout(4, 4)
        assert layout["n_qx"] == 2
        assert layout["n_qy"] == 2
        assert layout["n_qvel"] == 4
        assert layout["n_qphase"] == 1
        assert layout["total_qubits"] == 9

    def test_02_initialization_unitarity_and_norm(self):
        qc, state, total_mass, layout = quantum_initialize_two_phase_dambreak(4, 4)
        assert qc.num_qubits == 9
        is_valid, norm = validate_normalization(state)
        assert is_valid
        assert np.isclose(norm, 1.0, atol=1e-10)
        assert total_mass > 0.0

    def test_03_exact_initial_state_reconstruction_fidelity(self):
        phi_c, rho_c, u_c, f_c, g_c = initialize_two_phase_dambreak(4, 4)
        state, total_mass, layout = encode_distribution(f_c, phi_c)
        probs = np.abs(state)**2
        rho_q, u_q, phi_q = decode_distribution(probs, layout, total_mass=total_mass)
        
        err_rho = float(np.linalg.norm(rho_q - rho_c) / np.linalg.norm(rho_c))
        err_phi = float(np.linalg.norm(phi_q - phi_c) / (np.linalg.norm(phi_c) + 1e-14))
        
        assert err_rho < 1e-10, f"Initial density encoding error ({err_rho}) exceeds 1e-10"
        assert err_phi < 1e-10, f"Initial phase encoding error ({err_phi}) exceeds 1e-10"
