"""
Explicit Construction of Carleman Linear Operators.
"""
import numpy as np
import scipy.sparse as sp

def construct_carleman_matrix_2nd_order(A1, A2, n_dim):
    """
    Constructs the block Carleman matrix A_C for dx/dt = A1 x + A2 (x (x) x):
    A_C = [ A1       A2      ]
          [ 0   A1(x)I + I(x)A1 ]
    Dimension: n_dim + n_dim^2
    """
    I = np.eye(n_dim)
    A22 = np.kron(A1, I) + np.kron(I, A1)
    
    row1 = np.hstack((A1, A2))
    row2 = np.hstack((np.zeros((n_dim**2, n_dim)), A22))
    A_C = np.vstack((row1, row2))
    return A_C

def construct_discrete_carleman_step(F1, F2, n_dim):
    """
    Constructs the discrete Carleman step matrix M_C for x_{t+1} = F1 x_t + F2 (x_t (x) x_t):
    x_{t+1} = F1 x_t + F2 (x_t (x) x_t)
    (x_{t+1} (x) x_{t+1}) = (F1 (x) F1) (x_t (x) x_t) + O(x^3)
    
    M_C = [ F1      F2     ]
          [ 0    F1 (x) F1 ]
    """
    M22 = np.kron(F1, F1)
    row1 = np.hstack((F1, F2))
    row2 = np.hstack((np.zeros((n_dim**2, n_dim)), M22))
    M_C = np.vstack((row1, row2))
    return M_C
