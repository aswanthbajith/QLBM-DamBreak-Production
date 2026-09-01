import os

repo_dir = "/home/aswa/Research/QLBM-DamBreak"
tests_dir = os.path.join(repo_dir, "tests")

# 1. tests/test_d2q9.py
with open(os.path.join(tests_dir, "test_d2q9.py"), "w") as f:
    f.write("""import pytest
import numpy as np
from classical.d2q9 import C_X, C_Y, C, W, CS2, OPPOSITE

class TestD2Q9Lattice:
    def test_01_weights_sum_to_one(self):
        assert np.isclose(np.sum(W), 1.0, atol=1e-14)

    def test_02_velocity_vectors_symmetry(self):
        assert np.allclose(np.sum(W[:, None] * C, axis=0), [0.0, 0.0], atol=1e-14)

    def test_03_speed_of_sound(self):
        cs2_calc = np.sum(W * (C_X**2))
        assert np.isclose(cs2_calc, CS2, atol=1e-14)

    def test_04_opposite_involution(self):
        for i in range(9):
            opp = OPPOSITE[i]
            assert OPPOSITE[opp] == i
            assert C_X[i] == -C_X[opp]
            assert C_Y[i] == -C_Y[opp]
""")

# 2. tests/test_equilibrium.py
with open(os.path.join(tests_dir, "test_equilibrium.py"), "w") as f:
    f.write("""import pytest
import numpy as np
from classical.equilibrium import compute_equilibrium, compute_macroscopic
from classical.d2q9 import C_X, C_Y

class TestEquilibrium:
    def test_01_mass_and_momentum_conservation(self):
        rho = np.array([[1.0, 0.5], [0.8, 1.2]])
        u = np.array([[[0.05, -0.02], [0.01, 0.0]], [[0.0, 0.03], [-0.04, 0.02]]])
        
        f_eq = compute_equilibrium(rho, u)
        rho_rec, u_rec = compute_macroscopic(f_eq)
        
        assert np.allclose(rho_rec, rho, atol=1e-12)
        assert np.allclose(u_rec, u, atol=1e-12)

    def test_02_zero_velocity_rest_state(self):
        rho = np.ones((2, 2))
        u = np.zeros((2, 2, 2))
        f_eq = compute_equilibrium(rho, u)
        from classical.d2q9 import W
        for i in range(9):
            assert np.allclose(f_eq[i], W[i], atol=1e-12)
""")

# 3. tests/test_collision.py
with open(os.path.join(tests_dir, "test_collision.py"), "w") as f:
    f.write("""import pytest
import numpy as np
from classical.equilibrium import compute_equilibrium, compute_macroscopic
from classical.collision import collide_bgk

class TestCollision:
    def test_01_mass_conservation_under_collision(self):
        rho = np.array([[1.0, 0.5], [0.8, 1.2]])
        u = np.array([[[0.05, -0.02], [0.01, 0.0]], [[0.0, 0.03], [-0.04, 0.02]]])
        f_eq = compute_equilibrium(rho, u)
        
        # Perturb populations
        f_in = f_eq * (1.0 + 0.01 * np.sin(np.arange(9)[:, None, None]))
        f_out = collide_bgk(f_in, omega=1.0)
        
        rho_in = np.sum(f_in, axis=0)
        rho_out = np.sum(f_out, axis=0)
        assert np.allclose(rho_in, rho_out, atol=1e-12)
""")

# 4. tests/test_streaming.py
with open(os.path.join(tests_dir, "test_streaming.py"), "w") as f:
    f.write("""import pytest
import numpy as np
from classical.streaming import stream

class TestStreaming:
    def test_01_streaming_mass_conservation(self):
        f = np.random.rand(9, 4, 4)
        f_s = stream(f)
        assert np.isclose(np.sum(f), np.sum(f_s), atol=1e-12)

    def test_02_rest_particle_does_not_move(self):
        f = np.zeros((9, 4, 4))
        f[0, 2, 2] = 1.0
        f_s = stream(f)
        assert f_s[0, 2, 2] == 1.0
""")

# 5. tests/test_boundary.py
with open(os.path.join(tests_dir, "test_boundary.py"), "w") as f:
    f.write("""import pytest
import numpy as np
from classical.boundary import apply_noslip_box
from classical.d2q9 import OPPOSITE

class TestBoundary:
    def test_01_noslip_box_reflection(self):
        f_pre = np.ones((9, 4, 4))
        f_post = np.zeros((9, 4, 4))
        f_b = apply_noslip_box(f_post, f_pre)
        # Check that perimeter boundaries are reflected
        for i in range(9):
            opp = OPPOSITE[i]
            assert np.allclose(f_b[i, 0, :], f_pre[opp, 0, :])
            assert np.allclose(f_b[i, -1, :], f_pre[opp, -1, :])
""")

