import pytest
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
