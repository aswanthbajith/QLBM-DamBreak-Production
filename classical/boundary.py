"""
Boundary Conditions for D2Q9 LBM (Periodic, Half-Way Bounce-Back, Walls, Obstacles).
"""
import numpy as np
from classical.d2q9 import OPPOSITE

def apply_periodic(f):
    """
    Periodic boundary conditions are natively handled by np.roll in streaming.
    """
    return f

def apply_bounce_back_walls(f_post_stream, f_pre_stream, solid_mask):
    """
    Half-way bounce-back on solid obstacle nodes:
    Populations hitting solid nodes are reflected back in opposite direction:
    f_i(fluid) = f_opposite(solid)
    """
    f_out = np.copy(f_post_stream)
    for i in range(9):
        opp = OPPOSITE[i]
        f_out[i, solid_mask] = f_pre_stream[opp, solid_mask]
    return f_out

def apply_noslip_box(f, f_coll):
    """
    Enforce half-way bounce-back on all four domain perimeter walls (bottom, top, left, right).
    """
    Ny, Nx = f.shape[1], f.shape[2]
    solid_mask = np.zeros((Ny, Nx), dtype=bool)
    solid_mask[0, :] = True
    solid_mask[-1, :] = True
    solid_mask[:, 0] = True
    solid_mask[:, -1] = True
    return apply_bounce_back_walls(f, f_coll, solid_mask)
