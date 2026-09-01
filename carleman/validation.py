"""
Validation of Carleman Linearization against Classical Reference.
"""
import numpy as np
import scipy.linalg as la
from carleman.linearize import lift_state, project_state
from carleman.operator import construct_discrete_carleman_step

def validate_carleman_single_step(x0, F1, F2, atol=1e-7):
    """
    Verifies that order-2 Carleman linearization matches the quadratic system
    identically in the first step: x_1 = F1 x0 + F2 (x0 (x) x0).
    """
    n_dim = len(x0)
    M_C = construct_discrete_carleman_step(F1, F2, n_dim)
    
    y0 = lift_state(x0, order=2)
    y1 = M_C @ y0
    x1_c = project_state(y1, n_dim)
    
    x1_exact = F1 @ x0 + F2 @ np.kron(x0, x0)
    diff = la.norm(x1_exact - x1_c)
    
    return {
        "passed": bool(diff < atol),
        "difference": float(diff),
        "relative_error": float(diff / (la.norm(x1_exact) + 1e-14))
    }
