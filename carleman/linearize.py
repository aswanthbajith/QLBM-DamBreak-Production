"""
Carleman Linearization Transformation & Lifting Functions.
"""
import numpy as np

def lift_state(x, order=2):
    """
    Lifts a state vector x into its Carleman representation up to given polynomial order.
    For order=1: returns x
    For order=2: returns [x, x (x) x]
    """
    x = np.asarray(x, dtype=np.float64).flatten()
    if order == 1:
        return x
    elif order == 2:
        x_kron_x = np.kron(x, x)
        return np.concatenate((x, x_kron_x))
    else:
        terms = [x]
        curr = x
        for _ in range(2, order + 1):
            curr = np.kron(curr, x)
            terms.append(curr)
        return np.concatenate(terms)

def project_state(y, n_dim):
    """
    Extracts the original linear physical state from a Carleman lifted state y.
    """
    return y[:n_dim]
