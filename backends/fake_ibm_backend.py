"""
Fake IBM Eagle 127-Qubit Heavy-Hex Backend Harness.
"""
from qiskit.providers.fake_provider import GenericBackendV2

def get_fake_ibm_backend():
    return GenericBackendV2(num_qubits=127)
