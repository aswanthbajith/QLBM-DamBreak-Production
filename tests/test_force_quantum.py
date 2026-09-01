"""
Unit tests for Quantum Gravitational Body Forcing Module.
"""
import numpy as np
import pytest
from classical.two_phase import initialize_two_phase_dambreak
from quantum.state_preparation import get_two_phase_register_layout
from quantum.force_quantum import (
    compute_buoyancy_force_increment,
    apply_quantum_force,
    build_forcing_operator_matrix,
    build_forcing_unitary_dilation,
    build_forcing_circuit
)


def test_buoyancy_directionality():
    nx, ny = 4, 4
    phi, rho, u, f, g = initialize_two_phase_dambreak(nx, ny)
    delta_f = compute_buoyancy_force_increment(rho, g_acc=-0.001, rho_gas=0.1)

    # Downward velocities (4, 7, 8) must have negative delta_f under negative g_acc when rho > rho_gas
    # Actually delta_f = 3 * w_i * (rho - rho_gas) * g_y * c_iy
    # If g_y = -0.001 < 0, for downward velocities c_iy = -1, delta_f > 0 (downward momentum increases)
    for v in [4, 7, 8]:
        assert np.all(delta_f[v] >= 0.0)
    for v in [2, 5, 6]:
        assert np.all(delta_f[v] <= 0.0)
    for v in [0, 1, 3]:
        assert np.all(delta_f[v] == 0.0)


def test_apply_quantum_force_conservation():
    nx, ny = 4, 4
    phi, rho, u, f, g = initialize_two_phase_dambreak(nx, ny)
    f_forced = apply_quantum_force(f, rho, g_acc=-0.001)

    # Mass must be strictly conserved: sum_i delta_f_i = 3 * (rho - rho_gas) * g_y * (sum_i w_i c_iy) = 0
    mass_before = np.sum(f)
    mass_after = np.sum(f_forced)
    assert np.isclose(mass_before, mass_after, atol=1e-12)


def test_forcing_unitary_dilation():
    nx, ny = 4, 4
    phi, rho, u, f, g = initialize_two_phase_dambreak(nx, ny)
    layout = get_two_phase_register_layout(nx, ny)

    F = build_forcing_operator_matrix(rho, layout, g_acc=-0.001)
    assert F.shape == (512, 512)

    U_force, alpha_force, err = build_forcing_unitary_dilation(F)
    assert U_force.shape == (1024, 1024)
    assert alpha_force >= 1.0
    assert err < 1e-12

    qc = build_forcing_circuit(U_force, num_qubits=10)
    assert qc.num_qubits == 10
