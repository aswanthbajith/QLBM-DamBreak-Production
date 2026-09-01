"""
Local Carleman Collision Circuit (PRE 113, 035307).
"""
import numpy as np
from qiskit import QuantumCircuit

def build_local_carleman_collision_circuit(omega=1.0):
    """
    Builds the local Carleman collision circuit operating on the 4-qubit velocity register.
    Applies single-qubit rotations and CNOT gates to implement the local relaxation.
    """
    qc = QuantumCircuit(4, name="LocalCarlemanCollision")
    theta = 2.0 * np.arcsin(np.sqrt(np.clip(omega / 2.0, 0.0, 1.0)))
    
    # Local parameterized unitary embedding
    qc.ry(theta, 0)
    qc.cx(0, 1)
    qc.rz(0.45, 1)
    qc.cx(0, 1)
    qc.ry(theta * 0.5, 2)
    qc.cx(2, 3)
    qc.rz(0.30, 3)
    qc.cx(2, 3)
    return qc
