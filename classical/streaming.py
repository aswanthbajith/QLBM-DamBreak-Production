"""
Exact Spatial Streaming Permutation for D2Q9 Lattice.
"""
import numpy as np
from classical.d2q9 import C_X, C_Y

def stream(f):
    """
    Stream populations along discrete velocity directions:
    f_i(x + c_i, t + dt) = f_i^*(x, t)
    f shape: (9, Ny, Nx)
    """
    f_streamed = np.zeros_like(f)
    for i in range(9):
        # Shift along y by C_Y[i], shift along x by C_X[i]
        f_streamed[i] = np.roll(np.roll(f[i], shift=C_Y[i], axis=0), shift=C_X[i], axis=1)
    return f_streamed
