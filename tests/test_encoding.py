import pytest
import numpy as np
from quantum.encoding import map_state_to_register

class TestQuantumEncoding:
    def test_01_state_normalization(self):
        f = np.ones((9, 2, 2)) / 36.0
        state, norm, n_qubits = map_state_to_register(f)
        assert n_qubits == 6
        assert np.isclose(np.linalg.norm(state), 1.0)
