import pytest
from qiskit.quantum_info import Operator
from quantum.two_phase_encoding import get_two_phase_register_layout
from quantum.two_phase_collision import build_two_phase_collision_circuit

class TestTwoPhaseCollision:
    def test_01_collision_unitarity(self):
        layout = get_two_phase_register_layout(2, 2)
        qc = build_two_phase_collision_circuit(layout)
        op = Operator(qc)
        assert op.is_unitary(atol=1e-12)
