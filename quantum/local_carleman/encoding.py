"""
Local Carleman State Encoding (PRE 113, 035307).
"""
import numpy as np
from qiskit import QuantumCircuit

def encode_local_state(f_node):
    """
    Encodes 9-channel distribution at a single node into a 4-qubit normalized state.
    f_node: array of shape (9,)
    """
    norm = np.linalg.norm(f_node)
    f_norm = f_node / (norm + 1e-14)
    
    # 9 components mapped into 16-dimensional Hilbert space (4 qubits)
    state = np.zeros(16, dtype=np.complex128)
    state[:9] = f_norm
    
    qc = QuantumCircuit(4, name="LocalEncode")
    # Amplitude initialization
    qc.initialize(state, [0, 1, 2, 3])
    return qc, norm
