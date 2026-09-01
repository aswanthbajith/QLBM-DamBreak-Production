import pytest
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
