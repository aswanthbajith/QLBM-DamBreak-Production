import pytest
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
