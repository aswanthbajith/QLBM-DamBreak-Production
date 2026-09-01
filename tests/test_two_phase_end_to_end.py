import pytest
import numpy as np
from quantum.two_phase_step import quantum_two_phase_step, reconstruct_density, reconstruct_velocity, reconstruct_phase
from scripts.hardware_preflight import run_preflight
from quantum.two_phase_encoding import get_two_phase_register_layout, quantum_initialize_two_phase_dambreak
from quantum.two_phase_collision import build_two_phase_collision_circuit
from quantum.streaming import build_two_phase_streaming_circuit
from quantum.two_phase_boundary import build_two_phase_boundary_circuit


class TestTwoPhaseEndToEnd:
    def test_01_single_step_aer_ideal(self):
        res = quantum_two_phase_step(nx=4, ny=4, timesteps=1, backend="aer_ideal", shots=2048)
        rho = res["rho"]
        phi = res["phi"]
        u = res["u"]
        assert rho.shape == (4, 4)
        assert phi.shape == (4, 4)
        assert u.shape == (2, 4, 4)
        assert np.all(phi >= 0.0) and np.all(phi <= 1.0)
        assert np.all(rho > 0.0)

    def test_02_single_step_aer_noisy(self):
        res = quantum_two_phase_step(nx=4, ny=4, timesteps=1, backend="aer_noisy", shots=2048)
        assert res["rho"].shape == (4, 4)
        assert np.all(res["phi"] >= 0.0) and np.all(res["phi"] <= 1.0)

    def test_03_single_step_fake_ibm(self):
        res = quantum_two_phase_step(nx=4, ny=4, timesteps=1, backend="fake_ibm", shots=2048)
        assert res["rho"].shape == (4, 4)
        assert np.all(res["phi"] >= 0.0) and np.all(res["phi"] <= 1.0)

    def test_04_multi_step_aer_ideal(self):
        res = quantum_two_phase_step(nx=4, ny=4, timesteps=2, backend="aer_ideal", shots=2048)
        assert res["rho"].shape == (4, 4)
        assert np.all(res["phi"] >= 0.0) and np.all(res["phi"] <= 1.0)

    def test_05_hardware_preflight_safety(self):
        status = run_preflight(nx=4, ny=4, timesteps=1, return_dict=True)
        assert status["required_qubits"] == 9
        assert status["available_qubits"] >= 9
        assert "submission_permitted" in status
        assert not status["submission_permitted"]

    def test_06_circuit_depth_and_structure(self):
        layout = get_two_phase_register_layout(4, 4)
        qc, state, total_mass, _ = quantum_initialize_two_phase_dambreak(4, 4)
        coll = build_two_phase_collision_circuit(layout)
        stream = build_two_phase_streaming_circuit(layout)
        bnd = build_two_phase_boundary_circuit(layout)
        
        qc.append(coll, range(layout["total_qubits"]))
        qc.append(stream, range(layout["total_qubits"]))
        qc.append(bnd, range(layout["total_qubits"]))
        qc.measure_all()
        
        assert qc.num_qubits == 9
        assert qc.depth() >= 4
