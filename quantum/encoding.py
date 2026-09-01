"""
D2Q9 Discrete Velocity & Spatial Encoding Scheme.
"""
import numpy as np
from qiskit import QuantumCircuit

CHANNEL_BITSTRINGS = {
    0: "0000", # c0 (0,0)
    1: "0001", # c1 (1,0)
    2: "0010", # c2 (0,1)
    3: "0011", # c3 (-1,0)
    4: "0100", # c4 (0,-1)
    5: "0101", # c5 (1,1)
    6: "0110", # c6 (-1,1)
    7: "0111", # c7 (-1,-1)
    8: "1000"  # c8 (1,-1)
}

def map_state_to_register(f_array):
    """
    Encodes full (9, Ny, Nx) array into a normalized quantum statevector.
    """
    Ny, Nx = f_array.shape[1], f_array.shape[2]
    n_spatial_x = int(np.ceil(np.log2(Nx)))
    n_spatial_y = int(np.ceil(np.log2(Ny)))
    n_qubits = n_spatial_x + n_spatial_y + 4
    
    total_dim = 2**n_qubits
    state = np.zeros(total_dim, dtype=np.complex128)
    
    for i in range(9):
        for y in range(Ny):
            for x in range(Nx):
                # index calculation: [vel (4 bits) | spatial_y | spatial_x]
                idx = (i << (n_spatial_x + n_spatial_y)) | (y << n_spatial_x) | x
                state[idx] = f_array[i, y, x]
                
    norm = np.linalg.norm(state)
    if norm > 0:
        state /= norm
    return state, norm, n_qubits
