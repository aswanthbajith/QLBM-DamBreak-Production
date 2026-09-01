"""
Carleman Truncation Error Bounds, Sparsity & Normalization.
"""
import numpy as np
import scipy.linalg as la

class CarlemanTruncator:
    def __init__(self, n_dim, order=2):
        self.n_dim = n_dim
        self.order = order
        if order == 1:
            self.dim_C = n_dim
        elif order == 2:
            self.dim_C = n_dim + n_dim**2
        else:
            self.dim_C = sum(n_dim**k for k in range(1, order + 1))
            
    def required_qubits(self):
        """
        Number of qubits needed to represent the Carleman state: ceil(log2(D_C)).
        """
        return int(np.ceil(np.log2(self.dim_C)))
    
    def estimate_truncation_error(self, x0, F1, F2, steps=10):
        """
        Estimates the analytical Carleman truncation error compared to exact recurrence.
        """
        from carleman.operator import construct_discrete_carleman_step
        from carleman.linearize import lift_state, project_state
        
        M_C = construct_discrete_carleman_step(F1, F2, self.n_dim)
        
        x_exact = np.copy(x0)
        y_carleman = lift_state(x0, order=self.order)
        
        errors = []
        for _ in range(steps):
            # Exact nonlinear step
            x_exact = F1 @ x_exact + F2 @ np.kron(x_exact, x_exact)
            # Linear Carleman step
            y_carleman = M_C @ y_carleman
            x_c = project_state(y_carleman, self.n_dim)
            
            err = la.norm(x_exact - x_c) / (la.norm(x_exact) + 1e-14)
            errors.append(err)
            
        return errors
