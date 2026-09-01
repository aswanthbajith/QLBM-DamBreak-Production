"""
Quantum Boundary Condition Circuits (Periodic, Bounce-Back, Obstacles).
"""
from qiskit import QuantumCircuit

def build_bounce_back_circuit(num_qubits=4):
    """
    Applies bit-flip and phase reflections to swap opposite discrete velocities:
    c1 <-> c3, c2 <-> c4, c5 <-> c7, c6 <-> c8.
    """
    qc = QuantumCircuit(num_qubits, name="BounceBack")
    qc.cx(0, 1)
    qc.x(0)
    qc.cx(0, 1)
    return qc
