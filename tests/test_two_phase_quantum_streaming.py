import pytest
from qiskit.quantum_info import Operator
from quantum.streaming import create_quantum_streaming_circuit

class TestTwoPhaseQuantumStreaming:
    def test_01_spatial_shift_unitarity(self):
        qc = create_quantum_streaming_circuit(4, 4)
        op = Operator(qc)
        assert op.is_unitary(atol=1e-12)
