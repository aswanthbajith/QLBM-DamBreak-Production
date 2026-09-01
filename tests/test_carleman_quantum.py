"""
Unit tests for Quantum Carleman Linearization and Dilation Module.
"""
import numpy as np
import pytest
from classical.two_phase import initialize_two_phase_dambreak
from quantum.carleman_quantum import (
    build_second_order_carleman_matrices,
    build_second_order_evaluation_operator,
    lift_two_phase_state,
    build_closed_carleman_matrix,
    analyze_carleman_truncation_error,
    build_carleman_unitary_dilation,
    build_carleman_collision_circuit
)


def test_carleman_dimensions():
    M1, M2 = build_second_order_carleman_matrices(tau_f=0.8, tau_g=0.7, rho0=1.0)
    assert M1.shape == (18, 18)
    assert M2.shape == (18, 324)

    A_eval = build_second_order_evaluation_operator(tau_f=0.8, tau_g=0.7, rho0=1.0)
    assert A_eval.shape == (18, 342)


def test_lifting_and_evaluation():
    nx, ny = 4, 4
    phi, rho, u, f, g = initialize_two_phase_dambreak(nx, ny)
    f_node = f[:, 0, 0]
    g_node = g[:, 0, 0]

    Y2 = lift_two_phase_state(f_node, g_node, order=2)
    assert len(Y2) == 342

    A_eval = build_second_order_evaluation_operator(tau_f=0.8, tau_g=0.7, rho0=float(rho[0, 0]))
    psi_next = A_eval @ Y2
    assert len(psi_next) == 18


def test_closed_carleman_truncation_analysis():
    nx, ny = 4, 4
    phi, rho, u, f, g = initialize_two_phase_dambreak(nx, ny)
    f_node = f[:, 0, 0]
    g_node = g[:, 0, 0]

    res = analyze_carleman_truncation_error(f_node, g_node, tau_f=0.8, tau_g=0.7, rho0=float(rho[0,0]))
    # For single-step linear term evaluation, psi_A and psi_B should agree
    assert res["psi_difference"] < 1e-12
    # Quadratic layer exhibits truncation difference
    assert "quadratic_layer_truncation_error" in res


def test_10qubit_unitary_dilation():
    A_eval = build_second_order_evaluation_operator(tau_f=0.8, tau_g=0.7, rho0=1.0)
    U, alpha, err = build_carleman_unitary_dilation(A_eval, target_dim=512)

    assert U.shape == (1024, 1024)
    assert alpha > 1.0
    assert err < 1e-12

    # Verify Sz.-Nagy block extraction
    extracted_block = U[:18, :342]
    expected_block = A_eval / alpha
    diff = np.max(np.abs(extracted_block - expected_block))
    assert diff < 1e-12


def test_collision_circuit_synthesis():
    A_eval = build_second_order_evaluation_operator(tau_f=0.8, tau_g=0.7, rho0=1.0)
    U, alpha, _ = build_carleman_unitary_dilation(A_eval, target_dim=512)
    qc = build_carleman_collision_circuit(U, num_qubits=10)
    assert qc.num_qubits == 10
