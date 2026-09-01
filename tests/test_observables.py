"""
Unit tests for Quantum Observables Estimation Module.
"""
import numpy as np
import pytest
from classical.two_phase import initialize_two_phase_dambreak, compute_density, compute_velocity, compute_phase_field
from quantum.state_preparation import get_two_phase_register_layout, compute_two_phase_amplitudes
from quantum.observables_quantum import (
    compute_quantum_expectation_observables,
    estimate_observables_from_shots,
    build_velocity_observable_operator
)


def test_quantum_expectation_matches_classical():
    nx, ny = 4, 4
    phi_c, rho_c, u_c, f, g = initialize_two_phase_dambreak(nx, ny)
    layout = get_two_phase_register_layout(nx, ny)

    statevector, total_mass, _ = compute_two_phase_amplitudes(f, g, layout=layout)
    rho_q, u_q, phi_q = compute_quantum_expectation_observables(statevector, total_mass, layout)

    assert np.allclose(rho_q, rho_c, atol=1e-12)
    assert np.allclose(u_q, u_c, atol=1e-12)
    assert np.allclose(phi_q, phi_c, atol=1e-12)


def test_velocity_observable_operators():
    nx, ny = 4, 4
    phi_c, rho_c, u_c, f, g = initialize_two_phase_dambreak(nx, ny)
    layout = get_two_phase_register_layout(nx, ny)

    statevector, total_mass, _ = compute_two_phase_amplitudes(f, g, layout=layout)
    Cx = build_velocity_observable_operator('x', layout)
    Cy = build_velocity_observable_operator('y', layout)

    assert Cx.shape == (512, 512)
    assert Cy.shape == (512, 512)

    # Momentum expectation values: <psi| Cx |psi> = sum_x,y,i f_i cx_i / M
    exp_cx = float(np.real(statevector.conj().T @ Cx @ statevector)) * total_mass
    exp_cy = float(np.real(statevector.conj().T @ Cy @ statevector)) * total_mass

    classical_px = float(np.sum(rho_c * u_c[0]))
    classical_py = float(np.sum(rho_c * u_c[1]))

    assert np.isclose(exp_cx, classical_px, atol=1e-12)
    assert np.isclose(exp_cy, classical_py, atol=1e-12)


def test_shot_estimation_convergence():
    nx, ny = 4, 4
    phi_c, rho_c, u_c, f, g = initialize_two_phase_dambreak(nx, ny)
    layout = get_two_phase_register_layout(nx, ny)

    statevector, total_mass, _ = compute_two_phase_amplitudes(f, g, layout=layout)
    probs = np.abs(statevector) ** 2
    total_shots = 500000
    counts_arr = np.random.multinomial(total_shots, probs)

    counts = {}
    for idx, count in enumerate(counts_arr):
        if count > 0:
            bitstring = format(idx, f"0{layout['total_qubits']}b")
            counts[bitstring] = count

    rho_est, u_est, phi_est = estimate_observables_from_shots(counts, total_shots, total_mass, layout)
    rel_err_rho = np.linalg.norm(rho_est - rho_c) / np.linalg.norm(rho_c)
    rel_err_phi = np.linalg.norm(phi_est - phi_c) / np.linalg.norm(phi_c)

    assert rel_err_rho < 0.05
    assert rel_err_phi < 0.05
