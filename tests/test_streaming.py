import pytest
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
