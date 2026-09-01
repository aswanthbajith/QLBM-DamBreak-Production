import pytest
from qiskit.quantum_info import Operator
from PHASE11_STRUCTURED_QSVT import build_structured_collision_oracle

class TestQuantumCollision:
    def test_01_collision_unitarity(self):
        qc = build_structured_collision_oracle()
        op = Operator(qc)
        assert op.is_unitary(atol=1e-12)
