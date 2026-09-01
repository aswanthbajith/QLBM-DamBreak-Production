"""
D2Q9 Lattice Constants, Velocity Vectors, and Weights.
"""
import numpy as np

# D2Q9 Discrete Velocities (c_x, c_y)
# c0 = (0, 0)
# c1 = (1, 0), c2 = (0, 1), c3 = (-1, 0), c4 = (0, -1)
# c5 = (1, 1), c6 = (-1, 1), c7 = (-1, -1), c8 = (1, -1)
C_X = np.array([0, 1, 0, -1, 0, 1, -1, -1, 1], dtype=np.int32)
C_Y = np.array([0, 0, 1, 0, -1, 1, 1, -1, -1], dtype=np.int32)
C = np.column_stack((C_X, C_Y))

# D2Q9 Lattice Weights
W = np.array([
    4.0 / 9.0,                                      # c0
    1.0 / 9.0, 1.0 / 9.0, 1.0 / 9.0, 1.0 / 9.0,    # c1, c2, c3, c4
    1.0 / 36.0, 1.0 / 36.0, 1.0 / 36.0, 1.0 / 36.0 # c5, c6, c7, c8
], dtype=np.float64)

# Speed of sound squared in lattice units
CS2 = 1.0 / 3.0

# Opposite direction indices for bounce-back
# 0->0, 1->3, 2->4, 3->1, 4->2, 5->7, 6->8, 7->5, 8->6
OPPOSITE = np.array([0, 3, 4, 1, 2, 7, 8, 5, 6], dtype=np.int32)
