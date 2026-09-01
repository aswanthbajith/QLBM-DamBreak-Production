import pytest
from qiskit.quantum_info import Operator
from quantum.streaming import create_quantum_streaming_circuit

class TestQuantumStreaming:
    def test_01_streaming_unitarity(self):
        qc = create_quantum_streaming_circuit(2, 2)
        op = Operator(qc)
        assert op.is_unitary(atol=1e-12)
