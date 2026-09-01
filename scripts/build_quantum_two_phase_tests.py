import os

repo_dir = "/home/aswa/Research/QLBM-DamBreak"
tests_dir = os.path.join(repo_dir, "tests")

# 1. tests/test_two_phase_encoding.py
with open(os.path.join(tests_dir, "test_two_phase_encoding.py"), "w") as f:
    f.write("""import pytest
import numpy as np
from quantum.two_phase_encoding import get_two_phase_register_layout, quantum_initialize_two_phase_dambreak

class TestTwoPhaseEncoding:
    def test_01_register_layout_4x4(self):
        layout = get_two_phase_register_layout(4, 4)
        assert layout["n_qx"] == 2
        assert layout["n_qy"] == 2
        assert layout["n_qvel"] == 4
        assert layout["n_qphase"] == 1
        assert layout["total_qubits"] == 9

    def test_02_initialization_unitarity_and_norm(self):
        qc, state, norm, layout = quantum_initialize_two_phase_dambreak(4, 4)
        assert qc.num_qubits == 9
        assert np.isclose(np.linalg.norm(state), 1.0, atol=1e-12)
        assert norm > 0.0
""")

# 2. tests/test_two_phase_collision.py
with open(os.path.join(tests_dir, "test_two_phase_collision.py"), "w") as f:
    f.write("""import pytest
from qiskit.quantum_info import Operator
from quantum.two_phase_encoding import get_two_phase_register_layout
from quantum.two_phase_collision import build_two_phase_collision_circuit

class TestTwoPhaseCollision:
    def test_01_collision_unitarity(self):
        layout = get_two_phase_register_layout(2, 2)
        qc = build_two_phase_collision_circuit(layout)
        op = Operator(qc)
        assert op.is_unitary(atol=1e-12)
""")

# 3. tests/test_two_phase_streaming.py
with open(os.path.join(tests_dir, "test_two_phase_quantum_streaming.py"), "w") as f:
    f.write("""import pytest
from qiskit.quantum_info import Operator
from quantum.streaming import create_quantum_streaming_circuit

class TestTwoPhaseQuantumStreaming:
    def test_01_spatial_shift_unitarity(self):
        qc = create_quantum_streaming_circuit(4, 4)
        op = Operator(qc)
        assert op.is_unitary(atol=1e-12)
""")

# 4. tests/test_two_phase_boundary.py
with open(os.path.join(tests_dir, "test_two_phase_boundary.py"), "w") as f:
    f.write("""import pytest
from qiskit.quantum_info import Operator
from quantum.two_phase_encoding import get_two_phase_register_layout
from quantum.two_phase_boundary import build_two_phase_boundary_circuit

class TestTwoPhaseBoundary:
    def test_01_boundary_unitarity(self):
        layout = get_two_phase_register_layout(2, 2)
        qc = build_two_phase_boundary_circuit(layout)
        op = Operator(qc)
        assert op.is_unitary(atol=1e-12)
""")

# 5. tests/test_two_phase_measurement.py
with open(os.path.join(tests_dir, "test_two_phase_measurement.py"), "w") as f:
    f.write("""import pytest
import numpy as np
from quantum.two_phase_step import reconstruct_two_phase_fields

class TestTwoPhaseMeasurement:
    def test_01_reconstruction_bounds(self):
        counts = {"000000000": 1000, "100000000": 1000}
        rho, u, phi = reconstruct_two_phase_fields(counts, nx=2, ny=2, total_mass=2.0)
        assert rho.shape == (2, 2)
        assert phi.shape == (2, 2)
        assert np.all(phi >= 0.0) and np.all(phi <= 1.0)
        assert np.isclose(np.sum(rho), 2.0, atol=1e-6)
""")

# 6. tests/test_two_phase_end_to_end.py
with open(os.path.join(tests_dir, "test_two_phase_end_to_end.py"), "w") as f:
    f.write("""import pytest
import numpy as np
from quantum.two_phase_step import quantum_two_phase_step

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
""")

print("Successfully generated all quantum two-phase unit tests.")
