"""
Unit tests for Quantum State Preparation Module.
"""
import numpy as np
import pytest
from classical.two_phase import initialize_two_phase_dambreak
from quantum.state_preparation import (
    get_two_phase_register_layout,
    compute_two_phase_amplitudes,
    build_exact_state_preparation_circuit,
    build_structured_dambreak_circuit,
    decode_statevector_to_distributions,
    decode_counts_to_distributions
)


def test_register_layout():
    layout = get_two_phase_register_layout(4, 4)
    assert layout["nx"] == 4
    assert layout["ny"] == 4
    assert layout["n_qx"] == 2
    assert layout["n_qy"] == 2
    assert layout["n_qvel"] == 4
    assert layout["n_qselector"] == 1
    assert layout["total_qubits"] == 9
    assert len(layout["registers"]["position_x"]) == 2
    assert len(layout["registers"]["position_y"]) == 2
    assert len(layout["registers"]["velocity"]) == 4
    assert len(layout["registers"]["selector"]) == 1


def test_statevector_normalization_and_exact_decoding():
    nx, ny = 4, 4
    phi, rho, u, f, g = initialize_two_phase_dambreak(nx, ny)
    layout = get_two_phase_register_layout(nx, ny)

    statevector, total_mass, _ = compute_two_phase_amplitudes(f, g, layout=layout)
    
    # 1. Norm must be strictly 1.0
    norm = np.linalg.norm(statevector)
    assert np.isclose(norm, 1.0, atol=1e-12)
    assert len(statevector) == 512

    # 2. Decoding must recover f and g to machine precision
    f_rec, g_rec = decode_statevector_to_distributions(statevector, total_mass, layout)
    assert np.allclose(f_rec, f, atol=1e-12)
    assert np.allclose(g_rec, g, atol=1e-12)


def test_exact_circuit_synthesis():
    nx, ny = 4, 4
    phi, rho, u, f, g = initialize_two_phase_dambreak(nx, ny)
    layout = get_two_phase_register_layout(nx, ny)

    qc, statevector, total_mass, metrics = build_exact_state_preparation_circuit(f, g, layout=layout)
    assert qc.num_qubits == 9
    assert metrics["qubits"] == 9
    assert metrics["hilbert_dimension"] == 512
    assert metrics["total_mass"] == total_mass
    assert "asymptotic_complexity" in metrics


def test_decode_counts_statistical_convergence():
    nx, ny = 4, 4
    phi, rho, u, f, g = initialize_two_phase_dambreak(nx, ny)
    layout = get_two_phase_register_layout(nx, ny)

    statevector, total_mass, _ = compute_two_phase_amplitudes(f, g, layout=layout)
    
    # Simulate high-shot sampling
    probs = np.abs(statevector) ** 2
    total_shots = 1000000
    counts_array = np.random.multinomial(total_shots, probs)
    
    counts_dict = {}
    for idx, count in enumerate(counts_array):
        if count > 0:
            bitstring = format(idx, f"0{layout['total_qubits']}b")
            counts_dict[bitstring] = count

    f_sampled, g_sampled = decode_counts_to_distributions(counts_dict, total_shots, total_mass, layout)
    
    # Relative error should be within shot noise O(1/sqrt(N_shots))
    err_f = np.max(np.abs(f_sampled - f)) / np.max(f)
    err_g = np.max(np.abs(g_sampled - g)) / np.max(g)
    assert err_f < 0.05
    assert err_g < 0.05