# 6. tests/test_carleman.py
with open(os.path.join(tests_dir, "test_carleman.py"), "w") as f:
    f.write("""import pytest
import numpy as np
from carleman.linearize import lift_state, project_state
from carleman.validation import validate_carleman_single_step

class TestCarleman:
    def test_01_lifting_and_projection(self):
        x = np.array([0.5, 0.2, -0.1])
        y = lift_state(x, order=2)
        assert len(y) == 3 + 9
        x_rec = project_state(y, 3)
        assert np.allclose(x, x_rec)

    def test_02_single_step_exactness(self):
        x0 = np.array([0.1, -0.2])
        F1 = np.array([[0.9, 0.1], [0.0, 0.8]])
        F2 = np.array([[0.05, 0.01, 0.02, 0.0], [0.01, 0.0, 0.03, 0.04]])
        res = validate_carleman_single_step(x0, F1, F2)
        assert res["passed"]
""")

# 7. tests/test_local_carleman.py
with open(os.path.join(tests_dir, "test_local_carleman.py"), "w") as f:
    f.write("""import pytest
import numpy as np
from quantum.local_carleman.encoding import encode_local_state
from quantum.local_carleman.collision import build_local_carleman_collision_circuit
from quantum.local_carleman.dynamic_circuit import build_dynamic_qlbm_step

class TestLocalCarleman:
    def test_01_local_encoding(self):
        f_node = np.ones(9) / 9.0
        qc, norm = encode_local_state(f_node)
        assert qc.num_qubits == 4
        assert np.isclose(norm, 1.0 / 3.0)

    def test_02_collision_circuit(self):
        qc = build_local_carleman_collision_circuit(omega=1.0)
        assert qc.num_qubits == 4
        ops = qc.count_ops()
        assert ops.get("cx", 0) == 4

    def test_03_dynamic_circuit(self):
        qc = build_dynamic_qlbm_step(2, 2, timesteps=1)
        assert qc.num_qubits == 6
        assert qc.num_clbits == 6
""")

# 8. tests/test_encoding.py
with open(os.path.join(tests_dir, "test_encoding.py"), "w") as f:
    f.write("""import pytest
import numpy as np
from quantum.encoding import map_state_to_register

class TestQuantumEncoding:
    def test_01_state_normalization(self):
        f = np.ones((9, 2, 2)) / 36.0
        state, norm, n_qubits = map_state_to_register(f)
        assert n_qubits == 6
        assert np.isclose(np.linalg.norm(state), 1.0)
""")

# 9. tests/test_quantum_streaming.py
with open(os.path.join(tests_dir, "test_quantum_streaming.py"), "w") as f:
    f.write("""import pytest
from qiskit.quantum_info import Operator
from quantum.streaming import create_quantum_streaming_circuit

class TestQuantumStreaming:
    def test_01_streaming_unitarity(self):
        qc = create_quantum_streaming_circuit(2, 2)
        op = Operator(qc)
        assert op.is_unitary(atol=1e-12)
""")

# 10. tests/test_quantum_collision.py
with open(os.path.join(tests_dir, "test_quantum_collision.py"), "w") as f:
    f.write("""import pytest
from qiskit.quantum_info import Operator
from PHASE11_STRUCTURED_QSVT import build_structured_collision_oracle

class TestQuantumCollision:
    def test_01_collision_unitarity(self):
        qc = build_structured_collision_oracle()
        op = Operator(qc)
        assert op.is_unitary(atol=1e-12)
""")

# 11. tests/test_ibm_backend.py
with open(os.path.join(tests_dir, "test_ibm_backend.py"), "w") as f:
    f.write("""import pytest
from backends.fake_ibm_backend import get_fake_ibm_backend
from backends.select_backend import select_real_backend
from backends.ibm_backend import IBMRuntimeServiceWrapper

class TestIBMBackend:
    def test_01_fake_backend_properties(self):
        backend = get_fake_ibm_backend()
        assert backend.num_qubits == 127
        assert "cx" in backend.operation_names

    def test_02_safety_interlock_default(self):
        wrapper = IBMRuntimeServiceWrapper()
        assert not wrapper.is_real_execution_allowed()
""")

# 12. tests/test_hardware_verification.py
with open(os.path.join(tests_dir, "test_hardware_verification.py"), "w") as f:
    f.write("""import pytest
from scripts.hardware_preflight import run_preflight

class TestHardwareVerification:
    def test_01_preflight_dry_run_interlock(self):
        allowed = run_preflight()
        assert not allowed # default dry-run prevents submission
""")

print("Successfully generated all 12 modular unit tests.")
