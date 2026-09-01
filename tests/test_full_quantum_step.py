"""
Unit tests for Quantum Dam-Break Timestep Stepper.
"""
import numpy as np
import pytest
from classical.two_phase import initialize_two_phase_dambreak
from quantum.state_preparation import get_two_phase_register_layout, compute_two_phase_amplitudes
from quantum.timestep_quantum import QuantumDamBreakStep, run_quantum_dambreak


def test_quantum_step_initialization():
    layout = get_two_phase_register_layout(4, 4)
    stepper = QuantumDamBreakStep(layout)
    assert stepper.S.shape == (512, 512)
    assert stepper.B.shape == (512, 512)
    assert stepper.U_spatial.shape == (512, 512)


def test_single_timestep_execution():
    nx, ny = 4, 4
    phi0, rho0, u0, f0, g0 = initialize_two_phase_dambreak(nx, ny)
    layout = get_two_phase_register_layout(nx, ny)
    stepper = QuantumDamBreakStep(layout)

    # 1. Step Hybrid
    f_next, g_next, phi_next, rho_next, u_next, metrics = stepper.step_hybrid(f0, g0)
    assert f_next.shape == (9, ny, nx)
    assert g_next.shape == (9, ny, nx)
    assert np.all(f_next >= 0.0)
    assert np.all(g_next >= 0.0)

    # 2. Step Quantum Statevector
    sv0, mass0, _ = compute_two_phase_amplitudes(f0, g0, layout=layout)
    sv1, mass1, rho1, u1, phi1, metrics1 = stepper.step_quantum_statevector(sv0, mass0)
    assert len(sv1) == 512
    assert np.isclose(np.linalg.norm(sv1), 1.0, atol=1e-12)
    assert np.allclose(rho1, rho_next, atol=1e-12)
